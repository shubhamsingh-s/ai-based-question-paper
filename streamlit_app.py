"import streamlit as st" 

import streamlit as st
import pandas as pd
import plotly.express as px
import random
import json
from datetime import datetime
import re

# Page configuration
st.set_page_config(
    page_title="QuestVibe",
    page_icon="📚",
    layout="wide"
)

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
    color: #ffffff !important;
    backdrop-filter: blur(15px);
    font-weight: 500;
}
.stTextInput > div > div > input::placeholder {
    color: rgba(255, 255, 255, 0.8);
}
/* Make sure text is visible in all input fields */
input, textarea, select {
    color: #ffffff !important;
}
/* Ensure password field text is also visible */
input[type="password"] {
    color: #ffffff !important;
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
                    <h2 style="text-align: center; color: white; margin-bottom: 2rem;">🔐 Login</h2>
                </div>
                """, unsafe_allow_html=True)
                with st.form("login_form"):
                    username = st.text_input("👤 Username", placeholder="Enter your username")
                    password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
                    st.info("💡 Password characters are hidden for security - this is normal!")
                    col1, col2, col3 = st.columns(3)
                    with col2:
                        submit_button = st.form_submit_button("🚀 Login", type="primary", use_container_width=True)
                    if submit_button:
                        if username in USERS and USERS[username]["password"] == password:
                            st.session_state.authenticated = True
                            st.session_state.current_user = {
                                "username": username,
                                "role": USERS[username]["role"],
                                "name": USERS[username]["name"]
                            }
                            st.success(f"✅ Welcome back, {USERS[username]['name']}!")
                            st.rerun()
                        else:
                            st.error("❌ Invalid username or password!")
                with st.expander("🔑 Demo Credentials"):
                    st.markdown("""
                    **Try these demo accounts:**
                    
                    👨‍💼 **Admin Account:**
                    - Username: `admin`
                    - Password: `admin123`
                    
                    👨‍🏫 **Teacher Account:**
                    - Username: `teacher`
                    - Password: `teacher123`
                    
                    👨‍🎓 **Student Account:**
                    - Username: `student`
                    - Password: `student123`
                    
                    🎯 **Demo Account:**
                    - Username: `demo`
                    - Password: `demo123`
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
            user_role_emoji = {"admin": "👨‍💼", "teacher": "👨‍🏫", "student": "👨‍🎓"}.get(st.session_state.current_user["role"], "👤")
            st.markdown(f"### {user_role_emoji} Welcome, {st.session_state.current_user['name']} ({st.session_state.current_user['role'].title()})")
    
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
    st.markdown("""
    <div class="footer">
        <p>🤖 Powered by AI • 🚀 Fully Automated • 📊 Smart Analytics • 🧠 Bloom's Taxonomy</p>
    </div>
    """, unsafe_allow_html=True)

def auto_generation_page():
    st.markdown("## 🤖 Auto Question Generation")
    st.write("Generate questions automatically from predefined syllabus topics")
    
    # Sample syllabus topics
    SYLLABUS_TOPICS = {
        "Database Management System": [
            "Introduction to DBMS", "ER Model", "Relational Model", "SQL", "Normalization",
            "Transaction Management", "Concurrency Control", "Database Security"
        ],
        "Big Data Fundamentals": [
            "Introduction to Big Data", "Hadoop Ecosystem", "MapReduce", "HDFS",
            "NoSQL Databases", "Data Processing", "Big Data Analytics"
        ],
        "Computer Networks": [
            "Network Fundamentals", "OSI Model", "TCP/IP", "Network Protocols",
            "Network Security", "Wireless Networks", "Network Management"
        ]
    }
    
    col1, col2 = st.columns(2)
    
    with col1:
        subject = st.selectbox("📚 Select Subject", list(SYLLABUS_TOPICS.keys()))
        num_questions = st.slider("📝 Number of Questions", 5, 50, 20)
    
    with col2:
        question_types = st.multiselect(
            "🎯 Question Types",
            ["MCQ", "Short Answer", "Long Answer", "Case Study"],
            default=["MCQ", "Short Answer"]
        )
    
    if st.button("🚀 Generate Questions", type="primary"):
        with st.spinner("🤖 Generating questions..."):
            # Simulate question generation
            topics = SYLLABUS_TOPICS[subject]
            questions = []
            
            for i in range(num_questions):
                topic = random.choice(topics)
                q_type = random.choice(question_types)
                
                if q_type == "MCQ":
                    question = f"{i+1}. What is {topic}? (MCQ)"
                    options = [f"Option A", f"Option B", f"Option C", f"Option D"]
                    questions.append({"type": q_type, "question": question, "options": options})
                else:
                    question = f"{i+1}. Explain {topic} in detail. ({q_type})"
                    questions.append({"type": q_type, "question": question})
            
            st.success(f"✅ Generated {len(questions)} questions!")
            
            # Display questions
            st.markdown("### 📋 Generated Questions")
            for q in questions:
                if q["type"] == "MCQ":
                    st.write(f"**{q['question']}**")
                    for opt in q["options"]:
                        st.write(f"   {opt}")
                else:
                    st.write(f"**{q['question']}**")
                st.write("---")
    
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
