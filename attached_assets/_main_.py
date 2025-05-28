import pandas as pd
import re
import os
import time
from typing import Dict, Optional, Tuple
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px  # Added for interactive visualization

# ANSI color codes for CLI readability
class Colors:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    RESET = "\033[0m"

# Available commands
COMMANDS = ["parse", "integrate", "analyze", "visualize", "exit"]

# Function to get user-defined output directory
def get_output_directory() -> str:
    while True:
        print(f"\n{Colors.BLUE}📂 Enter the output directory path for all results:{Colors.RESET}")
        output_dir = input().strip()
        try:
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
                print(f"{Colors.GREEN}✅ Created directory: {output_dir}{Colors.RESET}")
            return output_dir
        except OSError as e:
            print(f"{Colors.RED}❌ ERROR: Could not create directory {output_dir}. {e}{Colors.RESET}")

# Generate timestamped filenames
def generate_filename(base_name: str, extension: str, output_dir: str) -> str:
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    return os.path.join(output_dir, f"{base_name}_{timestamp}.{extension}")

# Generic FASTA parser with dynamic key-value handling
def parse_fasta(file_path: str, output_path: str, fields: Dict[str, Optional[callable]]) -> Optional[str]:
    if not os.path.isfile(file_path):
        print(f"{Colors.RED}❌ ERROR: File {file_path} does not exist or is not a file.{Colors.RESET}")
        return None

    data: Dict[str, list] = {key: [] for key in fields.keys()}
    current_entry: Dict[str, str] = {key: "" for key in fields.keys()}
    kv_pattern = re.compile(r"(\w+)=(\S+)")  # For key-value pairs in headers
    
    try:
        with open(file_path, "r") as fasta_file:
            for line in fasta_file:
                line = line.strip()
                if not line:
                    continue
                if line.startswith(">"):
                    if any(current_entry.values()):  # Save previous entry
                        for key in fields:
                            data[key].append(current_entry[key])
                    current_entry = {key: "" for key in fields.keys()}
                    header = line[1:]
                    header_dict = dict(kv_pattern.findall(header))  # Parse key-value pairs
                    for key, parser in fields.items():
                        if parser:
                            current_entry[key] = parser(header, header_dict)
                else:
                    current_entry["Sequence"] += line

            if any(current_entry.values()):  # Save last entry
                for key in fields:
                    data[key].append(current_entry[key])

        if not any(data.values()):
            print(f"{Colors.RED}❌ ERROR: No valid data found in {file_path}.{Colors.RESET}")
            return None

        df = pd.DataFrame(data)
        df.to_csv(output_path, index=False)
        print(f"{Colors.GREEN}✅ Data saved: {output_path} ({len(df)} entries parsed){Colors.RESET}")
        return output_path
    except Exception as e:
        print(f"{Colors.RED}❌ ERROR: Failed to parse {file_path}. {e}{Colors.RESET}")
        return None

# Parse proteomics FASTA
def parse_proteomics(file_path: str, output_dir: str) -> Optional[str]:
    output_path = generate_filename("proteomics_parsed", "csv", output_dir)
    print(f"{Colors.BLUE}🔍 Parsing proteomics FASTA file...{Colors.RESET}")
    fields = {
        "Protein": lambda header, kv: kv.get("ID", header.split()[0]),  # ID= or first part
        "Sequence": None
    }
    return parse_fasta(file_path, output_path, fields)

# Parse genomics FASTA
def parse_genomics(file_path: str, output_dir: str) -> Optional[str]:
    output_path = generate_filename("genomics_parsed", "csv", output_dir)
    print(f"{Colors.BLUE}🔍 Parsing genomics FASTA file...{Colors.RESET}")
    fields = {
        "Gene": lambda header, kv: kv.get("GeneID", kv.get("gene", kv.get("GN", header.split()[0]))),
        "Chromosome": lambda header, kv: kv.get("chromosome", kv.get("chr", "")),
        "Sequence": None
    }
    return parse_fasta(file_path, output_path, fields)

