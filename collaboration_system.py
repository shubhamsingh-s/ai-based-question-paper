import streamlit as st
import json
import time
from datetime import datetime
from typing import Dict, List, Any
import threading
import queue

class CollaborationSystem:
    """Real-time collaboration system for QuestVibe"""
    
    def __init__(self):
        self.active_users = {}
        self.shared_questions = {}
        self.comments = {}
        self.collaboration_history = {}
    
    def add_user_to_session(self, user_id: str, user_name: str, session_id: str):
        """Add user to collaboration session"""
        if session_id not in self.active_users:
            self.active_users[session_id] = {}
        
        self.active_users[session_id][user_id] = {
            'name': user_name,
            'joined_at': datetime.now().isoformat(),
            'last_activity': datetime.now().isoformat()
        }
        
        self.log_activity(session_id, f"{user_name} joined the session")
    
    def remove_user_from_session(self, user_id: str, session_id: str):
        """Remove user from collaboration session"""
        if session_id in self.active_users and user_id in self.active_users[session_id]:
            user_name = self.active_users[session_id][user_id]['name']
            del self.active_users[session_id][user_id]
            self.log_activity(session_id, f"{user_name} left the session")
    
    def share_question(self, session_id: str, question: Dict, shared_by: str):
        """Share a question in collaboration session"""
        if session_id not in self.shared_questions:
            self.shared_questions[session_id] = []
        
        shared_question = {
            'question': question,
            'shared_by': shared_by,
            'shared_at': datetime.now().isoformat(),
            'likes': 0,
            'comments': []
        }
        
        self.shared_questions[session_id].append(shared_question)
        self.log_activity(session_id, f"{shared_by} shared a question")
    
    def add_comment(self, session_id: str, question_index: int, comment: str, user_name: str):
        """Add comment to shared question"""
        if session_id in self.shared_questions and question_index < len(self.shared_questions[session_id]):
            comment_data = {
                'text': comment,
                'user': user_name,
                'timestamp': datetime.now().isoformat()
            }
            
            self.shared_questions[session_id][question_index]['comments'].append(comment_data)
            self.log_activity(session_id, f"{user_name} commented on a question")
    
    def like_question(self, session_id: str, question_index: int):
        """Like a shared question"""
        if session_id in self.shared_questions and question_index < len(self.shared_questions[session_id]):
            self.shared_questions[session_id][question_index]['likes'] += 1
    
    def log_activity(self, session_id: str, activity: str):
        """Log collaboration activity"""
        if session_id not in self.collaboration_history:
            self.collaboration_history[session_id] = []
        
        self.collaboration_history[session_id].append({
            'activity': activity,
            'timestamp': datetime.now().isoformat()
        })
    
    def get_session_data(self, session_id: str) -> Dict[str, Any]:
        """Get current session data"""
        return {
            'active_users': self.active_users.get(session_id, {}),
            'shared_questions': self.shared_questions.get(session_id, []),
            'history': self.collaboration_history.get(session_id, [])
        }

# Global collaboration system
collab_system = CollaborationSystem()

def collaboration_dashboard():
    """Real-time collaboration dashboard"""
    st.markdown("## 🤝 Real-time Collaboration")
    st.write("Collaborate with other users in real-time")
    
    # Session management
    st.markdown("### 📋 Session Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        session_id = st.text_input(
            "Session ID",
            value="questvibe_session_001",
            help="Enter or create a session ID"
        )
        
        user_name = st.text_input(
            "Your Name",
            value=st.session_state.get('current_user', {}).get('name', 'Anonymous'),
            help="Your display name in the session"
        )
    
    with col2:
        if st.button("🟢 Join Session", type="primary"):
            user_id = f"user_{int(time.time())}"
            collab_system.add_user_to_session(user_id, user_name, session_id)
            st.session_state['collab_user_id'] = user_id
            st.session_state['collab_session_id'] = session_id
            st.success(f"✅ Joined session: {session_id}")
        
        if st.button("🔴 Leave Session"):
            if 'collab_user_id' in st.session_state:
                collab_system.remove_user_from_session(
                    st.session_state['collab_user_id'], 
                    session_id
                )
                del st.session_state['collab_user_id']
                st.success("✅ Left session")
    
    # Active users
    if session_id in collab_system.active_users:
        st.markdown("### 👥 Active Users")
        
        users = collab_system.active_users[session_id]
        if users:
            for user_id, user_data in users.items():
                st.write(f"👤 {user_data['name']} (joined: {user_data['joined_at'][:19]})")
        else:
            st.info("No active users in this session")
    
    # Share questions
    st.markdown("### 📤 Share Questions")
    
    sample_question = {
        'question': 'What is the difference between SQL and NoSQL databases?',
        'type': 'Short Answer',
        'difficulty': 'Medium',
        'topic': 'Database Systems'
    }
    
    if st.button("📤 Share Sample Question"):
        if 'collab_user_id' in st.session_state:
            collab_system.share_question(
                session_id, 
                sample_question, 
                user_name
            )
            st.success("✅ Question shared!")
        else:
            st.error("❌ Please join a session first")
    
    # Shared questions
    st.markdown("### 📋 Shared Questions")
    
    if session_id in collab_system.shared_questions:
        questions = collab_system.shared_questions[session_id]
        
        if questions:
            for i, shared_q in enumerate(questions):
                with st.expander(f"Question {i+1} by {shared_q['shared_by']}", expanded=True):
                    q = shared_q['question']
                    
                    st.markdown(f"**{q['question']}**")
                    st.write(f"Type: {q['type']} | Difficulty: {q['difficulty']} | Topic: {q['topic']}")
                    
                    # Like button
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        if st.button(f"👍 Like ({shared_q['likes']})", key=f"like_{i}"):
                            collab_system.like_question(session_id, i)
                            st.rerun()
                    
                    # Comments
                    st.markdown("#### 💬 Comments")
                    
                    for comment in shared_q['comments']:
                        st.write(f"**{comment['user']}**: {comment['text']}")
                        st.caption(f"Posted: {comment['timestamp'][:19]}")
                    
                    # Add comment
                    new_comment = st.text_input(
                        "Add a comment",
                        key=f"comment_{i}",
                        placeholder="Type your comment here..."
                    )
                    
                    if st.button("💬 Post Comment", key=f"post_{i}"):
                        if new_comment:
                            collab_system.add_comment(session_id, i, new_comment, user_name)
                            st.success("✅ Comment posted!")
                            st.rerun()
        else:
            st.info("No questions shared yet")
    
    # Activity feed
    st.markdown("### 📊 Activity Feed")
    
    if session_id in collab_system.collaboration_history:
        activities = collab_system.collaboration_history[session_id]
        
        if activities:
            for activity in activities[-10:]:  # Show last 10 activities
                st.write(f"🕒 {activity['timestamp'][:19]} - {activity['activity']}")
        else:
            st.info("No activity yet")
    
    # Export collaboration data
    st.markdown("### 📤 Export Collaboration Data")
    
    if st.button("📊 Export Session Data"):
        session_data = collab_system.get_session_data(session_id)
        
        st.download_button(
            label="📥 Download Session Data (JSON)",
            data=json.dumps(session_data, indent=2),
            file_name=f"collaboration_session_{session_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )

if __name__ == "__main__":
    collaboration_dashboard() 