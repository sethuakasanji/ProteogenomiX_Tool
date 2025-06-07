import streamlit as st
import os
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Legal - ProteogenomiX",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Legal Information")

# Navigation for legal documents
tab1, tab2, tab3 = st.tabs(["📋 Privacy Policy", "📜 Terms of Service", "🛡️ Data Protection"])

with tab1:
    st.subheader("🔒 Privacy Policy")
    
    # Load privacy policy template
    privacy_policy_path = Path("templates/privacy_policy.md")
    if privacy_policy_path.exists():
        with open(privacy_policy_path, 'r', encoding='utf-8') as f:
            privacy_content = f.read()
        st.markdown(privacy_content)
    else:
        st.markdown("""
        # ProteogenomiX Privacy Policy
        
        **Last Updated:** January 2024
        
        ## 1. Information We Collect
        
        ### Personal Information
        - **Account Information:** Name, email address, and password when you create an account
        - **Payment Information:** Processed securely through PayPal (we don't store credit card details)
        - **Profile Information:** Research affiliation, user type, and experience level (optional)
        
        ### Research Data
        - **Uploaded Files:** Proteomics and genomics data files (FASTA format)
        - **Analysis Results:** Biomarker identification results and associated metadata
        - **Usage Data:** File upload timestamps, analysis completion times, and processing statistics
        
        ### Technical Information
        - **Log Data:** IP addresses, browser type, device information, and access times
        - **Cookies:** Session management and user preferences
        - **Performance Data:** Processing times and system performance metrics
        
        ## 2. How We Use Your Information
        
        ### Research Services
        - Process your biological data to identify potential biomarkers
        - Generate analysis reports and visualizations
        - Provide data export and download capabilities
        - Send processing completion notifications
        
        ### Account Management
        - Authenticate your identity and manage your account
        - Process subscription payments and billing
        - Provide customer support and technical assistance
        - Send important service updates and security notices
        
        ### Service Improvement
        - Analyze usage patterns to improve our algorithms
        - Monitor system performance and reliability
        - Develop new features based on user feedback
        - Ensure security and prevent fraudulent activities
        
        ## 3. Data Security and Protection
        
        ### Security Measures
        - **Encryption:** All data transmitted using TLS/SSL encryption
        - **Access Controls:** Role-based access with strong authentication
        - **Data Isolation:** User data is logically separated and secured
        - **Regular Backups:** Automated backups with encryption at rest
        
        ### Data Retention
        - **Account Data:** Retained while your account is active
        - **Research Data:** Retained for 2 years after account closure (unless deleted)
        - **Payment Data:** Billing records retained for 7 years for tax compliance
        - **Analysis Results:** Available for download for 1 year
        
        ### Data Location
        - Primary servers located in secure data centers
        - Backups stored in geographically distributed locations
        - Data processing complies with applicable regional regulations
        
        ## 4. Data Sharing and Disclosure
        
        ### We Do Not Sell Your Data
        ProteogenomiX never sells, rents, or trades your personal or research data.
        
        ### Limited Sharing
        We may share information only in these circumstances:
        - **Service Providers:** Third-party services that help operate our platform (e.g., PayPal for payments)
        - **Legal Requirements:** When required by law, court order, or to protect our rights
        - **Business Transfer:** In the event of a merger or acquisition (with data protection guarantees)
        - **Consent:** When you explicitly authorize sharing for research collaboration
        
        ### Research Collaboration
        - You can choose to share anonymized results with research partners
        - Individual sequences and identifying information are never shared
        - Statistical summaries may be used for academic publications (with consent)
        
        ## 5. Your Rights and Choices
        
        ### Access and Control
        - **Access:** View all data associated with your account
        - **Download:** Export your data and analysis results
        - **Update:** Modify your account information and preferences
        - **Delete:** Request deletion of your account and associated data
        
        ### Communication Preferences
        - **Email Notifications:** Control which emails you receive
        - **Marketing:** Opt-out of promotional communications
        - **Research Updates:** Choose to receive scientific updates
        
        ### Data Portability
        - Download your data in standard formats (CSV, PDF)
        - Transfer data to other research platforms
        - Receive machine-readable copies of your information
        
        ## 6. Compliance with Data Protection Laws
        
        ### GDPR (European Union)
        - **Lawful Basis:** Processing based on contract and legitimate interests
        - **Data Subject Rights:** Full compliance with GDPR requirements
        - **Data Protection Officer:** Available for privacy inquiries
        - **Data Transfers:** Adequate protection for international transfers
        
        ### CCPA (California)
        - **Consumer Rights:** Full disclosure and control over personal information
        - **No Sale:** We do not sell personal information
        - **Non-Discrimination:** Equal service regardless of privacy choices
        
        ### DPDP Act (India)
        - **Data Fiduciary:** Compliance with Indian data protection requirements
        - **Consent Management:** Clear consent mechanisms for data processing
        - **Data Localization:** Compliance with local data storage requirements
        
        ## 7. Children's Privacy
        
        ProteogenomiX is not intended for users under 16 years of age. We do not knowingly collect personal information from children under 16. If you believe we have collected information from a child under 16, please contact us immediately.
        
        ## 8. International Data Transfers
        
        Your data may be processed in countries other than your own. We ensure adequate protection through:
        - **Adequacy Decisions:** Transfers to countries with adequate protection
        - **Standard Contractual Clauses:** EU-approved contract terms
        - **Certification Programs:** Participation in recognized privacy frameworks
        
        ## 9. Updates to This Policy
        
        We may update this Privacy Policy to reflect changes in our practices or legal requirements. We will:
        - Post the updated policy on our website
        - Send email notifications for material changes
        - Provide the effective date of changes
        - Maintain previous versions for reference
        
        ## 10. Contact Information
        
        ### Privacy Questions
        **Email:** privacy@proteogenomix.com  
        **Response Time:** 5-7 business days
        
        ### Data Protection Officer
        **Email:** dpo@proteogenomix.com  
        **Address:** [Company Address]
        
        ### General Support
        **Email:** support@proteogenomix.com  
        **Website:** https://proteogenomix.com/contact
        
        ---
        
        **Effective Date:** January 1, 2024  
        **Last Reviewed:** January 2024
        
        This Privacy Policy is part of our Terms of Service. By using ProteogenomiX, you agree to the collection and use of information in accordance with this policy.
        """)