# Integrate proteomics and genomics data
def integrate_data(proteomics_file: str, genomics_file: str, output_dir: str) -> Optional[str]:
    output_path = generate_filename("integrated_data", "csv", output_dir)
    print(f"{Colors.BLUE}🔄 Integrating proteomics and genomics data...{Colors.RESET}")
    try:
        proteomics_df = pd.read_csv(proteomics_file)
        genomics_df = pd.read_csv(genomics_file)

        # Dynamic matching: try sequence first, then fall back to IDs
        if "Sequence" in proteomics_df.columns and "Sequence" in genomics_df.columns:
            integrated_df = pd.merge(
                proteomics_df, genomics_df, on="Sequence", how="inner", suffixes=("_prot", "_geno")
            )
            print(f"{Colors.YELLOW}🔍 Matched {len(integrated_df)} entries by sequence.{Colors.RESET}")
        
        # If sequence match is empty or not available, try ID-based matching
        if len(integrated_df) == 0 or "Sequence" not in proteomics_df.columns:
            print(f"{Colors.YELLOW}⚠ No sequence match. Attempting ID-based integration...{Colors.RESET}")
            # Extract IDs from Protein/Gene using regex (e.g., digits from "sp|P12345" or "GeneID=123")
            proteomics_df["Protein_ID"] = proteomics_df["Protein"].str.extract(r"(\d+)")
            genomics_df["Gene_ID"] = genomics_df["Gene"].str.extract(r"(\d+)")
            integrated_df = pd.merge(
                proteomics_df, genomics_df, left_on="Protein_ID", right_on="Gene_ID", 
                how="inner", suffixes=("_prot", "_geno")
            )

        if len(integrated_df) == 0:
            print(f"{Colors.RED}❌ No matches found between datasets.{Colors.RESET}")
            return None

        integrated_df.to_csv(output_path, index=False)
        print(f"{Colors.GREEN}✅ Integrated data saved: {output_path} ({len(integrated_df)} rows){Colors.RESET}")
        return output_path
    except Exception as e:
        print(f"{Colors.RED}❌ ERROR: Integration failed. {e}{Colors.RESET}")
        return None

# Biomarker analysis with regex and stats
def analyze_biomarkers(integrated_file: str, output_dir: str) -> Optional[str]:
    output_path = generate_filename("biomarkers", "csv", output_dir)
    biomarkers_only_path = generate_filename("biomarkers_only", "csv", output_dir)
    print(f"{Colors.BLUE}🔬 Analyzing biomarkers...{Colors.RESET}")
    try:
        df = pd.read_csv(integrated_file)
        
        # Determine which sequence column to use (prioritize proteomics)
        sequence_col = None
        if "Sequence_prot" in df.columns:
            sequence_col = "Sequence_prot"
            print(f"{Colors.YELLOW}🔍 Using proteomic sequence ('Sequence_prot') for biomarker analysis.{Colors.RESET}")
        elif "Sequence_geno" in df.columns:
            sequence_col = "Sequence_geno"
            print(f"{Colors.YELLOW}🔍 No proteomic sequence found. Using genomic sequence ('Sequence_geno') instead.{Colors.RESET}")
        elif "Sequence" in df.columns:
            sequence_col = "Sequence"
            print(f"{Colors.YELLOW}🔍 Using single sequence column ('Sequence') for biomarker analysis.{Colors.RESET}")
        else:
            raise ValueError("No sequence column found in the integrated data (expected 'Sequence', 'Sequence_prot', or 'Sequence_geno')")

        # Criteria for biomarkers
        # 1. Sequence length > 100
        df["Seq_Length"] = df[sequence_col].str.len()
        df["Length_Gt_100"] = df["Seq_Length"] > 100
        # 2. Contains specific motif "KR[ST]" (e.g., phosphorylation sites)
        motif_pattern = re.compile(r"KR[ST]")
        df["Has_Motif"] = df[sequence_col].apply(lambda x: bool(motif_pattern.search(str(x))))
        # 3. High variability in sequence (unique amino acids > 15)
        df["Unique_AA"] = df[sequence_col].apply(lambda x: len(set(str(x))))
        df["Unique_AA_Gt_15"] = df["Unique_AA"] > 15
        # 4. Exclude mitochondrial sequences if "Chromosome" is "MT"
        if "Chromosome" in df.columns:
            df["Is_Not_MT"] = df["Chromosome"].apply(lambda x: str(x).upper() != "MT")
        else:
            df["Is_Not_MT"] = True

        # Biomarker flag: combine all criteria
        df["Is_Biomarker"] = (
            df["Length_Gt_100"] & 
            df["Has_Motif"] & 
            df["Unique_AA_Gt_15"] & 
            df["Is_Not_MT"]
        )
        
        # Save full analysis (for reference)
        df.to_csv(output_path, index=False)
        
        # Extract only biomarkers
        biomarkers_df = df[df["Is_Biomarker"] == True]
        if biomarkers_df.empty:
            print(f"{Colors.YELLOW}⚠ No biomarkers identified.{Colors.RESET}")
        else:
            # Select relevant columns including criteria and Is_Biomarker
            relevant_columns = [col for col in [
                "Protein", "Protein_ID", "Gene", "Gene_ID", sequence_col, "Chromosome", 
                "Seq_Length", "Length_Gt_100", "Has_Motif", "Unique_AA", "Unique_AA_Gt_15", "Is_Not_MT", "Is_Biomarker"
            ] if col in df.columns]
            biomarkers_df = biomarkers_df[relevant_columns]
            biomarkers_df.to_csv(biomarkers_only_path, index=False)
            print(f"{Colors.GREEN}✅ Biomarkers-only output saved: {biomarkers_only_path} ({len(biomarkers_df)} biomarkers identified){Colors.RESET}")

        # Summary
        biomarker_count = df["Is_Biomarker"].sum()
        print(f"{Colors.GREEN}✅ Full analysis saved: {output_path} ({biomarker_count} biomarkers identified){Colors.RESET}")
        return output_path
    except Exception as e:
        print(f"{Colors.RED}❌ ERROR: Biomarker analysis failed. {e}{Colors.RESET}")
        return None
