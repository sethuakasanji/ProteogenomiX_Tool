import streamlit as st
import sys
from pathlib import Path
import pandas as pd
import time

# Add core modules to path
sys.path.append(str(Path(__file__).parent.parent))

from core.biomarker_engine import ProteogenomicsEngine
from core.auth import AuthManager
from core.database import DatabaseManager
from core.file_handler import FileHandler
from core.email_service import EmailService

# Check authentication
if not st.session_state.get('authenticated', False):
    st.error("Please log in to access this page")
    st.switch_page("app.py")
    st.stop()

# Initialize managers
engine = ProteogenomicsEngine()
auth_manager = AuthManager()
db_manager = DatabaseManager()
file_handler = FileHandler()
email_service = EmailService()

st.title("🔬 Biomarker Analysis")
st.subheader("Upload and analyze your proteomics and genomics data")

# Medical disclaimer
st.error("""
⚠️ **MEDICAL DISCLAIMER**: 
These are potential biomarkers for research purposes only. 
Please verify all results independently before any clinical application or real-world implementation. 
This tool is not intended for clinical diagnosis or treatment decisions.
""")

# Check user limits
user_email = st.session_state.user_data['email']
can_analyze, limit_message = auth_manager.can_perform_analysis(user_email)

if not can_analyze:
    st.error(f"❌ {limit_message}")
    if st.button("Upgrade to Premium", type="primary"):
        st.switch_page("pages/3_💳_Subscription.py")
    st.stop()

st.info(f"ℹ️ {limit_message}")

# Analysis configuration
st.markdown("---")
st.subheader("Analysis Configuration")

analysis_name = st.text_input(
    "Analysis Name", 
    placeholder="Enter a descriptive name for your analysis",
    help="Give your analysis a unique name for easy identification"
)

# File upload section
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📄 Proteomics Data")
    st.write("Upload FASTA file containing protein sequences")
    
    proteomics_option = st.radio(
        "Choose data source:",
        ["Upload File", "Use Sample Data"],
        key="proteomics_option"
    )
    
    if proteomics_option == "Upload File":
        proteomics_file = st.file_uploader(
            "Choose proteomics FASTA file",
            type=['fasta', 'fa', 'fas'],
            help="Maximum file size: 100MB"
        )
        proteomics_content = None
        if proteomics_file:
            is_valid, message = file_handler.validate_file(proteomics_file, "fasta")
            if is_valid:
                proteomics_content = file_handler.read_fasta_file(proteomics_file)
                if proteomics_content:
                    file_info = file_handler.get_file_info(proteomics_file)
                    st.success(f"✅ File loaded: {file_info['name']} ({file_info['size_formatted']})")
            else:
                st.error(f"❌ {message}")
    else:
        st.info("📋 Using sample proteomics data")
        proteomics_content = file_handler.create_sample_fasta("proteomics")
        proteomics_file = "sample_proteomics.fasta"

with col2:
    st.markdown("### 🧬 Genomics Data")
    st.write("Upload FASTA file containing genomic sequences")
    
    genomics_option = st.radio(
        "Choose data source:",
        ["Upload File", "Use Sample Data"],
        key="genomics_option"
    )
    
    if genomics_option == "Upload File":
        genomics_file = st.file_uploader(
            "Choose genomics FASTA file",
            type=['fasta', 'fa', 'fas'],
            help="Maximum file size: 100MB"
        )
        genomics_content = None
        if genomics_file:
            is_valid, message = file_handler.validate_file(genomics_file, "fasta")
            if is_valid:
                genomics_content = file_handler.read_fasta_file(genomics_file)
                if genomics_content:
                    file_info = file_handler.get_file_info(genomics_file)
                    st.success(f"✅ File loaded: {file_info['name']} ({file_info['size_formatted']})")
            else:
                st.error(f"❌ {message}")
    else:
        st.info("📋 Using sample genomics data")
        genomics_content = file_handler.create_sample_fasta("genomics")
        genomics_file = "sample_genomics.fasta"

