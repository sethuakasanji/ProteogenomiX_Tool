import streamlit as st
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add core modules to path
sys.path.append(str(Path(__file__).parent.parent))

from core.payment import PayPalManager
from core.auth import AuthManager
from core.database import DatabaseManager
from core.email_service import EmailService

# Check authentication
if not st.session_state.get('authenticated', False):
    st.error("Please log in to access this page")
    st.switch_page("app.py")
    st.stop()

# Initialize managers
paypal_manager = PayPalManager()
auth_manager = AuthManager()
db_manager = DatabaseManager()
email_service = EmailService()

st.title("💳 Subscription Management")
st.subheader("Choose the plan that fits your research needs")

user_email = st.session_state.user_data['email']
current_plan = st.session_state.subscription_plan

# Current subscription status
st.markdown("---")
st.subheader("📋 Current Subscription")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Current Plan", current_plan.title())
with col2:
    if current_plan == 'premium':
        end_date = st.session_state.user_data.get('subscription_end_date', 'N/A')
        st.metric("Plan Expires", end_date[:10] if end_date else 'N/A')
    else:
        st.metric("Monthly Usage", f"{st.session_state.user_data.get('monthly_usage', 0)}/5")
with col3:
    if current_plan == 'premium':
        st.metric("Status", "Active")
    else:
        remaining = 5 - st.session_state.user_data.get('monthly_usage', 0)
        st.metric("Remaining", f"{remaining} analyses")

# Plan comparison
st.markdown("---")
st.subheader("📊 Plan Comparison")

