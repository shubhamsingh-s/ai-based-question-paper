import sqlite3
import json
from datetime import datetime

def create_database():
    """Create SQLite database with tables for tracking user interactions"""
    conn = sqlite3.connect('question_paper_analytics.db')
    cursor = conn.cursor()
    
    # Table for user sessions
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            user_ip TEXT,
            user_agent TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Table for question generation requests
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS generation_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            generation_type TEXT NOT NULL, -- 'auto', 'manual', 'analysis'
            subject TEXT,
            exam_title TEXT,
            total_questions INTEGER,
            total_marks INTEGER,
            duration INTEGER,
            question_types TEXT, -- JSON array
            difficulty TEXT,
            topics_used TEXT, -- JSON array
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Table for generated questions
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS generated_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            request_id INTEGER,
            question_text TEXT NOT NULL,
            question_type TEXT NOT NULL,
            topic TEXT NOT NULL,
            marks INTEGER,
            bloom_level TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (request_id) REFERENCES generation_requests (id)
        )
    ''')
    
    # Table for analytics data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS analytics_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            request_id INTEGER,
            type_counts TEXT, -- JSON object
            topic_counts TEXT, -- JSON object
            bloom_counts TEXT, -- JSON object
            total_questions INTEGER,
            total_marks INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (request_id) REFERENCES generation_requests (id)
        )
    ''')
    
    # Table for file uploads
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS file_uploads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            file_name TEXT NOT NULL,
            file_type TEXT NOT NULL,
            file_size INTEGER,
            upload_purpose TEXT, -- 'syllabus', 'analysis'
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Table for export activities
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS export_activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            request_id INTEGER,
            export_format TEXT NOT NULL, -- 'txt', 'json', 'csv'
            file_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (request_id) REFERENCES generation_requests (id)
        )
    ''')
    
    # Table for user feedback
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            feedback_type TEXT, -- 'rating', 'comment', 'bug_report'
            rating INTEGER, -- 1-5 stars
            comment TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database created successfully!")

def insert_sample_data():
    """Insert sample data for testing"""
    conn = sqlite3.connect('question_paper_analytics.db')
    cursor = conn.cursor()
    
    # Sample session
    cursor.execute('''
        INSERT INTO user_sessions (session_id, user_ip, user_agent)
        VALUES (?, ?, ?)
    ''', ('sample_session_1', '192.168.1.1', 'Mozilla/5.0'))
    
    # Sample generation request
    cursor.execute('''
        INSERT INTO generation_requests 
        (session_id, generation_type, subject, exam_title, total_questions, total_marks, duration, question_types, difficulty, topics_used)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        'sample_session_1',
        'auto',
        'Database Management System',
        'DBMS Midterm Exam',
        25,
        100,
        180,
        json.dumps(['MCQ', 'Short Answer', 'Long Answer']),
        'Mixed',
        json.dumps(['Database Design', 'SQL', 'Normalization'])
    ))
    
    request_id = cursor.lastrowid
    
    # Sample questions
    sample_questions = [
        ('What is the primary purpose of Database Design?', 'MCQ', 'Database Design', 1, 'Understand'),
        ('Explain the concept of SQL.', 'Short Answer', 'SQL', 3, 'Apply'),
        ('Discuss Normalization in detail with examples.', 'Long Answer', 'Normalization', 8, 'Analyze')
    ]
    
    for question in sample_questions:
        cursor.execute('''
            INSERT INTO generated_questions 
            (request_id, question_text, question_type, topic, marks, bloom_level)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (request_id, question[0], question[1], question[2], question[3], question[4]))
    
    # Sample analytics
    cursor.execute('''
        INSERT INTO analytics_data 
        (request_id, type_counts, topic_counts, bloom_counts, total_questions, total_marks)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        request_id,
        json.dumps({'MCQ': 1, 'Short Answer': 1, 'Long Answer': 1}),
        json.dumps({'Database Design': 1, 'SQL': 1, 'Normalization': 1}),
        json.dumps({'Understand': 1, 'Apply': 1, 'Analyze': 1}),
        3,
        12
    ))
    
    conn.commit()
    conn.close()
    print("Sample data inserted successfully!")

if __name__ == "__main__":
    create_database()
    insert_sample_data() 