with tab2:
    st.subheader("📜 Terms of Service")
    
    # Load terms of service template
    terms_path = Path("templates/terms_of_service.md")
    if terms_path.exists():
        with open(terms_path, 'r', encoding='utf-8') as f:
            terms_content = f.read()
        st.markdown(terms_content)
    else:
        st.markdown("""
        # ProteogenomiX Terms of Service
        
        **Last Updated:** January 2024
        
        ## 1. Acceptance of Terms
        
        By accessing and using ProteogenomiX ("Service", "Platform"), you accept and agree to be bound by the terms and provision of this agreement. If you do not agree to abide by the above, please do not use this service.
        
        ## 2. Description of Service
        
        ProteogenomiX is an advanced biomarker identification platform that processes proteomics and genomics data to identify potential biomarkers for research purposes. Our service includes:
        
        - FASTA file parsing and analysis
        - Proteomics and genomics data integration
        - Biomarker identification algorithms
        - Interactive data visualization
        - Research report generation
        - API access (Premium users)
        
        ## 3. Research Use Only - Important Disclaimer
        
        ### 🚨 CRITICAL DISCLAIMER
        **ProteogenomiX is designed exclusively for research purposes. The results generated by our platform are potential biomarkers that require independent validation before any clinical application.**
        
        ### Prohibited Uses
        You agree NOT to use ProteogenomiX for:
        - Clinical diagnosis or patient care
        - Treatment decisions or medical advice
        - Direct clinical applications without proper validation
        - Regulatory submissions without independent verification
        - Emergency medical situations
        
        ### Validation Requirements
        Before using any results in clinical or commercial applications, you must:
        - Conduct independent validation studies
        - Obtain appropriate regulatory approvals
        - Consult with qualified medical professionals
        - Follow established clinical research protocols
        - Comply with all applicable regulations
        
        ## 4. User Accounts and Registration
        
        ### Account Creation
        - You must provide accurate and complete information
        - You are responsible for maintaining account confidentiality
        - You must be at least 16 years old to create an account
        - One account per user (institutional accounts permitted)
        
        ### Account Security
        - Use strong passwords and enable two-factor authentication when available
        - Notify us immediately of any unauthorized access
        - You are responsible for all activities under your account
        - Do not share your account credentials
        
        ### Account Termination
        We reserve the right to terminate accounts that:
        - Violate these terms of service
        - Engage in fraudulent or illegal activities
        - Upload malicious or harmful content
        - Abuse our systems or resources
        
        ## 5. Subscription Plans and Payment
        
        ### Plan Types
        - **Freemium:** Basic features with limitations
        - **Premium Monthly:** ₹2,000 per month
        - **Premium Yearly:** ₹10,000 per year (save ₹14,000)
        
        ### Payment Terms
        - All payments processed through PayPal
        - Prices listed in Indian Rupees (INR)
        - Automatic renewal unless cancelled
        - No refunds for partial periods
        - Price changes with 30-day notice
        
        ### Billing and Refunds
        - Billing cycles begin on subscription activation
        - Failed payments may result in service suspension
        - Refunds only provided for service failures
        - Currency conversion rates determined by PayPal
        
        ## 6. Acceptable Use Policy
        
        ### Permitted Uses
        - Academic and scientific research
        - Biomarker discovery and validation
        - Educational purposes
        - Non-commercial research collaboration
        - Technology evaluation and benchmarking
        
        ### Prohibited Uses
        You may not use our service to:
        - Upload copyrighted or proprietary data without permission
        - Attempt to reverse engineer our algorithms
        - Disrupt or interfere with service operations
        - Share account credentials with unauthorized users
        - Use the service for illegal activities
        - Upload malicious code or harmful content
        
        ### Data Upload Guidelines
        - Only upload data you have rights to use
        - Ensure data compliance with ethical guidelines
        - Do not upload personally identifiable information
        - Respect intellectual property rights
        - Follow your institution's data sharing policies
        
        ## 7. Data Ownership and Intellectual Property
        
        ### Your Data
        - You retain ownership of all data you upload
        - You grant us license to process data for service delivery
        - You can delete your data at any time
        - We do not claim ownership of your research results
        
        ### Our Technology
        - ProteogenomiX algorithms and software are proprietary
        - You may not reverse engineer or copy our methods
        - Our trademarks and brand elements are protected
        - API usage subject to separate terms
        
        ### Generated Results
        - Analysis results belong to you
        - You may publish and share results as desired
        - Attribution to ProteogenomiX appreciated but not required
        - We may use anonymized statistics for service improvement
        
        ## 8. Service Availability and Performance
        
        ### Service Level
        - We strive for 99.9% uptime but do not guarantee continuous availability
        - Scheduled maintenance will be announced in advance
        - Processing times may vary based on data size and system load
        - Emergency maintenance may occur without notice
        
        ### Support
        - **Freemium:** Community support and documentation
        - **Premium:** Priority email support with 24-48 hour response
        - Support available in English
        - Complex technical issues may require additional time
        
        ### Data Backup
        - We maintain regular backups of user data
        - Users responsible for maintaining their own copies
        - Backup restoration may take 24-48 hours
        - Data recovery services available for Premium users
        
        ## 9. Privacy and Data Protection
        
        ### Data Handling
        - All data processing governed by our Privacy Policy
        - We implement industry-standard security measures
        - Data encrypted in transit and at rest
        - Access controls limit data exposure
        
        ### Data Retention
        - Active account data retained indefinitely
        - Deleted account data purged within 30 days
        - Backup data retained for disaster recovery
        - Legal requirements may extend retention periods
        
        ### International Transfers
        - Data may be processed in multiple countries
        - Adequate protection measures in place
        - Compliance with applicable data protection laws
        
        ## 10. Limitation of Liability
        
        ### Service Disclaimer
        ProteogenomiX is provided "as is" without warranties of any kind. We disclaim all warranties, express or implied, including:
        - Accuracy of analysis results
        - Fitness for particular purposes
        - Uninterrupted service availability
        - Security of data transmission
        
        ### Liability Limits
        Our liability is limited to the maximum extent permitted by law:
        - Total liability not to exceed 12 months of subscription fees
        - No liability for indirect, consequential, or punitive damages
        - No liability for research setbacks or lost opportunities
        - No liability for third-party actions or data breaches
        
        ### Research Risks
        You acknowledge that:
        - Bioinformatics analysis has inherent limitations
        - Results require independent validation
        - False positives and negatives may occur
        - Clinical applications require separate approval processes
        
        ## 11. Indemnification
        
        You agree to indemnify and hold harmless ProteogenomiX from claims arising from:
        - Your use of the service
        - Violation of these terms
        - Infringement of third-party rights
        - Misuse of analysis results
        - Unauthorized data uploads
        
        ## 12. Termination
        
        ### Termination by You
        - Cancel subscription anytime through account settings
        - Account closure takes effect at end of billing period
        - Data download available for 30 days after cancellation
        - Premium features disabled immediately upon cancellation
        
        ### Termination by Us
        We may terminate your account for:
        - Violation of terms of service
        - Non-payment of fees
        - Illegal or harmful activities
        - Extended account inactivity (12+ months)
        
        ### Effects of Termination
        Upon termination:
        - Access to service immediately suspended
        - Data retention per our Privacy Policy
        - Outstanding fees remain due
        - Survival of applicable terms
        
        ## 13. Changes to Terms
        
        ### Modification Rights
        We reserve the right to modify these terms:
        - Changes effective upon posting
        - Material changes require 30-day notice
        - Continued use constitutes acceptance
        - Previous versions available upon request
        
        ### Notification Methods
        - Email notification to registered address
        - In-app notifications
        - Website posting
        - Version history maintained
        
        ## 14. Governing Law and Jurisdiction
        
        ### Applicable Law
        These terms are governed by the laws of India, without regard to conflict of law principles.
        
        ### Dispute Resolution
        - Initial resolution through good faith negotiation
        - Mediation through recognized mediation services
        - Final resolution through courts in [Jurisdiction], India
        - Class action waiver applies
        
        ### International Users
        - Compliance with local laws is user's responsibility
        - Export control laws may apply
        - Currency and tax obligations vary by location
        
        ## 15. Miscellaneous
        
        ### Entire Agreement
        These terms constitute the entire agreement between you and ProteogenomiX regarding use of the service.
        
        ### Severability
        If any provision is found unenforceable, the remainder of the terms remain in effect.
        
        ### Assignment
        - You may not assign these terms without our consent
        - We may assign our rights and obligations
        - Terms bind successors and assigns
        
        ### Force Majeure
        Neither party liable for delays due to circumstances beyond reasonable control.
        
        ## 16. Contact Information
        
        ### Legal Questions
        **Email:** legal@proteogenomix.com  
        **Response Time:** 5-7 business days
        
        ### General Support
        **Email:** support@proteogenomix.com  
        **Website:** https://proteogenomix.com/contact
        
        ### Business Inquiries
        **Email:** business@proteogenomix.com
        
        ---
        
        **Effective Date:** January 1, 2024  
        **Last Reviewed:** January 2024
        
        By using ProteogenomiX, you acknowledge that you have read, understood, and agree to be bound by these Terms of Service.
        """)

