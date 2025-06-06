import streamlit as st
import os
import sys
from pathlib import Path

# Add core modules to path
sys.path.append(str(Path(__file__).parent))

from core.auth import AuthManager
from core.database import DatabaseManager

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_data' not in st.session_state:
    st.session_state.user_data = None
if 'subscription_plan' not in st.session_state:
    st.session_state.subscription_plan = 'freemium'

# Page configuration
st.set_page_config(
    page_title="ProteogenomiX - Advanced Biomarker Identification Tool",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize managers
auth_manager = AuthManager()
db_manager = DatabaseManager()

def show_login_page():
    """Display login/registration page"""
    st.title("🧬 ProteogenomiX")
    st.subheader("Advanced Biomarker Identification Tool")
    
    # Medical Disclaimer
    st.error("""
    ⚠️ **IMPORTANT MEDICAL DISCLAIMER**: 
    This tool identifies potential biomarkers for research purposes only. 
    All results must be independently verified before any clinical application or real-world implementation. 
    This tool is not intended for clinical diagnosis, treatment decisions, or patient care.
    """)
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        st.subheader("Login to Your Account")
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")
            
            if submit:
                if auth_manager.authenticate(email, password):
                    st.session_state.authenticated = True
                    st.session_state.user_data = auth_manager.get_user_data(email)
                    st.session_state.subscription_plan = st.session_state.user_data.get('subscription_plan', 'freemium')
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid credentials")
    
    with tab2:
        st.subheader("Create New Account")
        with st.form("register_form"):
            reg_email = st.text_input("Email Address")
            reg_password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            full_name = st.text_input("Full Name")
            organization = st.text_input("Organization (Optional)")
            agree_terms = st.checkbox("I agree to the Terms of Service and Privacy Policy")
            
            submit_reg = st.form_submit_button("Create Account")
            
            if submit_reg:
                if not agree_terms:
                    st.error("Please agree to the Terms of Service and Privacy Policy")
                elif reg_password != confirm_password:
                    st.error("Passwords do not match")
                elif len(reg_password) < 8:
                    st.error("Password must be at least 8 characters long")
                elif auth_manager.register_user(reg_email, reg_password, full_name, organization):
                    st.success("Account created successfully! Please login.")
                else:
                    st.error("Registration failed. Email may already exist.")

def show_main_app():
    """Display main application"""
    # Sidebar with user info
    with st.sidebar:
        st.image("data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHZpZXdCb3g9IjAgMCA0MCA0MCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGNpcmNsZSBjeD0iMjAiIGN5PSIyMCIgcj0iMjAiIGZpbGw9IiNGRjZCNkIiLz4KPHN2ZyB4PSI4IiB5PSI4IiB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSI+CjxwYXRoIGQ9Ik0xMiAyQzYuNDggMiAyIDYuNDggMiAxMlM2LjQ4IDIyIDEyIDIyUzIyIDE3LjUyIDIyIDEyUzE3LjUyIDIgMTIgMloiIGZpbGw9IndoaXRlIi8+CjxwYXRoIGQ9Ik0xMiA2VjE4TTYgMTJIMTgiIHN0cm9rZT0iI0ZGNkI2QiIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiLz4KPC9zdmc+Cjwvc3ZnPgo=", width=40)
        st.write(f"**{st.session_state.user_data['full_name']}**")
        st.write(f"Plan: **{st.session_state.subscription_plan.title()}**")
        
        if st.button("Logout", type="secondary"):
            st.session_state.authenticated = False
            st.session_state.user_data = None
            st.session_state.subscription_plan = 'freemium'
            st.rerun()
    
    # Main content
    st.title("🧬 ProteogenomiX Dashboard")
    st.subheader("Advanced Biomarker Identification Tool")
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Analyses", db_manager.get_user_analysis_count(st.session_state.user_data['email']))
    with col2:
        plan_limit = "Unlimited" if st.session_state.subscription_plan == 'premium' else "5/month"
        st.metric("Plan Limit", plan_limit)
    with col3:
        st.metric("Files Processed", db_manager.get_user_file_count(st.session_state.user_data['email']))
    with col4:
        st.metric("Biomarkers Found", db_manager.get_user_biomarker_count(st.session_state.user_data['email']))
    
    # Navigation cards
    st.markdown("---")
    st.subheader("Available Tools")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        with st.container():
            st.markdown("### 🔬 Analysis")
            st.write("Upload and analyze proteomics/genomics data")
            if st.button("Start Analysis", key="analysis_btn", type="primary"):
                st.switch_page("pages/1_🔬_Analysis.py")
    
    with col2:
        with st.container():
            st.markdown("### 📊 Dashboard")
            st.write("View your analysis results and history")
            if st.button("View Dashboard", key="dashboard_btn", type="primary"):
                st.switch_page("pages/2_📊_Dashboard.py")
    
    with col3:
        with st.container():
            st.markdown("### 💳 Subscription")
            st.write("Manage your subscription and billing")
            if st.button("Manage Subscription", key="subscription_btn", type="primary"):
                st.switch_page("pages/3_💳_Subscription.py")
    
    # Recent activity
    st.markdown("---")
    st.subheader("Recent Activity")
    recent_analyses = db_manager.get_recent_analyses(st.session_state.user_data['email'], limit=5)
    
    if recent_analyses:
        for analysis in recent_analyses:
            with st.expander(f"Analysis: {analysis['analysis_name']} - {analysis['created_at']}"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"**Status:** {analysis['status']}")
                with col2:
                    st.write(f"**Files:** {analysis['file_count']}")
                with col3:
                    st.write(f"**Biomarkers:** {analysis['biomarker_count']}")
    else:
        st.info("No recent analyses. Start your first analysis using the Analysis tool above!")

def main():
    """Main application entry point"""
    if not st.session_state.authenticated:
        show_login_page()
    else:
        show_main_app()

if __name__ == "__main__":
    main()
