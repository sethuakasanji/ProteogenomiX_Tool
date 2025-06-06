import requests
import os
import json
from datetime import datetime, timedelta
from typing import Optional, Dict
import secrets

# PayPal API Configuration
PAYPAL_CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID", "demo_client_id")
PAYPAL_CLIENT_SECRET = os.getenv("PAYPAL_CLIENT_SECRET", "demo_client_secret")
PAYPAL_BASE_URL = os.getenv("PAYPAL_BASE_URL", "https://api.sandbox.paypal.com")  # Use sandbox for testing

class PayPalIntegration:
    def __init__(self):
        self.client_id = PAYPAL_CLIENT_ID
        self.client_secret = PAYPAL_CLIENT_SECRET
        self.base_url = PAYPAL_BASE_URL
        self.access_token = None
        self.token_expires_at = None
    
    def get_access_token(self) -> Optional[str]:
        """Get PayPal access token"""
        try:
            if self.access_token and self.token_expires_at and datetime.now() < self.token_expires_at:
                return self.access_token
            
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
                token_data = response.json()
                self.access_token = token_data["access_token"]
                expires_in = token_data.get("expires_in", 3600)
                self.token_expires_at = datetime.now() + timedelta(seconds=expires_in - 60)
                return self.access_token
            else:
                print(f"Failed to get access token: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Error getting access token: {e}")
            return None
    
    def create_subscription_plan(self, plan_type: str) -> Optional[str]:
        """Create a subscription plan in PayPal"""
        try:
            access_token = self.get_access_token()
            if not access_token:
                return None
            
            url = f"{self.base_url}/v1/billing/plans"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json",
                "PayPal-Request-Id": secrets.token_urlsafe(16)
            }
            
            # Plan configuration
            if plan_type == "monthly":
                plan_data = {
                    "product_id": "PROTEOGENOMIX_MONTHLY",
                    "name": "ProteogenomiX Premium Monthly",
                    "description": "Monthly subscription to ProteogenomiX Premium features",
                    "status": "ACTIVE",
                    "billing_cycles": [{
                        "frequency": {
                            "interval_unit": "MONTH",
                            "interval_count": 1
                        },
                        "tenure_type": "REGULAR",
                        "sequence": 1,
                        "total_cycles": 0,
                        "pricing_scheme": {
                            "fixed_price": {
                                "value": "2000",
                                "currency_code": "INR"
                            }
                        }
                    }],
                    "payment_preferences": {
                        "auto_bill_outstanding": True,
                        "setup_fee": {
                            "value": "0",
                            "currency_code": "INR"
                        },
                        "setup_fee_failure_action": "CONTINUE",
                        "payment_failure_threshold": 3
                    }
                }
            else:  # annual
                plan_data = {
                    "product_id": "PROTEOGENOMIX_ANNUAL",
                    "name": "ProteogenomiX Premium Annual",
                    "description": "Annual subscription to ProteogenomiX Premium features",
                    "status": "ACTIVE",
                    "billing_cycles": [{
                        "frequency": {
                            "interval_unit": "YEAR",
                            "interval_count": 1
                        },
                        "tenure_type": "REGULAR",
                        "sequence": 1,
                        "total_cycles": 0,
                        "pricing_scheme": {
                            "fixed_price": {
                                "value": "10000",
                                "currency_code": "INR"
                            }
                        }
                    }],
                    "payment_preferences": {
                        "auto_bill_outstanding": True,
                        "setup_fee": {
                            "value": "0",
                            "currency_code": "INR"
                        },
                        "setup_fee_failure_action": "CONTINUE",
                        "payment_failure_threshold": 3
                    }
                }
            
            response = requests.post(url, headers=headers, json=plan_data)
            
            if response.status_code == 201:
                plan_info = response.json()
                return plan_info["id"]
            else:
                print(f"Failed to create subscription plan: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Error creating subscription plan: {e}")
            return None
    
    def create_subscription(self, user_email: str, plan_id: str) -> Optional[str]:
        """Create a subscription for a user"""
        try:
            access_token = self.get_access_token()
            if not access_token:
                return None
            
            url = f"{self.base_url}/v1/billing/subscriptions"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json",
                "PayPal-Request-Id": secrets.token_urlsafe(16)
            }
            
            subscription_data = {
                "plan_id": plan_id,
                "start_time": (datetime.now() + timedelta(minutes=5)).isoformat() + "Z",
                "subscriber": {
                    "email_address": user_email
                },
                "application_context": {
                    "brand_name": "ProteogenomiX",
                    "locale": "en-IN",
                    "shipping_preference": "NO_SHIPPING",
                    "user_action": "SUBSCRIBE_NOW",
                    "payment_method": {
                        "payer_selected": "PAYPAL",
                        "payee_preferred": "IMMEDIATE_PAYMENT_REQUIRED"
                    },
                    "return_url": "https://proteogenomix.com/subscription/success",
                    "cancel_url": "https://proteogenomix.com/subscription/cancel"
                }
            }
            
            response = requests.post(url, headers=headers, json=subscription_data)
            
            if response.status_code == 201:
                subscription_info = response.json()
                # Return the approval URL for user to complete payment
                for link in subscription_info.get("links", []):
                    if link["rel"] == "approve":
                        return link["href"]
                return None
            else:
                print(f"Failed to create subscription: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Error creating subscription: {e}")
            return None
    
    def verify_subscription(self, subscription_id: str) -> Optional[Dict]:
        """Verify and get subscription details"""
        try:
            access_token = self.get_access_token()
            if not access_token:
                return None
            
            url = f"{self.base_url}/v1/billing/subscriptions/{subscription_id}"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json"
            }
            
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Failed to verify subscription: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Error verifying subscription: {e}")
            return None
    
    def cancel_subscription(self, subscription_id: str, reason: str = "User requested cancellation") -> bool:
        """Cancel a subscription"""
        try:
            access_token = self.get_access_token()
            if not access_token:
                return False
            
            url = f"{self.base_url}/v1/billing/subscriptions/{subscription_id}/cancel"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json"
            }
            
            cancel_data = {
                "reason": reason
            }
            
            response = requests.post(url, headers=headers, json=cancel_data)
            
            return response.status_code == 204
        except Exception as e:
            print(f"Error cancelling subscription: {e}")
            return False

