import streamlit as st
import sys
from pathlib import Path
from datetime import datetime

# Add core modules to path
sys.path.append(str(Path(__file__).parent.parent))

from core.database import DatabaseManager
from core.email_service import EmailService

# Check authentication
if not st.session_state.get('authenticated', False):
    st.error("Please log in to access this page")
    st.switch_page("app.py")
    st.stop()

# Initialize managers
db_manager = DatabaseManager()
email_service = EmailService()

st.title("💬 Feedback & Support")
st.subheader("Help us improve ProteogenomiX")

user_email = st.session_state.user_data['email']
user_name = st.session_state.user_data['full_name']

# Feedback type selection
st.markdown("---")
st.subheader("📝 What would you like to share?")

feedback_type = st.selectbox(
    "Type of Feedback",
    ["Bug Report", "Feature Request", "General Feedback", "Technical Support", "Billing Support"],
    help="Select the type of feedback you'd like to provide"
)

# Dynamic form based on feedback type
st.markdown("---")

if feedback_type == "Bug Report":
    st.subheader("🐛 Bug Report")
    st.write("Help us fix issues by providing detailed information about the problem.")
    
    with st.form("bug_report_form"):
        col1, col2 = st.columns(2)
        with col1:
            severity = st.selectbox(
                "Severity",
                ["Low", "Medium", "High", "Critical"],
                help="How severely does this bug affect your work?"
            )
        with col2:
            browser = st.selectbox(
                "Browser",
                ["Chrome", "Firefox", "Safari", "Edge", "Other"],
                help="Which browser were you using?"
            )
        
        bug_summary = st.text_input(
            "Bug Summary",
            placeholder="Brief description of the issue",
            help="Provide a short, clear summary of the bug"
        )
        
        steps_to_reproduce = st.text_area(
            "Steps to Reproduce",
            placeholder="1. Go to...\n2. Click on...\n3. Expected vs actual behavior...",
            help="Detailed steps to reproduce the issue",
            height=100
        )
        
        error_message = st.text_area(
            "Error Message (if any)",
            placeholder="Copy and paste any error messages you received",
            help="Include any error messages or codes you encountered",
            height=80
        )
        
        additional_info = st.text_area(
            "Additional Information",
            placeholder="Any other relevant details, browser version, operating system, etc.",
            help="Any additional context that might help us resolve the issue",
            height=80
        )
        
        submit_bug = st.form_submit_button("🚀 Submit Bug Report", type="primary")
        
        if submit_bug:
            if not bug_summary or not steps_to_reproduce:
                st.error("Please fill in the bug summary and steps to reproduce")
            else:
                # Compile bug report
                message = f"""
BUG REPORT DETAILS:

Summary: {bug_summary}
Severity: {severity}
Browser: {browser}

Steps to Reproduce:
{steps_to_reproduce}

Error Message:
{error_message}

Additional Information:
{additional_info}

Reporter: {user_name} ({user_email})
Subscription: {st.session_state.subscription_plan}
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                """.strip()
                
                if db_manager.save_feedback(user_email, "Bug Report", bug_summary, message):
                    st.success("✅ Bug report submitted successfully! Our team will investigate this issue.")
                    try:
                        email_service.send_feedback_acknowledgment_email(user_email, user_name, "bug report")
                    except:
                        pass
                else:
                    st.error("Failed to submit bug report. Please try again.")

elif feedback_type == "Feature Request":
    st.subheader("💡 Feature Request")
    st.write("Suggest new features or improvements to make ProteogenomiX even better.")
    
    with st.form("feature_request_form"):
        col1, col2 = st.columns(2)
        with col1:
            priority = st.selectbox(
                "Priority",
                ["Nice to have", "Important", "Critical for my work"],
                help="How important is this feature for your research?"
            )
        with col2:
            category = st.selectbox(
                "Category",
                ["Analysis Features", "Visualization", "User Interface", "API/Integration", "Performance", "Other"],
                help="What area does this feature relate to?"
            )
        
        feature_title = st.text_input(
            "Feature Title",
            placeholder="Brief title for your feature request",
            help="Provide a clear, concise title for the feature"
        )
        
        feature_description = st.text_area(
            "Feature Description",
            placeholder="Describe the feature you'd like to see...",
            help="Detailed description of the proposed feature",
            height=120
        )
        
        use_case = st.text_area(
            "Use Case",
            placeholder="How would you use this feature? What problem does it solve?",
            help="Explain how this feature would help your research or workflow",
            height=100
        )
        
        alternatives = st.text_area(
            "Current Alternatives",
            placeholder="How do you currently handle this task? What tools do you use?",
            help="Describe any workarounds or alternative tools you currently use",
            height=80
        )
        
        submit_feature = st.form_submit_button("💡 Submit Feature Request", type="primary")
        
        if submit_feature:
            if not feature_title or not feature_description:
                st.error("Please provide a feature title and description")
            else:
                message = f"""
FEATURE REQUEST DETAILS:

Title: {feature_title}
Priority: {priority}
Category: {category}

Description:
{feature_description}

Use Case:
{use_case}

Current Alternatives:
{alternatives}

Requestor: {user_name} ({user_email})
Subscription: {st.session_state.subscription_plan}
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                """.strip()
                
                if db_manager.save_feedback(user_email, "Feature Request", feature_title, message):
                    st.success("✅ Feature request submitted! We'll consider it for future updates.")
                    try:
                        email_service.send_feedback_acknowledgment_email(user_email, user_name, "feature request")
                    except:
                        pass
                else:
                    st.error("Failed to submit feature request. Please try again.")