# Visualization with plotly for interactivity
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np

def visualize_data(analysis_file: str, output_dir: str) -> Optional[str]:
    output_path = generate_filename("visualization", "html", output_dir)  # Change to HTML for interactivity
    print(f"{Colors.BLUE}📊 Generating enhanced interactive visualization...{Colors.RESET}")
    try:
        df = pd.read_csv(analysis_file)
        
        # Ensure required columns exist
        if "Seq_Length" not in df.columns or "Is_Biomarker" not in df.columns:
            raise ValueError("Required columns 'Seq_Length' and 'Is_Biomarker' not found in the data.")
        
        # Debug: Print DataFrame columns and sample data for Chromosome
        print(f"{Colors.YELLOW}🔍 DataFrame columns: {list(df.columns)}{Colors.RESET}")
        if "Chromosome" in df.columns:
            print(f"{Colors.YELLOW}🔍 Sample Chromosome values: {df['Chromosome'].head().tolist()}{Colors.RESET}")
            # Replace NaN or empty values with a placeholder
            df["Chromosome"] = df["Chromosome"].fillna("Unknown")
        else:
            print(f"{Colors.YELLOW}🔍 Chromosome column not found in DataFrame.{Colors.RESET}")
        
        # Create subplots: 2 rows, 3 columns
        # Row 1: Histogram (col 1), Scatter (col 2), Violin (col 3)
        # Row 2: Table (spanning all columns)
        fig = make_subplots(
            rows=2, cols=3,
            subplot_titles=(
                "Sequence Length Distribution",
                "Unique AA vs. Sequence Length",
                "Seq Length Distribution by Biomarker",
                "Summary Statistics"
            ),
            specs=[
                [{"type": "histogram"}, {"type": "scatter"}, {"type": "violin"}],
                [{"type": "table", "colspan": 3}, None, None]
            ],
            column_widths=[0.4, 0.3, 0.3],
            row_heights=[0.7, 0.3],
            vertical_spacing=0.1
        )
        
        # --- Histogram (Sequence Length Distribution) ---
        hist_traces = []
        for biomarker_status in df["Is_Biomarker"].unique():
            hist_df = df[df["Is_Biomarker"] == biomarker_status]
            hist_trace = go.Histogram(
                x=hist_df["Seq_Length"],
                name=f"Biomarker: {biomarker_status}",
                marker_color="#FF7F0E" if biomarker_status else "#2CA02C",
                opacity=0.7,
                showlegend=True
            )
            hist_traces.append(hist_trace)
        
        for trace in hist_traces:
            fig.add_trace(trace, row=1, col=1)
        
        # Find the bin with the most biomarkers for annotation
        biomarker_df = df[df["Is_Biomarker"] == True]
        if not biomarker_df.empty:
            hist_data = go.Histogram(x=biomarker_df["Seq_Length"]).x
            bin_counts = pd.Series(hist_data).value_counts()
            if not bin_counts.empty:
                max_bin = bin_counts.idxmax()
                max_count = bin_counts.max()
                fig.add_annotation(
                    x=max_bin,
                    y=max_count,
                    text=f"Most Biomarkers: {max_count}",
                    showarrow=True,
                    arrowhead=2,
                    ax=20,
                    ay=-30,
                    row=1, col=1
                )
        
        # --- Scatter Plot (Unique_AA vs. Seq_Length) ---
        if "Unique_AA" in df.columns:
            scatter_trace = go.Scatter(
                x=df["Seq_Length"],
                y=df["Unique_AA"],
                mode="markers",
                marker=dict(
                    color=df["Is_Biomarker"].map({True: "#FF7F0E", False: "#2CA02C"}),
                    size=8,
                    opacity=0.6
                ),
                name="Data Points",
                showlegend=False
            )
            fig.add_trace(scatter_trace, row=1, col=2)
        
        # --- Violin Plot (Seq_Length Distribution by Is_Biomarker) ---
        for biomarker_status in df["Is_Biomarker"].unique():
            violin_df = df[df["Is_Biomarker"] == biomarker_status]
            violin_trace = go.Violin(
                x=[str(biomarker_status)] * len(violin_df),
                y=violin_df["Seq_Length"],
                name=f"Biomarker: {biomarker_status}",
                box_visible=True,
                meanline_visible=True,
                fillcolor="#FF7F0E" if biomarker_status else "#2CA02C",
                opacity=0.7,
                showlegend=False
            )
            fig.add_trace(violin_trace, row=1, col=3)
        
        # --- Summary Table ---
        # Compute summary statistics
        total_entries = len(df)
        total_biomarkers = df["Is_Biomarker"].sum()
        avg_seq_length = df["Seq_Length"].mean()
        avg_unique_aa = df["Unique_AA"].mean() if "Unique_AA" in df.columns else "N/A"
        
        table_trace = go.Table(
            header=dict(
                values=["Metric", "Value"],
                fill_color="paleturquoise",
                align="left"
            ),
            cells=dict(
                values=[
                    ["Total Entries", "Total Biomarkers", "Avg Sequence Length", "Avg Unique AA"],
                    [total_entries, total_biomarkers, f"{avg_seq_length:.2f}", f"{avg_unique_aa:.2f}" if avg_unique_aa != "N/A" else "N/A"]
                ],
                fill_color="lavender",
                align="left"
            )
        )
        fig.add_trace(table_trace, row=2, col=1)
        
        # --- Hover Template for Plots ---
        hover_cols = ["Protein", "Gene", "Chromosome", "Unique_AA", "Has_Motif"]
        available_cols = [col for col in hover_cols if col in df.columns]
        hover_template = "<b>Seq Length</b>: %{x}<br><b>Count</b>: %{y}<br><b>Biomarker</b>: %{customdata[0]}"
        for i, col in enumerate(available_cols, 1):
            hover_template += f"<br><b>{col}</b>: %{{customdata[{i}]}}"
        hover_template += "<extra></extra>"
        
        # Update traces with custom data and hover template (for non-table traces)
        custom_data = df[["Is_Biomarker"] + available_cols].values.T
        for trace in fig.data[:-1]:  # Exclude the table trace
            trace.customdata = custom_data.T
            trace.hovertemplate = hover_template
        
        # --- Add Dropdown for Filtering by Biomarker Status ---
        fig.update_layout(
            updatemenus=[
                dict(
                    buttons=[
                        dict(
                            label="All Data",
                            method="update",
                            args=[{"visible": [True] * len(fig.data)},
                                  {"title": "Sequence Length Analysis (All Data)"}]
                        ),
                        dict(
                            label="Biomarkers Only",
                            method="update",
                            args=[
                                {"visible": [True if "Biomarker: True" in trace.name else False for trace in fig.data[:-1]] + [True]},
                                {"title": "Sequence Length Analysis (Biomarkers Only)"}
                            ]
                        ),
                        dict(
                            label="Non-Biomarkers Only",
                            method="update",
                            args=[
                                {"visible": [True if "Biomarker: False" in trace.name else False for trace in fig.data[:-1]] + [True]},
                                {"title": "Sequence Length Analysis (Non-Biomarkers Only)"}
                            ]
                        )
                    ],
                    direction="down",
                    showactive=True,
                    x=0.1,
                    xanchor="left",
                    y=1.2,
                    yanchor="top"
                )
            ]
        )
        
        # --- Add Slider for Filtering by Seq_Length ---
        min_seq_length = int(df["Seq_Length"].min())
        max_seq_length = int(df["Seq_Length"].max())
        fig.update_layout(
            sliders=[
                dict(
                    active=0,
                    currentvalue={"prefix": "Seq Length Range: "},
                    pad={"t": 50},
                    steps=[
                        dict(
                            label=f"{min_seq_length} - {max_seq_length}",
                            method="update",
                            args=[
                                {"x": [df["Seq_Length"]] * len(hist_traces) + [df["Seq_Length"]] + [df["Seq_Length"]] * 2},
                                {"y": [None] * len(hist_traces) + [df["Unique_AA"]] + [df["Seq_Length"]] * 2},
                                {"visible": [True] * len(fig.data)}
                            ]
                        )
                        for min_val in range(min_seq_length, max_seq_length, (max_seq_length - min_seq_length) // 10)
                    ] + [
                        dict(
                            label=f"{max_seq_length}",
                            method="update",
                            args=[
                                {"x": [df["Seq_Length"]] * len(hist_traces) + [df["Seq_Length"]] + [df["Seq_Length"]] * 2},
                                {"y": [None] * len(hist_traces) + [df["Unique_AA"]] + [df["Seq_Length"]] * 2},
                                {"visible": [True] * len(fig.data)}
                            ]
                        )
                    ]
                )
            ]
        )
        
        # Customize layout
        fig.update_layout(
            title="Sequence Length Analysis",
            xaxis_title="Sequence Length",
            yaxis_title="Count",
            xaxis2_title="Sequence Length",
            yaxis2_title="Unique Amino Acids",
            xaxis3_title="Biomarker Status",
            yaxis3_title="Sequence Length",
            legend_title="Biomarker Status",
            bargap=0.1,
            hovermode="closest",
            height=800,
            width=1400,
            margin=dict(t=150)  # Extra space for dropdown and slider
        )
        
        # Save as interactive HTML file
        fig.write_html(output_path)
        
        print(f"{Colors.GREEN}✅ Enhanced interactive visualization saved: {output_path} (Open in a web browser){Colors.RESET}")
        return output_path
    except Exception as e:
        print(f"{Colors.RED}❌ ERROR: Visualization failed. {e}{Colors.RESET}")
        return None

# Main CLI loop
def main():
    print(f"\n{Colors.BLUE}🔹 Welcome to the Proteogenomics CLI Tool 🔹{Colors.RESET}")
    print(f"{Colors.YELLOW}Available commands: {', '.join(COMMANDS)}{Colors.RESET}")
    
    output_dir = get_output_directory()
    
    while True:
        print(f"\n{Colors.BLUE}🔧 Enter a command ({', '.join(COMMANDS)}):{Colors.RESET}")
        command = input().strip().lower()
        
        if command not in COMMANDS:
            print(f"{Colors.RED}❌ Invalid command. Available: {', '.join(COMMANDS)}{Colors.RESET}")
            continue
        
        if command == "exit":
            print(f"{Colors.GREEN}👋 Exiting the tool. Bye!{Colors.RESET}")
            break
        
        if command == "parse":
            print(f"{Colors.YELLOW}📌 Parsing: Choose data type (proteomics/genomics):{Colors.RESET}")
            data_type = input().strip().lower()
            if data_type not in ["proteomics", "genomics"]:
                print(f"{Colors.RED}❌ Invalid data type. Use 'proteomics' or 'genomics'.{Colors.RESET}")
                continue
            file_path = input(f"Enter {data_type} FASTA file path: ").strip()
            parser = parse_proteomics if data_type == "proteomics" else parse_genomics
            parser(file_path, output_dir)
        
        elif command == "integrate":
            proteomics_file = input("Enter proteomics CSV file path: ").strip()
            genomics_file = input("Enter genomics CSV file path: ").strip()
            integrate_data(proteomics_file, genomics_file, output_dir)
        
        elif command == "analyze":
            integrated_file = input("Enter integrated CSV file path: ").strip()
            analyze_biomarkers(integrated_file, output_dir)
        
        elif command == "visualize":
            analysis_file = input("Enter analysis CSV file path: ").strip()
            visualize_data(analysis_file, output_dir)

if __name__ == "__main__":
    main()
