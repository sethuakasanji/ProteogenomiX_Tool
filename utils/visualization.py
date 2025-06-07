import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Dict, List, Optional

class VisualizationGenerator:
    """Generates interactive visualizations for proteomics and genomics analysis"""
    
    def __init__(self):
        self.color_palette = [
            '#2E86AB', '#A23B72', '#F18F01', '#C73E1D',
            '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4',
            '#FFEAA7', '#DDA0DD', '#98D8C8', '#F7DC6F'
        ]
    
    def create_biomarker_distribution(self, df: pd.DataFrame) -> go.Figure:
        """Create biomarker distribution visualization"""
        fig = go.Figure()
        
        if 'biomarker_score' in df.columns:
            fig.add_trace(go.Histogram(
                x=df['biomarker_score'],
                nbinsx=30,
                name='Biomarker Score Distribution',
                marker_color='#2E86AB',
                opacity=0.7
            ))
            
            fig.update_layout(
                title='Biomarker Score Distribution',
                xaxis_title='Biomarker Score',
                yaxis_title='Frequency',
                template='plotly_white',
                height=400
            )
        
        return fig
    
    def create_expression_heatmap(self, df: pd.DataFrame) -> go.Figure:
        """Create expression level heatmap"""
        fig = go.Figure()
        
        if all(col in df.columns for col in ['protein_id', 'gene_id', 'expression_level']):
            # Create a pivot table for heatmap
            pivot_data = df.pivot_table(
                index='protein_id', 
                columns='gene_id', 
                values='expression_level', 
                aggfunc='mean'
            ).fillna(0)
            
            fig.add_trace(go.Heatmap(
                z=pivot_data.values,
                x=pivot_data.columns,
                y=pivot_data.index,
                colorscale='Viridis',
                name='Expression Levels'
            ))
            
            fig.update_layout(
                title='Expression Level Heatmap',
                xaxis_title='Gene ID',
                yaxis_title='Protein ID',
                template='plotly_white',
                height=600
            )
        
        return fig
    
    def create_correlation_plot(self, df: pd.DataFrame) -> go.Figure:
        """Create correlation plot between proteomics and genomics data"""
        fig = go.Figure()
        
        if all(col in df.columns for col in ['proteomics_value', 'genomics_value']):
            fig.add_trace(go.Scatter(
                x=df['proteomics_value'],
                y=df['genomics_value'],
                mode='markers',
                marker=dict(
                    size=8,
                    color=df.get('biomarker_score', '#2E86AB'),
                    colorscale='Viridis',
                    showscale=True,
                    colorbar=dict(title="Biomarker Score")
                ),
                text=df.get('protein_id', ''),
                hovertemplate='<b>%{text}</b><br>' +
                             'Proteomics: %{x}<br>' +
                             'Genomics: %{y}<extra></extra>',
                name='Data Points'
            ))
            
            # Add trend line
            if len(df) > 1:
                z = np.polyfit(df['proteomics_value'], df['genomics_value'], 1)
                p = np.poly1d(z)
                fig.add_trace(go.Scatter(
                    x=df['proteomics_value'],
                    y=p(df['proteomics_value']),
                    mode='lines',
                    name='Trend Line',
                    line=dict(color='red', dash='dash')
                ))
            
            fig.update_layout(
                title='Proteomics vs Genomics Correlation',
                xaxis_title='Proteomics Value',
                yaxis_title='Genomics Value',
                template='plotly_white',
                height=500
            )
        
        return fig
    
    def create_top_biomarkers_chart(self, df: pd.DataFrame, top_n: int = 20) -> go.Figure:
        """Create top biomarkers bar chart"""
        fig = go.Figure()
        
        if 'biomarker_score' in df.columns and 'protein_id' in df.columns:
            top_biomarkers = df.nlargest(top_n, 'biomarker_score')
            
            fig.add_trace(go.Bar(
                x=top_biomarkers['biomarker_score'],
                y=top_biomarkers['protein_id'],
                orientation='h',
                marker_color='#A23B72',
                name='Biomarker Score'
            ))
            
            fig.update_layout(
                title=f'Top {top_n} Potential Biomarkers',
                xaxis_title='Biomarker Score',
                yaxis_title='Protein ID',
                template='plotly_white',
                height=600,
                yaxis=dict(tickmode='linear')
            )
        
        return fig
    
    def create_pathway_enrichment_plot(self, df: pd.DataFrame) -> go.Figure:
        """Create pathway enrichment visualization"""
        fig = go.Figure()
        
        if 'pathway' in df.columns and 'enrichment_score' in df.columns:
            pathway_scores = df.groupby('pathway')['enrichment_score'].mean().sort_values(ascending=True)
            
            fig.add_trace(go.Bar(
                x=pathway_scores.values,
                y=pathway_scores.index,
                orientation='h',
                marker_color='#F18F01',
                name='Enrichment Score'
            ))
            
            fig.update_layout(
                title='Pathway Enrichment Analysis',
                xaxis_title='Enrichment Score',
                yaxis_title='Biological Pathway',
                template='plotly_white',
                height=500
            )
        
        return fig
    
    def create_volcano_plot(self, df: pd.DataFrame) -> go.Figure:
        """Create volcano plot for differential expression"""
        fig = go.Figure()
        
        if all(col in df.columns for col in ['log_fold_change', 'p_value']):
            # Calculate -log10(p_value)
            df['neg_log_p'] = -np.log10(df['p_value'].replace(0, 1e-300))
            
            # Color points based on significance
            colors = []
            for _, row in df.iterrows():
                if abs(row['log_fold_change']) > 1 and row['p_value'] < 0.05:
                    colors.append('red')
                elif abs(row['log_fold_change']) > 1:
                    colors.append('orange')
                elif row['p_value'] < 0.05:
                    colors.append('blue')
                else:
                    colors.append('grey')
            
            fig.add_trace(go.Scatter(
                x=df['log_fold_change'],
                y=df['neg_log_p'],
                mode='markers',
                marker=dict(
                    color=colors,
                    size=6,
                    opacity=0.7
                ),
                text=df.get('protein_id', ''),
                hovertemplate='<b>%{text}</b><br>' +
                             'Log Fold Change: %{x}<br>' +
                             '-Log10(p-value): %{y}<extra></extra>',
                name='Proteins'
            ))
            
            # Add significance lines
            fig.add_hline(y=-np.log10(0.05), line_dash="dash", line_color="red", 
                         annotation_text="p=0.05")
            fig.add_vline(x=1, line_dash="dash", line_color="red")
            fig.add_vline(x=-1, line_dash="dash", line_color="red")
            
            fig.update_layout(
                title='Volcano Plot - Differential Expression',
                xaxis_title='Log2 Fold Change',
                yaxis_title='-Log10(p-value)',
                template='plotly_white',
                height=500
            )
        
        return fig
    
    def create_summary_dashboard(self, analysis_data: Dict) -> Dict[str, go.Figure]:
        """Create a comprehensive dashboard with multiple visualizations"""
        figures = {}
        
        if 'biomarker_df' in analysis_data:
            df = analysis_data['biomarker_df']
            
            figures['distribution'] = self.create_biomarker_distribution(df)
            figures['top_biomarkers'] = self.create_top_biomarkers_chart(df)
            
            if all(col in df.columns for col in ['proteomics_value', 'genomics_value']):
                figures['correlation'] = self.create_correlation_plot(df)
            
            if all(col in df.columns for col in ['log_fold_change', 'p_value']):
                figures['volcano'] = self.create_volcano_plot(df)
            
            if 'pathway' in df.columns:
                figures['pathway'] = self.create_pathway_enrichment_plot(df)
        
        return figures
    
    def create_analysis_summary_metrics(self, df: pd.DataFrame) -> Dict:
        """Create summary metrics for analysis results"""
        metrics = {
            'total_proteins': len(df) if 'protein_id' in df.columns else 0,
            'significant_biomarkers': 0,
            'avg_biomarker_score': 0,
            'top_score': 0
        }
        
        if 'biomarker_score' in df.columns:
            metrics['significant_biomarkers'] = len(df[df['biomarker_score'] > 0.7])
            metrics['avg_biomarker_score'] = df['biomarker_score'].mean()
            metrics['top_score'] = df['biomarker_score'].max()
        
        return metrics