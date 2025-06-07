import io
from datetime import datetime
from typing import Dict, List, Optional
import pandas as pd
import streamlit as st
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie
from reportlab.lib.colors import HexColor
import plotly.graph_objects as go
import plotly.io as pio

class PDFGenerator:
    """Generates PDF reports for biomarker analysis results"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        """Setup custom styles for the PDF"""
        # Title style
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            textColor=HexColor('#FF6B6B'),
            alignment=1  # Center alignment
        )
        
        # Header style
        self.header_style = ParagraphStyle(
            'CustomHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            textColor=HexColor('#2C3E50'),
            borderWidth=0,
            borderColor=HexColor('#FF6B6B'),
            borderPadding=5
        )
        
        # Subheader style
        self.subheader_style = ParagraphStyle(
            'CustomSubHeader',
            parent=self.styles['Heading3'],
            fontSize=14,
            spaceAfter=8,
            textColor=HexColor('#34495E')
        )
        
        # Body style
        self.body_style = ParagraphStyle(
            'CustomBody',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=6,
            textColor=HexColor('#2C3E50')
        )
        
        # Disclaimer style
        self.disclaimer_style = ParagraphStyle(
            'Disclaimer',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=HexColor('#E74C3C'),
            borderWidth=1,
            borderColor=HexColor('#E74C3C'),
            borderPadding=8,
            backColor=HexColor('#FADAD7')
        )
    
    def generate_analysis_report(self, analysis_name: str, results_df: pd.DataFrame, 
                               summary_stats: Dict, user_name: str) -> Optional[bytes]:
        """Generate a comprehensive PDF report for biomarker analysis"""
        try:
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(
                buffer,
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=18
            )
            
            # Build the story (content)
            story = []
            
            # Title and header
            story.append(Paragraph("ProteogenomiX", self.title_style))
            story.append(Paragraph("Advanced Biomarker Identification Tool", self.styles['Normal']))
            story.append(Spacer(1, 20))
            
            # Analysis information
            story.append(Paragraph(f"Analysis Report: {analysis_name}", self.header_style))
            story.append(Spacer(1, 12))
            
            # Report metadata
            metadata_data = [
                ['Generated For:', user_name],
                ['Analysis Name:', analysis_name],
                ['Generated On:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
                ['Total Entries:', f"{summary_stats.get('total_entries', 0):,}"],
                ['Biomarkers Found:', f"{summary_stats.get('biomarker_count', 0):,}"],
                ['Success Rate:', f"{summary_stats.get('biomarker_percentage', 0):.2f}%"]
            ]
            
            metadata_table = Table(metadata_data, colWidths=[2*inch, 3*inch])
            metadata_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), HexColor('#F8F9FA')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, HexColor('#E0E0E0')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('ROWBACKGROUNDS', (0, 0), (-1, -1), [HexColor('#FFFFFF'), HexColor('#F8F9FA')])
            ]))
            story.append(metadata_table)
            story.append(Spacer(1, 20))
            
            # Medical disclaimer
            disclaimer_text = """
            <b>IMPORTANT MEDICAL DISCLAIMER:</b><br/>
            These are potential biomarkers for research purposes only. 
            Please verify all results independently before any clinical application or real-world implementation. 
            This tool is not intended for clinical diagnosis or treatment decisions.
            """
            story.append(Paragraph(disclaimer_text, self.disclaimer_style))
            story.append(Spacer(1, 20))
            
            # Executive Summary
            story.append(Paragraph("Executive Summary", self.header_style))
            
            summary_text = f"""
            This analysis processed {summary_stats.get('total_entries', 0):,} biological sequences and identified 
            {summary_stats.get('biomarker_count', 0):,} potential biomarkers ({summary_stats.get('biomarker_percentage', 0):.2f}% success rate).
            
            The average sequence length was {summary_stats.get('avg_sequence_length', 0):.0f} amino acids, 
            with sequences ranging from {summary_stats.get('min_sequence_length', 0)} to {summary_stats.get('max_sequence_length', 0)} amino acids.
            
            {summary_stats.get('motif_percentage', 0):.1f}% of sequences contained the target motif pattern, 
            and {summary_stats.get('length_criteria_percentage', 0):.1f}% met the minimum length requirement.
            """
            story.append(Paragraph(summary_text, self.body_style))
            story.append(Spacer(1, 15))
            
            # Analysis Criteria
            story.append(Paragraph("Biomarker Identification Criteria", self.header_style))
            
            criteria_text = """
            Biomarkers were identified based on the following computational criteria:
            <br/><br/>
            <b>1. Sequence Length > 100 amino acids:</b> Longer sequences are more likely to represent functional proteins
            <br/><br/>
            <b>2. Motif Presence (KR[ST]):</b> Contains specific patterns associated with phosphorylation sites
            <br/><br/>
            <b>3. Amino Acid Diversity > 15:</b> High variability indicates potential functional importance
            <br/><br/>
            <b>4. Non-Mitochondrial Origin:</b> Excludes mitochondrial sequences for most biomarker applications
            <br/><br/>
            <b>Final Classification:</b> Sequences meeting ALL criteria are classified as potential biomarkers
            """
            story.append(Paragraph(criteria_text, self.body_style))
            story.append(Spacer(1, 20))
            
            # Results Summary Table
            story.append(Paragraph("Results Summary", self.header_style))
            
            # Create summary statistics table
            biomarkers_df = results_df[results_df['Is_Biomarker'] == True] if 'Is_Biomarker' in results_df.columns else pd.DataFrame()
            
            summary_data = [
                ['Metric', 'All Sequences', 'Biomarkers Only', 'Percentage'],
                ['Total Count', f"{len(results_df):,}", f"{len(biomarkers_df):,}", f"{len(biomarkers_df)/len(results_df)*100:.1f}%" if len(results_df) > 0 else "0%"],
                ['Avg Length', f"{results_df['Seq_Length'].mean():.0f}", f"{biomarkers_df['Seq_Length'].mean():.0f}" if len(biomarkers_df) > 0 else "N/A", ""],
                ['Min Length', f"{results_df['Seq_Length'].min()}", f"{biomarkers_df['Seq_Length'].min()}" if len(biomarkers_df) > 0 else "N/A", ""],
                ['Max Length', f"{results_df['Seq_Length'].max()}", f"{biomarkers_df['Seq_Length'].max()}" if len(biomarkers_df) > 0 else "N/A", ""],
                ['With Motif', f"{results_df['Has_Motif'].sum():,}", f"{biomarkers_df['Has_Motif'].sum():,}" if len(biomarkers_df) > 0 else "0", f"{results_df['Has_Motif'].sum()/len(results_df)*100:.1f}%"],
                ['Length > 100', f"{results_df['Length_Gt_100'].sum():,}", f"{biomarkers_df['Length_Gt_100'].sum():,}" if len(biomarkers_df) > 0 else "0", f"{results_df['Length_Gt_100'].sum()/len(results_df)*100:.1f}%"]
            ]
            
            summary_table = Table(summary_data, colWidths=[2*inch, 1.5*inch, 1.5*inch, 1*inch])
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), HexColor('#FF6B6B')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 1, HexColor('#E0E0E0')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#FFFFFF'), HexColor('#F8F9FA')])
            ]))
            story.append(summary_table)
            story.append(Spacer(1, 20))
            
            # Top biomarkers table (if any)
            if len(biomarkers_df) > 0:
                story.append(Paragraph("Top Biomarker Candidates", self.header_style))
                
                # Select top biomarkers (by sequence length or other criteria)
                top_biomarkers = biomarkers_df.nlargest(10, 'Seq_Length')
                
                biomarker_data = [['Protein/Gene', 'Length', 'Unique AA', 'Has Motif', 'Chromosome']]
                
                for _, row in top_biomarkers.iterrows():
                    protein_name = row.get('Protein', row.get('Gene', 'Unknown'))[:25] + "..." if len(str(row.get('Protein', row.get('Gene', 'Unknown')))) > 25 else str(row.get('Protein', row.get('Gene', 'Unknown')))
                    biomarker_data.append([
                        protein_name,
                        str(row['Seq_Length']),
                        str(row['Unique_AA']),
                        "Yes" if row['Has_Motif'] else "No",
                        str(row.get('Chromosome', 'N/A'))[:10]
                    ])
                
                biomarker_table = Table(biomarker_data, colWidths=[2.5*inch, 0.8*inch, 0.8*inch, 0.8*inch, 1.1*inch])
                biomarker_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), HexColor('#34495E')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 8),
                    ('GRID', (0, 0), (-1, -1), 1, HexColor('#E0E0E0')),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#FFFFFF'), HexColor('#F8F9FA')])
                ]))
                story.append(biomarker_table)
                story.append(Spacer(1, 20))
            
            # Recommendations
            story.append(Paragraph("Recommendations and Next Steps", self.header_style))
            
            recommendations_text = """
            <b>1. Experimental Validation:</b> Validate computational predictions using appropriate laboratory methods
            <br/><br/>
            <b>2. Literature Review:</b> Cross-reference identified biomarkers with published research
            <br/><br/>
            <b>3. Functional Analysis:</b> Investigate biological functions and pathways of identified proteins
            <br/><br/>
            <b>4. Clinical Relevance:</b> Assess relevance to specific diseases or conditions (if applicable)
            <br/><br/>
            <b>5. Quality Control:</b> Verify sequence quality and annotation accuracy
            <br/><br/>
            <b>6. Regulatory Compliance:</b> Ensure compliance with relevant guidelines before clinical application
            """
            story.append(Paragraph(recommendations_text, self.body_style))
            story.append(Spacer(1, 20))
            
            # Footer
            story.append(Paragraph("Technical Notes", self.subheader_style))
            footer_text = f"""
            Report generated by ProteogenomiX v1.0 on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            <br/>
            Analysis algorithm based on sequence-based biomarker identification criteria
            <br/>
            For technical support or questions, contact support@proteogenomix.com
            """
            story.append(Paragraph(footer_text, self.styles['Normal']))
            
            # Build PDF
            doc.build(story)
            
            # Get PDF data
            buffer.seek(0)
            pdf_data = buffer.getvalue()
            buffer.close()
            
            return pdf_data
            
        except Exception as e:
            st.error(f"Error generating PDF report: {str(e)}")
            return None
    
    def generate_summary_report(self, user_analyses: List[Dict], user_name: str) -> Optional[bytes]:
        """Generate a summary report of all user analyses"""
        try:
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(
                buffer,
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=18
            )
            
            story = []
            
            # Title
            story.append(Paragraph("ProteogenomiX", self.title_style))
            story.append(Paragraph("User Analysis Summary Report", self.styles['Normal']))
            story.append(Spacer(1, 20))
            
            # User information
            story.append(Paragraph(f"Analysis Summary for: {user_name}", self.header_style))
            story.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", self.body_style))
            story.append(Spacer(1, 15))
            
            # Overall statistics
            total_analyses = len(user_analyses)
            total_biomarkers = sum(analysis.get('biomarker_count', 0) for analysis in user_analyses)
            total_entries = sum(analysis.get('total_entries', 0) for analysis in user_analyses)
            
            stats_data = [
                ['Metric', 'Value'],
                ['Total Analyses', f"{total_analyses:,}"],
                ['Total Biomarkers Found', f"{total_biomarkers:,}"],
                ['Total Entries Processed', f"{total_entries:,}"],
                ['Average Biomarkers per Analysis', f"{total_biomarkers/total_analyses:.1f}" if total_analyses > 0 else "0"],
                ['Overall Success Rate', f"{total_biomarkers/total_entries*100:.2f}%" if total_entries > 0 else "0%"]
            ]
            
            stats_table = Table(stats_data, colWidths=[3*inch, 2*inch])
            stats_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), HexColor('#FF6B6B')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, HexColor('#E0E0E0')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            story.append(stats_table)
            story.append(Spacer(1, 20))
            
            # Analysis history table
            story.append(Paragraph("Analysis History", self.header_style))
            
            history_data = [['Analysis Name', 'Date', 'Biomarkers', 'Total Entries', 'Success Rate']]
            
            for analysis in user_analyses[:20]:  # Show last 20 analyses
                success_rate = (analysis.get('biomarker_count', 0) / analysis.get('total_entries', 1) * 100) if analysis.get('total_entries', 0) > 0 else 0
                history_data.append([
                    analysis.get('analysis_name', 'Unknown')[:25] + "..." if len(analysis.get('analysis_name', 'Unknown')) > 25 else analysis.get('analysis_name', 'Unknown'),
                    analysis.get('created_at', 'Unknown')[:10],
                    str(analysis.get('biomarker_count', 0)),
                    str(analysis.get('total_entries', 0)),
                    f"{success_rate:.1f}%"
                ])
            
            history_table = Table(history_data, colWidths=[2*inch, 1*inch, 1*inch, 1*inch, 1*inch])
            history_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), HexColor('#34495E')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, HexColor('#E0E0E0')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#FFFFFF'), HexColor('#F8F9FA')])
            ]))
            story.append(history_table)
            
            # Build PDF
            doc.build(story)
            
            buffer.seek(0)
            pdf_data = buffer.getvalue()
            buffer.close()
            
            return pdf_data
            
        except Exception as e:
            st.error(f"Error generating summary report: {str(e)}")
            return None