elif feedback_type == "General Feedback":
    st.subheader("📣 General Feedback")
    st.write("Share your thoughts, suggestions, or experiences with ProteogenomiX.")
    
    with st.form("general_feedback_form"):
        col1, col2 = st.columns(2)
        with col1:
            overall_rating = st.selectbox(
                "Overall Rating",
                ["⭐⭐⭐⭐⭐ Excellent", "⭐⭐⭐⭐ Good", "⭐⭐⭐ Average", "⭐⭐ Poor", "⭐ Very Poor"],
                help="How would you rate your overall experience?"
            )
        with col2:
            recommend = st.selectbox(
                "Would you recommend ProteogenomiX?",
                ["Definitely", "Probably", "Not sure", "Probably not", "Definitely not"],
                help="Would you recommend our platform to colleagues?"
            )
        
        feedback_subject = st.text_input(
            "Subject",
            placeholder="What's your feedback about?",
            help="Brief subject for your feedback"
        )
        
        feedback_message = st.text_area(
            "Your Feedback",
            placeholder="Share your thoughts, experiences, or suggestions...",
            help="Tell us what you think about ProteogenomiX",
            height=150
        )
        
        what_you_like = st.text_area(
            "What do you like most?",
            placeholder="What features or aspects do you find most valuable?",
            help="Help us understand what's working well",
            height=80
        )
        
        improvements = st.text_area(
            "What could be improved?",
            placeholder="Any suggestions for improvements?",
            help="Help us identify areas for improvement",
            height=80
        )
        
        submit_general = st.form_submit_button("📤 Submit Feedback", type="primary")
        
        if submit_general:
            if not feedback_subject or not feedback_message:
                st.error("Please provide a subject and your feedback")
            else:
                # Extract rating number
                rating = int(overall_rating[0])
                
                message = f"""
GENERAL FEEDBACK:

Subject: {feedback_subject}
Overall Rating: {overall_rating}
Recommendation: {recommend}

Feedback:
{feedback_message}

What you like most:
{what_you_like}

Suggested improvements:
{improvements}

User: {user_name} ({user_email})
Subscription: {st.session_state.subscription_plan}
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                """.strip()
                
                if db_manager.save_feedback(user_email, "General Feedback", feedback_subject, message, rating):
                    st.success("✅ Thank you for your feedback! We appreciate your input.")
                    try:
                        email_service.send_feedback_acknowledgment_email(user_email, user_name, "feedback")
                    except:
                        pass
                else:
                    st.error("Failed to submit feedback. Please try again.")

elif feedback_type == "Technical Support":
    st.subheader("🔧 Technical Support")
    st.write("Get help with technical issues or questions about using ProteogenomiX.")
    
    with st.form("technical_support_form"):
        col1, col2 = st.columns(2)
        with col1:
            urgency = st.selectbox(
                "Urgency",
                ["Low - General question", "Medium - Affecting my work", "High - Blocking my research", "Critical - System down"],
                help="How urgent is your request?"
            )
        with col2:
            issue_area = st.selectbox(
                "Issue Area",
                ["File Upload", "Data Analysis", "Results/Visualization", "Account/Login", "Performance", "API", "Other"],
                help="What area are you having trouble with?"
            )
        
        support_subject = st.text_input(
            "Subject",
            placeholder="Brief description of your issue",
            help="Summarize your technical issue"
        )
        
        issue_description = st.text_area(
            "Issue Description",
            placeholder="Describe the technical issue you're experiencing...",
            help="Provide detailed information about the problem",
            height=120
        )
        
        error_details = st.text_area(
            "Error Messages/Screenshots",
            placeholder="Copy any error messages or describe what you see on screen",
            help="Include any error messages, codes, or describe unexpected behavior",
            height=100
        )
        
        system_info = st.text_area(
            "System Information",
            placeholder="Operating system, browser version, file types you're working with...",
            help="Technical details that might help us diagnose the issue",
            height=80
        )
        
        submit_support = st.form_submit_button("🆘 Submit Support Request", type="primary")
        
        if submit_support:
            if not support_subject or not issue_description:
                st.error("Please provide a subject and description of your issue")
            else:
                message = f"""
TECHNICAL SUPPORT REQUEST:

Subject: {support_subject}
Urgency: {urgency}
Issue Area: {issue_area}

Issue Description:
{issue_description}

Error Details:
{error_details}

System Information:
{system_info}

User: {user_name} ({user_email})
Subscription: {st.session_state.subscription_plan}
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                """.strip()
                
                if db_manager.save_feedback(user_email, "Technical Support", support_subject, message):
                    st.success("✅ Support request submitted! Our technical team will assist you shortly.")
                    if "critical" in urgency.lower() or "high" in urgency.lower():
                        st.info("🚨 High priority request detected. You should receive a response within 4 hours.")
                    try:
                        email_service.send_feedback_acknowledgment_email(user_email, user_name, "support request")
                    except:
                        pass
                else:
                    st.error("Failed to submit support request. Please try again.")

