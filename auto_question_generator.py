import streamlit as st
import pandas as pd
import plotly.express as px
import random
import json
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Auto Question Generator",
    page_icon="🤖",
    layout="wide"
)

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

def generate_question(topic, question_type):
    """Generate a question for a given topic and type"""
    templates = QUESTION_TEMPLATES.get(question_type, [f"Describe {topic}."])
    template = random.choice(templates)
    question = template.format(topic=topic)
    
    # Assign marks based on question type
    marks_map = {
        "MCQ": 1,
        "Short Answer": 3,
        "Long Answer": 8,
        "Case Study": 10
    }
    
    marks = marks_map.get(question_type, 5)
    bloom_level = random.choice(BLOOM_LEVELS)
    
    return {
        'question': question,
        'type': question_type,
        'topic': topic,
        'marks': marks,
        'bloom_level': bloom_level
    }

def generate_question_paper(subject, num_questions, question_types, difficulty="Mixed"):
    """Generate a complete question paper"""
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
            question = generate_question(topic, qtype)
            questions.append(question)
    
    return questions

def analyze_questions(questions):
    """Analyze generated questions"""
    if not questions:
        return {}
    
    type_counts = {}
    topic_counts = {}
    bloom_counts = {}
    total_marks = 0
    
    for q in questions:
        qtype = q['type']
        topic = q['topic']
        bloom = q['bloom_level']
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

def main():
    st.markdown("""
    # 🤖 Auto Question Generator
    
    **Fully Automated Question Paper Generation System**
    
    This AI-powered system automatically generates comprehensive question papers from predefined syllabus topics.
    """)
    
    # Auto-generate configuration
    st.markdown("## ⚙️ Auto Configuration")
    
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
            questions = generate_question_paper(subject, total_questions, question_types, difficulty)
            
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
            
            # Analytics Dashboard
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
            
            # Export Options
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
    
    # Quick Stats
    st.markdown("---")
    st.markdown("### 🎯 System Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Subjects Available", len(SYLLABUS_TOPICS), "📚")
    
    with col2:
        total_topics = sum(len(topics) for topics in SYLLABUS_TOPICS.values())
        st.metric("Total Topics", total_topics, "🎯")
    
    with col3:
        st.metric("Question Types", 4, "📝")
    
    with col4:
        st.metric("Bloom's Levels", 6, "🧠")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>🤖 Powered by AI • 🚀 Fully Automated • 📊 Smart Analytics</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 