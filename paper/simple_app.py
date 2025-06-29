import streamlit as st
import pandas as pd
import plotly.express as px
import os
import tempfile
import random
import json
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Question Paper Maker",
    page_icon="📚",
    layout="wide"
)

# Custom CSS for enhanced styling
st.markdown("""
<style>
/* Main styling */
.main {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
}

/* Header styling */
.main .block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Custom title styling */
h1 {
    background: linear-gradient(45deg, #FF6B6B, #4ECDC4, #45B7D1, #96CEB4);
    background-size: 300% 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: gradient 3s ease infinite;
    text-align: center;
    font-size: 3.5rem !important;
    font-weight: 800 !important;
    margin-bottom: 2rem !important;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
}

@keyframes gradient {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Subtitle styling */
h2 {
    color: #2c3e50 !important;
    font-weight: 600 !important;
    border-left: 4px solid #3498db;
    padding-left: 1rem;
    margin-top: 2rem !important;
}

h3 {
    color: #34495e !important;
    font-weight: 600 !important;
    margin-top: 1.5rem !important;
}

/* Card styling */
.stButton > button {
    background: linear-gradient(45deg, #667eea, #764ba2) !important;
    color: white !important;
    border: none !important;
    border-radius: 15px !important;
    padding: 0.75rem 2rem !important;
    font-weight: 600 !important;
    font-size: 1.1rem !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
    margin: 0.5rem 0 !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(0,0,0,0.3) !important;
    background: linear-gradient(45deg, #764ba2, #667eea) !important;
}

/* Primary button styling */
.stButton > button[data-baseweb="button"] {
    background: linear-gradient(45deg, #FF6B6B, #4ECDC4) !important;
    font-size: 1.2rem !important;
    padding: 1rem 2.5rem !important;
    border-radius: 25px !important;
}

.stButton > button[data-baseweb="button"]:hover {
    background: linear-gradient(45deg, #4ECDC4, #FF6B6B) !important;
    transform: translateY(-3px) !important;
    box-shadow: 0 8px 25px rgba(0,0,0,0.3) !important;
}

/* Feature cards styling */
div[data-testid="column"] {
    background: rgba(255, 255, 255, 0.95) !important;
    border-radius: 20px !important;
    padding: 2rem !important;
    margin: 1rem 0.5rem !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.1) !important;
    backdrop-filter: blur(10px) !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    transition: all 0.3s ease !important;
}

div[data-testid="column"]:hover {
    transform: translateY(-5px) !important;
    box-shadow: 0 12px 40px rgba(0,0,0,0.15) !important;
}

/* Metric styling */
div[data-testid="metric-container"] {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    border-radius: 15px !important;
    padding: 1.5rem !important;
    color: white !important;
    text-align: center !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
    margin: 0.5rem 0 !important;
}

/* Expander styling */
.streamlit-expanderHeader {
    background: linear-gradient(45deg, #f8f9fa, #e9ecef) !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    color: #2c3e50 !important;
    border: none !important;
    margin: 0.5rem 0 !important;
}

.streamlit-expanderContent {
    background: rgba(248, 249, 250, 0.8) !important;
    border-radius: 10px !important;
    padding: 1rem !important;
    margin-top: 0.5rem !important;
}

/* Selectbox styling */
.stSelectbox > div > div {
    background: white !important;
    border-radius: 10px !important;
    border: 2px solid #e9ecef !important;
}

/* Multiselect styling */
.stMultiSelect > div > div {
    background: white !important;
    border-radius: 10px !important;
    border: 2px solid #e9ecef !important;
}

/* Text input styling */
.stTextInput > div > div > input {
    border-radius: 10px !important;
    border: 2px solid #e9ecef !important;
}

/* Text area styling */
.stTextArea > div > div > textarea {
    border-radius: 10px !important;
    border: 2px solid #e9ecef !important;
}

/* Number input styling */
.stNumberInput > div > div > input {
    border-radius: 10px !important;
    border: 2px solid #e9ecef !important;
}

/* Slider styling */
.stSlider > div > div > div > div {
    background: linear-gradient(45deg, #667eea, #764ba2) !important;
}

/* File uploader styling */
.stFileUploader > div {
    border: 2px dashed #667eea !important;
    border-radius: 15px !important;
    background: rgba(102, 126, 234, 0.1) !important;
    padding: 2rem !important;
}

/* Success message styling */
.stSuccess {
    background: linear-gradient(45deg, #28a745, #20c997) !important;
    color: white !important;
    border-radius: 10px !important;
    padding: 1rem !important;
    border: none !important;
}

/* Error message styling */
.stError {
    background: linear-gradient(45deg, #dc3545, #fd7e14) !important;
    color: white !important;
    border-radius: 10px !important;
    padding: 1rem !important;
    border: none !important;
}

/* Info message styling */
.stInfo {
    background: linear-gradient(45deg, #17a2b8, #6f42c1) !important;
    color: white !important;
    border-radius: 10px !important;
    padding: 1rem !important;
    border: none !important;
}

/* Warning message styling */
.stWarning {
    background: linear-gradient(45deg, #ffc107, #fd7e14) !important;
    color: white !important;
    border-radius: 10px !important;
    padding: 1rem !important;
    border: none !important;
}

/* Download button styling */
.stDownloadButton > button {
    background: linear-gradient(45deg, #28a745, #20c997) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.75rem 1.5rem !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
}

.stDownloadButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(0,0,0,0.3) !important;
    background: linear-gradient(45deg, #20c997, #28a745) !important;
}

/* Footer styling */
.footer {
    background: linear-gradient(135deg, #2c3e50, #34495e) !important;
    color: white !important;
    text-align: center !important;
    padding: 2rem !important;
    border-radius: 20px !important;
    margin-top: 3rem !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.1) !important;
}

/* Chart container styling */
div[data-testid="stPlotlyChart"] {
    background: white !important;
    border-radius: 15px !important;
    padding: 1rem !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
    margin: 1rem 0 !important;
}

/* Divider styling */
hr {
    border: none !important;
    height: 3px !important;
    background: linear-gradient(45deg, #667eea, #764ba2) !important;
    border-radius: 2px !important;
    margin: 2rem 0 !important;
}

/* Custom scrollbar */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(45deg, #667eea, #764ba2);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(45deg, #764ba2, #667eea);
}

/* Animation for page load */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.main .block-container {
    animation: fadeInUp 0.8s ease-out;
}

/* Responsive design */
@media (max-width: 768px) {
    h1 {
        font-size: 2.5rem !important;
    }
    
    div[data-testid="column"] {
        margin: 0.5rem 0 !important;
    }
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'show_question_creation' not in st.session_state:
    st.session_state.show_question_creation = False
if 'show_analysis' not in st.session_state:
    st.session_state.show_analysis = False
if 'show_auto_generation' not in st.session_state:
    st.session_state.show_auto_generation = False
if 'show_admin_dashboard' not in st.session_state:
    st.session_state.show_admin_dashboard = False

# Initialize database session
if 'session_id' not in st.session_state:
    try:
        from database_manager import db_manager
        st.session_state.session_id = db_manager.create_session()
    except:
        st.session_state.session_id = "demo_session"

# Database logging function
def log_activity(generation_type, subject=None, exam_title=None, total_questions=None, 
                total_marks=None, duration=None, question_types=None, difficulty=None, 
                topics_used=None, questions=None, analysis=None):
    """Log user activity to database"""
    try:
        from database_manager import db_manager
        
        # Log generation request
        request_id = db_manager.log_generation_request(
            st.session_state.session_id, generation_type, subject, exam_title,
            total_questions, total_marks, duration, question_types, difficulty, topics_used
        )
        
        # Log generated questions
        if questions:
            db_manager.log_generated_questions(request_id, questions)
        
        # Log analytics
        if analysis:
            db_manager.log_analytics(request_id, analysis)
        
        # Update session activity
        db_manager.update_session_activity(st.session_state.session_id)
        
        return request_id
    except Exception as e:
        st.warning(f"Database logging failed: {e}")
        return None

# Predefined syllabus topics for different subjects
SYLLABUS_TOPICS = {
    "Database Management System": [
        "Database Design and ER Model",
        "Relational Algebra and SQL",
        "Normalization and Database Design",
        "Transaction Management",
        "Concurrency Control",
        "Database Security",
        "Distributed Databases",
        "Data Warehousing",
        "Big Data and NoSQL",
        "Database Administration"
    ],
    "Big Data Fundamentals": [
        "Introduction to Big Data",
        "Hadoop Ecosystem",
        "MapReduce Programming",
        "HDFS Architecture",
        "Spark Framework",
        "Data Processing Pipelines",
        "Machine Learning with Big Data",
        "Data Visualization",
        "Cloud Computing for Big Data",
        "Big Data Analytics"
    ],
    "Computer Networks": [
        "Network Architecture",
        "OSI Model and TCP/IP",
        "Network Protocols",
        "Routing Algorithms",
        "Network Security",
        "Wireless Networks",
        "Network Management",
        "Internet Technologies",
        "Network Performance",
        "Emerging Network Technologies"
    ],
    "Operating Systems": [
        "Process Management",
        "Memory Management",
        "File Systems",
        "CPU Scheduling",
        "Deadlock Prevention",
        "Virtual Memory",
        "Device Management",
        "System Security",
        "Distributed Systems",
        "Real-time Systems"
    ]
}

# Enhanced question templates for different types
QUESTION_TEMPLATES = {
    "MCQ": [
        "Which of the following best describes {topic}?",
        "What is the primary purpose of {topic}?",
        "Which statement is true about {topic}?",
        "In the context of {topic}, what does X represent?",
        "Which approach is most commonly used for {topic}?"
    ],
    "Short Answer": [
        "Explain the concept of {topic}.",
        "Describe the key components of {topic}.",
        "What are the main advantages of {topic}?",
        "How does {topic} work in practice?",
        "List the important features of {topic}."
    ],
    "Long Answer": [
        "Discuss {topic} in detail with examples and applications.",
        "Analyze the importance of {topic} in modern computing systems.",
        "Compare and contrast different approaches to {topic}.",
        "Explain the implementation and challenges of {topic}.",
        "Describe the evolution and future trends of {topic}."
    ],
    "Case Study": [
        "Consider a scenario where {topic} needs to be implemented. What would be your approach?",
        "Analyze a real-world problem that can be solved using {topic}.",
        "Design a solution using {topic} for a given business requirement.",
        "Evaluate the effectiveness of {topic} in a specific context.",
        "Propose improvements to an existing {topic} implementation."
    ]
}

# Bloom's taxonomy levels
BLOOM_LEVELS = ["Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"]

def generate_questions(topics, num_questions, question_types):
    """Generate questions based on topics and parameters"""
    questions = []
    
    for topic in topics:
        for qtype in question_types:
            if qtype == "MCQ":
                templates = QUESTION_TEMPLATES.get("MCQ", [f"Which of the following best describes {topic}?"])
                question = random.choice(templates).format(topic=topic)
                marks = 1
            elif qtype == "Short Answer":
                templates = QUESTION_TEMPLATES.get("Short Answer", [f"Explain the concept of {topic}."])
                question = random.choice(templates).format(topic=topic)
                marks = 3
            elif qtype == "Long Answer":
                templates = QUESTION_TEMPLATES.get("Long Answer", [f"Discuss {topic} in detail with examples."])
                question = random.choice(templates).format(topic=topic)
                marks = 8
            elif qtype == "Case Study":
                templates = QUESTION_TEMPLATES.get("Case Study", [f"Consider a scenario where {topic} needs to be implemented."])
                question = random.choice(templates).format(topic=topic)
                marks = 10
            else:
                question = f"Describe {topic}."
                marks = 5
            
            questions.append({
                'question': question,
                'type': qtype,
                'topic': topic,
                'marks': marks,
                'bloom_level': random.choice(BLOOM_LEVELS)
            })
    
    return questions[:num_questions]

def generate_auto_questions(subject, num_questions, question_types, difficulty="Mixed"):
    """Generate questions automatically from predefined syllabus"""
    topics = SYLLABUS_TOPICS.get(subject, [])
    if not topics:
        return []
    
    questions = []
    questions_per_type = num_questions // len(question_types)
    remaining = num_questions % len(question_types)
    
    for qtype in question_types:
        count = questions_per_type + (1 if remaining > 0 else 0)
        remaining -= 1
        
        # Select topics for this question type
        selected_topics = random.sample(topics, min(count, len(topics)))
        if count > len(topics):
            # If we need more questions than topics, repeat some topics
            additional_needed = count - len(topics)
            additional_topics = random.choices(topics, k=additional_needed)
            selected_topics.extend(additional_topics)
        
        for topic in selected_topics[:count]:
            question = generate_questions([topic], 1, [qtype])[0]
            questions.append(question)
    
    return questions

def analyze_questions(questions):
    """Analyze generated questions"""
    if not questions:
        return {}
    
    # Question type distribution
    type_counts = {}
    topic_counts = {}
    bloom_counts = {}
    total_marks = 0
    
    for q in questions:
        qtype = q['type']
        topic = q['topic']
        bloom = q.get('bloom_level', 'Understand')
        marks = q['marks']
        
        type_counts[qtype] = type_counts.get(qtype, 0) + 1
        topic_counts[topic] = topic_counts.get(topic, 0) + 1
        bloom_counts[bloom] = bloom_counts.get(bloom, 0) + 1
        total_marks += marks
    
    return {
        'type_counts': type_counts,
        'topic_counts': topic_counts,
        'bloom_counts': bloom_counts,
        'total_marks': total_marks,
        'total_questions': len(questions)
    }

def question_creation_page():
    st.markdown("## 📝 Question Paper Creation")
    st.markdown("---")
    
    # Syllabus input
    st.subheader("📚 Syllabus Input")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        syllabus_file = st.file_uploader("Upload Syllabus", type=['pdf', 'docx', 'txt'])
        syllabus_text = ""
        
        if syllabus_file:
            st.success(f"✅ File uploaded: {syllabus_file.name}")
            # For now, we'll use text input as fallback
            syllabus_text = st.text_area("Or paste syllabus topics (one per line)", height=200)
        else:
            syllabus_text = st.text_area("Paste syllabus topics (one per line)", height=200)
    
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
                    
                    # Analyze questions
                    analysis = analyze_questions(questions)
                    
                    # Log activity to database
                    request_id = log_activity(
                        generation_type="manual",
                        subject="Custom Syllabus",
                        exam_title=exam_title,
                        total_questions=total_questions,
                        total_marks=analysis.get('total_marks', 0),
                        duration=duration,
                        question_types=question_types,
                        difficulty=difficulty,
                        topics_used=topics,
                        questions=questions,
                        analysis=analysis
                    )
                    
                    st.success("Question paper generated successfully!")
                    
                    # Display generated paper
                    st.markdown("## 📄 Generated Question Paper")
                    st.markdown(f"**{exam_title}**")
                    st.markdown(f"**Total Marks:** {analysis.get('total_marks', 0)} | **Duration:** {duration} minutes")
                    
                    if request_id:
                        st.info(f"📊 Activity logged with ID: {request_id}")
                    
                    # Display questions
                    st.subheader("Questions")
                    for i, question in enumerate(questions, 1):
                        with st.expander(f"Q{i} ({question['type']}, {question['topic']}, {question['marks']} marks, {question['bloom_level']})"):
                            st.write(f"**Question:** {question['question']}")
                            st.write(f"**Bloom's Level:** {question['bloom_level']}")
                    
                    # Enhanced Analytics
                    st.subheader("📊 Paper Analytics")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if analysis.get('type_counts'):
                            type_df = pd.DataFrame([
                                {'Type': k, 'Count': v} for k, v in analysis['type_counts'].items()
                            ])
                            fig1 = px.pie(type_df, values='Count', names='Type', title='Question Type Distribution')
                            st.plotly_chart(fig1, use_container_width=True)
                        
                        if analysis.get('bloom_counts'):
                            bloom_df = pd.DataFrame([
                                {'Level': k, 'Count': v} for k, v in analysis['bloom_counts'].items()
                            ])
                            fig3 = px.bar(bloom_df, x='Level', y='Count', title="Bloom's Taxonomy Distribution")
                            st.plotly_chart(fig3, use_container_width=True)
                    
                    with col2:
                        if analysis.get('topic_counts'):
                            topic_df = pd.DataFrame([
                                {'Topic': k, 'Count': v} for k, v in analysis['topic_counts'].items()
                            ])
                            fig2 = px.bar(topic_df, x='Topic', y='Count', title='Topic Distribution')
                            fig2.update_xaxes(tickangle=45)
                            st.plotly_chart(fig2, use_container_width=True)
                        
                        # Summary Statistics
                        st.markdown("### 📈 Summary Statistics")
                        col_a, col_b = st.columns(2)
                        with col_a:
                            st.metric("Total Questions", analysis.get('total_questions', 0))
                            st.metric("Total Marks", analysis.get('total_marks', 0))
                        with col_b:
                            st.metric("Question Types", len(analysis.get('type_counts', {})))
                            st.metric("Topics Covered", len(analysis.get('topic_counts', {})))
                    
                    # Enhanced Export Options
                    st.subheader("📤 Export Options")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        # Export as Text
                        export_text = f"{exam_title}\n"
                        export_text += f"Total Marks: {analysis.get('total_marks', 0)}\n"
                        export_text += f"Duration: {duration} minutes\n"
                        export_text += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                        
                        for i, q in enumerate(questions, 1):
                            export_text += f"Q{i} ({q['type']}, {q['marks']} marks, {q['bloom_level']}): {q['question']}\n\n"
                        
                        st.download_button(
                            '📄 Download as Text',
                            export_text,
                            file_name='question_paper.txt',
                            mime='text/plain'
                        )
                    
                    with col2:
                        # Export as JSON
                        export_data = {
                            'exam_title': exam_title,
                            'total_marks': analysis.get('total_marks', 0),
                            'duration': duration,
                            'generated_at': datetime.now().isoformat(),
                            'questions': questions,
                            'analysis': analysis
                        }
                        
                        st.download_button(
                            '📊 Download as JSON',
                            json.dumps(export_data, indent=2),
                            file_name='question_paper.json',
                            mime='application/json'
                        )
                    
                    with col3:
                        # Export as CSV
                        questions_df = pd.DataFrame(questions)
                        csv_data = questions_df.to_csv(index=False)
                        
                        st.download_button(
                            '📋 Download as CSV',
                            csv_data,
                            file_name='questions.csv',
                            mime='text/csv'
                        )
            else:
                st.error("No topics found in syllabus!")
        else:
            st.error("Please provide syllabus content!")
    
    # Back button
    if st.button("← Back to Home"):
        st.session_state.show_question_creation = False
        st.rerun()

def analysis_page():
    st.markdown("## 📊 Pattern Analysis")
    st.markdown("---")
    
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
    
    # Back button
    if st.button("← Back to Home"):
        st.session_state.show_analysis = False
        st.rerun()

def auto_generation_page():
    st.markdown("## 🤖 Auto Question Generation")
    st.markdown("---")
    st.markdown("**Fully Automated Question Paper Generation System**")
    
    # Auto-generate configuration
    st.markdown("### ⚙️ Auto Configuration")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        subject = st.selectbox(
            "Select Subject",
            list(SYLLABUS_TOPICS.keys()),
            index=0
        )
        
        # Show available topics
        topics = SYLLABUS_TOPICS[subject]
        st.markdown(f"**Available Topics:** {len(topics)}")
        with st.expander("View Topics"):
            for i, topic in enumerate(topics, 1):
                st.write(f"{i}. {topic}")
    
    with col2:
        total_questions = st.slider("Total Questions", 10, 50, 25)
        question_types = st.multiselect(
            "Question Types",
            ['MCQ', 'Short Answer', 'Long Answer', 'Case Study'],
            default=['MCQ', 'Short Answer', 'Long Answer']
        )
    
    with col3:
        difficulty = st.selectbox("Difficulty Level", ['Easy', 'Medium', 'Hard', 'Mixed'])
        exam_title = st.text_input("Exam Title", f"{subject} - Auto Generated Paper")
        duration = st.number_input("Duration (minutes)", 60, 300, 180)
    
    # Auto-generate button
    if st.button("🚀 Generate Question Paper Automatically", type="primary"):
        if not question_types:
            st.error("Please select at least one question type!")
            return
        
        with st.spinner("🤖 AI is generating your question paper..."):
            # Generate questions
            questions = generate_auto_questions(subject, total_questions, question_types, difficulty)
            
            # Analyze questions
            analysis = analyze_questions(questions)
            
            # Log activity to database
            request_id = log_activity(
                generation_type="auto",
                subject=subject,
                exam_title=exam_title,
                total_questions=total_questions,
                total_marks=analysis.get('total_marks', 0),
                duration=duration,
                question_types=question_types,
                difficulty=difficulty,
                topics_used=list(analysis.get('topic_counts', {}).keys()),
                questions=questions,
                analysis=analysis
            )
            
            st.success("✅ Question paper generated successfully!")
            
            # Display generated paper
            st.markdown("## 📄 Generated Question Paper")
            st.markdown(f"**{exam_title}**")
            st.markdown(f"**Subject:** {subject} | **Total Marks:** {analysis.get('total_marks', 0)} | **Duration:** {duration} minutes")
            st.markdown(f"**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            if request_id:
                st.info(f"📊 Activity logged with ID: {request_id}")
            
            # Display questions
            st.subheader("📝 Questions")
            for i, question in enumerate(questions, 1):
                with st.expander(f"Q{i} ({question['type']}, {question['topic']}, {question['marks']} marks, {question['bloom_level']})"):
                    st.write(f"**Question:** {question['question']}")
                    st.write(f"**Bloom's Level:** {question['bloom_level']}")
            
            # Enhanced Analytics Dashboard
            st.subheader("📊 Comprehensive Analytics")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Question Type Distribution
                if analysis.get('type_counts'):
                    type_df = pd.DataFrame([
                        {'Type': k, 'Count': v} for k, v in analysis['type_counts'].items()
                    ])
                    fig1 = px.pie(type_df, values='Count', names='Type', title='Question Type Distribution')
                    st.plotly_chart(fig1, use_container_width=True)
                
                # Bloom's Taxonomy Distribution
                if analysis.get('bloom_counts'):
                    bloom_df = pd.DataFrame([
                        {'Level': k, 'Count': v} for k, v in analysis['bloom_counts'].items()
                    ])
                    fig3 = px.bar(bloom_df, x='Level', y='Count', title="Bloom's Taxonomy Distribution")
                    st.plotly_chart(fig3, use_container_width=True)
            
            with col2:
                # Topic Distribution
                if analysis.get('topic_counts'):
                    topic_df = pd.DataFrame([
                        {'Topic': k, 'Count': v} for k, v in analysis['topic_counts'].items()
                    ])
                    fig2 = px.bar(topic_df, x='Topic', y='Count', title='Topic Distribution')
                    fig2.update_xaxes(tickangle=45)
                    st.plotly_chart(fig2, use_container_width=True)
                
                # Summary Statistics
                st.markdown("### 📈 Summary Statistics")
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("Total Questions", analysis.get('total_questions', 0))
                    st.metric("Total Marks", analysis.get('total_marks', 0))
                with col_b:
                    st.metric("Question Types", len(analysis.get('type_counts', {})))
                    st.metric("Topics Covered", len(analysis.get('topic_counts', {})))
            
            # Enhanced Export Options
            st.subheader("📤 Export Options")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                # Export as Text
                export_text = f"{exam_title}\n"
                export_text += f"Subject: {subject}\n"
                export_text += f"Total Marks: {analysis.get('total_marks', 0)}\n"
                export_text += f"Duration: {duration} minutes\n"
                export_text += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                
                for i, q in enumerate(questions, 1):
                    export_text += f"Q{i} ({q['type']}, {q['marks']} marks, {q['bloom_level']}): {q['question']}\n\n"
                
                st.download_button(
                    '📄 Download as Text',
                    export_text,
                    file_name=f'{subject}_question_paper.txt',
                    mime='text/plain'
                )
            
            with col2:
                # Export as JSON
                export_data = {
                    'exam_title': exam_title,
                    'subject': subject,
                    'total_marks': analysis.get('total_marks', 0),
                    'duration': duration,
                    'generated_at': datetime.now().isoformat(),
                    'questions': questions,
                    'analysis': analysis
                }
                
                st.download_button(
                    '📊 Download as JSON',
                    json.dumps(export_data, indent=2),
                    file_name=f'{subject}_question_paper.json',
                    mime='application/json'
                )
            
            with col3:
                # Export as CSV
                questions_df = pd.DataFrame(questions)
                csv_data = questions_df.to_csv(index=False)
                
                st.download_button(
                    '📋 Download as CSV',
                    csv_data,
                    file_name=f'{subject}_questions.csv',
                    mime='text/csv'
                )
    
    # Back button
    if st.button("← Back to Home"):
        st.session_state.show_auto_generation = False
        st.rerun()

def admin_dashboard_page():
    """Admin dashboard page"""
    st.markdown("## 📊 Admin Dashboard")
    st.markdown("---")
    
    try:
        from database_manager import db_manager
        
        # Get analytics summary
        summary = db_manager.get_analytics_summary()
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("👥 Total Sessions", summary['total_sessions'])
        
        with col2:
            st.metric("📝 Total Requests", summary['total_requests'])
        
        with col3:
            st.metric("❓ Questions Generated", summary['total_questions'])
        
        with col4:
            avg_questions = summary['total_questions'] / max(summary['total_requests'], 1)
            st.metric("📊 Avg Questions/Request", f"{avg_questions:.1f}")
        
        # Recent requests
        st.markdown("### 📋 Recent Activity")
        recent_requests = db_manager.get_recent_requests(10)
        
        if recent_requests:
            df = pd.DataFrame(recent_requests, columns=[
                'ID', 'Type', 'Subject', 'Title', 'Questions', 'Marks', 'Created', 'IP'
            ])
            df['Created'] = pd.to_datetime(df['Created']).dt.strftime('%Y-%m-%d %H:%M')
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No recent activity found.")
        
        # Popular subjects
        if summary['popular_subjects']:
            st.markdown("### 📚 Popular Subjects")
            subjects_df = pd.DataFrame(summary['popular_subjects'], columns=['Subject', 'Count'])
            fig = px.bar(subjects_df, x='Subject', y='Count', title='Most Requested Subjects')
            st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error loading admin dashboard: {e}")
        st.info("Please ensure the database is properly initialized.")
    
    # Back button
    if st.button("← Back to Home"):
        st.session_state.show_admin_dashboard = False
        st.rerun()

def main():
    # Check if we should show question creation or analysis
    if st.session_state.show_question_creation:
        question_creation_page()
        return
    
    if st.session_state.show_analysis:
        analysis_page()
        return
    
    if st.session_state.show_auto_generation:
        auto_generation_page()
        return
    
    if st.session_state.show_admin_dashboard:
        admin_dashboard_page()
        return
    
    # Welcome Section
    st.markdown("""
    # Welcome to Question Paper Maker!

    This intelligent system helps you create comprehensive question papers based on your syllabus topics.
    """)

    # Feature Cards
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        ### 📚 Syllabus-Based
        Generate questions from your specific syllabus topics
        """)

    with col2:
        st.markdown("""
        ### 🤖 Auto Generation
        Fully automated question paper creation with predefined topics
        """)

    with col3:
        st.markdown("""
        ### 🎯 Multiple Types
        Support for MCQ, Short Answer, Long Answer, and Case Study questions
        """)

    with col4:
        st.markdown("""
        ### 📊 Smart Analysis
        Get detailed analytics and visualizations with Bloom's taxonomy
        """)

    # Navigation Section
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
            st.session_state.show_question_creation = True
            st.rerun()

    with col3:
        st.markdown("### 📊 Pattern Analysis")
        st.write("Analyze past papers to understand exam patterns")
        if st.button("Start Analysis", key="analyze_btn"):
            st.session_state.show_analysis = True
            st.rerun()

    # Admin Dashboard Section
    st.markdown("---")
    st.markdown("### 🔧 Admin Access")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        st.markdown("### 📊 Admin Dashboard")
        st.write("View analytics, user activity, and system insights")
        if st.button("Open Admin Dashboard", key="admin_btn"):
            st.session_state.show_admin_dashboard = True
            st.rerun()

    # Quick Stats
    st.markdown("---")
    st.markdown("### 📈 System Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Subjects Available", len(SYLLABUS_TOPICS), "📚")

    with col2:
        total_topics = sum(len(topics) for topics in SYLLABUS_TOPICS.values())
        st.metric("Total Topics", total_topics, "🎯")

    with col3:
        st.metric("Question Types", "4 Supported", "📝")

    with col4:
        st.metric("Bloom's Levels", "6 Levels", "🧠")

    # Footer
    st.markdown("---")
    st.markdown("""
    <div class="footer">
        <p>🤖 Powered by AI • 🚀 Fully Automated • 📊 Smart Analytics • 🧠 Bloom's Taxonomy</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 