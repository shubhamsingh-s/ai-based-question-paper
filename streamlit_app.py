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
    # If authenticated, show a simple dashboard
    st.markdown(f"### 👋 Welcome, {st.session_state.current_user['name']} ({st.session_state.current_user['role'].title()})")
    st.write("You are now logged in! (Main app features go here.)")
    if st.button("🚪 Logout", type="secondary"):
        st.session_state.authenticated = False
        st.session_state.current_user = None
        st.rerun()

if __name__ == "__main__":
    main()
else:
    main() 