with tab3:
    st.subheader("🛡️ Data Protection & Compliance")
    
    st.markdown("""
    # Data Protection Framework
    
    ## Regulatory Compliance
    
    ProteogenomiX is designed to comply with major data protection regulations:
    
    ### 🇪🇺 GDPR (General Data Protection Regulation)
    - **Lawful basis for processing:** Contract and legitimate interests
    - **Data subject rights:** Access, rectification, erasure, portability
    - **Data protection by design:** Privacy built into our systems
    - **International transfers:** Adequate safeguards in place
    
    ### 🇺🇸 CCPA (California Consumer Privacy Act)
    - **Consumer rights:** Know, delete, opt-out, non-discrimination
    - **No sale of personal information:** We never sell your data
    - **Transparent disclosure:** Clear information about data use
    - **Response procedures:** Timely handling of consumer requests
    
    ### 🇮🇳 DPDP Act (Digital Personal Data Protection Act)
    - **Data fiduciary obligations:** Compliance with Indian requirements
    - **Consent management:** Clear and specific consent mechanisms
    - **Data localization:** Adherence to data residency requirements
    - **Breach notification:** Timely reporting of security incidents
    
    ## Security Measures
    
    ### Technical Safeguards
    - **Encryption:** TLS 1.3 for data in transit, AES-256 for data at rest
    - **Access controls:** Role-based permissions and multi-factor authentication
    - **Network security:** Firewalls, intrusion detection, and monitoring
    - **Secure development:** Code reviews, vulnerability scanning, penetration testing
    
    ### Administrative Safeguards
    - **Employee training:** Regular privacy and security awareness programs
    - **Access management:** Principle of least privilege and regular access reviews
    - **Incident response:** Documented procedures for security breach handling
    - **Vendor management:** Third-party security assessments and contracts
    
    ### Physical Safeguards
    - **Data centers:** Tier 3+ certified facilities with 24/7 security
    - **Environmental controls:** Temperature, humidity, and power monitoring
    - **Access logging:** Physical access tracking and surveillance
    - **Redundancy:** Geographic distribution and disaster recovery capabilities
    
    ## Research Data Ethics
    
    ### Ethical Guidelines
    - **IRB approval:** Encourage users to obtain institutional review board approval
    - **Informed consent:** Users responsible for appropriate consent for data use
    - **Data minimization:** Process only data necessary for analysis
    - **Purpose limitation:** Use data only for stated research purposes
    
    ### Special Categories of Data
    - **Genetic information:** Enhanced protection for genomic data
    - **Health data:** Compliance with health information regulations
    - **Research protections:** Additional safeguards for human subjects research
    - **Anonymization:** Tools and guidance for data de-identification
    
    ## Rights and Controls
    
    ### Your Data Rights
    1. **Right to access:** View all data we hold about you
    2. **Right to rectification:** Correct inaccurate personal information
    3. **Right to erasure:** Request deletion of your data
    4. **Right to portability:** Download your data in standard formats
    5. **Right to restrict processing:** Limit how we use your data
    6. **Right to object:** Opt-out of certain processing activities
    
    ### Exercising Your Rights
    - **Online tools:** Self-service options in your account settings
    - **Email requests:** Send requests to privacy@proteogenomix.com
    - **Response time:** 30 days for most requests (may be extended in complex cases)
    - **Identity verification:** We may request verification to protect your privacy
    
    ## International Considerations
    
    ### Cross-Border Data Transfers
    - **Adequacy decisions:** Transfers to countries with adequate protection
    - **Standard contractual clauses:** EU-approved transfer mechanisms
    - **Binding corporate rules:** Internal privacy standards for global operations
    - **Certification schemes:** Participation in recognized privacy frameworks
    
    ### Regional Variations
    - **Data localization:** Compliance with local data residency requirements
    - **Sector-specific rules:** Healthcare, financial, and research-specific regulations
    - **Emerging regulations:** Monitoring and adapting to new privacy laws
    - **Cultural considerations:** Respecting regional privacy expectations
    
    ## Transparency and Accountability
    
    ### Regular Reporting
    - **Privacy impact assessments:** For new features and data processing activities
    - **Compliance audits:** Regular internal and external privacy assessments
    - **Transparency reports:** Annual disclosure of government requests and data breaches
    - **Community updates:** Regular communication about privacy practices
    
    ### Continuous Improvement
    - **Privacy by design:** Building privacy into new features from the start
    - **User feedback:** Regular surveys and feedback collection on privacy practices
    - **Industry standards:** Participation in privacy and security industry groups
    - **Best practices:** Adoption of emerging privacy protection technologies
    
    ## Breach Notification
    
    ### Detection and Response
    - **Monitoring systems:** 24/7 monitoring for security incidents
    - **Incident classification:** Systematic assessment of breach severity
    - **Containment procedures:** Immediate steps to limit breach impact
    - **Investigation process:** Thorough analysis of breach causes and effects
    
    ### Notification Requirements
    - **Regulatory notification:** 72 hours to supervisory authorities (where required)
    - **User notification:** Prompt notification to affected users
    - **Public disclosure:** Transparency about significant breaches
    - **Remediation steps:** Clear information about protective measures taken
    
    ## Contact Our Privacy Team
    
    ### Data Protection Officer
    **Email:** dpo@proteogenomix.com  
    **Role:** Independent privacy oversight and user advocacy
    
    ### Privacy Team
    **Email:** privacy@proteogenomix.com  
    **Response Time:** 5-7 business days for most inquiries
    
    ### Regulatory Inquiries
    **Email:** compliance@proteogenomix.com  
    **Purpose:** Official regulatory communications and compliance questions
    
    ---
    
    *Last updated: January 2024*
    
    Our commitment to data protection is ongoing. We regularly review and update our practices to ensure the highest standards of privacy and security for our research community.
    """)

# Compliance checklist
st.markdown("---")
st.subheader("✅ Compliance Checklist")

compliance_items = {
    "Privacy Policy": "✅ Comprehensive privacy policy covering all major regulations",
    "Terms of Service": "✅ Clear terms addressing research use and limitations",
    "Data Encryption": "✅ TLS for transit, AES-256 for storage",
    "Access Controls": "✅ Role-based permissions and authentication",
    "User Rights": "✅ Tools for data access, download, and deletion",
    "Breach Response": "✅ Incident response procedures documented",
    "GDPR Compliance": "✅ Data protection by design and default",
    "CCPA Compliance": "✅ Consumer privacy rights implementation",
    "Research Ethics": "✅ Guidelines for responsible data use",
    "International Transfers": "✅ Adequate safeguards for cross-border data"
}

for item, status in compliance_items.items():
    st.write(f"{status} **{item}**")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 12px;'>
    <p>ProteogenomiX - Advanced Biomarker Identification Tool</p>
    <p>Committed to privacy, security, and responsible research practices</p>
    <p>For legal questions: legal@proteogenomix.com</p>
</div>
""", unsafe_allow_html=True)
