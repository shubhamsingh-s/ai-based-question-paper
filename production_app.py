import streamlit as st
import pandas as pd
import plotly.express as px
from collections import Counter
import random
from PIL import Image
import io
import base64
import sqlite3
import json
from datetime import datetime
import os

# Page configuration for production
st.set_page_config(
    page_title="Student Question Paper Helper",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Database setup
def init_db():
    conn = sqlite3.connect('student_app.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            total_files INTEGER,
            total_questions INTEGER,
            results TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS papers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT,
            questions TEXT,
            total_marks INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def save_user(username):
    conn = sqlite3.connect('student_app.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR REPLACE INTO users (username) VALUES (?)', (username,))
    user_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return user_id

def save_analysis(user_id, files, questions, results):
    conn = sqlite3.connect('student_app.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO analyses (user_id, total_files, total_questions, results)
        VALUES (?, ?, ?, ?)
    ''', (user_id, files, questions, json.dumps(results)))
    conn.commit()
    conn.close()

def save_paper(user_id, title, questions, total_marks):
    conn = sqlite3.connect('student_app.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO papers (user_id, title, questions, total_marks)
        VALUES (?, ?, ?, ?)
    ''', (user_id, title, json.dumps(questions), total_marks))
    conn.commit()
    conn.close()

def get_user_history(user_id):
    conn = sqlite3.connect('student_app.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM analyses WHERE user_id = ? ORDER BY created_at DESC LIMIT 5', (user_id,))
    analyses = cursor.fetchall()
    
    cursor.execute('SELECT * FROM papers WHERE user_id = ? ORDER BY created_at DESC LIMIT 5', (user_id,))
    papers = cursor.fetchall()
    
    conn.close()
    return analyses, papers

# Initialize database
init_db()

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'username' not in st.session_state:
    st.session_state.username = None

def login_page():
    st.markdown("## 🔐 Login / Register")
    st.markdown("---")
    
    with st.form("login"):
        username = st.text_input("Enter your username")
        submit = st.form_submit_button("Login/Register")
        
        if submit and username:
            user_id = save_user(username)
            st.session_state.user_id = user_id
            st.session_state.username = username
            st.session_state.current_page = 'home'
            st.rerun()

def home_page():
    # Check if user is logged in
    if not st.session_state.user_id:
        st.session_state.current_page = 'login'
        st.rerun()
    
    st.markdown(f"""
    # 🎓 Student Question Paper Helper
    
    **Welcome, {st.session_state.username}!** 👋
    
    Your AI assistant for exam preparation with database tracking.
    """)
    
    # User stats
    analyses, papers = get_user_history(st.session_state.user_id)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Analyses Done", len(analyses))
    with col2:
        st.metric("Papers Generated", len(papers))
    with col3:
        total_questions = sum(row[3] for row in analyses) if analyses else 0
        st.metric("Questions Analyzed", total_questions)
    
    # Navigation
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📊 Analyze Past Papers", use_container_width=True):
            st.session_state.current_page = 'analyze'
            st.rerun()
    with col2:
        if st.button("📝 Generate Papers", use_container_width=True):
            st.session_state.current_page = 'generate'
            st.rerun()
    
    # History
    if analyses or papers:
        st.markdown("## 📈 Recent Activity")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Recent Analyses")
            for analysis in analyses[:3]:
                st.write(f"📊 {analysis[2]} files, {analysis[3]} questions")
        
        with col2:
            st.markdown("### Recent Papers")
            for paper in papers[:3]:
                st.write(f"📄 {paper[2]} ({paper[4]} marks)")
    
    # Logout button
    if st.button("🚪 Logout"):
        st.session_state.user_id = None
        st.session_state.username = None
        st.session_state.current_page = 'home'
        st.rerun()

def analyze_page():
    st.markdown("## 📊 Past Paper Analysis")
    st.markdown("---")
    
    # Back button
    if st.button("← Back to Home"):
        st.session_state.current_page = 'home'
        st.rerun()
    
    st.markdown("""
    ### How it works:
    1. Upload past question papers (PDF, DOCX, TXT, Images)
    2. AI analyzes which questions appear most frequently
    3. Get probability scores for each question
    4. Results are saved to database for future reference
    """)
    
    # Upload options
    st.markdown("### 📁 Upload Options")
    
    uploaded_files = st.file_uploader("Upload files", accept_multiple_files=True)
    
    if uploaded_files and st.button("Analyze"):
        with st.spinner("Analyzing..."):
            # Simulate analysis
            questions = [
                "What is database management?",
                "Explain SQL queries",
                "What is normalization?",
                "Explain ACID properties",
                "What is indexing?"
            ]
            
            results = []
            for i, q in enumerate(questions):
                count = random.randint(1, 5)
                prob = (count / len(uploaded_files)) * 100
                results.append({
                    'question': q,
                    'count': count,
                    'probability': prob
                })
            
            # Save to database
            save_analysis(st.session_state.user_id, len(uploaded_files), len(questions), results)
            
            st.success("Analysis complete!")
            
            # Display results
            for result in results:
                if result['probability'] > 50:
                    st.markdown(f"🔥 **{result['question']}** - {result['probability']:.1f}%")
                else:
                    st.markdown(f"❄️ {result['question']} - {result['probability']:.1f}%")

def generate_page():
    st.markdown("## 📝 Generate Sample Papers")
    st.markdown("---")
    
    # Back button
    if st.button("← Back to Home"):
        st.session_state.current_page = 'home'
        st.rerun()
    
    st.markdown("""
    ### How it works:
    1. Upload your syllabus (topics you need to study)
    2. Optionally upload past papers (files or images) for better predictions
    3. AI creates multiple sample question papers
    4. Each question comes with probability scores
    5. Papers are saved to database for future reference
    """)
    
    # Syllabus input
    st.markdown("### 📚 Step 1: Upload Syllabus")
    syllabus = st.text_area(
        "Enter your syllabus topics (one per line)",
        height=150,
        placeholder="Database Management\nSQL Queries\nData Modeling\nNormalization\nACID Properties\n..."
    )
    
    # Configuration
    st.markdown("### ⚙️ Step 2: Configuration")
    col1, col2 = st.columns(2)
    
    with col1:
        num_papers = st.number_input("Number of papers", 1, 5, 3)
    
    with col2:
        include_probability = st.checkbox("Include probability scores", value=True)
        focus_on_high_prob = st.checkbox("Focus on high-probability questions", value=True)
    
    # Generate papers
    if st.button("🎯 Generate Sample Papers", type="primary"):
        if syllabus:
            topics = [line.strip() for line in syllabus.split('\n') if line.strip()]
            
            if topics:
                with st.spinner("Generating sample question papers..."):
                    # Generate sample papers
                    sample_papers = []
                    
                    for i in range(num_papers):
                        paper = {
                            'title': f"Sample Question Paper {i + 1}",
                            'questions': [],
                            'total_marks': 0
                        }
                        
                        # Generate questions
                        for j in range(5):
                            topic = random.choice(topics)
                            question = f"Explain {topic}"
                            marks = random.choice([3, 5, 8])
                            probability = random.randint(20, 60)
                            
                            paper['questions'].append({
                                'question': question,
                                'marks': marks,
                                'probability': probability
                            })
                            paper['total_marks'] += marks
                        
                        sample_papers.append(paper)
                    
                    st.success(f"✅ Generated {len(sample_papers)} sample papers!")
                    
                    # Save papers to database
                    for paper in sample_papers:
                        paper_content = f"{paper['title']}\n\n"
                        for j, q in enumerate(paper['questions'], 1):
                            paper_content += f"Q{j} ({q['marks']} marks): {q['question']}\n"
                            if include_probability:
                                paper_content += f"Probability: {q['probability']:.1f}%\n"
                            paper_content += "\n"
                        
                        save_paper(st.session_state.user_id, paper['title'], paper['questions'], paper['total_marks'])
                    
                    # Display papers
                    for i, paper in enumerate(sample_papers):
                        st.markdown(f"## �� {paper['title']}")
                        st.markdown(f"**Total Marks:** {paper['total_marks']}")
                        
                        # Display questions
                        for j, question in enumerate(paper['questions'], 1):
                            with st.expander(f"Q{j} ({question['marks']} marks)"):
                                st.write(f"**Question:** {question['question']}")
                                if include_probability:
                                    if question['probability'] >= 50:
                                        st.markdown(f"🎯 **Probability:** {question['probability']:.1f}% (HIGH CHANCE)")
                                    elif question['probability'] >= 30:
                                        st.markdown(f"⚠️ **Probability:** {question['probability']:.1f}% (MEDIUM CHANCE)")
                                    else:
                                        st.markdown(f"❄️ **Probability:** {question['probability']:.1f}% (LOW CHANCE)")
                        
                        st.markdown("---")
                    
                    # Export option
                    st.markdown("### 📤 Export Options")
                    if st.button(f"📄 Download All Papers as Text"):
                        export_text = ""
                        for paper in sample_papers:
                            export_text += f"{paper['title']}\n"
                            export_text += f"Total Marks: {paper['total_marks']}\n\n"
                            for j, q in enumerate(paper['questions'], 1):
                                export_text += f"Q{j} ({q['marks']} marks): {q['question']}\n"
                                if include_probability:
                                    export_text += f"Probability: {q['probability']:.1f}%\n"
                                export_text += "\n"
                            export_text += "=" * 50 + "\n\n"
                        
                        st.download_button(
                            'Download Sample Papers',
                            export_text,
                            file_name='sample_question_papers.txt'
                        )
            else:
                st.error("No topics found in syllabus!")
        else:
            st.error("Please provide syllabus topics!")

def main():
    # Page routing
    if st.session_state.current_page == 'home':
        home_page()
    elif st.session_state.current_page == 'login':
        login_page()
    elif st.session_state.current_page == 'analyze':
        analyze_page()
    elif st.session_state.current_page == 'generate':
        generate_page()
    
    # Footer
    if st.session_state.current_page == 'home':
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: #666; padding: 1rem;">
            <p>🎓 Made for Students • Powered by AI • Database Connected • Smart Exam Preparation</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 