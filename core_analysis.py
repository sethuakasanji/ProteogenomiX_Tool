import pandas as pd
import re
import time
from typing import Dict, Optional, Tuple, List
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from io import StringIO

def parse_fasta_data(content: str, data_type: str) -> pd.DataFrame:
    """
    Parse FASTA content and return DataFrame
    Adapted from original CLI tool
    """
    print(f"Parsing {data_type} FASTA data...")
    
    # Initialize data structure based on type
    if data_type == 'proteomics':
        data = {"Protein": [], "Sequence": []}
    else:  # genomics
        data = {"Gene": [], "Chromosome": [], "Sequence": []}
    
    current_entry = {key: "" for key in data.keys()}
    kv_pattern = re.compile(r"(\w+)=(\S+)")
    
    lines = content.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        if line.startswith(">"):
            # Save previous entry
            if any(current_entry.values()):
                for key in data:
                    data[key].append(current_entry[key])
            
            # Reset current entry
            current_entry = {key: "" for key in data.keys()}
            
            # Parse header
            header = line[1:]
            header_dict = dict(kv_pattern.findall(header))
            
            if data_type == 'proteomics':
                # Extract protein ID
                protein_id = header_dict.get("ID", header.split()[0])
                current_entry["Protein"] = protein_id
            else:  # genomics
                # Extract gene and chromosome info
                gene_id = header_dict.get("GeneID", 
                         header_dict.get("gene", 
                         header_dict.get("GN", header.split()[0])))
                chromosome = header_dict.get("chromosome", 
                           header_dict.get("chr", ""))
                current_entry["Gene"] = gene_id
                current_entry["Chromosome"] = chromosome
        else:
            # Append sequence
            current_entry["Sequence"] += line
    
    # Save last entry
    if any(current_entry.values()):
        for key in data:
            data[key].append(current_entry[key])
    
    df = pd.DataFrame(data)
    print(f"Parsed {len(df)} entries from {data_type} data")
    return df

def integrate_datasets(proteomics_df: pd.DataFrame, genomics_df: pd.DataFrame) -> pd.DataFrame:
    """
    Integrate proteomics and genomics datasets
    Adapted from original CLI tool
    """
    print("Integrating proteomics and genomics datasets...")
    
    integrated_df = pd.DataFrame()
    
    # Try sequence-based matching first
    if "Sequence" in proteomics_df.columns and "Sequence" in genomics_df.columns:
        integrated_df = pd.merge(
            proteomics_df, genomics_df, 
            on="Sequence", how="inner", 
            suffixes=("_prot", "_geno")
        )
        print(f"Sequence-based matching: {len(integrated_df)} entries")
    
    # If no sequence matches or insufficient matches, try ID-based matching
    if len(integrated_df) == 0:
        print("Attempting ID-based integration...")
        
        # Extract IDs using regex
        proteomics_df_copy = proteomics_df.copy()
        genomics_df_copy = genomics_df.copy()
        
        proteomics_df_copy["Protein_ID"] = proteomics_df_copy["Protein"].str.extract(r"(\d+)")
        genomics_df_copy["Gene_ID"] = genomics_df_copy["Gene"].str.extract(r"(\d+)")
        
        integrated_df = pd.merge(
            proteomics_df_copy, genomics_df_copy,
            left_on="Protein_ID", right_on="Gene_ID",
            how="inner", suffixes=("_prot", "_geno")
        )
        print(f"ID-based matching: {len(integrated_df)} entries")
    
    if len(integrated_df) == 0:
        print("Warning: No matches found between datasets")
        # Return empty DataFrame with expected columns
        return pd.DataFrame(columns=['Protein', 'Sequence_prot', 'Gene', 'Chromosome', 'Sequence_geno'])
    
    print(f"Successfully integrated {len(integrated_df)} entries")
    return integrated_df

