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
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'show_question_creation' not in st.session_state:
    st.session_state.show_question_creation = False
if 'show_analysis' not in st.session_state:
    st.session_state.show_analysis = False
if 'show_auto_generation' not in st.session_state:
    st.session_state.show_auto_generation = False

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

# Question templates for different types
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
            
            st.success("✅ Question paper generated successfully!")
            
            # Display generated paper
            st.markdown("## 📄 Generated Question Paper")
            st.markdown(f"**{exam_title}**")
            st.markdown(f"**Subject:** {subject} | **Total Marks:** {analysis.get('total_marks', 0)} | **Duration:** {duration} minutes")
            st.markdown(f"**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
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

def main():
    # Check if we should show auto generation
    if st.session_state.show_auto_generation:
        auto_generation_page()
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
            st.info("Manual creation feature coming soon!")

    with col3:
        st.markdown("### 📊 Pattern Analysis")
        st.write("Analyze past papers to understand exam patterns")
        if st.button("Start Analysis", key="analyze_btn"):
            st.info("Pattern analysis feature coming soon!")

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