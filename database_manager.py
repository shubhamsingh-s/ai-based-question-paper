import sqlite3
import json
import uuid
from datetime import datetime
import streamlit as st

class DatabaseManager:
    def __init__(self, db_path='question_paper_analytics.db'):
        self.db_path = db_path
    
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    def create_session(self, user_ip=None, user_agent=None):
        """Create a new user session"""
        session_id = str(uuid.uuid4())
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO user_sessions (session_id, user_ip, user_agent)
            VALUES (?, ?, ?)
        ''', (session_id, user_ip, user_agent))
        
        conn.commit()
        conn.close()
        return session_id
    
    def update_session_activity(self, session_id):
        """Update last activity for a session"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE user_sessions 
            SET last_activity = CURRENT_TIMESTAMP
            WHERE session_id = ?
        ''', (session_id,))
        
        conn.commit()
        conn.close()
    
    def log_generation_request(self, session_id, generation_type, subject=None, 
                             exam_title=None, total_questions=None, total_marks=None, 
                             duration=None, question_types=None, difficulty=None, topics_used=None):
        """Log a question generation request"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO generation_requests 
            (session_id, generation_type, subject, exam_title, total_questions, total_marks, 
             duration, question_types, difficulty, topics_used)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            session_id, generation_type, subject, exam_title, total_questions, total_marks,
            duration, json.dumps(question_types) if question_types else None,
            difficulty, json.dumps(topics_used) if topics_used else None
        ))
        
        request_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return request_id
    
    def log_generated_questions(self, request_id, questions):
        """Log generated questions"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        for question in questions:
            cursor.execute('''
                INSERT INTO generated_questions 
                (request_id, question_text, question_type, topic, marks, bloom_level)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                request_id, question['question'], question['type'], 
                question['topic'], question['marks'], question.get('bloom_level', 'Understand')
            ))
        
        conn.commit()
        conn.close()
    
    def log_analytics(self, request_id, analysis):
        """Log analytics data"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO analytics_data 
            (request_id, type_counts, topic_counts, bloom_counts, total_questions, total_marks)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            request_id,
            json.dumps(analysis.get('type_counts', {})),
            json.dumps(analysis.get('topic_counts', {})),
            json.dumps(analysis.get('bloom_counts', {})),
            analysis.get('total_questions', 0),
            analysis.get('total_marks', 0)
        ))
        
        conn.commit()
        conn.close()
    
    def log_file_upload(self, session_id, file_name, file_type, file_size, upload_purpose):
        """Log file upload activity"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO file_uploads 
            (session_id, file_name, file_type, file_size, upload_purpose)
            VALUES (?, ?, ?, ?, ?)
        ''', (session_id, file_name, file_type, file_size, upload_purpose))
        
        conn.commit()
        conn.close()
    
    def log_export_activity(self, request_id, export_format, file_name):
        """Log export activity"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO export_activities 
            (request_id, export_format, file_name)
            VALUES (?, ?, ?)
        ''', (request_id, export_format, file_name))
        
        conn.commit()
        conn.close()
    
    def log_feedback(self, session_id, feedback_type, rating=None, comment=None):
        """Log user feedback"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO user_feedback 
            (session_id, feedback_type, rating, comment)
            VALUES (?, ?, ?, ?)
        ''', (session_id, feedback_type, rating, comment))
        
        conn.commit()
        conn.close()
    
    def get_analytics_summary(self):
        """Get overall analytics summary"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Total sessions
        cursor.execute('SELECT COUNT(*) FROM user_sessions')
        total_sessions = cursor.fetchone()[0]
        
        # Total requests
        cursor.execute('SELECT COUNT(*) FROM generation_requests')
        total_requests = cursor.fetchone()[0]
        
        # Total questions generated
        cursor.execute('SELECT COUNT(*) FROM generated_questions')
        total_questions = cursor.fetchone()[0]
        
        # Most popular subjects
        cursor.execute('''
            SELECT subject, COUNT(*) as count 
            FROM generation_requests 
            WHERE subject IS NOT NULL 
            GROUP BY subject 
            ORDER BY count DESC 
            LIMIT 5
        ''')
        popular_subjects = cursor.fetchall()
        
        # Most popular question types
        cursor.execute('''
            SELECT question_type, COUNT(*) as count 
            FROM generated_questions 
            GROUP BY question_type 
            ORDER BY count DESC
        ''')
        popular_question_types = cursor.fetchall()
        
        conn.close()
        
        return {
            'total_sessions': total_sessions,
            'total_requests': total_requests,
            'total_questions': total_questions,
            'popular_subjects': popular_subjects,
            'popular_question_types': popular_question_types
        }
    
    def get_user_activity(self, days=7):
        """Get user activity for the last N days"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT DATE(created_at) as date, COUNT(*) as count
            FROM generation_requests
            WHERE created_at >= datetime('now', '-{} days')
            GROUP BY DATE(created_at)
            ORDER BY date
        '''.format(days))
        
        activity_data = cursor.fetchall()
        conn.close()
        
        return activity_data
    
    def get_recent_requests(self, limit=10):
        """Get recent generation requests"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT gr.id, gr.generation_type, gr.subject, gr.exam_title, 
                   gr.total_questions, gr.total_marks, gr.created_at,
                   us.user_ip
            FROM generation_requests gr
            LEFT JOIN user_sessions us ON gr.session_id = us.session_id
            ORDER BY gr.created_at DESC
            LIMIT ?
        ''', (limit,))
        
        requests = cursor.fetchall()
        conn.close()
        
        return requests
    
    def get_question_statistics(self):
        """Get detailed question statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Question type distribution
        cursor.execute('''
            SELECT question_type, COUNT(*) as count
            FROM generated_questions
            GROUP BY question_type
            ORDER BY count DESC
        ''')
        type_stats = cursor.fetchall()
        
        # Bloom's taxonomy distribution
        cursor.execute('''
            SELECT bloom_level, COUNT(*) as count
            FROM generated_questions
            GROUP BY bloom_level
            ORDER BY count DESC
        ''')
        bloom_stats = cursor.fetchall()
        
        # Topic distribution
        cursor.execute('''
            SELECT topic, COUNT(*) as count
            FROM generated_questions
            GROUP BY topic
            ORDER BY count DESC
            LIMIT 10
        ''')
        topic_stats = cursor.fetchall()
        
        conn.close()
        
        return {
            'type_stats': type_stats,
            'bloom_stats': bloom_stats,
            'topic_stats': topic_stats
        }
    
    def search_requests(self, search_term=None, subject=None, date_from=None, date_to=None):
        """Search generation requests with filters"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = '''
            SELECT gr.id, gr.generation_type, gr.subject, gr.exam_title, 
                   gr.total_questions, gr.total_marks, gr.created_at,
                   us.user_ip
            FROM generation_requests gr
            LEFT JOIN user_sessions us ON gr.session_id = us.session_id
            WHERE 1=1
        '''
        params = []
        
        if search_term:
            query += " AND (gr.exam_title LIKE ? OR gr.subject LIKE ?)"
            params.extend([f'%{search_term}%', f'%{search_term}%'])
        
        if subject:
            query += " AND gr.subject = ?"
            params.append(subject)
        
        if date_from:
            query += " AND gr.created_at >= ?"
            params.append(date_from)
        
        if date_to:
            query += " AND gr.created_at <= ?"
            params.append(date_to)
        
        query += " ORDER BY gr.created_at DESC"
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        
        return results

# Initialize database manager
db_manager = DatabaseManager() 