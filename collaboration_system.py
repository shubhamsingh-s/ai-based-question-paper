import streamlit as st
import json
import sqlite3
from datetime import datetime
from typing import Dict, List, Any

def init_collaboration_db():
    """Initialize database tables for the collaboration system."""
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    
    # Main session table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS collaboration_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_name TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Users in a session
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS session_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER,
            user_name TEXT NOT NULL,
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES collaboration_sessions (id)
        )
    ''')
    
    # Shared questions in a session
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS shared_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER,
            question_text TEXT NOT NULL,
            question_type TEXT,
            difficulty TEXT,
            topic TEXT,
            shared_by TEXT NOT NULL,
            likes INTEGER DEFAULT 0,
            shared_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES collaboration_sessions (id)
        )
    ''')
    
    # Comments on shared questions
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS question_comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_id INTEGER,
            comment_text TEXT NOT NULL,
            user_name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (question_id) REFERENCES shared_questions (id)
        )
    ''')
    conn.commit()
    conn.close()

# --- Database Functions ---

def get_or_create_session(session_name: str) -> int:
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM collaboration_sessions WHERE session_name = ?", (session_name,))
    session = cursor.fetchone()
    if session:
        session_id = session[0]
    else:
        cursor.execute("INSERT INTO collaboration_sessions (session_name) VALUES (?)", (session_name,))
        session_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return session_id

def add_user_to_session(session_id: int, user_name: str):
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO session_users (session_id, user_name) VALUES (?, ?)", (session_id, user_name))
    conn.commit()
    conn.close()

def get_active_users(session_id: int) -> List[Dict[str, Any]]:
    conn = sqlite3.connect('user_data.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT user_name, joined_at FROM session_users WHERE session_id = ? ORDER BY joined_at DESC", (session_id,))
    users = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return users

def share_question(session_id: int, question: Dict, shared_by: str):
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO shared_questions (session_id, question_text, question_type, difficulty, topic, shared_by) VALUES (?, ?, ?, ?, ?, ?)",
        (session_id, question['question'], question['type'], question['difficulty'], question['topic'], shared_by)
    )
    conn.commit()
    conn.close()

def get_shared_questions(session_id: int) -> List[Dict[str, Any]]:
    conn = sqlite3.connect('user_data.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM shared_questions WHERE session_id = ? ORDER BY shared_at DESC", (session_id,))
    questions = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return questions

def like_question(question_id: int):
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE shared_questions SET likes = likes + 1 WHERE id = ?", (question_id,))
    conn.commit()
    conn.close()

def add_comment(question_id: int, comment_text: str, user_name: str):
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO question_comments (question_id, comment_text, user_name) VALUES (?, ?, ?)", (question_id, comment_text, user_name))
    conn.commit()
    conn.close()

def get_comments(question_id: int) -> List[Dict[str, Any]]:
    conn = sqlite3.connect('user_data.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM question_comments WHERE question_id = ? ORDER BY created_at ASC", (question_id,))
    comments = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return comments

# --- Streamlit Dashboard ---

def collaboration_dashboard():
    """Real-time collaboration dashboard powered by a database."""
    st.markdown("## 🤝 Real-time Collaboration (DB-Powered)")
    st.write("Collaborate with other users. All data is persistent.")
    
    init_collaboration_db()

    # --- Session and User Setup ---
    st.markdown("### 📋 Session Management")
    session_name = st.text_input(
        "Session Name",
        value=st.session_state.get('collab_session_name', 'default-session'),
        help="Enter a session name to join or create."
    )
    user_name = st.text_input(
        "Your Name",
        value=st.session_state.get('current_user', {}).get('name', 'Anonymous'),
        help="Your display name in the session."
    )
    
    if st.button("🚀 Join or Create Session", type="primary"):
        st.session_state['collab_session_name'] = session_name
        st.session_state['collab_user_name'] = user_name
        session_id = get_or_create_session(session_name)
        st.session_state['collab_session_id'] = session_id
        # Add user to session if not already there for this session
        active_users = [u['user_name'] for u in get_active_users(session_id)]
        if user_name not in active_users:
            add_user_to_session(session_id, user_name)
        st.success(f"✅ Joined session: '{session_name}' as '{user_name}'")
        st.rerun()

    if 'collab_session_id' not in st.session_state:
        st.info("Please join a session to begin collaborating.")
        return

    session_id = st.session_state['collab_session_id']
    
    # --- Main Collaboration Area ---
    col1, col2 = st.columns([1, 2])

    with col1:
        # --- Active Users ---
        st.markdown("### 👥 Active Users")
        active_users_list = get_active_users(session_id)
        if active_users_list:
            for user in active_users_list:
                st.write(f"👤 {user['user_name']}")
        else:
            st.info("No active users yet.")
            
        # --- Share Question Form ---
        st.markdown("### 📤 Share a New Question")
        with st.form("share_question_form", clear_on_submit=True):
            question_text = st.text_area("Question Text")
            q_type = st.selectbox("Question Type", ["MCQ", "Short Answer", "Long Answer", "Case Study"])
            q_difficulty = st.select_slider("Difficulty", ["Easy", "Medium", "Hard"])
            q_topic = st.text_input("Topic")
            submitted = st.form_submit_button("Share Question")

            if submitted and question_text:
                new_question = {
                    'question': question_text,
                    'type': q_type,
                    'difficulty': q_difficulty,
                    'topic': q_topic
                }
                share_question(session_id, new_question, user_name)
                st.success("✅ Question shared!")
                st.rerun()

    with col2:
        # --- Shared Questions Feed ---
        st.markdown("### 📋 Shared Questions")
        shared_questions_list = get_shared_questions(session_id)
        if shared_questions_list:
            for q in shared_questions_list:
                with st.expander(f"Q by {q['shared_by']}: {q['question_text'][:50]}...", expanded=True):
                    st.markdown(f"**{q['question_text']}**")
                    st.caption(f"Type: {q['question_type']} | Difficulty: {q['difficulty']} | Topic: {q['topic']}")
                    
                    # --- Likes and Comments ---
                    like_col, comment_col = st.columns([1, 3])
                    with like_col:
                        if st.button(f"👍 Like ({q['likes']})", key=f"like_{q['id']}"):
                            like_question(q['id'])
                            st.rerun()
                    
                    st.markdown("---")
                    st.write("💬 **Comments**")
                    comments = get_comments(q['id'])
                    for comment in comments:
                        st.markdown(f"> **{comment['user_name']}**: {comment['comment_text']}")
                        st.caption(f"_{comment['created_at'][:16]}_")
                    
                    comment_text = st.text_input("Add a comment", key=f"comment_input_{q['id']}")
                    if st.button("Post Comment", key=f"comment_btn_{q['id']}"):
                        if comment_text:
                            add_comment(q['id'], comment_text, user_name)
                            st.rerun()
        else:
            st.info("No questions have been shared in this session yet.")

if __name__ == "__main__":
    collaboration_dashboard() 