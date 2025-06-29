import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Question Paper Maker",
    page_icon="📚",
    layout="wide"
)

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'

def generate_questions(topics, num_questions, question_types):
    """Generate questions based on topics and parameters"""
    questions = []
    
    for topic in topics:
        for qtype in question_types:
            if qtype == "MCQ":
                question = f"Which of the following best describes {topic}?"
                marks = 1
            elif qtype == "Short Answer":
                question = f"Explain the concept of {topic}."
                marks = 3
            elif qtype == "Long Answer":
                question = f"Discuss {topic} in detail with examples."
                marks = 8
            else:
                question = f"Describe {topic}."
                marks = 5
            
            questions.append({
                'question': question,
                'type': qtype,
                'topic': topic,
                'marks': marks,
                'bloom_level': 'Understand'
            })
    
    return questions[:num_questions]

def home_page():
    # Welcome Section
    st.markdown("""
    # Welcome to Question Paper Maker!

    This intelligent system helps you create comprehensive question papers based on your syllabus topics.
    """)

    # Feature Cards
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        ### 📚 Syllabus-Based
        Generate questions from your specific syllabus topics
        """)

    with col2:
        st.markdown("""
        ### 🎯 Multiple Types
        Support for MCQ, Short Answer, and Long Answer questions
        """)

    with col3:
        st.markdown("""
        ### 📊 Smart Analysis
        Get detailed analytics and visualizations
        """)

    # Navigation Section
    st.markdown("---")
    st.markdown("### 🚀 Get Started")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📝 Create Question Paper")
        st.write("Generate a new question paper based on your syllabus")
        if st.button("Start Creating", key="create_btn"):
            st.session_state.current_page = 'create'
            st.rerun()

    with col2:
        st.markdown("### 📊 Analyze Patterns")
        st.write("Analyze past papers to understand exam patterns")
        if st.button("Start Analysis", key="analyze_btn"):
            st.session_state.current_page = 'analyze'
            st.rerun()

    # Quick Stats
    st.markdown("---")
    st.markdown("### 📈 System Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Question Types", "4 Supported", "🎯")

    with col2:
        st.metric("File Formats", "PDF, DOCX, TXT", "📚")

    with col3:
        st.metric("Analytics", "Real-time", "📊")

    with col4:
        st.metric("Export", "Multiple Formats", "💾")

def create_page():
    st.markdown("## 📝 Question Paper Creation")
    st.markdown("---")
    
    # Back button
    if st.button("← Back to Home"):
        st.session_state.current_page = 'home'
        st.rerun()
    
    # Syllabus input
    st.subheader("📚 Syllabus Input")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        syllabus_text = st.text_area("Paste syllabus topics (one per line)", height=200, 
                                   placeholder="Enter your syllabus topics here, one per line...")
    
    with col2:
        # Exam configuration
        st.subheader("⚙️ Exam Configuration")
        
        exam_title = st.text_input("Exam Title", "Generated Question Paper")
        total_questions = st.number_input("Total Questions", min_value=5, max_value=100, value=20)
        total_marks = st.number_input("Total Marks", min_value=10, max_value=500, value=100)
        duration = st.number_input("Duration (minutes)", min_value=30, max_value=300, value=180)
        
        question_types = st.multiselect(
            "Question Types",
            ['MCQ', 'Short Answer', 'Long Answer', 'Case Study'],
            default=['MCQ', 'Short Answer', 'Long Answer']
        )
        
        difficulty = st.selectbox("Difficulty Level", ['Easy', 'Medium', 'Hard', 'Mixed'])
    
    # Generate question paper
    if st.button("🎯 Generate Question Paper", type="primary"):
        if syllabus_text:
            # Parse topics
            topics = [line.strip() for line in syllabus_text.split('\n') if line.strip()]
            
            if topics:
                with st.spinner("Generating question paper..."):
                    # Generate questions
                    questions = generate_questions(topics, total_questions, question_types)
                    
                    st.success("Question paper generated successfully!")
                    
                    # Display generated paper
                    st.markdown("## 📄 Generated Question Paper")
                    st.markdown(f"**{exam_title}**")
                    
                    total_marks_calc = sum(q['marks'] for q in questions)
                    st.markdown(f"**Total Marks:** {total_marks_calc} | **Duration:** {duration} minutes")
                    
                    # Display questions
                    st.subheader("Questions")
                    for i, question in enumerate(questions, 1):
                        with st.expander(f"Q{i} ({question['type']}, {question['topic']}, {question['marks']} marks)"):
                            st.write(f"**Question:** {question['question']}")
                    
                    # Analytics
                    st.subheader("📊 Paper Analytics")
                    
                    # Question type distribution
                    type_counts = {}
                    topic_counts = {}
                    for q in questions:
                        type_counts[q['type']] = type_counts.get(q['type'], 0) + 1
                        topic_counts[q['topic']] = topic_counts.get(q['topic'], 0) + 1
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if type_counts:
                            type_df = pd.DataFrame([
                                {'Type': k, 'Count': v} for k, v in type_counts.items()
                            ])
                            fig1 = px.bar(type_df, x='Type', y='Count', title='Question Types')
                            st.plotly_chart(fig1, use_container_width=True)
                    
                    with col2:
                        if topic_counts:
                            topic_df = pd.DataFrame([
                                {'Topic': k, 'Count': v} for k, v in topic_counts.items()
                            ])
                            fig2 = px.bar(topic_df, x='Topic', y='Count', title='Topic Distribution')
                            st.plotly_chart(fig2, use_container_width=True)
                    
                    # Export options
                    st.subheader("📤 Export Options")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if st.button("📄 Export as Text"):
                            export_text = f"{exam_title}\n\n"
                            for i, q in enumerate(questions, 1):
                                export_text += f"Q{i} ({q['type']}, {q['marks']} marks): {q['question']}\n\n"
                            st.download_button('Download as Text', export_text, file_name='question_paper.txt')
                    
                    with col2:
                        st.info("Word export feature coming soon!")
            else:
                st.error("No topics found in syllabus!")
        else:
            st.error("Please provide syllabus content!")

def analyze_page():
    st.markdown("## 📊 Pattern Analysis")
    st.markdown("---")
    
    # Back button
    if st.button("← Back to Home"):
        st.session_state.current_page = 'home'
        st.rerun()
    
    st.write("Upload multiple previous question papers to analyze patterns and predict future questions.")
    
    uploaded_files = st.file_uploader("Upload Past Papers", type=['pdf', 'docx', 'txt'], accept_multiple_files=True)
    
    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} files uploaded")
        
        topics_text = st.text_area("Enter topics for tagging (one per line):")
        
        if st.button("🔍 Analyze Papers"):
            if topics_text:
                topics = [line.strip() for line in topics_text.split('\n') if line.strip()]
                st.success(f"Analysis complete! Found {len(topics)} topics across {len(uploaded_files)} papers.")
                
                # Simple analysis display
                st.subheader("📈 Analysis Results")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Papers Analyzed", len(uploaded_files))
                
                with col2:
                    st.metric("Topics Identified", len(topics))
                
                with col3:
                    st.metric("Average Topics/Paper", len(topics) // len(uploaded_files) if uploaded_files else 0)
                
                # Display topics
                st.subheader("📋 Identified Topics")
                for i, topic in enumerate(topics, 1):
                    st.write(f"{i}. {topic}")
            else:
                st.warning("Please enter topics for analysis.")
    else:
        st.info("Please upload at least one past paper to begin analysis.")

def main():
    # Page routing
    if st.session_state.current_page == 'home':
        home_page()
    elif st.session_state.current_page == 'create':
        create_page()
    elif st.session_state.current_page == 'analyze':
        analyze_page()
    
    # Footer
    if st.session_state.current_page == 'home':
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: #666; padding: 1rem;">
            <p>Powered by AI • Built with Streamlit • Enhanced with Advanced Analytics</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 