import requests
import streamlit as st
from typing import Dict, Optional
import json
import os
from datetime import datetime, timedelta

class PayPalManager:
    """Handles PayPal payment integration"""
    
    def __init__(self):
        # PayPal configuration - use environment variables in production
        self.client_id = os.getenv("PAYPAL_CLIENT_ID", "demo_client_id")
        self.client_secret = os.getenv("PAYPAL_CLIENT_SECRET", "demo_secret")
        self.base_url = os.getenv("PAYPAL_BASE_URL", "https://api.sandbox.paypal.com")  # sandbox for testing
        
        # Pricing configuration
        self.pricing = {
            "premium_monthly": {
                "amount": "2000",
                "currency": "INR",
                "description": "ProteogenomiX Premium Monthly Plan"
            },
            "premium_yearly": {
                "amount": "10000",
                "currency": "INR", 
                "description": "ProteogenomiX Premium Yearly Plan"
            }
        }
    
    def get_access_token(self) -> Optional[str]:
        """Get PayPal access token"""
        try:
            url = f"{self.base_url}/v1/oauth2/token"
            headers = {
                "Accept": "application/json",
                "Accept-Language": "en_US",
            }
            data = "grant_type=client_credentials"
            
            response = requests.post(
                url, 
                headers=headers, 
                data=data,
                auth=(self.client_id, self.client_secret)
            )
            
            if response.status_code == 200:
                return response.json().get("access_token")
            else:
                st.error(f"PayPal authentication failed: {response.text}")
                return None
                
        except Exception as e:
            st.error(f"PayPal connection error: {str(e)}")
            return None
    
    def create_payment(self, plan_type: str, user_email: str, return_url: str, cancel_url: str) -> Optional[Dict]:
        """Create PayPal payment"""
        try:
            access_token = self.get_access_token()
            if not access_token:
                return None
            
            if plan_type not in self.pricing:
                st.error("Invalid plan type")
                return None
            
            pricing = self.pricing[plan_type]
            
            url = f"{self.base_url}/v1/payments/payment"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}",
            }
            
            payment_data = {
                "intent": "sale",
                "payer": {
                    "payment_method": "paypal"
                },
                "transactions": [{
                    "amount": {
                        "total": pricing["amount"],
                        "currency": pricing["currency"]
                    },
                    "description": pricing["description"],
                    "custom": json.dumps({
                        "user_email": user_email,
                        "plan_type": plan_type,
                        "timestamp": datetime.now().isoformat()
                    })
                }],
                "redirect_urls": {
                    "return_url": return_url,
                    "cancel_url": cancel_url
                }
            }
            
            response = requests.post(url, headers=headers, json=payment_data)
            
            if response.status_code == 201:
                payment = response.json()
                # Extract approval URL
                for link in payment.get("links", []):
                    if link.get("rel") == "approval_url":
                        payment["approval_url"] = link.get("href")
                        break
                return payment
            else:
                st.error(f"Payment creation failed: {response.text}")
                return None
                
        except Exception as e:
            st.error(f"Payment creation error: {str(e)}")
            return None
    
    def execute_payment(self, payment_id: str, payer_id: str) -> Optional[Dict]:
        """Execute approved PayPal payment"""
        try:
            access_token = self.get_access_token()
            if not access_token:
                return None
            
            url = f"{self.base_url}/v1/payments/payment/{payment_id}/execute"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}",
            }
            
            execute_data = {
                "payer_id": payer_id
            }
            
            response = requests.post(url, headers=headers, json=execute_data)
            
            if response.status_code == 200:
                return response.json()
            else:
                st.error(f"Payment execution failed: {response.text}")
                return None
                
        except Exception as e:
            st.error(f"Payment execution error: {str(e)}")
            return None
    
    def get_payment_details(self, payment_id: str) -> Optional[Dict]:
        """Get PayPal payment details"""
        try:
            access_token = self.get_access_token()
            if not access_token:
                return None
            
            url = f"{self.base_url}/v1/payments/payment/{payment_id}"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}",
            }
            
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                return response.json()
            else:
                st.error(f"Failed to get payment details: {response.text}")
                return None
                
        except Exception as e:
            st.error(f"Error getting payment details: {str(e)}")
            return None
    
    def create_subscription_plan(self, plan_type: str) -> Optional[Dict]:
        """Create PayPal subscription plan (for recurring payments)"""
        try:
            access_token = self.get_access_token()
            if not access_token:
                return None
            
            if plan_type not in self.pricing:
                st.error("Invalid plan type")
                return None
            
            pricing = self.pricing[plan_type]
            frequency = "MONTH" if "monthly" in plan_type else "YEAR"
            
            url = f"{self.base_url}/v1/billing/plans"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}",
                "PayPal-Request-Id": f"plan-{plan_type}-{datetime.now().timestamp()}"
            }
            
            plan_data = {
                "product_id": "PROTEOGENOMIX_PREMIUM",
                "name": f"ProteogenomiX Premium {frequency.title()}ly",
                "description": pricing["description"],
                "status": "ACTIVE",
                "billing_cycles": [{
                    "frequency": {
                        "interval_unit": frequency,
                        "interval_count": 1
                    },
                    "tenure_type": "REGULAR",
                    "sequence": 1,
                    "pricing_scheme": {
                        "fixed_price": {
                            "value": pricing["amount"],
                            "currency_code": pricing["currency"]
                        }
                    }
                }],
                "payment_preferences": {
                    "auto_bill_outstanding": True,
                    "setup_fee": {
                        "value": "0",
                        "currency_code": pricing["currency"]
                    },
                    "setup_fee_failure_action": "CONTINUE",
                    "payment_failure_threshold": 3
                }
            }
            
            response = requests.post(url, headers=headers, json=plan_data)
            
            if response.status_code == 201:
                return response.json()
            else:
                st.error(f"Subscription plan creation failed: {response.text}")
                return None
                
        except Exception as e:
            st.error(f"Subscription plan creation error: {str(e)}")
            return None
    
    def format_amount_for_display(self, amount: str, currency: str = "INR") -> str:
        """Format amount for display"""
        if currency == "INR":
            return f"₹{amount}"
        else:
            return f"{amount} {currency}"
    
    def get_plan_benefits(self, plan_type: str) -> Dict:
        """Get plan benefits for display"""
        if plan_type == "premium_monthly":
            return {
                "duration": "1 Month",
                "price": self.format_amount_for_display(self.pricing[plan_type]["amount"]),
                "savings": "None",
                "features": [
                    "Unlimited biomarker analyses",
                    "Advanced visualizations", 
                    "Priority processing",
                    "API access",
                    "Priority support",
                    "Export to PDF",
                    "Batch processing"
                ]
            }
        elif plan_type == "premium_yearly":
            monthly_equivalent = int(self.pricing[plan_type]["amount"]) / 12
            monthly_regular = int(self.pricing["premium_monthly"]["amount"])
            savings = monthly_regular - monthly_equivalent
            return {
                "duration": "1 Year",
                "price": self.format_amount_for_display(self.pricing[plan_type]["amount"]),
                "savings": f"Save ₹{savings:.0f}/month",
                "features": [
                    "All Premium features",
                    "Best value - 58% savings",
                    "Priority feature requests",
                    "Extended data retention",
                    "Advanced analytics",
                    "Custom integrations",
                    "Dedicated support"
                ]
            }
        else:
            return {}
