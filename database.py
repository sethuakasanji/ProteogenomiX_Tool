import sqlite3
import os
from datetime import datetime
import pandas as pd
from typing import Optional, List, Dict

DATABASE_PATH = "proteogenomix.db"

def init_database():
    """Initialize the SQLite database with required tables"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            plan TEXT DEFAULT 'freemium',
            created_at TEXT NOT NULL,
            updated_at TEXT,
            is_active BOOLEAN DEFAULT 1,
            subscription_id TEXT,
            premium_expires_at TEXT,
            api_key TEXT UNIQUE
        )
    """)
    
    # Processing history table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS processing_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT NOT NULL,
            proteomics_filename TEXT,
            genomics_filename TEXT,
            biomarkers_found INTEGER DEFAULT 0,
            processing_time_seconds REAL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (user_email) REFERENCES users (email)
        )
    """)
    
    # User feedback table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT NOT NULL,
            feedback_type TEXT NOT NULL,
            rating INTEGER,
            feedback_text TEXT,
            created_at TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            FOREIGN KEY (user_email) REFERENCES users (email)
        )
    """)
    
    # Subscription tracking table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subscriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT NOT NULL,
            subscription_id TEXT UNIQUE,
            plan_type TEXT NOT NULL,
            amount REAL NOT NULL,
            currency TEXT DEFAULT 'INR',
            status TEXT DEFAULT 'pending',
            created_at TEXT NOT NULL,
            expires_at TEXT,
            paypal_transaction_id TEXT,
            FOREIGN KEY (user_email) REFERENCES users (email)
        )
    """)
    
    # API usage tracking (for premium users)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS api_usage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT NOT NULL,
            api_key TEXT NOT NULL,
            endpoint TEXT,
            request_count INTEGER DEFAULT 0,
            date_used TEXT NOT NULL,
            FOREIGN KEY (user_email) REFERENCES users (email)
        )
    """)
    
    conn.commit()
    conn.close()
    print("Database initialized successfully")

def save_processing_result(user_email: str, proteomics_file: str, genomics_file: str, 
                          biomarkers_count: int, processing_time: float) -> bool:
    """Save processing result to database"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO processing_history 
            (user_email, proteomics_filename, genomics_filename, biomarkers_found, 
             processing_time_seconds, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_email, proteomics_file, genomics_file, biomarkers_count, 
              processing_time, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error saving processing result: {e}")
        return False

def get_user_processing_history(user_email: str, limit: int = 10) -> pd.DataFrame:
    """Get user's processing history"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        
        query = """
            SELECT proteomics_filename, genomics_filename, biomarkers_found, 
                   processing_time_seconds, created_at
            FROM processing_history 
            WHERE user_email = ?
            ORDER BY created_at DESC
            LIMIT ?
        """
        
        df = pd.read_sql_query(query, conn, params=(user_email, limit))
        conn.close()
        
        if not df.empty:
            df['created_at'] = pd.to_datetime(df['created_at'])
            df = df.rename(columns={
                'proteomics_filename': 'Proteomics File',
                'genomics_filename': 'Genomics File',
                'biomarkers_found': 'Biomarkers Found',
                'processing_time_seconds': 'Processing Time (s)',
                'created_at': 'Date Processed'
            })
        
        return df
    except Exception as e:
        print(f"Error getting processing history: {e}")
        return pd.DataFrame()

def save_user_feedback(user_email: str, feedback_type: str, rating: int, 
                      feedback_text: str) -> bool:
    """Save user feedback to database"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO user_feedback 
            (user_email, feedback_type, rating, feedback_text, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (user_email, feedback_type, rating, feedback_text, 
              datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error saving feedback: {e}")
        return False

def get_user_feedback_summary() -> Dict:
    """Get feedback summary statistics"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        # Average rating
        cursor.execute("SELECT AVG(rating) FROM user_feedback WHERE rating IS NOT NULL")
        avg_rating = cursor.fetchone()[0] or 0
        
        # Total feedback count
        cursor.execute("SELECT COUNT(*) FROM user_feedback")
        total_feedback = cursor.fetchone()[0]
        
        # Feedback by type
        cursor.execute("""
            SELECT feedback_type, COUNT(*) 
            FROM user_feedback 
            GROUP BY feedback_type
        """)
        feedback_by_type = dict(cursor.fetchall())
        
        conn.close()
        
        return {
            'average_rating': round(avg_rating, 1),
            'total_feedback': total_feedback,
            'feedback_by_type': feedback_by_type
        }
    except Exception as e:
        print(f"Error getting feedback summary: {e}")
        return {}

