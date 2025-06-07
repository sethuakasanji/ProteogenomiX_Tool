import sqlite3
import hashlib
import os
from datetime import datetime, timedelta
import secrets

DATABASE_PATH = "proteogenomix.db"

def hash_password(password: str) -> str:
    """Hash password using SHA-256 with salt"""
    salt = os.urandom(32)
    pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return salt.hex() + pwd_hash.hex()

def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash"""
    try:
        salt = bytes.fromhex(hashed[:64])
        stored_hash = hashed[64:]
        pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        return pwd_hash.hex() == stored_hash
    except:
        return False

def register_user(email: str, password: str, plan: str = 'freemium') -> bool:
    """Register a new user"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        # Check if user already exists
        cursor.execute("SELECT email FROM users WHERE email = ?", (email,))
        if cursor.fetchone():
            conn.close()
            return False
        
        # Hash password and create user
        hashed_password = hash_password(password)
        created_at = datetime.now().isoformat()
        
        cursor.execute("""
            INSERT INTO users (email, password_hash, plan, created_at, is_active)
            VALUES (?, ?, ?, ?, ?)
        """, (email, hashed_password, plan, created_at, True))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Registration error: {e}")
        return False

def authenticate_user(email: str, password: str) -> bool:
    """Authenticate user login"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT password_hash, is_active FROM users 
            WHERE email = ?
        """, (email,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result and result[1]:  # User exists and is active
            return verify_password(password, result[0])
        return False
    except Exception as e:
        print(f"Authentication error: {e}")
        return False

def get_user_plan(email: str) -> str:
    """Get user's subscription plan"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute("SELECT plan FROM users WHERE email = ?", (email,))
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result else 'freemium'
    except Exception as e:
        print(f"Get user plan error: {e}")
        return 'freemium'

def is_premium_user(email: str) -> bool:
    """Check if user has premium plan"""
    plan = get_user_plan(email)
    return plan == 'premium'

def update_user_plan(email: str, plan: str, subscription_id: str = None) -> bool:
    """Update user's subscription plan"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        updated_at = datetime.now().isoformat()
        
        if plan == 'premium':
            # Set premium expiry date (1 year from now)
            expiry_date = (datetime.now() + timedelta(days=365)).isoformat()
            cursor.execute("""
                UPDATE users 
                SET plan = ?, subscription_id = ?, premium_expires_at = ?, updated_at = ?
                WHERE email = ?
            """, (plan, subscription_id, expiry_date, updated_at, email))
        else:
            cursor.execute("""
                UPDATE users 
                SET plan = ?, updated_at = ?
                WHERE email = ?
            """, (plan, updated_at, email))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Update user plan error: {e}")
        return False

def get_user_info(email: str) -> dict:
    """Get complete user information"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT email, plan, created_at, premium_expires_at, 
                   subscription_id, is_active
            FROM users WHERE email = ?
        """, (email,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'email': result[0],
                'plan': result[1],
                'created_at': result[2],
                'premium_expires_at': result[3],
                'subscription_id': result[4],
                'is_active': result[5]
            }
        return None
    except Exception as e:
        print(f"Get user info error: {e}")
        return None

def check_premium_expiry(email: str) -> bool:
    """Check if premium subscription has expired"""
    try:
        user_info = get_user_info(email)
        if not user_info or user_info['plan'] != 'premium':
            return False
        
        if user_info['premium_expires_at']:
            expiry_date = datetime.fromisoformat(user_info['premium_expires_at'])
            if datetime.now() > expiry_date:
                # Downgrade to freemium
                update_user_plan(email, 'freemium')
                return False
        
        return True
    except Exception as e:
        print(f"Check premium expiry error: {e}")
        return False

def generate_api_key(email: str) -> str:
    """Generate API key for premium users"""
    try:
        if not is_premium_user(email):
            return None
        
        api_key = secrets.token_urlsafe(32)
        
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE users SET api_key = ? WHERE email = ?
        """, (api_key, email))
        
        conn.commit()
        conn.close()
        
        return api_key
    except Exception as e:
        print(f"Generate API key error: {e}")
        return None

def validate_api_key(api_key: str) -> str:
    """Validate API key and return user email"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT email FROM users 
            WHERE api_key = ? AND plan = 'premium' AND is_active = 1
        """, (api_key,))
        
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result else None
    except Exception as e:
        print(f"Validate API key error: {e}")
        return None
