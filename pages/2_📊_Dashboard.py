import streamlit as st
import pandas as pd
import io
import time
from pathlib import Path
import os
import sys

# Add core modules to path
sys.path.append(str(Path(__file__).parent.parent))

from core.biomarker_engine import ProteogenomicsEngine
from core.database import DatabaseManager
from core.auth import AuthManager
from core.email_service import EmailService
from utils.visualization import VisualizationGenerator

# Page configuration
st.set_page_config(
    page_title="Dashboard - ProteogenomiX",
    page_icon="🧬",
    layout="wide"
)

# Check authentication
if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.error("Please login to access the dashboard")
    st.stop()

# Initialize services
@st.cache_resource
def init_services():
    db_manager = DatabaseManager()
    auth_manager = AuthManager()
    email_service = EmailService()
    biomarker_engine = ProteogenomicsEngine()
    viz_generator = VisualizationGenerator()
    return db_manager, auth_manager, email_service, biomarker_engine, viz_generator

db_manager, auth_manager, email_service, biomarker_engine, viz_generator = init_services()

st.title("🧬 ProteogenomiX Dashboard")
st.write("Upload and analyze your proteomics and genomics data")

# Medical disclaimer
st.warning("""
⚠️ **Medical Disclaimer**: These are potential biomarkers for research purposes only. 
Please verify all results independently before any clinical application or real-world implementation. 
This tool is not intended for clinical diagnosis or treatment decisions.
""")

# User plan information
user_data = st.session_state.get('user_data', {})
user_plan = user_data.get('subscription_plan', 'freemium')
plan_features = auth_manager.get_plan_features(user_plan)

# Plan information sidebar
with st.sidebar:
    st.subheader(f"📋 Your Plan: {user_plan.title()}")
    st.write(f"**Max File Size:** {plan_features['max_file_size']}")
    st.write(f"**Processing:** {plan_features['file_processing']}")
    st.write(f"**Visualizations:** {plan_features['visualizations']}")
    st.write(f"**Export Formats:** {', '.join(plan_features['export_formats'])}")
    
    if user_plan == 'freemium':
        st.info("💡 Upgrade to Premium for unlimited processing and advanced features!")

# Main dashboard
tab1, tab2, tab3 = st.tabs(["📤 Upload Files", "🔬 Sample Data", "📊 Recent Analyses"])

with tab1:
    st.subheader("Upload Your Data Files")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Proteomics Data (FASTA)**")
        proteomics_file = st.file_uploader(
            "Choose proteomics FASTA file",
            type=['fasta', 'fa', 'txt'],
            key="proteomics_upload"
        )
        
        if proteomics_file:
            file_size = len(proteomics_file.getvalue())
            st.write(f"File size: {file_size / (1024*1024):.2f} MB")
            
            # Check file size limits
            user_email = st.session_state.get('user_data', {}).get('email', '')
            if not auth_manager.check_file_size_limit(user_email, file_size):
                st.error(f"File size exceeds your plan limit of {plan_features['max_file_size']}")
                proteomics_file = None
    
    with col2:
        st.write("**Genomics Data (FASTA)**")
        genomics_file = st.file_uploader(
            "Choose genomics FASTA file",
            type=['fasta', 'fa', 'txt'],
            key="genomics_upload"
        )
        
        if genomics_file:
            file_size = len(genomics_file.getvalue())
            st.write(f"File size: {file_size / (1024*1024):.2f} MB")
            
            # Check file size limits
            if not auth_manager.check_file_size_limit(st.session_state.user_email, file_size):
                st.error(f"File size exceeds your plan limit of {plan_features['max_file_size']}")
                genomics_file = None
    
    # Process files
    if st.button("🚀 Start Analysis", type="primary", use_container_width=True):
        if not proteomics_file or not genomics_file:
            st.error("Please upload both proteomics and genomics files")
        else:
            # Create analysis record
            analysis_id = db_manager.create_analysis(
                st.session_state.user_email,
                f"{proteomics_file.name} + {genomics_file.name}",
                "combined"
            )
            
            # Process files
            with st.spinner("Processing your data... This may take a few minutes."):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Read file contents
                status_text.text("Reading files...")
                progress_bar.progress(20)
                
                proteomics_content = proteomics_file.getvalue().decode('utf-8')
                genomics_content = genomics_file.getvalue().decode('utf-8')
                
                # Process with biomarker engine
                status_text.text("Analyzing biomarkers...")
                progress_bar.progress(50)
                
                result = biomarker_engine.process_files(
                    proteomics_content,
                    genomics_content,
                    st.session_state.user_email,
                    analysis_id
                )
                
                progress_bar.progress(90)
                
                if result["success"]:
                    progress_bar.progress(100)
                    status_text.text("Analysis complete!")
                    
                    st.success(f"""
                    ✅ **Analysis Complete!**
                    - Total sequences: {result['total_sequences']}
                    - Biomarkers found: {result['biomarker_count']}
                    - Success rate: {result['biomarker_percentage']}%
                    """)
                    
                    # Store results in session for immediate viewing
                    st.session_state[f'analysis_{analysis_id}'] = result
                    
                    # Send email notification
                    user_info = auth_manager.get_user_info(st.session_state.user_email)
                    if user_info:
                        email_service.send_analysis_complete_email(
                            st.session_state.user_email,
                            user_info['name'],
                            analysis_id,
                            result['biomarker_count']
                        )
                    
                    # Show quick results
                    if 'results_df' in result:
                        st.subheader("Quick Results Preview")
                        df = result['results_df']
                        
                        # Show biomarkers only
                        biomarkers_df = df[df['Is_Biomarker'] == True]
                        if not biomarkers_df.empty:
                            st.write("**Identified Biomarkers:**")
                            display_cols = [col for col in ['Protein', 'Gene', 'Seq_Length', 'Unique_AA'] if col in biomarkers_df.columns]
                            st.dataframe(biomarkers_df[display_cols].head(10))
                        else:
                            st.info("No biomarkers identified with current criteria.")
                        
                        # Download options
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            csv_data = df.to_csv(index=False)
                            st.download_button(
                                "📄 Download Full Results (CSV)",
                                csv_data,
                                f"proteogenomix_analysis_{analysis_id}.csv",
                                "text/csv",
                                use_container_width=True
                            )
                        
                        with col2:
                            if not biomarkers_df.empty:
                                biomarkers_csv = biomarkers_df.to_csv(index=False)
                                st.download_button(
                                    "🧬 Download Biomarkers Only (CSV)",
                                    biomarkers_csv,
                                    f"proteogenomix_biomarkers_{analysis_id}.csv",
                                    "text/csv",
                                    use_container_width=True
                                )
                else:
                    st.error(f"Analysis failed: {result.get('error', 'Unknown error')}")

