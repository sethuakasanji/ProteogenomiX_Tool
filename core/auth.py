import hashlib
import sqlite3
import streamlit as st
from typing import Optional, Dict, Tuple
import re
from datetime import datetime, timedelta
import secrets

class AuthManager:
    """Handles user authentication and session management"""
    
    def __init__(self, db_path: str = "proteogenomix.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize user authentication database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                full_name TEXT NOT NULL,
                organization TEXT,
                subscription_plan TEXT DEFAULT 'freemium',
                subscription_end_date TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                last_login TEXT,
                is_active BOOLEAN DEFAULT 1,
                email_verified BOOLEAN DEFAULT 0,
                analysis_count INTEGER DEFAULT 0,
                monthly_usage INTEGER DEFAULT 0,
                usage_reset_date TEXT
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                session_token TEXT UNIQUE,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                expires_at TEXT,
                is_active BOOLEAN DEFAULT 1,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def validate_email(self, email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def validate_password(self, password: str) -> bool:
        """Validate password strength"""
        if len(password) < 8:
            return False
        if not re.search(r'[A-Za-z]', password):
            return False
        if not re.search(r'[0-9]', password):
            return False
        return True
    
    def register_user(self, email: str, password: str, full_name: str, organization: str = "") -> bool:
        """Register a new user"""
        try:
            if not self.validate_email(email):
                st.error("Invalid email format")
                return False
            
            if not self.validate_password(password):
                st.error("Password must be at least 8 characters with letters and numbers")
                return False
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check if email already exists
            cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
            if cursor.fetchone():
                st.error("Email already registered")
                conn.close()
                return False
            
            # Insert new user
            password_hash = self.hash_password(password)
            usage_reset_date = (datetime.now() + timedelta(days=30)).isoformat()
            
            cursor.execute("""
                INSERT INTO users (email, password_hash, full_name, organization, usage_reset_date)
                VALUES (?, ?, ?, ?, ?)
            """, (email, password_hash, full_name, organization, usage_reset_date))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            st.error(f"Registration failed: {str(e)}")
            return False
    
    def authenticate(self, email: str, password: str) -> bool:
        """Authenticate user credentials"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            password_hash = self.hash_password(password)
            cursor.execute("""
                SELECT id, is_active FROM users 
                WHERE email = ? AND password_hash = ?
            """, (email, password_hash))
            
            result = cursor.fetchone()
            if result and result[1]:  # User exists and is active
                # Update last login
                cursor.execute("""
                    UPDATE users SET last_login = CURRENT_TIMESTAMP 
                    WHERE email = ?
                """, (email,))
                conn.commit()
                conn.close()
                return True
            
            conn.close()
            return False
            
        except Exception as e:
            st.error(f"Authentication failed: {str(e)}")
            return False
    
    def get_user_data(self, email: str) -> Optional[Dict]:
        """Get user data by email"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, email, full_name, organization, subscription_plan,
                       subscription_end_date, created_at, analysis_count,
                       monthly_usage, usage_reset_date
                FROM users WHERE email = ?
            """, (email,))
            
            result = cursor.fetchone()
            if result:
                user_data = {
                    'id': result[0],
                    'email': result[1],
                    'full_name': result[2],
                    'organization': result[3],
                    'subscription_plan': result[4],
                    'subscription_end_date': result[5],
                    'created_at': result[6],
                    'analysis_count': result[7],
                    'monthly_usage': result[8],
                    'usage_reset_date': result[9]
                }
                
                # Reset monthly usage if needed
                if self.should_reset_monthly_usage(user_data['usage_reset_date']):
                    self.reset_monthly_usage(email)
                    user_data['monthly_usage'] = 0
                
                conn.close()
                return user_data
            
            conn.close()
            return None
            
        except Exception as e:
            st.error(f"Error fetching user data: {str(e)}")
            return None
    
    def should_reset_monthly_usage(self, reset_date_str: str) -> bool:
        """Check if monthly usage should be reset"""
        try:
            reset_date = datetime.fromisoformat(reset_date_str)
            return datetime.now() > reset_date
        except:
            return True
    
    def reset_monthly_usage(self, email: str):
        """Reset monthly usage counter"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            new_reset_date = (datetime.now() + timedelta(days=30)).isoformat()
            cursor.execute("""
                UPDATE users SET monthly_usage = 0, usage_reset_date = ?
                WHERE email = ?
            """, (new_reset_date, email))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            st.error(f"Error resetting usage: {str(e)}")
    
    def update_subscription(self, email: str, plan: str, end_date: str = None):
        """Update user subscription plan"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE users SET subscription_plan = ?, subscription_end_date = ?
                WHERE email = ?
            """, (plan, end_date, email))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            st.error(f"Error updating subscription: {str(e)}")
            return False
    
    def increment_analysis_count(self, email: str):
        """Increment analysis count for user"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE users SET analysis_count = analysis_count + 1,
                                monthly_usage = monthly_usage + 1
                WHERE email = ?
            """, (email,))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            st.error(f"Error updating analysis count: {str(e)}")
    
    def can_perform_analysis(self, email: str) -> Tuple[bool, str]:
        """Check if user can perform analysis based on plan limits"""
        user_data = self.get_user_data(email)
        if not user_data:
            return False, "User not found"
        
        if user_data['subscription_plan'] == 'premium':
            return True, "Premium user - unlimited access"
        
        # Freemium limits
        if user_data['monthly_usage'] >= 5:
            return False, "Monthly limit reached (5 analyses). Upgrade to Premium for unlimited access."
        
        return True, f"Remaining analyses this month: {5 - user_data['monthly_usage']}"
    
    def get_plan_features(self, plan: str) -> Dict:
        """Get plan features and limitations"""
        if plan == 'premium':
            return {
                'max_file_size': '500MB',
                'file_processing': 'Priority (2x faster)',
                'visualizations': 'Advanced',
                'export_formats': ['CSV', 'PDF', 'JSON'],
                'monthly_limit': 'Unlimited',
                'api_access': True,
                'priority_support': True
            }
        else:  # freemium
            return {
                'max_file_size': '50MB',
                'file_processing': 'Standard',
                'visualizations': 'Basic',
                'export_formats': ['CSV'],
                'monthly_limit': '5 analyses',
                'api_access': False,
                'priority_support': False
            }
    
    def check_file_size_limit(self, email: str, file_size: int) -> bool:
        """Check if file size is within user's plan limits"""
        user_data = self.get_user_data(email)
        if not user_data:
            return False
        
        # Premium users: 500MB limit
        if user_data['subscription_plan'] == 'premium':
            return file_size <= 500 * 1024 * 1024
        
        # Freemium users: 50MB limit
        return file_size <= 50 * 1024 * 1024
