import smtplib
import os
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
from datetime import datetime
from typing import Optional
import logging

# Email configuration from environment variables
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS", "support@proteogenomix.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "your_app_password")
FROM_NAME = "ProteogenomiX Support"

def send_email(to_email: str, subject: str, body: str, html_body: str = None) -> bool:
    """
    Send email notification
    """
    try:
        # Create message
        msg = MimeMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = f"{FROM_NAME} <{EMAIL_ADDRESS}>"
        msg['To'] = to_email
        
        # Add plain text body
        text_part = MimeText(body, 'plain')
        msg.attach(text_part)
        
        # Add HTML body if provided
        if html_body:
            html_part = MimeText(html_body, 'html')
            msg.attach(html_part)
        
        # Connect to server and send email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        
        text = msg.as_string()
        server.sendmail(EMAIL_ADDRESS, to_email, text)
        server.quit()
        
        print(f"Email sent successfully to {to_email}")
        return True
    
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")
        return False

def send_welcome_email(user_email: str) -> bool:
    """Send welcome email to new users"""
    subject = "Welcome to ProteogenomiX! 🧬"
    
    body = f"""
Welcome to ProteogenomiX - Advanced Biomarker Identification Tool!

Thank you for joining our platform. You now have access to powerful tools for analyzing proteomics and genomics data to identify potential biomarkers.

Your Freemium Account Includes:
• Basic FASTA file parsing
• Dataset integration capabilities
• CSV result downloads
• Up to 1000 entries per analysis

Getting Started:
1. Upload your proteomics and genomics FASTA files
2. Run the analysis pipeline
3. Download your results
4. Consider upgrading to Premium for advanced features

Need Help?
Visit our documentation or contact support at support@proteogenomix.com

Best regards,
The ProteogenomiX Team

---
IMPORTANT: Results are for research purposes only. Please verify independently before clinical use.
"""
    
    html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .header {{ background-color: #2E8B57; color: white; padding: 20px; text-align: center; }}
        .content {{ padding: 20px; }}
        .features {{ background-color: #F0F8FF; padding: 15px; border-radius: 5px; }}
        .warning {{ background-color: #FFE4E1; border-left: 4px solid #FF6B6B; padding: 10px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🧬 Welcome to ProteogenomiX!</h1>
        <p>Advanced Biomarker Identification Tool</p>
    </div>
    
    <div class="content">
        <p>Thank you for joining our platform. You now have access to powerful tools for analyzing proteomics and genomics data to identify potential biomarkers.</p>
        
        <div class="features">
            <h3>Your Freemium Account Includes:</h3>
            <ul>
                <li>✅ Basic FASTA file parsing</li>
                <li>✅ Dataset integration capabilities</li>
                <li>✅ CSV result downloads</li>
                <li>✅ Up to 1000 entries per analysis</li>
            </ul>
        </div>
        
        <h3>Getting Started:</h3>
        <ol>
            <li>Upload your proteomics and genomics FASTA files</li>
            <li>Run the analysis pipeline</li>
            <li>Download your results</li>
            <li>Consider upgrading to Premium for advanced features</li>
        </ol>
        
        <p><strong>Need Help?</strong><br>
        Visit our documentation or contact support at <a href="mailto:support@proteogenomix.com">support@proteogenomix.com</a></p>
        
        <p>Best regards,<br>The ProteogenomiX Team</p>
        
        <div class="warning">
            <strong>IMPORTANT:</strong> Results are for research purposes only. Please verify independently before clinical use.
        </div>
    </div>
</body>
</html>
"""
    
    return send_email(user_email, subject, body, html_body)

def send_notification_email(user_email: str, notification_type: str, message: str) -> bool:
    """Send general notification email"""
    
    subject_map = {
        "Analysis Complete": "🎉 Your ProteogenomiX Analysis is Complete!",
        "Subscription Activated": "✅ Premium Subscription Activated",
        "Subscription Cancelled": "📋 Subscription Cancelled",
        "Payment Failed": "⚠️ Payment Issue - Action Required",
        "Account Suspended": "🚨 Account Suspended",
        "Password Reset": "🔐 Password Reset Request"
    }
    
    subject = subject_map.get(notification_type, f"ProteogenomiX Notification: {notification_type}")
    
    body = f"""
Dear ProteogenomiX User,

{message}

If you have any questions or need assistance, please don't hesitate to contact our support team at support@proteogenomix.com

Best regards,
The ProteogenomiX Team

---
This is an automated message from ProteogenomiX.
"""
    
    html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .header {{ background-color: #2E8B57; color: white; padding: 20px; text-align: center; }}
        .content {{ padding: 20px; }}
        .message {{ background-color: #F0F8FF; padding: 15px; border-radius: 5px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🧬 ProteogenomiX</h1>
        <p>Advanced Biomarker Identification Tool</p>
    </div>
    
    <div class="content">
        <p>Dear ProteogenomiX User,</p>
        
        <div class="message">
            {message.replace('\n', '<br>')}
        </div>
        
        <p>If you have any questions or need assistance, please don't hesitate to contact our support team at <a href="mailto:support@proteogenomix.com">support@proteogenomix.com</a></p>
        
        <p>Best regards,<br>The ProteogenomiX Team</p>
        
        <hr>
        <small>This is an automated message from ProteogenomiX.</small>
    </div>
</body>
</html>
"""
    
    return send_email(user_email, subject, body, html_body)

def send_subscription_confirmation(user_email: str, plan_type: str, amount: float) -> bool:
    """Send subscription confirmation email"""
    subject = "✅ Premium Subscription Activated - ProteogenomiX"
    
    plan_name = "Monthly" if plan_type == "monthly" else "Annual"
    currency_symbol = "₹"
    
    body = f"""
Congratulations! Your ProteogenomiX Premium subscription has been activated.

Subscription Details:
• Plan: {plan_name} Premium
• Amount: {currency_symbol}{amount:,.0f}
• Status: Active
• Activated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}

Premium Features Now Available:
✅ Unlimited data processing
✅ Advanced biomarker analysis
✅ Interactive visualizations
✅ PDF report generation
✅ Priority email support
✅ API access for integration
✅ Real-time processing notifications

You can now access all Premium features in your ProteogenomiX dashboard.

Thank you for choosing ProteogenomiX Premium!

Best regards,
The ProteogenomiX Team
"""
    
    html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .header {{ background-color: #2E8B57; color: white; padding: 20px; text-align: center; }}
        .content {{ padding: 20px; }}
        .subscription-details {{ background-color: #E8F5E8; padding: 15px; border-radius: 5px; border-left: 4px solid #28A745; }}
        .features {{ background-color: #F0F8FF; padding: 15px; border-radius: 5px; }}
        .premium-badge {{ background-color: #FFD700; color: #333; padding: 5px 10px; border-radius: 15px; font-weight: bold; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🧬 ProteogenomiX</h1>
        <p><span class="premium-badge">PREMIUM ACTIVATED</span></p>
    </div>
    
    <div class="content">
        <h2>🎉 Congratulations! Your Premium subscription is now active.</h2>
        
        <div class="subscription-details">
            <h3>Subscription Details:</h3>
            <ul>
                <li><strong>Plan:</strong> {plan_name} Premium</li>
                <li><strong>Amount:</strong> {currency_symbol}{amount:,.0f}</li>
                <li><strong>Status:</strong> Active</li>
                <li><strong>Activated:</strong> {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</li>
            </ul>
        </div>
        
        <div class="features">
            <h3>Premium Features Now Available:</h3>
            <ul>
                <li>✅ Unlimited data processing</li>
                <li>✅ Advanced biomarker analysis</li>
                <li>✅ Interactive visualizations</li>
                <li>✅ PDF report generation</li>
                <li>✅ Priority email support</li>
                <li>✅ API access for integration</li>
                <li>✅ Real-time processing notifications</li>
            </ul>
        </div>
        
        <p>You can now access all Premium features in your ProteogenomiX dashboard.</p>
        
        <p><strong>Thank you for choosing ProteogenomiX Premium!</strong></p>
        
        <p>Best regards,<br>The ProteogenomiX Team</p>
    </div>
</body>
</html>
"""
    
    return send_email(user_email, subject, body, html_body)

def send_processing_complete_email(user_email: str, file_names: list, biomarkers_found: int, processing_time: float) -> bool:
    """Send processing completion notification"""
    subject = "🎉 Analysis Complete - ProteogenomiX"
    
    files_str = ", ".join(file_names) if len(file_names) <= 3 else f"{file_names[0]} and {len(file_names)-1} other files"
    
    body = f"""
Great news! Your ProteogenomiX analysis has completed successfully.

Analysis Summary:
• Files Processed: {files_str}
• Biomarkers Identified: {biomarkers_found}
• Processing Time: {processing_time:.2f} seconds
• Completed: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}

Your results are now available in your ProteogenomiX dashboard. You can download them in CSV format, and if you're a Premium user, you can also generate PDF reports.

Log in to your account to view and download your results:
https://proteogenomix.com/dashboard

Remember: These results are for research purposes only. Please verify all findings independently before any clinical application.

Best regards,
The ProteogenomiX Team
"""
    
    return send_notification_email(user_email, "Analysis Complete", body)

def send_feedback_acknowledgment(user_email: str, feedback_type: str) -> bool:
    """Send feedback acknowledgment email"""
    subject = "📝 Thank You for Your Feedback - ProteogenomiX"
    
    body = f"""
Thank you for taking the time to provide feedback about ProteogenomiX!

Feedback Type: {feedback_type}
Received: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}

Your feedback is valuable to us and helps improve the platform for all users. Our team will review your submission and may reach out if we need additional information.

If your feedback was regarding a technical issue or bug report, we'll work to address it in upcoming updates.

Thank you for being part of the ProteogenomiX community!

Best regards,
The ProteogenomiX Team
"""
    
    return send_notification_email(user_email, "Feedback Received", body)

# Mock email service for development
class MockEmailService:
    """Mock email service for development and testing"""
    
    def send_email(self, to_email: str, subject: str, body: str, html_body: str = None) -> bool:
        print(f"\n📧 MOCK EMAIL SERVICE")
        print(f"To: {to_email}")
        print(f"Subject: {subject}")
        print(f"Body Preview: {body[:100]}...")
        print(f"✅ Email would be sent in production\n")
        return True

# Use mock service in development
if os.getenv("ENVIRONMENT") == "development":
    # Override send_email function with mock
    def send_email(to_email: str, subject: str, body: str, html_body: str = None) -> bool:
        mock_service = MockEmailService()
        return mock_service.send_email(to_email, subject, body, html_body)