# Freemium vs Premium comparison
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 🆓 Freemium Plan
    
    **₹0/month**
    
    ✅ **Included Features:**
    - 5 biomarker analyses per month
    - Basic file upload (FASTA, CSV)
    - Standard processing speed
    - CSV export
    - Email support
    - Basic visualizations
    
    ❌ **Limitations:**
    - Limited monthly analyses
    - No PDF exports
    - No API access
    - Standard support priority
    """)
    
    if current_plan == 'freemium':
        st.success("✅ Current Plan")
    elif current_plan == 'premium':
        if st.button("⬇️ Downgrade to Freemium", type="secondary"):
            st.warning("Are you sure? You'll lose premium features immediately.")
            if st.button("Confirm Downgrade"):
                if auth_manager.update_subscription(user_email, 'freemium'):
                    st.session_state.subscription_plan = 'freemium'
                    st.success("Successfully downgraded to Freemium plan")
                    st.rerun()

with col2:
    st.markdown("""
    ### 💎 Premium Plan
    
    **Starting at ₹2,000/month**
    
    ✅ **Premium Features:**
    - 🚀 **Unlimited** biomarker analyses
    - ⚡ Priority processing (2x faster)
    - 📄 PDF report generation
    - 🔌 API access for automation
    - 📊 Advanced visualizations
    - 🎯 Priority customer support
    - 📦 Batch processing
    - 💾 Extended data retention
    - 🔧 Custom integrations
    - 🏆 Feature request priority
    
    💰 **Save with Annual Plans!**
    """)
    
    if current_plan == 'premium':
        st.success("✅ Current Plan")
    else:
        st.info("🚀 Upgrade to unlock unlimited research potential!")

# Premium plan options
if current_plan != 'premium':
    st.markdown("---")
    st.subheader("💎 Premium Plan Options")
    
    # Plan cards
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container():
            st.markdown("#### 📅 Monthly Plan")
            st.markdown("**₹2,000/month**")
            
            benefits_monthly = paypal_manager.get_plan_benefits("premium_monthly")
            if benefits_monthly:
                st.write(f"**Duration:** {benefits_monthly['duration']}")
                st.write(f"**Price:** {benefits_monthly['price']}")
                st.write("**Features:**")
                for feature in benefits_monthly['features']:
                    st.write(f"✅ {feature}")
            
            if st.button("💳 Subscribe Monthly", type="primary", key="monthly_plan"):
                st.session_state.selected_plan = "premium_monthly"
                st.session_state.show_payment = True
    
    with col2:
        with st.container():
            st.markdown("#### 🎉 Annual Plan (Best Value)")
            st.markdown("**₹10,000/year**")
            st.success("💰 Save ₹14,000 per year!")
            
            benefits_yearly = paypal_manager.get_plan_benefits("premium_yearly")
            if benefits_yearly:
                st.write(f"**Duration:** {benefits_yearly['duration']}")
                st.write(f"**Price:** {benefits_yearly['price']}")
                st.write(f"**Savings:** {benefits_yearly['savings']}")
                st.write("**Features:**")
                for feature in benefits_yearly['features']:
                    st.write(f"✅ {feature}")
            
            if st.button("💳 Subscribe Annually", type="primary", key="yearly_plan"):
                st.session_state.selected_plan = "premium_yearly"
                st.session_state.show_payment = True

# Payment processing
if st.session_state.get('show_payment', False):
    st.markdown("---")
    st.subheader("💳 Payment Information")
    
    selected_plan = st.session_state.get('selected_plan')
    plan_benefits = paypal_manager.get_plan_benefits(selected_plan)
    
    if plan_benefits:
        st.info(f"💎 You selected: **{selected_plan.replace('_', ' ').title()}** - {plan_benefits['price']}")
        
        # Payment summary
        st.markdown("#### 📋 Order Summary")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Plan:** {selected_plan.replace('_', ' ').title()}")
            st.write(f"**Duration:** {plan_benefits['duration']}")
            st.write(f"**Amount:** {plan_benefits['price']}")
        with col2:
            if 'savings' in plan_benefits:
                st.write(f"**Savings:** {plan_benefits['savings']}")
            st.write("**Payment Method:** PayPal")
            st.write("**Auto-renewal:** Yes")
        
        # Payment disclaimer
        st.warning("""
        ⚠️ **Payment Terms:**
        - Payments are processed securely through PayPal
        - Subscriptions auto-renew unless cancelled
        - Refunds available within 7 days of purchase
        - All prices are in Indian Rupees (INR)
        - Premium features activate immediately after payment
        """)
        
        # PayPal integration (Demo mode)
        st.markdown("#### 💳 Complete Payment")
        
        if st.button("🚀 Pay with PayPal", type="primary"):
            # In demo mode, simulate successful payment
            with st.spinner("Processing payment..."):
                # Simulate payment processing
                import time
                time.sleep(2)
                
                # Update subscription in database
                duration_months = 12 if "yearly" in selected_plan else 1
                end_date = (datetime.now() + timedelta(days=30 * duration_months)).isoformat()
                
                if auth_manager.update_subscription(user_email, 'premium', end_date):
                    # Save transaction record
                    amount = 10000 if "yearly" in selected_plan else 2000
                    transaction_id = f"DEMO_TXN_{int(datetime.now().timestamp())}"
                    
                    db_manager.save_payment_transaction(
                        user_email,
                        transaction_id,
                        "paypal",
                        amount,
                        selected_plan,
                        plan_benefits['duration']
                    )
                    
                    # Update session state
                    st.session_state.subscription_plan = 'premium'
                    st.session_state.user_data['subscription_plan'] = 'premium'
                    st.session_state.user_data['subscription_end_date'] = end_date
                    
                    # Send confirmation email
                    try:
                        email_service.send_subscription_confirmation_email(
                            user_email,
                            st.session_state.user_data['full_name'],
                            selected_plan,
                            str(amount),
                            plan_benefits['duration']
                        )
                    except:
                        pass  # Don't fail upgrade if email fails
                    
                    st.success("🎉 Payment successful! Premium features are now active!")
                    st.balloons()
                    
                    # Clear payment session
                    st.session_state.show_payment = False
                    st.session_state.selected_plan = None
                    
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error("Failed to update subscription. Please contact support.")
        
        if st.button("❌ Cancel", type="secondary"):
            st.session_state.show_payment = False
            st.session_state.selected_plan = None
            st.rerun()

# FAQ Section
st.markdown("---")
st.subheader("❓ Frequently Asked Questions")

with st.expander("💰 Billing & Payments"):
    st.markdown("""
    **Q: What payment methods do you accept?**
    A: We accept PayPal payments in Indian Rupees (INR). PayPal supports credit cards, debit cards, and bank transfers.
    
    **Q: When will I be charged?**
    A: You'll be charged immediately upon subscription. Renewals are processed automatically before your plan expires.
    
    **Q: Can I change my plan later?**
    A: Yes, you can upgrade or downgrade your plan at any time. Changes take effect immediately.
    
    **Q: Do you offer refunds?**
    A: Yes, we offer full refunds within 7 days of purchase if you're not satisfied.
    """)

with st.expander("🔄 Subscription Management"):
    st.markdown("""
    **Q: How do I cancel my subscription?**
    A: You can cancel through your PayPal account or contact our support team. You'll retain access until the end of your billing period.
    
    **Q: What happens when I downgrade?**
    A: You'll lose premium features immediately but retain access to your existing analysis results.
    
    **Q: Can I pause my subscription?**
    A: Currently, we don't offer subscription pausing. You can cancel and resubscribe when needed.
    """)

with st.expander("⚡ Premium Features"):
    st.markdown("""
    **Q: What's included in the Premium plan?**
    A: Unlimited analyses, priority processing, PDF exports, API access, advanced visualizations, and priority support.
    
    **Q: How much faster is priority processing?**
    A: Premium users get 2x faster processing and queue priority during high-traffic periods.
    
    **Q: Is there an API for automation?**
    A: Yes, Premium users get access to our REST API for programmatic analysis submission and result retrieval.
    """)

# Support contact
st.markdown("---")
st.info("💬 **Need help?** Contact our support team through the Feedback page or email us directly.")

# Navigation buttons
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🔬 Start Analysis"):
        st.switch_page("pages/1_🔬_Analysis.py")
with col2:
    if st.button("📊 View Dashboard"):
        st.switch_page("pages/2_📊_Dashboard.py")
with col3:
    if st.button("💬 Send Feedback"):
        st.switch_page("pages/4_💬_Feedback.py")
