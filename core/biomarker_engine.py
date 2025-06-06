import pandas as pd
import re
import os
import time
from typing import Dict, Optional, Tuple, List
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

class ProteogenomicsEngine:
    """Core engine for proteogenomics analysis based on the original CLI tool"""
    
    def __init__(self):
        self.results = {}
        self.processing_status = "idle"
    
    def parse_fasta(self, file_content: str, file_type: str, progress_callback=None) -> Optional[pd.DataFrame]:
        """
        Parse FASTA content with dynamic key-value handling
        """
        try:
            lines = file_content.strip().split('\n')
            
            if file_type == "proteomics":
                fields = {
                    "Protein": lambda header, kv: kv.get("ID", header.split()[0]),
                    "Sequence": None
                }
            else:  # genomics
                fields = {
                    "Gene": lambda header, kv: kv.get("GeneID", kv.get("gene", kv.get("GN", header.split()[0]))),
                    "Chromosome": lambda header, kv: kv.get("chromosome", kv.get("chr", "")),
                    "Sequence": None
                }
            
            data: Dict[str, list] = {key: [] for key in fields.keys()}
            current_entry: Dict[str, str] = {key: "" for key in fields.keys()}
            kv_pattern = re.compile(r"(\w+)=(\S+)")
            
            total_lines = len(lines)
            for i, line in enumerate(lines):
                if progress_callback:
                    progress_callback(i / total_lines)
                
                line = line.strip()
                if not line:
                    continue
                    
                if line.startswith(">"):
                    # Save previous entry
                    if any(current_entry.values()):
                        for key in fields:
                            data[key].append(current_entry[key])
                    
                    # Start new entry
                    current_entry = {key: "" for key in fields.keys()}
                    header = line[1:]
                    header_dict = dict(kv_pattern.findall(header))
                    
                    for key, parser in fields.items():
                        if parser:
                            current_entry[key] = parser(header, header_dict)
                else:
                    current_entry["Sequence"] += line
            
            # Save last entry
            if any(current_entry.values()):
                for key in fields:
                    data[key].append(current_entry[key])
            
            if not any(data.values()):
                raise ValueError("No valid data found in FASTA file")
            
            df = pd.DataFrame(data)
            return df
            
        except Exception as e:
            st.error(f"Error parsing FASTA file: {str(e)}")
            return None
    
    def integrate_data(self, proteomics_df: pd.DataFrame, genomics_df: pd.DataFrame, progress_callback=None) -> Optional[pd.DataFrame]:
        """
        Integrate proteomics and genomics data
        """
        try:
            if progress_callback:
                progress_callback(0.1)
            
            # Try sequence-based matching first
            if "Sequence" in proteomics_df.columns and "Sequence" in genomics_df.columns:
                integrated_df = pd.merge(
                    proteomics_df, genomics_df, on="Sequence", how="inner", suffixes=("_prot", "_geno")
                )
                
                if progress_callback:
                    progress_callback(0.5)
                
                if len(integrated_df) > 0:
                    if progress_callback:
                        progress_callback(1.0)
                    return integrated_df
            
            # Fallback to ID-based matching
            if progress_callback:
                progress_callback(0.6)
            
            # Extract IDs using regex
            proteomics_df["Protein_ID"] = proteomics_df["Protein"].str.extract(r"(\d+)")
            genomics_df["Gene_ID"] = genomics_df["Gene"].str.extract(r"(\d+)")
            
            integrated_df = pd.merge(
                proteomics_df, genomics_df, 
                left_on="Protein_ID", right_on="Gene_ID", 
                how="inner", suffixes=("_prot", "_geno")
            )
            
            if progress_callback:
                progress_callback(1.0)
            
            if len(integrated_df) == 0:
                raise ValueError("No matches found between datasets")
            
            return integrated_df
            
        except Exception as e:
            st.error(f"Error integrating data: {str(e)}")
            return None
    
    def analyze_biomarkers(self, integrated_df: pd.DataFrame, progress_callback=None) -> Optional[pd.DataFrame]:
        """
        Analyze biomarkers with enhanced criteria
        """
        try:
            if progress_callback:
                progress_callback(0.1)
            
            # Determine sequence column
            sequence_col = None
            if "Sequence_prot" in integrated_df.columns:
                sequence_col = "Sequence_prot"
            elif "Sequence_geno" in integrated_df.columns:
                sequence_col = "Sequence_geno"
            elif "Sequence" in integrated_df.columns:
                sequence_col = "Sequence"
            else:
                raise ValueError("No sequence column found in integrated data")
            
            if progress_callback:
                progress_callback(0.3)
            
            # Biomarker criteria
            integrated_df["Seq_Length"] = integrated_df[sequence_col].str.len()
            integrated_df["Length_Gt_100"] = integrated_df["Seq_Length"] > 100
            
            if progress_callback:
                progress_callback(0.5)
            
            # Motif analysis
            motif_pattern = re.compile(r"KR[ST]")
            integrated_df["Has_Motif"] = integrated_df[sequence_col].apply(
                lambda x: bool(motif_pattern.search(str(x)))
            )
            
            if progress_callback:
                progress_callback(0.7)
            
            # Unique amino acids
            integrated_df["Unique_AA"] = integrated_df[sequence_col].apply(
                lambda x: len(set(str(x)))
            )
            integrated_df["Unique_AA_Gt_15"] = integrated_df["Unique_AA"] > 15
            
            # Exclude mitochondrial sequences
            if "Chromosome" in integrated_df.columns:
                integrated_df["Is_Not_MT"] = integrated_df["Chromosome"].apply(
                    lambda x: str(x).upper() != "MT"
                )
            else:
                integrated_df["Is_Not_MT"] = True
            
            if progress_callback:
                progress_callback(0.9)
            
            # Combined biomarker flag
            integrated_df["Is_Biomarker"] = (
                integrated_df["Length_Gt_100"] & 
                integrated_df["Has_Motif"] & 
                integrated_df["Unique_AA_Gt_15"] & 
                integrated_df["Is_Not_MT"]
            )
            
            if progress_callback:
                progress_callback(1.0)
            
            return integrated_df
            
        except Exception as e:
            st.error(f"Error analyzing biomarkers: {str(e)}")
            return None
    
    def generate_visualizations(self, analysis_df: pd.DataFrame) -> Dict[str, go.Figure]:
        """
        Generate interactive visualizations using Plotly
        """
        try:
            visualizations = {}
            
            # 1. Sequence Length Distribution
            fig_hist = px.histogram(
                analysis_df, 
                x="Seq_Length", 
                color="Is_Biomarker",
                title="Sequence Length Distribution",
                labels={"Seq_Length": "Sequence Length", "count": "Count"},
                color_discrete_map={True: "#FF7F0E", False: "#2CA02C"}
            )
            fig_hist.update_layout(height=400)
            visualizations["length_distribution"] = fig_hist
            
            # 2. Biomarker Criteria Analysis
            criteria_data = {
                "Criteria": ["Length > 100", "Has Motif", "Unique AA > 15", "Not MT", "Final Biomarkers"],
                "Count": [
                    analysis_df["Length_Gt_100"].sum(),
                    analysis_df["Has_Motif"].sum(),
                    analysis_df["Unique_AA_Gt_15"].sum(),
                    analysis_df["Is_Not_MT"].sum(),
                    analysis_df["Is_Biomarker"].sum()
                ]
            }
            
            fig_criteria = px.bar(
                criteria_data,
                x="Criteria",
                y="Count",
                title="Biomarker Criteria Analysis",
                color="Count",
                color_continuous_scale="viridis"
            )
            fig_criteria.update_layout(height=400)
            visualizations["criteria_analysis"] = fig_criteria
            
            # 3. Unique AA vs Sequence Length Scatter
            fig_scatter = px.scatter(
                analysis_df,
                x="Seq_Length",
                y="Unique_AA",
                color="Is_Biomarker",
                title="Unique Amino Acids vs Sequence Length",
                labels={"Seq_Length": "Sequence Length", "Unique_AA": "Unique Amino Acids"},
                color_discrete_map={True: "#FF7F0E", False: "#2CA02C"}
            )
            fig_scatter.update_layout(height=400)
            visualizations["scatter_plot"] = fig_scatter
            
            # 4. Chromosome Distribution (if available)
            if "Chromosome" in analysis_df.columns and analysis_df["Chromosome"].notna().any():
                chromosome_counts = analysis_df.groupby(["Chromosome", "Is_Biomarker"]).size().reset_index(name="Count")
                fig_chromosome = px.bar(
                    chromosome_counts,
                    x="Chromosome",
                    y="Count",
                    color="Is_Biomarker",
                    title="Biomarker Distribution by Chromosome",
                    color_discrete_map={True: "#FF7F0E", False: "#2CA02C"}
                )
                fig_chromosome.update_layout(height=400)
                visualizations["chromosome_distribution"] = fig_chromosome
            
            return visualizations
            
        except Exception as e:
            st.error(f"Error generating visualizations: {str(e)}")
            return {}
    
    def get_analysis_summary(self, analysis_df: pd.DataFrame) -> Dict:
        """
        Generate analysis summary statistics
        """
        try:
            total_entries = len(analysis_df)
            biomarker_count = analysis_df["Is_Biomarker"].sum()
            biomarker_percentage = (biomarker_count / total_entries) * 100 if total_entries > 0 else 0
            
            summary = {
                "total_entries": total_entries,
                "biomarker_count": int(biomarker_count),
                "biomarker_percentage": round(biomarker_percentage, 2),
                "avg_sequence_length": round(analysis_df["Seq_Length"].mean(), 2),
                "max_sequence_length": int(analysis_df["Seq_Length"].max()),
                "min_sequence_length": int(analysis_df["Seq_Length"].min()),
                "avg_unique_aa": round(analysis_df["Unique_AA"].mean(), 2),
                "motif_percentage": round((analysis_df["Has_Motif"].sum() / total_entries) * 100, 2),
                "length_criteria_percentage": round((analysis_df["Length_Gt_100"].sum() / total_entries) * 100, 2)
            }
            
            return summary
            
        except Exception as e:
            st.error(f"Error generating summary: {str(e)}")
            return {}