with tab2:
    st.subheader("🧪 Try Sample Data")
    st.write("Test the platform with our sample proteomics and genomics data")
    
    sample_data = biomarker_engine.get_sample_data()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Sample Proteomics Data**")
        with st.expander("View sample proteomics FASTA"):
            st.code(sample_data["proteomics"][:500] + "...", language="text")
    
    with col2:
        st.write("**Sample Genomics Data**")
        with st.expander("View sample genomics FASTA"):
            st.code(sample_data["genomics"][:500] + "...", language="text")
    
    if st.button("🧪 Analyze Sample Data", type="secondary", use_container_width=True):
        # Create analysis record
        analysis_id = db_manager.create_analysis(
            st.session_state.user_email,
            "sample_data.fasta",
            "sample"
        )
        
        with st.spinner("Processing sample data..."):
            progress_bar = st.progress(0)
            
            progress_bar.progress(30)
            time.sleep(0.5)  # Simulate processing time
            
            result = biomarker_engine.process_files(
                sample_data["proteomics"],
                sample_data["genomics"],
                st.session_state.user_email,
                analysis_id
            )
            
            progress_bar.progress(100)
            
            if result["success"]:
                st.success(f"""
                ✅ **Sample Analysis Complete!**
                - Total sequences: {result['total_sequences']}
                - Biomarkers found: {result['biomarker_count']}
                - Success rate: {result['biomarker_percentage']}%
                """)
                
                # Show sample results
                if 'results_df' in result:
                    df = result['results_df']
                    biomarkers_df = df[df['Is_Biomarker'] == True]
                    
                    if not biomarkers_df.empty:
                        st.write("**Sample Biomarkers Found:**")
                        display_cols = [col for col in ['Protein', 'Gene', 'Seq_Length', 'Has_Motif', 'Unique_AA'] if col in biomarkers_df.columns]
                        st.dataframe(biomarkers_df[display_cols])
                    
                    # Download sample results
                    csv_data = df.to_csv(index=False)
                    st.download_button(
                        "📄 Download Sample Results",
                        csv_data,
                        f"proteogenomix_sample_analysis.csv",
                        "text/csv"
                    )
            else:
                st.error(f"Sample analysis failed: {result.get('error', 'Unknown error')}")

with tab3:
    st.subheader("📊 Your Recent Analyses")
    
    user_analyses = db_manager.get_user_analyses(st.session_state.user_email)
    
    if user_analyses:
        for analysis in user_analyses[:10]:  # Show last 10
            with st.expander(f"📊 {analysis['filename']} - {analysis['created_at'][:16]}"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write(f"**Status:** {analysis['status']}")
                    st.write(f"**Type:** {analysis['file_type']}")
                
                with col2:
                    st.write(f"**Biomarkers:** {analysis.get('biomarkers_count', 'N/A')}")
                    st.write(f"**Total Sequences:** {analysis.get('total_sequences', 'N/A')}")
                
                with col3:
                    if analysis['status'] == 'completed':
                        if st.button(f"View Results", key=f"view_{analysis['id']}"):
                            st.switch_page("pages/2_📊_Analysis.py")
                    else:
                        st.write(f"Status: {analysis['status']}")
    else:
        st.info("No analyses yet. Upload your first files above to get started!")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 12px;'>
    <p>ProteogenomiX - Advanced Biomarker Identification Tool</p>
    <p>For research purposes only. Not for clinical use.</p>
</div>
""", unsafe_allow_html=True)
