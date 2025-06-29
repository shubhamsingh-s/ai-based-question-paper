"import streamlit as st" 

import streamlit as st
import pandas as pd
import plotly.express as px
import random
import json
from datetime import datetime
import re
import sqlite3
import os
import requests
import openai
from typing import List, Dict, Any

# Page configuration
st.set_page_config(
    page_title="QuestVibe",
    page_icon="📚",
    layout="wide"
)

# Database setup
def init_database():
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            institution TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            session_start TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            session_end TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS question_generations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            subject TEXT,
            num_questions INTEGER,
            question_types TEXT,
            generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    conn.commit()
    conn.close()

# Initialize database
init_database()

# Custom CSS for enhanced styling
st.markdown("""
<style>
/* Main background styling with aesthetic image */
.main {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
}
.stApp {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
    background-attachment: fixed;
}
.main .block-container {
    background: rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(20px);
    border-radius: 20px;
    padding: 2rem;
    margin: 1rem;
    border: 1px solid rgba(255, 255, 255, 0.4);
    box-shadow: 0 8px 32px rgba(0,0,0,0.2);
}
h1 {
    background: linear-gradient(45deg, #FF6B6B, #4ECDC4, #45B7D1, #96CEB4);
    background-size: 300% 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: gradient 3s ease infinite;
    text-align: center;
    font-size: 3.5rem;
    font-weight: 800;
    margin-bottom: 2rem;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}
@keyframes gradient {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
.stButton > button {
    background: linear-gradient(45deg, #667eea, #764ba2);
    color: white;
    border: none;
    border-radius: 15px;
    padding: 0.75rem 2rem;
    font-weight: 600;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0,0,0,0.4);
}
.stButton > button[data-baseweb="button"] {
    background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
    font-size: 1.2rem;
    padding: 1rem 2.5rem;
    border-radius: 25px;
}
div[data-testid="column"] {
    background: rgba(255, 255, 255, 0.25);
    border-radius: 20px;
    padding: 2rem;
    margin: 1rem 0.5rem;
    box-shadow: 0 8px 32px rgba(0,0,0,0.15);
    border: 1px solid rgba(255, 255, 255, 0.4);
    transition: all 0.3s ease;
    backdrop-filter: blur(20px);
}
div[data-testid="column"]:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 40px rgba(0,0,0,0.2);
    background: rgba(255, 255, 255, 0.3);
}
div[data-testid="metric-container"] {
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.9), rgba(118, 75, 162, 0.9));
    border-radius: 15px;
    padding: 1.5rem;
    color: white;
    text-align: center;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    margin: 0.5rem 0;
    backdrop-filter: blur(10px);
}
.footer {
    background: linear-gradient(135deg, rgba(44, 62, 80, 0.9), rgba(52, 73, 94, 0.9));
    color: white;
    text-align: center;
    padding: 2rem;
    border-radius: 20px;
    margin-top: 3rem;
    box-shadow: 0 8px 32px rgba(0,0,0,0.2);
    backdrop-filter: blur(15px);
}
p, h2, h3, h4, h5, h6 {
    color: #ffffff;
    font-weight: 600;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
}
div[data-testid="stMarkdown"] {
    background: rgba(255, 255, 255, 0.15);
    padding: 1rem;
    border-radius: 10px;
    margin: 0.5rem 0;
    backdrop-filter: blur(15px);
    border: 1px solid rgba(255, 255, 255, 0.3);
}
.stTextInput > div > div > input {
    background: rgba(255, 255, 255, 0.25);
    border-radius: 10px;
    border: 1px solid rgba(255, 255, 255, 0.4);
    color: #000000 !important;
    backdrop-filter: blur(15px);
    font-weight: 500;
}
.stTextInput > div > div > input::placeholder {
    color: rgba(0, 0, 0, 0.6);
}
/* Make sure text is visible in all input fields */
input, textarea, select {
    color: #000000 !important;
}
/* Ensure password field text is also visible */
input[type="password"] {
    color: #000000 !important;
}
.stSelectbox > div > div > div {
    background: rgba(255, 255, 255, 0.25);
    border-radius: 10px;
    border: 1px solid rgba(255, 255, 255, 0.4);
    backdrop-filter: blur(15px);
}
.stSlider > div > div > div > div {
    background: rgba(255, 255, 255, 0.25);
}
.stAlert {
    background: rgba(255, 255, 255, 0.2);
    border-radius: 15px;
    backdrop-filter: blur(15px);
    border: 1px solid rgba(255, 255, 255, 0.4);
}
.streamlit-expanderHeader {
    background: rgba(255, 255, 255, 0.2);
    border-radius: 10px;
    padding: 1rem;
    margin: 0.5rem 0;
    border: 1px solid rgba(255, 255, 255, 0.4);
    backdrop-filter: blur(15px);
    color: #ffffff;
    font-weight: 600;
}
.streamlit-expanderContent {
    background: rgba(255, 255, 255, 0.15);
    border-radius: 10px;
    padding: 1rem;
    margin: 0.5rem 0;
    border: 1px solid rgba(255, 255, 255, 0.3);
    backdrop-filter: blur(15px);
}
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255, 255, 255, 0.2);
    border-radius: 10px;
    padding: 0.5rem;
    margin: 0.5rem 0;
}
</style>
""", unsafe_allow_html=True)

# --- Simple user database (for demo) ---
USERS = {
    "admin": {"password": "admin123", "role": "admin", "name": "Administrator"},
    "teacher": {"password": "teacher123", "role": "teacher", "name": "Teacher"},
    "student": {"password": "student123", "role": "student", "name": "Student"},
    "demo": {"password": "demo123", "role": "teacher", "name": "Demo User"}
}

# Super User credentials (hidden admin access)
SUPER_USER = {
    "username": "superadmin",
    "password": "questvibe2024",
    "role": "super_admin",
    "name": "Super Administrator"
}

def save_user_to_database(name, institution):
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (name, institution, role) 
        VALUES (?, ?, ?)
    ''', (name, institution, 'user'))
    user_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return user_id

def get_user_by_id(user_id):
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def log_session(user_id):
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO sessions (user_id) 
        VALUES (?)
    ''', (user_id,))
    session_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return session_id