# Global PayPal integration instance
paypal = PayPalIntegration()

def create_subscription(user_email: str, plan_type: str, amount: float) -> Optional[str]:
    """
    Create a subscription for the user
    Returns PayPal approval URL for payment completion
    """
    try:
        # First, create or get the subscription plan
        plan_id = paypal.create_subscription_plan(plan_type)
        if not plan_id:
            print("Failed to create subscription plan")
            return None
        
        # Create subscription for the user
        approval_url = paypal.create_subscription(user_email, plan_id)
        
        if approval_url:
            print(f"Subscription created successfully for {user_email}")
            return approval_url
        else:
            print("Failed to create subscription")
            return None
    
    except Exception as e:
        print(f"Error in create_subscription: {e}")
        return None

def verify_payment(subscription_id: str) -> bool:
    """
    Verify if the payment/subscription is successful
    """
    try:
        subscription_details = paypal.verify_subscription(subscription_id)
        
        if subscription_details:
            status = subscription_details.get("status", "").upper()
            return status in ["ACTIVE", "APPROVED"]
        
        return False
    except Exception as e:
        print(f"Error verifying payment: {e}")
        return False

def handle_payment_webhook(webhook_data: Dict) -> bool:
    """
    Handle PayPal webhook notifications
    This would be called by a webhook endpoint
    """
    try:
        event_type = webhook_data.get("event_type", "")
        
        if event_type == "BILLING.SUBSCRIPTION.ACTIVATED":
            # Subscription activated
            subscription_id = webhook_data["resource"]["id"]
            subscriber_email = webhook_data["resource"]["subscriber"]["email_address"]
            
            # Update user to premium in database
            from auth import update_user_plan
            from database import save_subscription
            
            # Get subscription details to determine plan type and amount
            subscription_details = paypal.verify_subscription(subscription_id)
            if subscription_details:
                plan_id = subscription_details.get("plan_id", "")
                
                # Determine plan type and amount from plan_id or other details
                if "MONTHLY" in plan_id:
                    plan_type = "monthly"
                    amount = 2000
                else:
                    plan_type = "annual"
                    amount = 10000
                
                # Update user plan
                update_user_plan(subscriber_email, "premium", subscription_id)
                
                # Save subscription record
                save_subscription(subscriber_email, subscription_id, plan_type, amount)
                
                print(f"User {subscriber_email} upgraded to premium")
                return True
        
        elif event_type == "BILLING.SUBSCRIPTION.CANCELLED":
            # Subscription cancelled
            subscription_id = webhook_data["resource"]["id"]
            
            # Update user to freemium
            # This would require getting user email from subscription_id
            # Implementation depends on your database structure
            print(f"Subscription {subscription_id} cancelled")
            return True
        
        return False
    except Exception as e:
        print(f"Error handling payment webhook: {e}")
        return False

def get_subscription_status(subscription_id: str) -> str:
    """Get current status of a subscription"""
    try:
        subscription_details = paypal.verify_subscription(subscription_id)
        if subscription_details:
            return subscription_details.get("status", "UNKNOWN")
        return "NOT_FOUND"
    except Exception as e:
        print(f"Error getting subscription status: {e}")
        return "ERROR"

# For development/testing with mock PayPal integration
class MockPayPalIntegration:
    """Mock PayPal integration for development and testing"""
    
    def create_subscription_plan(self, plan_type: str) -> str:
        return f"MOCK_PLAN_{plan_type.upper()}"
    
    def create_subscription(self, user_email: str, plan_id: str) -> str:
        return f"https://mock-paypal.com/approve?subscription_id=MOCK_SUB_{secrets.token_urlsafe(8)}"
    
    def verify_subscription(self, subscription_id: str) -> Dict:
        return {
            "id": subscription_id,
            "status": "ACTIVE",
            "subscriber": {"email_address": "test@example.com"}
        }

# Use mock integration in development
if os.getenv("ENVIRONMENT") == "development":
    paypal = MockPayPalIntegration()
