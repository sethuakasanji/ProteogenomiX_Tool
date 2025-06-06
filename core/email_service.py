import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import streamlit as st
from typing import Optional, List
from datetime import datetime

class EmailService:
    """Handles email notifications and communications"""
    
    def __init__(self):
        # Email configuration - use environment variables
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.email_address = os.getenv("EMAIL_ADDRESS", "noreply@proteogenomix.com")
        self.email_password = os.getenv("EMAIL_PASSWORD", "demo_password")
        self.company_name = "ProteogenomiX"
    
    def send_email(self, to_email: str, subject: str, body: str, 
                   attachments: List[str] = None, is_html: bool = False) -> bool:
        """Send email with optional attachments"""
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = f"{self.company_name} <{self.email_address}>"
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Add body
            if is_html:
                msg.attach(MIMEText(body, 'html'))
            else:
                msg.attach(MIMEText(body, 'plain'))
            
            # Add attachments
            if attachments:
                for file_path in attachments:
                    if os.path.isfile(file_path):
                        with open(file_path, "rb") as attachment:
                            part = MIMEBase('application', 'octet-stream')
                            part.set_payload(attachment.read())
                        
                        encoders.encode_base64(part)
                        part.add_header(
                            'Content-Disposition',
                            f'attachment; filename= {os.path.basename(file_path)}'
                        )
                        msg.attach(part)
            
            # Send email
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email_address, self.email_password)
            server.send_message(msg)
            server.quit()
            
            return True
            
        except Exception as e:
            st.error(f"Email sending failed: {str(e)}")
            return False
    
    def send_welcome_email(self, user_email: str, user_name: str) -> bool:
        """Send welcome email to new users"""
        subject = f"Welcome to {self.company_name} - Your Biomarker Research Platform"
        
        body = f"""
        Dear {user_name},

        Welcome to ProteogenomiX - Advanced Biomarker Identification Tool!

        We're excited to have you join our community of researchers and biotech professionals. 
        Your account has been successfully created and you can now start analyzing your proteomics and genomics data.

        🔬 What you can do with your account:
        • Upload and analyze FASTA files (proteomics and genomics)
        • Identify potential biomarkers using advanced algorithms
        • Generate interactive visualizations and reports
        • Download results in CSV and PDF formats

        ⚠️ Important Disclaimer:
        Please remember that all biomarker identifications are for research purposes only. 
        Results should be independently verified before any clinical application.

        🚀 Getting Started:
        1. Log in to your dashboard
        2. Try our sample datasets to familiarize yourself with the platform
        3. Upload your own data files for analysis
        4. Explore the interactive visualizations and results

        💎 Upgrade to Premium:
        • Unlimited analyses (vs 5/month for free users)
        • Advanced visualizations and export options
        • Priority processing and support
        • API access for integration

        If you have any questions or need assistance, our support team is here to help.

        Best regards,
        The ProteogenomiX Team

        ---
        This is an automated message. Please do not reply to this email.
        """
        
        return self.send_email(user_email, subject, body)
    
    def send_analysis_completion_email(self, user_email: str, user_name: str, 
                                     analysis_name: str, biomarker_count: int, 
                                     total_entries: int) -> bool:
        """Send email when analysis is completed"""
        subject = f"Analysis Complete: {analysis_name}"
        
        body = f"""
        Dear {user_name},

        Your biomarker analysis "{analysis_name}" has been completed successfully!

        📊 Analysis Results:
        • Total entries processed: {total_entries:,}
        • Potential biomarkers identified: {biomarker_count:,}
        • Success rate: {(biomarker_count/total_entries*100):.1f}%

        🔬 Next Steps:
        1. Review your results in the dashboard
        2. Download detailed reports (CSV/PDF)
        3. Explore interactive visualizations
        4. Verify findings through additional research

        ⚠️ Research Disclaimer:
        These are potential biomarkers identified through computational analysis. 
        Please verify all results independently before any clinical application or real-world implementation.

        Access your results: Log in to your ProteogenomiX dashboard

        Thank you for using ProteogenomiX!

        Best regards,
        The ProteogenomiX Team
        """
        
        return self.send_email(user_email, subject, body)
    
    def send_subscription_confirmation_email(self, user_email: str, user_name: str, 
                                          plan_type: str, amount: str, duration: str) -> bool:
        """Send subscription confirmation email"""
        subject = "Subscription Confirmed - Premium Features Activated"
        
        body = f"""
        Dear {user_name},

        Thank you for upgrading to ProteogenomiX Premium!

        💳 Payment Confirmation:
        • Plan: {plan_type.replace('_', ' ').title()}
        • Amount: ₹{amount}
        • Duration: {duration}
        • Status: Activated

        🚀 Premium Features Now Available:
        • Unlimited biomarker analyses
        • Advanced interactive visualizations
        • Priority processing (faster results)
        • Export to PDF reports
        • API access for automation
        • Priority customer support
        • Batch processing capabilities

        Your premium features are now active and ready to use!

        📧 Support:
        If you have any questions about your subscription or need assistance, 
        please contact our premium support team.

        Thank you for choosing ProteogenomiX!

        Best regards,
        The ProteogenomiX Team
        """
        
        return self.send_email(user_email, subject, body)
    
    def send_feedback_acknowledgment_email(self, user_email: str, user_name: str, 
                                         feedback_type: str) -> bool:
        """Send feedback acknowledgment email"""
        subject = "Thank you for your feedback"
        
        body = f"""
        Dear {user_name},

        Thank you for taking the time to provide feedback about ProteogenomiX!

        We have received your {feedback_type.lower()} and our team will review it carefully. 
        Your input helps us improve our platform and better serve the research community.

        📝 What happens next:
        • Our team will review your feedback within 2-3 business days
        • If you've reported a bug, we'll prioritize it for fixing
        • Feature suggestions will be considered for future updates
        • We may follow up if we need additional information

        🔬 Continue Your Research:
        While we process your feedback, you can continue using ProteogenomiX for your biomarker research.

        Thank you for helping us build a better platform!

        Best regards,
        The ProteogenomiX Team
        """
        
        return self.send_email(user_email, subject, body)
    
    def send_password_reset_email(self, user_email: str, reset_token: str) -> bool:
        """Send password reset email"""
        subject = "Password Reset Request - ProteogenomiX"
        
        # In a real implementation, this would include a secure reset link
        body = f"""
        Dear User,

        We received a request to reset your ProteogenomiX account password.

        🔒 Security Notice:
        If you did not request this password reset, please ignore this email. 
        Your account remains secure.

        To reset your password:
        1. Contact our support team with this reference: {reset_token}
        2. Verify your identity
        3. Receive your new temporary password

        For security reasons, password resets must be handled through our support team.

        📧 Contact Support:
        Please email us with your reset request and include the reference number above.

        Best regards,
        The ProteogenomiX Team
        """
        
        return self.send_email(user_email, subject, body)
    
    def send_monthly_usage_report(self, user_email: str, user_name: str, 
                                analyses_count: int, biomarkers_found: int) -> bool:
        """Send monthly usage report"""
        subject = "Your Monthly ProteogenomiX Usage Report"
        
        body = f"""
        Dear {user_name},

        Here's your ProteogenomiX usage summary for this month:

        📊 Monthly Statistics:
        • Analyses completed: {analyses_count}
        • Total biomarkers identified: {biomarkers_found:,}
        • Platform engagement: Active user
        
        🔬 Research Impact:
        Your research this month has contributed to the advancement of biomarker discovery. 
        Keep up the excellent work!

        💡 Suggestions:
        • Try our new visualization features
        • Explore batch processing for larger datasets
        • Consider upgrading to Premium for unlimited access

        Thank you for being part of the ProteogenomiX community!

        Best regards,
        The ProteogenomiX Team
        """
        
        return self.send_email(user_email, subject, body)