def log_question_generation(user_id, subject, num_questions, question_types):
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO question_generations (user_id, subject, num_questions, question_types) 
        VALUES (?, ?, ?, ?)
    ''', (user_id, subject, num_questions, json.dumps(question_types)))
    conn.commit()
    conn.close()

def get_database_stats():
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    
    # Get user count
    cursor.execute('SELECT COUNT(*) FROM users')
    user_count = cursor.fetchone()[0]
    
    # Get total generations
    cursor.execute('SELECT COUNT(*) FROM question_generations')
    generation_count = cursor.fetchone()[0]
    
    # Get recent users
    cursor.execute('SELECT name, institution, created_at FROM users ORDER BY created_at DESC LIMIT 10')
    recent_users = cursor.fetchall()
    
    # Get recent generations
    cursor.execute('''
        SELECT u.name, u.institution, qg.subject, qg.num_questions, qg.generated_at 
        FROM question_generations qg 
        JOIN users u ON qg.user_id = u.id 
        ORDER BY qg.generated_at DESC LIMIT 10
    ''')
    recent_generations = cursor.fetchall()
    
    conn.close()
    return user_count, generation_count, recent_users, recent_generations

def admin_dashboard():
    st.markdown("## 📊 Admin Dashboard")
    st.write("Database analytics and user information")
    
    user_count, generation_count, recent_users, recent_generations = get_database_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Users", user_count, "👥")
    
    with col2:
        st.metric("Total Generations", generation_count, "📝")
    
    with col3:
        st.metric("Active Sessions", "Live", "🟢")
    
    with col4:
        st.metric("Database Status", "Connected", "✅")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 👥 Recent Users")
        if recent_users:
            for user in recent_users:
                st.write(f"**{user[0]}** - {user[1]} ({user[2][:10]}...)")
        else:
            st.write("No users yet")
    
    with col2:
        st.markdown("### 📝 Recent Generations")
        if recent_generations:
            for gen in recent_generations:
                st.write(f"**{gen[0]}** - {gen[2]} ({gen[3]} questions)")
        else:
            st.write("No generations yet")
    
    if st.button("🔙 Back to Dashboard"):
        st.session_state.show_admin = False
        st.rerun()

def super_admin_dashboard():
    st.markdown("## 🔓 Super Admin Dashboard")
    st.warning("⚠️ **SUPER ADMIN ACCESS** - Full database control")
    
    # Get all database data
    conn = sqlite3.connect('user_data.db')
    
    # Users table
    st.markdown("### 👥 All Users")
    users_df = pd.read_sql_query("SELECT * FROM users ORDER BY created_at DESC", conn)
    if not users_df.empty:
        st.dataframe(users_df, use_container_width=True)
        
        # Download users data
        csv = users_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Users Data (CSV)",
            data=csv,
            file_name="users_data.csv",
            mime="text/csv"
        )
    else:
        st.write("No users found in database")
    
    # Sessions table
    st.markdown("### 📊 User Sessions")
    sessions_df = pd.read_sql_query("""
        SELECT s.*, u.name, u.institution 
        FROM sessions s 
        JOIN users u ON s.user_id = u.id 
        ORDER BY s.session_start DESC
    """, conn)
    if not sessions_df.empty:
        st.dataframe(sessions_df, use_container_width=True)
        
        csv = sessions_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Sessions Data (CSV)",
            data=csv,
            file_name="sessions_data.csv",
            mime="text/csv"
        )
    else:
        st.write("No sessions found in database")
    
    # Question generations table
    st.markdown("### 📝 Question Generations")
    generations_df = pd.read_sql_query("""
        SELECT qg.*, u.name, u.institution 
        FROM question_generations qg 
        JOIN users u ON qg.user_id = u.id 
        ORDER BY qg.generated_at DESC
    """, conn)
    if not generations_df.empty:
        st.dataframe(generations_df, use_container_width=True)
        
        csv = generations_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Generations Data (CSV)",
            data=csv,
            file_name="generations_data.csv",
            mime="text/csv"
        )
    else:
        st.write("No question generations found in database")
    
    # Database statistics
    st.markdown("### 📈 Database Statistics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_users = len(users_df)
        st.metric("Total Users", total_users, "👥")
    
    with col2:
        total_sessions = len(sessions_df)
        st.metric("Total Sessions", total_sessions, "📊")
    
    with col3:
        total_generations = len(generations_df)
        st.metric("Total Generations", total_generations, "📝")
    
    with col4:
        if not generations_df.empty:
            avg_questions = generations_df['num_questions'].mean()
            st.metric("Avg Questions/Gen", f"{avg_questions:.1f}", "❓")
        else:
            st.metric("Avg Questions/Gen", "0", "❓")
    
    # Charts
    if not generations_df.empty:
        st.markdown("### 📊 Analytics Charts")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Subject distribution
            subject_counts = generations_df['subject'].value_counts()
            fig1 = px.pie(values=subject_counts.values, names=subject_counts.index, title="Question Generations by Subject")
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # Questions per generation
            fig2 = px.histogram(generations_df, x='num_questions', title="Distribution of Questions per Generation")
            st.plotly_chart(fig2, use_container_width=True)
    
    # Database management
    st.markdown("### 🗄️ Database Management")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🗑️ Clear All Data", type="secondary"):
            if st.checkbox("I understand this will delete ALL data permanently"):
                cursor = conn.cursor()
                cursor.execute("DELETE FROM question_generations")
                cursor.execute("DELETE FROM sessions")
                cursor.execute("DELETE FROM users")
                conn.commit()
                st.success("🗑️ All data cleared!")
                st.rerun()
    
    with col2:
        if st.button("📊 Export Full Database", type="secondary"):
            # Create a zip file with all data
            import zipfile
            import io
            
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
                # Add each table as CSV
                for table_name, df in [("users", users_df), ("sessions", sessions_df), ("generations", generations_df)]:
                    csv_data = df.to_csv(index=False)
                    zip_file.writestr(f"{table_name}.csv", csv_data)
            
            st.download_button(
                label="📦 Download Full Database (ZIP)",
                data=zip_buffer.getvalue(),
                file_name="questvibe_database.zip",
                mime="application/zip"
            )
    
    # AI Database Management
    st.markdown("### 🤖 AI Database Management")
    
    # Get database status
    db_status = st.session_state.questvibe_ai_db.get_database_status()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Subjects", db_status['total_subjects'], "📚")
    
    with col2:
        st.metric("Total Topics", db_status['total_topics'], "🎯")
    
    with col3:
        st.metric("Duplicates Found", len(db_status['duplicates']), "⚠️")
    
    with col4:
        if st.button("🧹 Clean Duplicates", type="secondary"):
            st.session_state.questvibe_ai_db.cleanup_database()
            st.success("✅ Database cleaned!")
            st.rerun()
    
    # Show branch statistics
    st.markdown("**📊 Subjects by Branch:**")
    for branch, count in db_status['branch_counts']:
        st.write(f"• **{branch}**: {count} subjects")
    
    # Show duplicates if any
    if db_status['duplicates']:
        st.markdown("**⚠️ Duplicate Subjects Found:**")
        for branch, subject, count in db_status['duplicates']:
            st.write(f"• {branch} - {subject} (appears {count} times)")
    
    # Repopulate database option
    st.markdown("**🔄 Database Operations:**")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Repopulate AI Database", type="primary"):
            st.session_state.questvibe_ai_db.populate_database()
            st.success("✅ AI Database repopulated!")
            st.rerun()
    
    with col2:
        if st.button("📊 Refresh Status", type="secondary"):
            st.rerun()
    
    # ChatGPT Configuration
    st.markdown("### 🤖 ChatGPT Configuration")
    
    # API Key management
    with st.expander("🔑 ChatGPT API Configuration", expanded=False):
        api_key = st.text_input("OpenAI API Key", type="password", 
                               help="Enter your OpenAI API key to enable ChatGPT integration")
        
        if api_key:
            st.session_state.questvibe_chatgpt.api_key = api_key
            st.success("✅ API key configured!")
        
        # Test ChatGPT connection
        if st.button("🧪 Test ChatGPT Connection", type="secondary"):
            if st.session_state.questvibe_chatgpt.api_key:
                try:
                    test_questions = st.session_state.questvibe_chatgpt.generate_questions(
                        "Test Subject", ["Test Topic"], 1, ["MCQ"]
                    )
                    if test_questions:
                        st.success("✅ ChatGPT connection successful!")
                        st.write("**Sample Question:**")
                        st.write(test_questions[0]['question'])
                    else:
                        st.error("❌ ChatGPT test failed - no questions generated")
                except Exception as e:
                    st.error(f"❌ ChatGPT test failed: {str(e)}")
            else:
                st.warning("⚠️ Please enter an API key first")
    
    # ChatGPT Statistics
    st.markdown("**📊 ChatGPT Usage Statistics:**")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        api_status = "✅ Connected" if st.session_state.questvibe_chatgpt.api_key else "❌ Not Connected"
        st.metric("API Status", api_status, "🔗")
    
    with col2:
        st.metric("Model", st.session_state.questvibe_chatgpt.model, "🤖")
    
    with col3:
        st.metric("Max Tokens", st.session_state.questvibe_chatgpt.max_tokens, "📝")
    
    # ChatGPT Features
    st.markdown("**✨ ChatGPT Features:**")
    features = [
        "Intelligent question generation",
        "Multiple difficulty levels",
        "Bloom's taxonomy integration", 
        "Industry-relevant content",
        "JSON response parsing",
        "Fallback generation system"
    ]
    
    for feature in features:
        st.write(f"• {feature}")
    
    conn.close()
    
    if st.button("🔙 Back to Dashboard"):
        st.session_state.show_super_admin = False
        st.rerun()

# AI Database Population System
class QuestVibeAIDatabase:
    def __init__(self):
        self.engineering_subjects = {
            "Computer Science Engineering": {
                "subjects": [
                    "Data Structures and Algorithms",
                    "Object-Oriented Programming",
                    "Database Management Systems",
                    "Computer Networks",
                    "Operating Systems",
                    "Software Engineering",
                    "Web Technologies",
                    "Machine Learning",
                    "Artificial Intelligence",
                    "Computer Architecture",
                    "Digital Logic Design",
                    "Computer Organization",
                    "Data Communication",
                    "Information Security",
                    "Cloud Computing",
                    "Big Data Analytics",
                    "Internet of Things",
                    "Mobile Computing",
                    "Computer Graphics",
                    "System Programming"
                ],
                "exam_topics": {
                    "Data Structures and Algorithms": [
                        "Arrays and Linked Lists", "Stacks and Queues", "Trees and Graphs",
                        "Sorting Algorithms", "Searching Algorithms", "Dynamic Programming",
                        "Greedy Algorithms", "Complexity Analysis", "Recursion", "Hash Tables"
                    ],
                    "Database Management Systems": [
                        "ER Model", "Relational Model", "SQL Queries", "Normalization",
                        "Transaction Management", "Concurrency Control", "Indexing",
                        "Database Security", "Distributed Databases", "NoSQL Databases"
                    ],
                    "Computer Networks": [
                        "OSI Model", "TCP/IP Protocol", "Network Topologies", "Routing Algorithms",
                        "Network Security", "Wireless Networks", "Network Management",
                        "Quality of Service", "Network Protocols", "Internet Architecture"
                    ]
                }
            },
            "Information Technology": {
                "subjects": [
                    "Programming Fundamentals",
                    "Data Structures",
                    "Database Systems",
                    "Computer Networks",
                    "Web Development",
                    "Software Testing",
                    "Information Security",
                    "Cloud Computing",
                    "Mobile App Development",
                    "Data Analytics",
                    "System Analysis and Design",
                    "Operating Systems",
                    "Computer Architecture",
                    "Digital Electronics",
                    "Computer Graphics",
                    "Multimedia Systems",
                    "E-Commerce",
                    "Enterprise Systems",
                    "Network Administration",
                    "IT Project Management"
                ],
                "exam_topics": {
                    "Programming Fundamentals": [
                        "Variables and Data Types", "Control Structures", "Functions",
                        "Arrays and Strings", "Object-Oriented Concepts", "Exception Handling",
                        "File I/O", "Memory Management", "Debugging", "Code Optimization"
                    ],
                    "Web Development": [
                        "HTML and CSS", "JavaScript", "PHP", "ASP.NET", "Web Servers",
                        "Client-Side Scripting", "Server-Side Scripting", "Web Security",
                        "Responsive Design", "Web APIs"
                    ]
                }
            },
            "Electronics and Communication": {
                "subjects": [
                    "Digital Electronics",
                    "Analog Electronics",
                    "Communication Systems",
                    "Signals and Systems",
                    "Electromagnetic Theory",
                    "Antenna Theory",
                    "Microwave Engineering",
                    "Optical Communication",
                    "Satellite Communication",
                    "Wireless Communication",
                    "Digital Signal Processing",
                    "VLSI Design",
                    "Microprocessors",
                    "Control Systems",
                    "Power Electronics",
                    "Electronic Devices",
                    "Circuit Theory",
                    "Network Analysis",
                    "Telecommunication Networks",
                    "Information Theory"
                ],
                "exam_topics": {
                    "Digital Electronics": [
                        "Boolean Algebra", "Logic Gates", "Combinational Circuits",
                        "Sequential Circuits", "Flip-Flops", "Counters", "Registers",
                        "Memory Devices", "Digital ICs", "VHDL Programming"
                    ],
                    "Communication Systems": [
                        "Amplitude Modulation", "Frequency Modulation", "Digital Modulation",
                        "Pulse Modulation", "Multiplexing", "Demodulation", "Noise Analysis",
                        "Channel Coding", "Error Detection", "Information Theory"
                    ]
                }
            },
            "Mechanical Engineering": {
                "subjects": [
                    "Engineering Mechanics",
                    "Strength of Materials",
                    "Machine Design",
                    "Thermodynamics",
                    "Fluid Mechanics",
                    "Heat Transfer",
                    "Manufacturing Processes",
                    "CAD/CAM",
                    "Automobile Engineering",
                    "Robotics",
                    "Control Systems",
                    "Material Science",
                    "Dynamics of Machines",
                    "Theory of Machines",
                    "Industrial Engineering",
                    "Refrigeration and Air Conditioning",
                    "Power Plant Engineering",
                    "Automation",
                    "Quality Control",
                    "Project Management"
                ],
                "exam_topics": {
                    "Engineering Mechanics": [
                        "Statics", "Dynamics", "Kinematics", "Kinetics", "Friction",
                        "Centroids", "Moment of Inertia", "Work and Energy", "Impulse and Momentum",
                        "Vibration Analysis"
                    ],
                    "Thermodynamics": [
                        "First Law", "Second Law", "Entropy", "Gas Cycles", "Vapor Cycles",
                        "Heat Engines", "Refrigeration Cycles", "Psychrometrics", "Combustion",
                        "Steam Tables"
                    ]
                }
            },
            "Civil Engineering": {
                "subjects": [
                    "Structural Analysis",
                    "Reinforced Concrete Design",
                    "Steel Structures",
                    "Transportation Engineering",
                    "Geotechnical Engineering",
                    "Hydraulics",
                    "Environmental Engineering",
                    "Surveying",
                    "Construction Management",
                    "Highway Engineering",
                    "Bridge Engineering",
                    "Water Resources",
                    "Irrigation Engineering",
                    "Town Planning",
                    "Building Materials",
                    "Soil Mechanics",
                    "Foundation Engineering",
                    "Earthquake Engineering",
                    "Traffic Engineering",
                    "Project Planning"
                ],
                "exam_topics": {
                    "Structural Analysis": [
                        "Beam Analysis", "Truss Analysis", "Frame Analysis", "Influence Lines",
                        "Deflection Analysis", "Stability Analysis", "Matrix Methods",
                        "Finite Element Method", "Plastic Analysis", "Dynamic Analysis"
                    ],
                    "Reinforced Concrete Design": [
                        "Flexural Design", "Shear Design", "Column Design", "Footing Design",
                        "Slab Design", "Beam Design", "Detailing", "Durability", "Serviceability",
                        "Code Provisions"
                    ]
                }
            }
        }
    
    def populate_database(self):
        """Automatically populate database with engineering subjects and topics"""
        conn = sqlite3.connect('user_data.db')
        cursor = conn.cursor()
        
        # Create subjects table if not exists with UNIQUE constraint
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS subjects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                branch TEXT NOT NULL,
                subject_name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(branch, subject_name)
            )
        ''')
        
        # Create topics table if not exists
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS topics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject_id INTEGER,
                topic_name TEXT NOT NULL,
                difficulty_level TEXT DEFAULT 'Medium',
                bloom_level TEXT DEFAULT 'Understanding',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(subject_id, topic_name),
                FOREIGN KEY (subject_id) REFERENCES subjects (id)
            )
        ''')
        
        # Create exam_patterns table if not exists
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS exam_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject_id INTEGER,
                pattern_name TEXT NOT NULL,
                total_questions INTEGER,
                mcq_count INTEGER,
                short_answer_count INTEGER,
                long_answer_count INTEGER,
                case_study_count INTEGER,
                time_duration INTEGER,
                marks_per_question REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (subject_id) REFERENCES subjects (id)
            )
        ''')
        
        # Clear existing data to prevent duplicates
        cursor.execute('DELETE FROM topics')
        cursor.execute('DELETE FROM subjects')
        
        # Populate subjects and topics
        for branch, data in self.engineering_subjects.items():
            for subject in data["subjects"]:
                try:
                    # Insert subject with UNIQUE constraint
                    cursor.execute('''
                        INSERT INTO subjects (branch, subject_name) 
                        VALUES (?, ?)
                    ''', (branch, subject))
                    
                    subject_id = cursor.lastrowid
                    
                    # Insert topics if available
                    if subject in data.get("exam_topics", {}):
                        for topic in data["exam_topics"][subject]:
                            try:
                                cursor.execute('''
                                    INSERT INTO topics (subject_id, topic_name) 
                                    VALUES (?, ?)
                                ''', (subject_id, topic))
                            except sqlite3.IntegrityError:
                                # Topic already exists, skip
                                pass
                except sqlite3.IntegrityError:
                    # Subject already exists, get its ID and add topics
                    cursor.execute('SELECT id FROM subjects WHERE branch = ? AND subject_name = ?', (branch, subject))
                    result = cursor.fetchone()
                    if result:
                        subject_id = result[0]
                        # Insert topics if available
                        if subject in data.get("exam_topics", {}):
                            for topic in data["exam_topics"][subject]:
                                try:
                                    cursor.execute('''
                                        INSERT INTO topics (subject_id, topic_name) 
                                        VALUES (?, ?)
                                    ''', (subject_id, topic))
                                except sqlite3.IntegrityError:
                                    # Topic already exists, skip
                                    pass
        
        # Clear and insert default exam patterns
        cursor.execute('DELETE FROM exam_patterns')
        default_patterns = [
            ("Mid Semester", 20, 10, 5, 3, 2, 90, 5.0),
            ("End Semester", 30, 15, 8, 5, 2, 180, 5.0),
            ("Unit Test", 15, 8, 4, 2, 1, 60, 5.0)
        ]
        
        for pattern_name, total, mcq, short, long, case_study, duration, marks in default_patterns:
            cursor.execute('''
                INSERT INTO exam_patterns 
                (pattern_name, total_questions, mcq_count, short_answer_count, long_answer_count, case_study_count, time_duration, marks_per_question) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (pattern_name, total, mcq, short, long, case_study, duration, marks))
        
        conn.commit()
        conn.close()
        
        return True
    
    def get_subjects_by_branch(self, branch):
        """Get all subjects for a specific engineering branch"""
        conn = sqlite3.connect('user_data.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT subject_name FROM subjects 
            WHERE branch = ? 
            ORDER BY subject_name
        ''', (branch,))
        
        subjects = [row[0] for row in cursor.fetchall()]
        conn.close()
        return subjects
    
    def get_topics_by_subject(self, subject_name):
        """Get all topics for a specific subject"""
        conn = sqlite3.connect('user_data.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT t.topic_name FROM topics t
            JOIN subjects s ON t.subject_id = s.id
            WHERE s.subject_name = ?
            ORDER BY t.topic_name
        ''', (subject_name,))
        
        topics = [row[0] for row in cursor.fetchall()]
        conn.close()
        return topics
    
    def get_exam_patterns(self):
        """Get all available exam patterns"""
        conn = sqlite3.connect('user_data.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM exam_patterns ORDER BY pattern_name')
        patterns = cursor.fetchall()
        conn.close()
        return patterns

    def cleanup_database(self):
        """Clean up duplicate data and ensure database integrity"""
        conn = sqlite3.connect('user_data.db')
        cursor = conn.cursor()
        
        # Remove duplicate subjects (keep the first occurrence)
        cursor.execute('''
            DELETE FROM subjects 
            WHERE id NOT IN (
                SELECT MIN(id) 
                FROM subjects 
                GROUP BY branch, subject_name
            )
        ''')
        
        # Remove duplicate topics (keep the first occurrence)
        cursor.execute('''
            DELETE FROM topics 
            WHERE id NOT IN (
                SELECT MIN(id) 
                FROM topics 
                GROUP BY subject_id, topic_name
            )
        ''')
        
        # Remove orphaned topics (topics without subjects)
        cursor.execute('''
            DELETE FROM topics 
            WHERE subject_id NOT IN (SELECT id FROM subjects)
        ''')
        
        conn.commit()
        conn.close()
        
        return True
    
    def get_database_status(self):
        """Get database status and statistics"""
        conn = sqlite3.connect('user_data.db')
        cursor = conn.cursor()
        
        # Count subjects by branch
        cursor.execute('''
            SELECT branch, COUNT(*) as count 
            FROM subjects 
            GROUP BY branch 
            ORDER BY branch
        ''')
        branch_counts = cursor.fetchall()
        
        # Count total topics
        cursor.execute('SELECT COUNT(*) FROM topics')
        total_topics = cursor.fetchone()[0]
        
        # Count total subjects
        cursor.execute('SELECT COUNT(*) FROM subjects')
        total_subjects = cursor.fetchone()[0]
        
        # Check for duplicates
        cursor.execute('''
            SELECT branch, subject_name, COUNT(*) as count 
            FROM subjects 
            GROUP BY branch, subject_name 
            HAVING COUNT(*) > 1
        ''')
        duplicates = cursor.fetchall()
        
        conn.close()
        
        return {
            'branch_counts': branch_counts,
            'total_topics': total_topics,
            'total_subjects': total_subjects,
            'duplicates': duplicates
        }

# Initialize AI Database System
if 'questvibe_ai_db' not in st.session_state:
    st.session_state.questvibe_ai_db = QuestVibeAIDatabase()
    # Automatically populate database on first run
    st.session_state.questvibe_ai_db.populate_database()

# ChatGPT Integration
class QuestVibeChatGPT:
    def __init__(self, api_key=None):
        self.api_key = api_key or st.secrets.get("OPENAI_API_KEY", "")
        self.model = "gpt-3.5-turbo"
        self.max_tokens = 1000
        
    def generate_questions(self, subject: str, topics: List[str], num_questions: int, question_types: List[str]) -> List[Dict]:
        """Generate intelligent questions using ChatGPT"""
        if not self.api_key:
            return self.generate_fallback_questions(subject, topics, num_questions, question_types)
        
        try:
            # Create prompt for ChatGPT
            prompt = self.create_question_prompt(subject, topics, num_questions, question_types)
            
            # Call ChatGPT API
            response = self.call_chatgpt_api(prompt)
            
            # Parse response
            questions = self.parse_chatgpt_response(response, question_types)
            
            return questions[:num_questions]  # Ensure we get the requested number
            
        except Exception as e:
            # Only show detailed error to super admins
            if hasattr(st.session_state, 'current_user') and st.session_state.current_user and st.session_state.current_user.get('role') == 'super_admin':
                st.warning(f"ChatGPT API error: {str(e)}. Using fallback generation.")
            # For normal users, just use fallback silently
            return self.generate_fallback_questions(subject, topics, num_questions, question_types)
    
    def create_question_prompt(self, subject: str, topics: List[str], num_questions: int, question_types: List[str]) -> str:
        """Create a detailed prompt for ChatGPT"""
        topics_text = ", ".join(topics)
        types_text = ", ".join(question_types)
        
        prompt = f"""
        You are an expert educator creating questions for {subject}. 
        
        Available topics: {topics_text}
        Question types needed: {types_text}
        Number of questions: {num_questions}
        
        Please generate {num_questions} questions with the following requirements:
        
        1. Questions should be relevant to the topics provided
        2. Mix of question types: {types_text}
        3. For MCQs, provide 4 options (A, B, C, D) with one correct answer
        4. Questions should test different cognitive levels (Remember, Understand, Apply, Analyze, Evaluate, Create)
        5. Difficulty should vary from easy to hard
        6. Questions should be practical and industry-relevant
        
        Format your response as JSON:
        {{
            "questions": [
                {{
                    "type": "MCQ/Short Answer/Long Answer/Case Study",
                    "question": "Question text here",
                    "options": ["A", "B", "C", "D"] (only for MCQ),
                    "correct_answer": "A" (only for MCQ),
                    "difficulty": "Easy/Medium/Hard",
                    "bloom_level": "Remember/Understand/Apply/Analyze/Evaluate/Create",
                    "topic": "specific topic from the list"
                }}
            ]
        }}
        
        Make sure the questions are high-quality, educational, and suitable for engineering students.
        """
        
        return prompt
    
    def call_chatgpt_api(self, prompt: str) -> str:
        """Call ChatGPT API"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are an expert educational content creator specializing in engineering education."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": self.max_tokens,
            "temperature": 0.7
        }
        
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            raise Exception(f"API call failed: {response.status_code}")
    
    def parse_chatgpt_response(self, response: str, question_types: List[str]) -> List[Dict]:
        """Parse ChatGPT response into structured questions"""
        try:
            # Try to extract JSON from response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            
            if json_start != -1 and json_end != 0:
                json_str = response[json_start:json_end]
                data = json.loads(json_str)
                
                if "questions" in data:
                    return data["questions"]
            
            # Fallback: parse manually
            return self.parse_manual_response(response, question_types)
            
        except Exception as e:
            # Only show parsing error to super admins
            if hasattr(st.session_state, 'current_user') and st.session_state.current_user and st.session_state.current_user.get('role') == 'super_admin':
                st.warning(f"Failed to parse ChatGPT response: {str(e)}")
            return self.parse_manual_response(response, question_types)
    
    def parse_manual_response(self, response: str, question_types: List[str]) -> List[Dict]:
        """Manually parse response if JSON parsing fails"""
        questions = []
        lines = response.split('\n')
        current_question = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Look for question patterns
            if any(qtype.lower() in line.lower() for qtype in question_types):
                if current_question:
                    questions.append(current_question)
                
                current_question = {
                    "type": "MCQ" if "mcq" in line.lower() else "Short Answer",
                    "question": line,
                    "options": [],
                    "difficulty": "Medium",
                    "bloom_level": "Understand",
                    "topic": "General"
                }
            elif current_question and line.startswith(('A.', 'B.', 'C.', 'D.')):
                current_question["options"].append(line)
        
        if current_question:
            questions.append(current_question)
        
        return questions
    
    def generate_fallback_questions(self, subject: str, topics: List[str], num_questions: int, question_types: List[str]) -> List[Dict]:
        """Generate questions without ChatGPT API"""
        questions = []
        
        for i in range(num_questions):
            topic = random.choice(topics)
            q_type = random.choice(question_types)
            
            if q_type == "MCQ":
                question = {
                    "type": "MCQ",
                    "question": f"{i+1}. What is {topic}?",
                    "options": [
                        f"A. {topic} is a fundamental concept",
                        f"B. {topic} is an advanced technique", 
                        f"C. {topic} is a basic principle",
                        f"D. {topic} is a complex system"
                    ],
                    "correct_answer": "A",
                    "difficulty": random.choice(["Easy", "Medium", "Hard"]),
                    "bloom_level": "Understand",
                    "topic": topic
                }
            else:
                question = {
                    "type": q_type,
                    "question": f"{i+1}. Explain {topic} in detail and discuss its applications in {subject}.",
                    "difficulty": random.choice(["Easy", "Medium", "Hard"]),
                    "bloom_level": "Analyze",
                    "topic": topic
                }
            
            questions.append(question)
        
        return questions
    
    def analyze_question_quality(self, questions: List[Dict]) -> Dict[str, Any]:
        """Analyze the quality and distribution of generated questions"""
        analysis = {
            "total_questions": len(questions),
            "type_distribution": {},
            "difficulty_distribution": {},
            "bloom_distribution": {},
            "topic_coverage": set(),
            "quality_score": 0
        }
        
        for q in questions:
            # Type distribution
            q_type = q.get("type", "Unknown")
            analysis["type_distribution"][q_type] = analysis["type_distribution"].get(q_type, 0) + 1
            
            # Difficulty distribution
            difficulty = q.get("difficulty", "Medium")
            analysis["difficulty_distribution"][difficulty] = analysis["difficulty_distribution"].get(difficulty, 0) + 1
            
            # Bloom level distribution
            bloom = q.get("bloom_level", "Understand")
            analysis["bloom_distribution"][bloom] = analysis["bloom_distribution"].get(bloom, 0) + 1
            
            # Topic coverage
            topic = q.get("topic", "General")
            analysis["topic_coverage"].add(topic)
        
        # Calculate quality score
        analysis["quality_score"] = min(100, len(questions) * 2 + len(analysis["topic_coverage"]) * 5)
        analysis["topic_coverage"] = list(analysis["topic_coverage"])
        
        return analysis

# Initialize ChatGPT
if 'questvibe_chatgpt' not in st.session_state:
    st.session_state.questvibe_chatgpt = QuestVibeChatGPT()

def main():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'current_user' not in st.session_state:
        st.session_state.current_user = None

    if not st.session_state.authenticated:
        st.markdown("""
        <div style="text-align: center; padding: 2rem;">
            <h1 style="background: linear-gradient(45deg, #FF6B6B, #4ECDC4, #45B7D1, #96CEB4); background-size: 300% 300%; -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; animation: gradient 3s ease infinite; font-size: 4rem; font-weight: 800; margin-bottom: 1rem;">QuestVibe</h1>
            <p style="font-size: 1.5rem; color: white; margin-bottom: 3rem;">AI-Powered Question Paper Generator</p>
        </div>
        """, unsafe_allow_html=True)
        with st.container():
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.markdown("""
                <div style="background: rgba(255, 255, 255, 0.2); backdrop-filter: blur(20px); border-radius: 20px; padding: 2rem; border: 1px solid rgba(255, 255, 255, 0.4); box-shadow: 0 8px 32px rgba(0,0,0,0.2);">
                    <h2 style="text-align: center; color: white; margin-bottom: 2rem;">👋 Welcome to QuestVibe</h2>
                </div>
                """, unsafe_allow_html=True)
                with st.form("login_form"):
                    name = st.text_input("👤 Your Name", placeholder="Enter your full name")
                    institution = st.text_input("🏫 Institution", placeholder="University/College/School name")
                    col1, col2, col3 = st.columns(3)
                    with col2:
                        submit_button = st.form_submit_button("Start Using QuestVibe", type="primary", use_container_width=True)
                    if submit_button:
                        if name.strip() and institution.strip():
                            # Check if this is a super user login attempt
                            if (name.strip().lower() == SUPER_USER["username"].lower() and 
                                institution.strip() == SUPER_USER["password"]):
                                # Super user access
                                st.session_state.authenticated = True
                                st.session_state.current_user = {
                                    "id": 0,
                                    "name": SUPER_USER["name"],
                                    "institution": "System Administration",
                                    "role": "super_admin",
                                    "session_id": 0
                                }
                                st.success("🔓 Super Admin access granted!")
                                st.rerun()
                            else:
                                # Regular user login
                                # Save user to database
                                user_id = save_user_to_database(name.strip(), institution.strip())
                                session_id = log_session(user_id)
                                
                                st.session_state.authenticated = True
                                st.session_state.current_user = {
                                    "id": user_id,
                                    "name": name.strip(),
                                    "institution": institution.strip(),
                                    "role": "user",
                                    "session_id": session_id
                                }
                                st.success(f"✅ Welcome to QuestVibe, {name.strip()}!")
                                st.rerun()
                        else:
                            st.error("❌ Please enter both your name and institution!")
                with st.expander("ℹ️ About QuestVibe"):
                    st.markdown("""
                    **QuestVibe** is an AI-powered question paper generator that helps educators create comprehensive exams.
                    
                    **Features:**
                    - 🤖 **Auto Generation**: Generate questions from predefined topics
                    - 📝 **Manual Creation**: Create questions from your own syllabus
                    - 📊 **Pattern Analysis**: Analyze exam patterns and trends
                    - 🗄️ **Database Tracking**: All your activities are securely stored
                    
                    **Your data is safe and will only be used to improve your experience.**
                    """)
                
                st.markdown("---")
                st.markdown("### ✨ Features Preview")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown("""
                    <div style="background: rgba(255, 255, 255, 0.15); border-radius: 15px; padding: 1rem; text-align: center; border: 1px solid rgba(255, 255, 255, 0.3);">
                        <h4 style="color: white;">🤖 Auto Generation</h4>
                        <p style="color: white;">AI-powered question paper creation</p>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    st.markdown("""
                    <div style="background: rgba(255, 255, 255, 0.15); border-radius: 15px; padding: 1rem; text-align: center; border: 1px solid rgba(255, 255, 255, 0.3);">
                        <h4 style="color: white;">📝 Manual Creation</h4>
                        <p style="color: white;">Custom question paper design</p>
                    </div>
                    """, unsafe_allow_html=True)
                with col3:
                    st.markdown("""
                    <div style="background: rgba(255, 255, 255, 0.15); border-radius: 15px; padding: 1rem; text-align: center; border: 1px solid rgba(255, 255, 255, 0.3);">
                        <h4 style="color: white;">📊 Pattern Analysis</h4>
                        <p style="color: white;">Smart exam pattern insights</p>
                    </div>
                    """, unsafe_allow_html=True)
        return
    # If authenticated, show the full dashboard
    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
    
    with col1:
        if st.session_state.current_user:
            st.markdown(f"### 👋 Welcome, {st.session_state.current_user['name']}")
            st.markdown(f"🏫 **Institution:** {st.session_state.current_user['institution']}")
    
    with col4:
        if st.button("🚪 Logout", type="secondary"):
            st.session_state.authenticated = False
            st.session_state.current_user = None
            st.rerun()
    
    # Initialize session state for navigation
    if 'show_auto_generation' not in st.session_state:
        st.session_state.show_auto_generation = False
    if 'show_manual_creation' not in st.session_state:
        st.session_state.show_manual_creation = False
    if 'show_pattern_analysis' not in st.session_state:
        st.session_state.show_pattern_analysis = False
    if 'show_admin' not in st.session_state:
        st.session_state.show_admin = False
    if 'show_super_admin' not in st.session_state:
        st.session_state.show_super_admin = False
    
    # Check which page to show
    if st.session_state.show_auto_generation:
        auto_generation_page()
        return
    elif st.session_state.show_manual_creation:
        manual_creation_page()
        return
    elif st.session_state.show_pattern_analysis:
        pattern_analysis_page()
        return
    elif st.session_state.show_admin:
        admin_dashboard()
        return
    elif st.session_state.show_super_admin:
        super_admin_dashboard()
        return
    
    # Main dashboard
    st.markdown("""
    # Welcome to QuestVibe!

    This intelligent system helps you create comprehensive question papers based on your syllabus topics.
    """)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("### 📚 Syllabus-Based")
        st.write("Generate questions from your specific syllabus topics")

    with col2:
        st.markdown("### 🤖 Auto Generation")
        st.write("Fully automated question paper creation with predefined topics")

    with col3:
        st.markdown("### 🎯 Multiple Types")
        st.write("Support for MCQ, Short Answer, Long Answer, and Case Study questions")

    with col4:
        st.markdown("### 📊 Smart Analysis")
        st.write("Get detailed analytics and visualizations with Bloom's taxonomy")

    st.markdown("---")
    st.markdown("### 🚀 Get Started")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 🤖 Auto Generation")
        st.write("Generate questions automatically from predefined syllabus topics")
        if st.button("Start Auto Generation", key="auto_btn", type="primary"):
            st.session_state.show_auto_generation = True
            st.rerun()

    with col2:
        st.markdown("### 📝 Manual Creation")
        st.write("Create questions manually by uploading or pasting syllabus")
        if st.button("Start Creating", key="create_btn"):
            st.session_state.show_manual_creation = True
            st.rerun()

    with col3:
        st.markdown("### 📊 Pattern Analysis")
        st.write("Analyze past papers to understand exam patterns")
        if st.button("Start Analysis", key="analyze_btn"):
            st.session_state.show_pattern_analysis = True
            st.rerun()

    st.markdown("---")
    st.markdown("### 📈 System Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Subjects Available", "5+", "📚")

    with col2:
        st.metric("Total Topics", "50+", "🎯")

    with col3:
        st.metric("Question Types", "4 Supported", "📝")

    with col4:
        st.metric("Bloom's Levels", "6 Levels", "🧠")

    st.markdown("---")
    
    # AI Database System Information
    st.markdown("### 🤖 AI Database System")
    st.write("QuestVibe uses an intelligent AI system that automatically populates the database with comprehensive engineering curriculum data.")
    
    # Show AI database statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_branches = len(st.session_state.questvibe_ai_db.engineering_subjects)
        st.metric("Engineering Branches", total_branches, "🏗️")
    
    with col2:
        total_subjects = sum(len(data["subjects"]) for data in st.session_state.questvibe_ai_db.engineering_subjects.values())
        st.metric("Total Subjects", total_subjects, "📚")
    
    with col3:
        total_topics = sum(len(topics) for branch_data in st.session_state.questvibe_ai_db.engineering_subjects.values() 
                          for topics in branch_data.get("exam_topics", {}).values())
        st.metric("Exam Topics", total_topics, "🎯")
    
    with col4:
        st.metric("AI Status", "Active", "🤖")
    
    # Show available branches
    st.markdown("**🏗️ Available Engineering Branches:**")
    branch_cols = st.columns(3)
    branches = list(st.session_state.questvibe_ai_db.engineering_subjects.keys())
    
    for i, branch in enumerate(branches):
        with branch_cols[i % 3]:
            st.markdown(f"• **{branch}**")
            subject_count = len(st.session_state.questvibe_ai_db.engineering_subjects[branch]["subjects"])
            st.write(f"  {subject_count} subjects")
    
    st.markdown("---")

    # Admin section
    if st.session_state.current_user and st.session_state.current_user.get('role') == 'admin':
        st.markdown("### 🔧 Admin Tools")
        if st.button("📊 View Database Analytics", type="secondary"):
            st.session_state.show_admin = True
            st.rerun()
    
    # Super Admin section (only for super_admin role)
    if st.session_state.current_user and st.session_state.current_user.get('role') == 'super_admin':
        st.markdown("### 🔓 Super Admin Tools")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📊 View Database Analytics", type="secondary"):
                st.session_state.show_admin = True
                st.rerun()
        with col2:
            if st.button("🔓 Full Database Access", type="primary"):
                st.session_state.show_super_admin = True
                st.rerun()
    
    st.markdown("---")
    st.markdown("""
    <div class="footer">
        <p>🤖 Powered by AI • 🚀 Fully Automated • 📊 Smart Analytics • 🧠 Bloom's Taxonomy</p>
    </div>
    """, unsafe_allow_html=True)

def auto_generation_page():
    st.markdown("## 🤖 Auto Question Generation")
    st.write("Generate questions automatically from AI-populated engineering subjects and topics")
    
    # Get engineering branches from AI database
    engineering_branches = list(st.session_state.questvibe_ai_db.engineering_subjects.keys())
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Select engineering branch
        selected_branch = st.selectbox("🏗️ Select Engineering Branch", engineering_branches)
        
        # Get subjects for selected branch
        subjects = st.session_state.questvibe_ai_db.get_subjects_by_branch(selected_branch)
        subject = st.selectbox("📚 Select Subject", subjects)
        
        num_questions = st.slider("📝 Number of Questions", 5, 50, 20)
    
    with col2:
        question_types = st.multiselect(
            "🎯 Question Types",
            ["MCQ", "Short Answer", "Long Answer", "Case Study"],
            default=["MCQ", "Short Answer"]
        )
        
        # Show available topics for selected subject
        if subject:
            topics = st.session_state.questvibe_ai_db.get_topics_by_subject(subject)
            if topics:
                st.markdown("**📖 Available Topics:**")
                for topic in topics[:5]:  # Show first 5 topics
                    st.write(f"• {topic}")
                if len(topics) > 5:
                    st.write(f"*... and {len(topics) - 5} more topics*")
    
    if st.button("🚀 Generate Questions", type="primary"):
        # Check if user is super admin
        is_super_admin = (hasattr(st.session_state, 'current_user') and 
                         st.session_state.current_user and 
                         st.session_state.current_user.get('role') == 'super_admin')
        
        # Show appropriate loading message
        if is_super_admin:
            with st.spinner("🤖 AI is generating intelligent questions using ChatGPT..."):
                # Log the generation activity to database
                if st.session_state.current_user:
                    log_question_generation(
                        st.session_state.current_user['id'],
                        subject,
                        num_questions,
                        question_types
                    )
                
                # Get topics from AI database
                topics = st.session_state.questvibe_ai_db.get_topics_by_subject(subject)
                if not topics:
                    # Fallback to hardcoded topics if none in database
                    topics = ["Introduction", "Basic Concepts", "Advanced Topics", "Applications", "Case Studies"]
                
                # Generate questions using ChatGPT
                questions = st.session_state.questvibe_chatgpt.generate_questions(
                    subject, topics, num_questions, question_types
                )
        else:
            # For normal users, show generic AI message
            with st.spinner("🤖 AI is generating intelligent questions..."):
                # Log the generation activity to database
                if st.session_state.current_user:
                    log_question_generation(
                        st.session_state.current_user['id'],
                        subject,
                        num_questions,
                        question_types
                    )
                
                # Get topics from AI database
                topics = st.session_state.questvibe_ai_db.get_topics_by_subject(subject)
                if not topics:
                    # Fallback to hardcoded topics if none in database
                    topics = ["Introduction", "Basic Concepts", "Advanced Topics", "Applications", "Case Studies"]
                
                # Generate questions using ChatGPT (with silent fallback for normal users)
                questions = st.session_state.questvibe_chatgpt.generate_questions(
                    subject, topics, num_questions, question_types
                )
        
        # Analyze question quality
        analysis = st.session_state.questvibe_chatgpt.analyze_question_quality(questions)
        
        # Show success message based on user role
        if is_super_admin:
            st.success(f"✅ Generated {len(questions)} intelligent questions using ChatGPT!")
        else:
            st.success(f"✅ Generated {len(questions)} intelligent questions!")
        
        st.info(f"🤖 AI used {len(topics)} topics from {selected_branch} - {subject}")
        
        # Show quality analysis
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Quality Score", f"{analysis['quality_score']}/100", "⭐")
        with col2:
            st.metric("Topics Covered", len(analysis['topic_coverage']), "🎯")
        with col3:
            st.metric("Question Types", len(analysis['type_distribution']), "📝")
        with col4:
            st.metric("Difficulty Levels", len(analysis['difficulty_distribution']), "📊")
        
        if st.session_state.current_user:
            st.info(f"📊 Activity logged for {st.session_state.current_user['name']} from {st.session_state.current_user['institution']}")
        
        # Display questions with enhanced formatting
        st.markdown("### 📋 Generated Questions")
        
        for i, q in enumerate(questions, 1):
            with st.expander(f"Question {i}: {q.get('type', 'Question')} - {q.get('difficulty', 'Medium')} Difficulty", expanded=True):
                st.markdown(f"**{q['question']}**")
                
                # Show question metadata
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"**Type:** {q.get('type', 'Unknown')}")
                with col2:
                    st.write(f"**Difficulty:** {q.get('difficulty', 'Medium')}")
                with col3:
                    st.write(f"**Bloom Level:** {q.get('bloom_level', 'Understand')}")
                
                # Show options for MCQ
                if q.get('type') == 'MCQ' and q.get('options'):
                    st.write("**Options:**")
                    for option in q['options']:
                        st.write(f"   {option}")
                    
                    if q.get('correct_answer'):
                        st.success(f"**Correct Answer:** {q.get('correct_answer')}")
                
                st.write(f"**Topic:** {q.get('topic', 'General')}")
                st.markdown("---")
    
    if st.button("🔙 Back to Dashboard"):
        st.session_state.show_auto_generation = False
        st.rerun()

def manual_creation_page():
    st.markdown("## 📝 Manual Question Creation")
    st.write("Create questions manually by uploading or pasting syllabus")
    
    tab1, tab2 = st.tabs(["📄 Upload Syllabus", "✏️ Paste Syllabus"])
    
    with tab1:
        uploaded_file = st.file_uploader("Choose a file", type=['txt', 'pdf', 'docx'])
        if uploaded_file is not None:
            st.success(f"✅ File uploaded: {uploaded_file.name}")
            st.write("File content will be processed here...")
    
    with tab2:
        syllabus_text = st.text_area("Paste your syllabus here:", height=200)
        if syllabus_text:
            st.write("Syllabus content will be processed here...")
    
    if st.button("🔙 Back to Dashboard"):
        st.session_state.show_manual_creation = False
        st.rerun()

def pattern_analysis_page():
    st.markdown("## 📊 Pattern Analysis")
    st.write("Analyze past papers to understand exam patterns")
    
    # Sample analytics data
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Papers", "25", "📄")
    
    with col2:
        st.metric("Avg Questions", "18", "❓")
    
    with col3:
        st.metric("MCQ %", "40%", "📊")
    
    with col4:
        st.metric("Difficulty", "Medium", "📈")
    
    # Sample chart
    st.markdown("### 📈 Question Type Distribution")
    data = pd.DataFrame({
        'Question Type': ['MCQ', 'Short Answer', 'Long Answer', 'Case Study'],
        'Count': [40, 30, 20, 10]
    })
    
    fig = px.pie(data, values='Count', names='Question Type', title='Question Type Distribution')
    st.plotly_chart(fig)
    
    if st.button("🔙 Back to Dashboard"):
        st.session_state.show_pattern_analysis = False
        st.rerun()

if __name__ == "__main__":
    main()
else:
    main() 