else:  # Billing Support
    st.subheader("💳 Billing Support")
    st.write("Get help with subscription, payment, or billing questions.")
    
    with st.form("billing_support_form"):
        col1, col2 = st.columns(2)
        with col1:
            billing_issue = st.selectbox(
                "Issue Type",
                ["Payment Problem", "Subscription Change", "Refund Request", "Invoice/Receipt", "Billing Question", "Other"],
                help="What type of billing issue are you experiencing?"
            )
        with col2:
            current_plan = st.text_input(
                "Current Plan",
                value=st.session_state.subscription_plan.title(),
                disabled=True,
                help="Your current subscription plan"
            )
        
        billing_subject = st.text_input(
            "Subject",
            placeholder="Brief description of your billing issue",
            help="Summarize your billing question or issue"
        )
        
        billing_details = st.text_area(
            "Details",
            placeholder="Describe your billing issue or question in detail...",
            help="Provide specific details about your billing concern",
            height=120
        )
        
        transaction_info = st.text_area(
            "Transaction Information",
            placeholder="Transaction ID, payment date, amount, etc. (if applicable)",
            help="Include any relevant transaction details",
            height=80
        )
        
        submit_billing = st.form_submit_button("💰 Submit Billing Request", type="primary")
        
        if submit_billing:
            if not billing_subject or not billing_details:
                st.error("Please provide a subject and details about your billing issue")
            else:
                message = f"""
BILLING SUPPORT REQUEST:

Subject: {billing_subject}
Issue Type: {billing_issue}
Current Plan: {st.session_state.subscription_plan}

Details:
{billing_details}

Transaction Information:
{transaction_info}

User: {user_name} ({user_email})
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                """.strip()
                
                if db_manager.save_feedback(user_email, "Billing Support", billing_subject, message):
                    st.success("✅ Billing request submitted! Our billing team will review your request.")
                    st.info("💡 For urgent billing issues, you can also contact PayPal directly through your account.")
                    try:
                        email_service.send_feedback_acknowledgment_email(user_email, user_name, "billing request")
                    except:
                        pass
                else:
                    st.error("Failed to submit billing request. Please try again.")

# Contact information
st.markdown("---")
st.subheader("📞 Alternative Contact Methods")

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    ### 📧 Email Support
    **General Support:** support@proteogenomix.com
    **Technical Issues:** tech@proteogenomix.com
    **Billing Questions:** billing@proteogenomix.com
    
    **Response Times:**
    - Freemium: 2-3 business days
    - Premium: 24 hours
    - Critical issues: 4 hours
    """)

with col2:
    st.markdown("""
    ### 🌐 Other Resources
    **Documentation:** Available in README
    **Sample Data:** Use sample datasets for testing
    **Community:** Share experiences with other researchers
    
    **Self-Help:**
    - Check FAQ in Legal section
    - Try sample data first
    - Review analysis guidelines
    """)

# Feedback statistics (for premium users)
if st.session_state.subscription_plan == 'premium':
    st.markdown("---")
    st.subheader("📊 Your Feedback History")
    
    # This would show user's previous feedback in a real implementation
    st.info("🔒 Premium Feature: View your feedback history and status updates here.")
    
    # Placeholder for feedback history
    st.write("Your recent feedback submissions would be displayed here, including:")
    st.write("- Submission date and type")
    st.write("- Current status (Open, In Progress, Resolved)")
    st.write("- Response from our team")
    st.write("- Follow-up actions")

# Quick actions
st.markdown("---")
st.subheader("⚡ Quick Actions")

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🔬 Back to Analysis"):
        st.switch_page("pages/1_🔬_Analysis.py")

with col2:
    if st.button("📊 View Dashboard"):
        st.switch_page("pages/2_📊_Dashboard.py")

with col3:
    if st.button("📋 Legal Info"):
        st.switch_page("pages/5_📋_Legal.py")

# Feedback guidelines
with st.expander("💡 Tips for Effective Feedback"):
    st.markdown("""
    ### 🎯 How to Write Good Feedback
    
    **For Bug Reports:**
    - Be specific about what went wrong
    - Include steps to reproduce the issue
    - Mention your browser and operating system
    - Copy exact error messages
    
    **For Feature Requests:**
    - Explain the problem you're trying to solve
    - Describe how the feature would help your research
    - Consider how other users might benefit
    
    **For General Feedback:**
    - Be honest and constructive
    - Mention specific features you like or dislike
    - Suggest concrete improvements
    
    **Response Expectations:**
    - We read every piece of feedback
    - Critical bugs get highest priority
    - Feature requests are evaluated for future releases
    - We may follow up for clarification
    """)