def save_subscription(user_email: str, subscription_id: str, plan_type: str, 
                     amount: float, paypal_transaction_id: str = None) -> bool:
    """Save subscription information"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        # Calculate expiry date
        from datetime import timedelta
        if plan_type == 'monthly':
            expires_at = (datetime.now() + timedelta(days=30)).isoformat()
        else:  # annual
            expires_at = (datetime.now() + timedelta(days=365)).isoformat()
        
        cursor.execute("""
            INSERT INTO subscriptions 
            (user_email, subscription_id, plan_type, amount, status, 
             created_at, expires_at, paypal_transaction_id)
            VALUES (?, ?, ?, ?, 'active', ?, ?, ?)
        """, (user_email, subscription_id, plan_type, amount, 
              datetime.now().isoformat(), expires_at, paypal_transaction_id))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error saving subscription: {e}")
        return False

def get_user_subscription(user_email: str) -> Optional[Dict]:
    """Get user's active subscription"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT subscription_id, plan_type, amount, created_at, expires_at, status
            FROM subscriptions 
            WHERE user_email = ? AND status = 'active'
            ORDER BY created_at DESC
            LIMIT 1
        """, (user_email,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'subscription_id': result[0],
                'plan_type': result[1],
                'amount': result[2],
                'created_at': result[3],
                'expires_at': result[4],
                'status': result[5]
            }
        return None
    except Exception as e:
        print(f"Error getting subscription: {e}")
        return None

def track_api_usage(user_email: str, api_key: str, endpoint: str) -> bool:
    """Track API usage for premium users"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        today = datetime.now().date().isoformat()
        
        # Check if record exists for today
        cursor.execute("""
            SELECT id, request_count FROM api_usage 
            WHERE user_email = ? AND api_key = ? AND endpoint = ? AND date_used = ?
        """, (user_email, api_key, endpoint, today))
        
        result = cursor.fetchone()
        
        if result:
            # Update existing record
            cursor.execute("""
                UPDATE api_usage 
                SET request_count = request_count + 1
                WHERE id = ?
            """, (result[0],))
        else:
            # Create new record
            cursor.execute("""
                INSERT INTO api_usage (user_email, api_key, endpoint, request_count, date_used)
                VALUES (?, ?, ?, 1, ?)
            """, (user_email, api_key, endpoint, today))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error tracking API usage: {e}")
        return False

def get_api_usage_stats(user_email: str, days: int = 30) -> pd.DataFrame:
    """Get API usage statistics for a user"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        
        query = """
            SELECT endpoint, SUM(request_count) as total_requests, date_used
            FROM api_usage 
            WHERE user_email = ? AND date_used >= date('now', '-{} days')
            GROUP BY endpoint, date_used
            ORDER BY date_used DESC
        """.format(days)
        
        df = pd.read_sql_query(query, conn, params=(user_email,))
        conn.close()
        
        return df
    except Exception as e:
        print(f"Error getting API usage stats: {e}")
        return pd.DataFrame()

def get_platform_stats() -> Dict:
    """Get overall platform statistics"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        # Total users
        cursor.execute("SELECT COUNT(*) FROM users WHERE is_active = 1")
        total_users = cursor.fetchone()[0]
        
        # Premium users
        cursor.execute("SELECT COUNT(*) FROM users WHERE plan = 'premium' AND is_active = 1")
        premium_users = cursor.fetchone()[0]
        
        # Total processing jobs
        cursor.execute("SELECT COUNT(*) FROM processing_history")
        total_jobs = cursor.fetchone()[0]
        
        # Total biomarkers found
        cursor.execute("SELECT SUM(biomarkers_found) FROM processing_history")
        total_biomarkers = cursor.fetchone()[0] or 0
        
        # Average processing time
        cursor.execute("SELECT AVG(processing_time_seconds) FROM processing_history")
        avg_processing_time = cursor.fetchone()[0] or 0
        
        conn.close()
        
        return {
            'total_users': total_users,
            'premium_users': premium_users,
            'freemium_users': total_users - premium_users,
            'total_processing_jobs': total_jobs,
            'total_biomarkers_found': total_biomarkers,
            'average_processing_time': round(avg_processing_time, 2)
        }
    except Exception as e:
        print(f"Error getting platform stats: {e}")
        return {}

def cleanup_expired_subscriptions():
    """Clean up expired subscriptions"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        current_time = datetime.now().isoformat()
        
        # Find expired subscriptions
        cursor.execute("""
            SELECT user_email FROM subscriptions 
            WHERE status = 'active' AND expires_at < ?
        """, (current_time,))
        
        expired_users = cursor.fetchall()
        
        # Update subscription status
        cursor.execute("""
            UPDATE subscriptions 
            SET status = 'expired' 
            WHERE status = 'active' AND expires_at < ?
        """, (current_time,))
        
        # Downgrade users to freemium
        for user_email in expired_users:
            cursor.execute("""
                UPDATE users 
                SET plan = 'freemium', premium_expires_at = NULL
                WHERE email = ?
            """, (user_email[0],))
        
        conn.commit()
        conn.close()
        
        print(f"Cleaned up {len(expired_users)} expired subscriptions")
        return True
    except Exception as e:
        print(f"Error cleaning up expired subscriptions: {e}")
        return False