# Analysis button
st.markdown("---")
if st.button("🚀 Start Analysis", type="primary", disabled=not analysis_name or not proteomics_content or not genomics_content):
    if not analysis_name:
        st.error("Please enter an analysis name")
    elif not proteomics_content or not genomics_content:
        st.error("Please upload both proteomics and genomics files")
    else:
        # Start analysis
        with st.spinner("Running biomarker analysis..."):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Step 1: Parse proteomics data
                status_text.text("Parsing proteomics data...")
                proteomics_df = engine.parse_fasta(
                    proteomics_content, 
                    "proteomics",
                    lambda p: progress_bar.progress(p * 0.2)
                )
                
                if proteomics_df is None:
                    st.error("Failed to parse proteomics data")
                    st.stop()
                
                # Step 2: Parse genomics data
                status_text.text("Parsing genomics data...")
                genomics_df = engine.parse_fasta(
                    genomics_content,
                    "genomics", 
                    lambda p: progress_bar.progress(0.2 + p * 0.2)
                )
                
                if genomics_df is None:
                    st.error("Failed to parse genomics data")
                    st.stop()
                
                # Step 3: Integrate data
                status_text.text("Integrating datasets...")
                integrated_df = engine.integrate_data(
                    proteomics_df,
                    genomics_df,
                    lambda p: progress_bar.progress(0.4 + p * 0.3)
                )
                
                if integrated_df is None or len(integrated_df) == 0:
                    st.error("Failed to integrate data or no matches found between datasets")
                    st.stop()
                
                # Step 4: Analyze biomarkers
                status_text.text("Analyzing biomarkers...")
                analysis_df = engine.analyze_biomarkers(
                    integrated_df,
                    lambda p: progress_bar.progress(0.7 + p * 0.3)
                )
                
                if analysis_df is None:
                    st.error("Failed to analyze biomarkers")
                    st.stop()
                
                progress_bar.progress(1.0)
                status_text.text("Analysis complete!")
                
                # Save results to database
                summary_stats = engine.get_analysis_summary(analysis_df)
                analysis_id = db_manager.save_analysis_result(
                    user_email,
                    analysis_name,
                    "integrated_analysis",
                    getattr(proteomics_file, 'name', 'sample_proteomics.fasta'),
                    getattr(genomics_file, 'name', 'sample_genomics.fasta'),
                    analysis_df,
                    summary_stats
                )
                
                # Update user analysis count
                auth_manager.increment_analysis_count(user_email)
                
                # Display results
                st.success("🎉 Analysis completed successfully!")
                
                # Results summary
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Entries", summary_stats['total_entries'])
                with col2:
                    st.metric("Biomarkers Found", summary_stats['biomarker_count'])
                with col3:
                    st.metric("Success Rate", f"{summary_stats['biomarker_percentage']:.1f}%")
                with col4:
                    st.metric("Avg Sequence Length", f"{summary_stats['avg_sequence_length']:.0f}")
                
                # Display data table
                st.subheader("📊 Analysis Results")
                
                # Filter options
                col1, col2 = st.columns(2)
                with col1:
                    show_biomarkers_only = st.checkbox("Show biomarkers only", value=True)
                with col2:
                    show_criteria = st.checkbox("Show criteria columns", value=True)
                
                # Prepare display dataframe
                display_df = analysis_df.copy()
                if show_biomarkers_only:
                    display_df = display_df[display_df['Is_Biomarker'] == True]
                
                if not show_criteria:
                    criteria_cols = ['Length_Gt_100', 'Has_Motif', 'Unique_AA_Gt_15', 'Is_Not_MT']
                    display_df = display_df.drop(columns=[col for col in criteria_cols if col in display_df.columns])
                
                st.dataframe(
                    display_df,
                    use_container_width=True,
                    height=400
                )
                
                # Download options
                st.subheader("📥 Download Results")
                col1, col2 = st.columns(2)
                
                with col1:
                    # CSV download
                    csv_data = analysis_df.to_csv(index=False)
                    st.download_button(
                        label="📄 Download Full Results (CSV)",
                        data=csv_data,
                        file_name=f"{analysis_name}_results.csv",
                        mime="text/csv"
                    )
                
                with col2:
                    # Biomarkers only CSV
                    biomarkers_df = analysis_df[analysis_df['Is_Biomarker'] == True]
                    biomarkers_csv = biomarkers_df.to_csv(index=False)
                    st.download_button(
                        label="🔬 Download Biomarkers Only (CSV)",
                        data=biomarkers_csv,
                        file_name=f"{analysis_name}_biomarkers.csv",
                        mime="text/csv"
                    )
                
                # Send completion email
                try:
                    email_service.send_analysis_completion_email(
                        user_email,
                        st.session_state.user_data['full_name'],
                        analysis_name,
                        summary_stats['biomarker_count'],
                        summary_stats['total_entries']
                    )
                except:
                    pass  # Don't fail analysis if email fails
                
                # Navigation to dashboard
                if st.button("📊 View in Dashboard", type="secondary"):
                    st.switch_page("pages/2_📊_Dashboard.py")
                
            except Exception as e:
                st.error(f"Analysis failed: {str(e)}")
                st.error("Please check your input files and try again.")

# Help section
with st.expander("❓ Help & Tips"):
    st.markdown("""
    ### File Format Requirements
    
    **FASTA Files:**
    - Must start with '>' character
    - Header line followed by sequence data
    - Supports standard FASTA format
    - Maximum file size: 100MB
    
    **Sample Header Formats:**
    
    **Proteomics:**
    ```
    >sp|P04637|P53_HUMAN Cellular tumor antigen p53 OS=Homo sapiens GN=TP53 PE=1 SV=4
    ```
    
    **Genomics:**
    ```
    >GeneID=7157|chr=17|gene=TP53 Homo sapiens tumor protein p53
    ```
    
    ### Biomarker Criteria
    
    Our algorithm identifies potential biomarkers based on:
    1. **Sequence Length > 100**: Longer sequences are more likely to be functional proteins
    2. **Motif Presence**: Contains specific patterns like "KR[ST]" (phosphorylation sites)
    3. **Amino Acid Diversity > 15**: High variability indicates functional importance
    4. **Non-Mitochondrial**: Excludes mitochondrial sequences for most applications
    
    ### Analysis Limits
    
    - **Freemium**: 5 analyses per month
    - **Premium**: Unlimited analyses
    
    ### Need Help?
    Contact our support team through the Feedback page if you encounter any issues.
    """)
