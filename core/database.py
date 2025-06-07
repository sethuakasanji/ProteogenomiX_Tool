import sqlite3
import pandas as pd
from typing import List, Dict, Optional
import json
from datetime import datetime
import streamlit as st

class DatabaseManager:
    """Manages all database operations for ProteogenomiX"""
    
    def __init__(self, db_path: str = "proteogenomix.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize all database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Analysis results table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analysis_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_email TEXT NOT NULL,
                analysis_name TEXT NOT NULL,
                analysis_type TEXT NOT NULL,
                status TEXT DEFAULT 'processing',
                file_count INTEGER DEFAULT 0,
                biomarker_count INTEGER DEFAULT 0,
                total_entries INTEGER DEFAULT 0,
                proteomics_file_name TEXT,
                genomics_file_name TEXT,
                results_data TEXT,
                summary_stats TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                completed_at TEXT
            )
        """)
        
        # User feedback table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_email TEXT NOT NULL,
                feedback_type TEXT NOT NULL,
                rating INTEGER,
                subject TEXT,
                message TEXT NOT NULL,
                status TEXT DEFAULT 'open',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                admin_response TEXT,
                responded_at TEXT
            )
        """)
        
        # File uploads table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS file_uploads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_email TEXT NOT NULL,
                file_name TEXT NOT NULL,
                file_type TEXT NOT NULL,
                file_size INTEGER,
                analysis_id INTEGER,
                upload_status TEXT DEFAULT 'uploaded',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (analysis_id) REFERENCES analysis_results (id)
            )
        """)
        
        # Payment transactions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS payment_transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_email TEXT NOT NULL,
                transaction_id TEXT UNIQUE,
                payment_method TEXT,
                amount REAL,
                currency TEXT DEFAULT 'INR',
                plan_type TEXT,
                plan_duration TEXT,
                status TEXT DEFAULT 'pending',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                completed_at TEXT
            )
        """)
        
        conn.commit()
        conn.close()
    
    def save_analysis_result(self, user_email: str, analysis_name: str, analysis_type: str,
                           proteomics_file: str, genomics_file: str, results_df: pd.DataFrame,
                           summary_stats: Dict) -> int:
        """Save analysis results to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            biomarker_count = results_df["Is_Biomarker"].sum() if "Is_Biomarker" in results_df.columns else 0
            total_entries = len(results_df)
            
            cursor.execute("""
                INSERT INTO analysis_results (
                    user_email, analysis_name, analysis_type, status, file_count,
                    biomarker_count, total_entries, proteomics_file_name,
                    genomics_file_name, results_data, summary_stats, completed_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                user_email, analysis_name, analysis_type, 'completed', 2,
                int(biomarker_count), total_entries, proteomics_file, genomics_file,
                results_df.to_json(), json.dumps(summary_stats), datetime.now().isoformat()
            ))
            
            analysis_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return analysis_id
            
        except Exception as e:
            st.error(f"Error saving analysis: {str(e)}")
            return None
    
    def get_user_analyses(self, user_email: str, limit: int = None) -> List[Dict]:
        """Get all analyses for a user"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            query = """
                SELECT id, analysis_name, analysis_type, status, file_count,
                       biomarker_count, total_entries, created_at, completed_at
                FROM analysis_results 
                WHERE user_email = ?
                ORDER BY created_at DESC
            """
            
            if limit:
                query += f" LIMIT {limit}"
            
            cursor.execute(query, (user_email,))
            results = cursor.fetchall()
            
            analyses = []
            for result in results:
                analyses.append({
                    'id': result[0],
                    'analysis_name': result[1],
                    'analysis_type': result[2],
                    'status': result[3],
                    'file_count': result[4],
                    'biomarker_count': result[5],
                    'total_entries': result[6],
                    'created_at': result[7],
                    'completed_at': result[8]
                })
            
            conn.close()
            return analyses
            
        except Exception as e:
            st.error(f"Error fetching analyses: {str(e)}")
            return []
    
    def get_analysis_details(self, analysis_id: int, user_email: str) -> Optional[Dict]:
        """Get detailed analysis results"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT analysis_name, analysis_type, status, biomarker_count,
                       total_entries, results_data, summary_stats, created_at,
                       proteomics_file_name, genomics_file_name
                FROM analysis_results 
                WHERE id = ? AND user_email = ?
            """, (analysis_id, user_email))
            
            result = cursor.fetchone()
            if result:
                return {
                    'analysis_name': result[0],
                    'analysis_type': result[1],
                    'status': result[2],
                    'biomarker_count': result[3],
                    'total_entries': result[4],
                    'results_data': result[5],
                    'summary_stats': result[6],
                    'created_at': result[7],
                    'proteomics_file_name': result[8],
                    'genomics_file_name': result[9]
                }
            
            conn.close()
            return None
            
        except Exception as e:
            st.error(f"Error fetching analysis details: {str(e)}")
            return None
    
    def save_feedback(self, user_email: str, feedback_type: str, subject: str,
                     message: str, rating: int = None) -> bool:
        """Save user feedback"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO user_feedback (user_email, feedback_type, rating, subject, message)
                VALUES (?, ?, ?, ?, ?)
            """, (user_email, feedback_type, rating, subject, message))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            st.error(f"Error saving feedback: {str(e)}")
            return False
    
    def get_user_analysis_count(self, user_email: str) -> int:
        """Get total analysis count for user"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT COUNT(*) FROM analysis_results WHERE user_email = ?
            """, (user_email,))
            
            count = cursor.fetchone()[0]
            conn.close()
            return count
            
        except Exception:
            return 0
    
    def get_user_file_count(self, user_email: str) -> int:
        """Get total file count for user"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT COUNT(*) FROM file_uploads WHERE user_email = ?
            """, (user_email,))
            
            count = cursor.fetchone()[0]
            conn.close()
            return count
            
        except Exception:
            return 0
    
    def get_user_biomarker_count(self, user_email: str) -> int:
        """Get total biomarker count for user"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT SUM(biomarker_count) FROM analysis_results WHERE user_email = ?
            """, (user_email,))
            
            result = cursor.fetchone()[0]
            conn.close()
            return result if result else 0
            
        except Exception:
            return 0
    
    def get_recent_analyses(self, user_email: str, limit: int = 5) -> List[Dict]:
        """Get recent analyses for dashboard"""
        return self.get_user_analyses(user_email, limit)
    
    def save_payment_transaction(self, user_email: str, transaction_id: str,
                               payment_method: str, amount: float, plan_type: str,
                               plan_duration: str) -> bool:
        """Save payment transaction"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO payment_transactions 
                (user_email, transaction_id, payment_method, amount, plan_type, plan_duration)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (user_email, transaction_id, payment_method, amount, plan_type, plan_duration))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            st.error(f"Error saving transaction: {str(e)}")
            return False