def analyze_biomarkers(integrated_df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Analyze integrated data to identify biomarkers
    Adapted from original CLI tool
    """
    print("Analyzing biomarkers...")
    
    if integrated_df.empty:
        return pd.DataFrame(), pd.DataFrame()
    
    df = integrated_df.copy()
    
    # Determine sequence column to use
    sequence_col = None
    if "Sequence_prot" in df.columns:
        sequence_col = "Sequence_prot"
    elif "Sequence_geno" in df.columns:
        sequence_col = "Sequence_geno"
    elif "Sequence" in df.columns:
        sequence_col = "Sequence"
    else:
        raise ValueError("No sequence column found in integrated data")
    
    print(f"Using sequence column: {sequence_col}")
    
    # Biomarker criteria analysis
    # 1. Sequence length > 100
    df["Seq_Length"] = df[sequence_col].str.len()
    df["Length_Gt_100"] = df["Seq_Length"] > 100
    
    # 2. Contains specific motif "KR[ST]" (phosphorylation sites)
    motif_pattern = re.compile(r"KR[ST]")
    df["Has_Motif"] = df[sequence_col].apply(
        lambda x: bool(motif_pattern.search(str(x))) if pd.notna(x) else False
    )
    
    # 3. High variability in sequence (unique amino acids > 15)
    df["Unique_AA"] = df[sequence_col].apply(
        lambda x: len(set(str(x))) if pd.notna(x) else 0
    )
    df["Unique_AA_Gt_15"] = df["Unique_AA"] > 15
    
    # 4. Exclude mitochondrial sequences
    if "Chromosome" in df.columns:
        df["Is_Not_MT"] = df["Chromosome"].apply(
            lambda x: str(x).upper() != "MT" if pd.notna(x) else True
        )
    else:
        df["Is_Not_MT"] = True
    
    # Combined biomarker flag
    df["Is_Biomarker"] = (
        df["Length_Gt_100"] & 
        df["Has_Motif"] & 
        df["Unique_AA_Gt_15"] & 
        df["Is_Not_MT"]
    )
    
    # Extract biomarkers
    biomarkers_df = df[df["Is_Biomarker"] == True].copy()
    
    # Select relevant columns for biomarkers output
    biomarker_columns = []
    for col in ["Protein", "Protein_ID", "Gene", "Gene_ID", sequence_col, 
                "Chromosome", "Seq_Length", "Length_Gt_100", "Has_Motif", 
                "Unique_AA", "Unique_AA_Gt_15", "Is_Not_MT", "Is_Biomarker"]:
        if col in df.columns:
            biomarker_columns.append(col)
    
    biomarkers_df = biomarkers_df[biomarker_columns]
    
    biomarker_count = len(biomarkers_df)
    print(f"Identified {biomarker_count} biomarkers out of {len(df)} total entries")
    
    return biomarkers_df, df

def generate_visualizations(analysis_df: pd.DataFrame) -> Dict[str, go.Figure]:
    """
    Generate interactive visualizations using Plotly
    Enhanced version of original CLI tool visualizations
    """
    print("Generating interactive visualizations...")
    
    if analysis_df.empty:
        return {}
    
    visualizations = {}
    
    # 1. Sequence Length Distribution
    fig1 = go.Figure()
    
    for biomarker_status in [True, False]:
        subset = analysis_df[analysis_df["Is_Biomarker"] == biomarker_status]
        if not subset.empty:
            fig1.add_trace(go.Histogram(
                x=subset["Seq_Length"],
                name=f"Biomarker: {biomarker_status}",
                opacity=0.7,
                marker_color="#FF7F0E" if biomarker_status else "#2CA02C"
            ))
    
    fig1.update_layout(
        title="Sequence Length Distribution",
        xaxis_title="Sequence Length",
        yaxis_title="Count",
        barmode='overlay',
        template="plotly_white"
    )
    visualizations["sequence_length_distribution"] = fig1
    
    # 2. Unique Amino Acids vs Sequence Length Scatter Plot
    fig2 = px.scatter(
        analysis_df,
        x="Seq_Length",
        y="Unique_AA",
        color="Is_Biomarker",
        title="Unique Amino Acids vs Sequence Length",
        labels={
            "Seq_Length": "Sequence Length",
            "Unique_AA": "Unique Amino Acids",
            "Is_Biomarker": "Is Biomarker"
        },
        template="plotly_white"
    )
    visualizations["scatter_unique_vs_length"] = fig2
    
    # 3. Biomarker Criteria Summary
    criteria_data = {
        'Criteria': ['Length > 100', 'Has Motif', 'Unique AA > 15', 'Not Mitochondrial'],
        'Count': [
            analysis_df["Length_Gt_100"].sum(),
            analysis_df["Has_Motif"].sum(),
            analysis_df["Unique_AA_Gt_15"].sum(),
            analysis_df["Is_Not_MT"].sum()
        ]
    }
    
    fig3 = px.bar(
        criteria_data,
        x='Criteria',
        y='Count',
        title="Biomarker Criteria Distribution",
        template="plotly_white"
    )
    visualizations["criteria_distribution"] = fig3
    
    # 4. Chromosome Distribution (if available)
    if "Chromosome" in analysis_df.columns:
        chrom_counts = analysis_df["Chromosome"].value_counts().head(10)
        
        fig4 = px.bar(
            x=chrom_counts.index,
            y=chrom_counts.values,
            title="Top 10 Chromosomes by Entry Count",
            labels={"x": "Chromosome", "y": "Count"},
            template="plotly_white"
        )
        visualizations["chromosome_distribution"] = fig4
    
    # 5. Biomarker vs Non-Biomarker Pie Chart
    biomarker_counts = analysis_df["Is_Biomarker"].value_counts()
    
    fig5 = px.pie(
        values=biomarker_counts.values,
        names=["Non-Biomarker", "Biomarker"],
        title="Biomarker vs Non-Biomarker Distribution",
        template="plotly_white"
    )
    visualizations["biomarker_pie_chart"] = fig5
    
    # 6. Sequence Length Box Plot by Biomarker Status
    fig6 = px.box(
        analysis_df,
        x="Is_Biomarker",
        y="Seq_Length",
        title="Sequence Length Distribution by Biomarker Status",
        labels={
            "Is_Biomarker": "Is Biomarker",
            "Seq_Length": "Sequence Length"
        },
        template="plotly_white"
    )
    visualizations["sequence_length_boxplot"] = fig6
    
    print(f"Generated {len(visualizations)} visualizations")
    return visualizations

def validate_fasta_format(content: str) -> bool:
    """Validate FASTA file format"""
    lines = content.strip().split('\n')
    has_header = False
    has_sequence = False
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith('>'):
            has_header = True
        elif has_header and not line.startswith('>'):
            has_sequence = True
            break
    
    return has_header and has_sequence

def get_processing_stats(analysis_df: pd.DataFrame) -> Dict:
    """Get processing statistics"""
    if analysis_df.empty:
        return {}
    
    stats = {
        'total_entries': len(analysis_df),
        'biomarkers_identified': analysis_df["Is_Biomarker"].sum(),
        'avg_sequence_length': analysis_df["Seq_Length"].mean(),
        'max_sequence_length': analysis_df["Seq_Length"].max(),
        'min_sequence_length': analysis_df["Seq_Length"].min(),
        'avg_unique_aa': analysis_df["Unique_AA"].mean(),
        'sequences_with_motif': analysis_df["Has_Motif"].sum(),
        'sequences_length_gt_100': analysis_df["Length_Gt_100"].sum()
    }
    
    return stats
