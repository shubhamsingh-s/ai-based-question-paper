import streamlit as st
import pandas as pd
import plotly.express as px
import random
import json
from datetime import datetime
import re

# Page configuration
st.set_page_config(
    page_title="Question Paper Maker",
    page_icon="📚",
    layout="wide"
)

# Custom CSS for enhanced styling
st.markdown("""
<style>
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
}

@keyframes gradient {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.stButton > button {
    background: linear-gradient(45deg, #667eea, #764ba2) !important;
    color: white !important;
    border: none !important;
    border-radius: 15px !important;
    padding: 0.75rem 2rem !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(0,0,0,0.3) !important;
}

.stButton > button[data-baseweb="button"] {
    background: linear-gradient(45deg, #FF6B6B, #4ECDC4) !important;
    font-size: 1.2rem !important;
    padding: 1rem 2.5rem !important;
    border-radius: 25px !important;
}

div[data-testid="column"] {
    background: rgba(255, 255, 255, 0.95) !important;
    border-radius: 20px !important;
    padding: 2rem !important;
    margin: 1rem 0.5rem !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.1) !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    transition: all 0.3s ease !important;
}

div[data-testid="column"]:hover {
    transform: translateY(-5px) !important;
    box-shadow: 0 12px 40px rgba(0,0,0,0.15) !important;
}

div[data-testid="metric-container"] {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    border-radius: 15px !important;
    padding: 1.5rem !important;
    color: white !important;
    text-align: center !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
    margin: 0.5rem 0 !important;
}

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
if 'show_auto_generation' not in st.session_state:
    st.session_state.show_auto_generation = False
if 'show_manual_creation' not in st.session_state:
    st.session_state.show_manual_creation = False
if 'show_pattern_analysis' not in st.session_state:
    st.session_state.show_pattern_analysis = False

# Predefined syllabus topics
SYLLABUS_TOPICS = {
    "Database Management System": [
        "Database Design and ER Model", "Relational Algebra and SQL", "Normalization and Database Design",
        "Transaction Management", "Concurrency Control", "Database Security", "Distributed Databases",
        "Data Warehousing", "Big Data and NoSQL", "Database Administration"
    ],
    "Big Data Fundamentals": [
        "Introduction to Big Data", "Hadoop Ecosystem", "MapReduce Programming", "HDFS Architecture",
        "Spark Framework", "Data Processing Pipelines", "Machine Learning with Big Data", "Data Visualization",
        "Cloud Computing for Big Data", "Big Data Analytics"
    ],
    "Computer Networks": [
        "Network Architecture", "OSI Model and TCP/IP", "Network Protocols", "Routing Algorithms",
        "Network Security", "Wireless Networks", "Network Management", "Internet Technologies",
        "Network Performance", "Emerging Network Technologies"
    ],
    "Operating Systems": [
        "Process Management", "Memory Management", "File Systems", "CPU Scheduling", "Deadlock Prevention",
        "Virtual Memory", "Device Management", "System Security", "Distributed Systems", "Real-time Systems"
    ]
}

# Question templates
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

BLOOM_LEVELS = ["Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"]

# Sample past papers for pattern analysis
SAMPLE_PAST_PAPERS = {
    "Database Management System": [
        {
            "year": "2023",
            "questions": [
                {"type": "MCQ", "topic": "ER Model", "marks": 1, "bloom": "Remember"},
                {"type": "MCQ", "topic": "SQL", "marks": 1, "bloom": "Understand"},
                {"type": "Short Answer", "topic": "Normalization", "marks": 3, "bloom": "Apply"},
                {"type": "Long Answer", "topic": "Transaction Management", "marks": 8, "bloom": "Analyze"},
                {"type": "Case Study", "topic": "Database Design", "marks": 10, "bloom": "Evaluate"}
            ]
        },
        {
            "year": "2022",
            "questions": [
                {"type": "MCQ", "topic": "Database Security", "marks": 1, "bloom": "Remember"},
                {"type": "MCQ", "topic": "Indexing", "marks": 1, "bloom": "Understand"},
                {"type": "Short Answer", "topic": "ACID Properties", "marks": 3, "bloom": "Apply"},
                {"type": "Long Answer", "topic": "Concurrency Control", "marks": 8, "bloom": "Analyze"},
                {"type": "Case Study", "topic": "Data Warehousing", "marks": 10, "bloom": "Evaluate"}
            ]
        }
    ],
    "Big Data Fundamentals": [
        {
            "year": "2023",
            "questions": [
                {"type": "MCQ", "topic": "Hadoop", "marks": 1, "bloom": "Remember"},
                {"type": "MCQ", "topic": "MapReduce", "marks": 1, "bloom": "Understand"},
                {"type": "Short Answer", "topic": "HDFS", "marks": 3, "bloom": "Apply"},
                {"type": "Long Answer", "topic": "Spark Framework", "marks": 8, "bloom": "Analyze"},
                {"type": "Case Study", "topic": "Big Data Analytics", "marks": 10, "bloom": "Evaluate"}
            ]
        }
    ]
}

def extract_topics_from_text(text):
    """Extract potential topics from uploaded/pasted text"""
    # Simple topic extraction - look for capitalized phrases
    lines = text.split('\n')
    topics = []
    
    for line in lines:
        line = line.strip()
        if len(line) > 10 and line[0].isupper():
            # Remove common words and punctuation
            clean_line = re.sub(r'[^\w\s]', '', line)
            if len(clean_line.split()) >= 2:
                topics.append(line)
    
    return topics[:20]  # Limit to 20 topics

def generate_questions_from_topics(topics, num_questions, question_types):
    """Generate questions from custom topics"""
    if not topics:
        return []
    
    questions = []
    questions_per_type = num_questions // len(question_types)
    remaining = num_questions % len(question_types)
    
    for qtype in question_types:
        count = questions_per_type + (1 if remaining > 0 else 0)
        remaining -= 1
        
        selected_topics = random.sample(topics, min(count, len(topics)))
        if count > len(topics):
            additional_needed = count - len(topics)
            additional_topics = random.choices(topics, k=additional_needed)
            selected_topics.extend(additional_topics)
        
        for topic in selected_topics[:count]:
            templates = QUESTION_TEMPLATES.get(qtype, [f"Describe {topic}."])
            question_text = random.choice(templates).format(topic=topic)
            
            marks_map = {"MCQ": 1, "Short Answer": 3, "Long Answer": 8, "Case Study": 10}
            marks = marks_map.get(qtype, 5)
            
            questions.append({
                'question': question_text,
                'type': qtype,
                'topic': topic,
                'marks': marks,
                'bloom_level': random.choice(BLOOM_LEVELS)
            })
    
    return questions

def generate_auto_questions(subject, num_questions, question_types):
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
        
        selected_topics = random.sample(topics, min(count, len(topics)))
        if count > len(topics):
            additional_needed = count - len(topics)
            additional_topics = random.choices(topics, k=additional_needed)
            selected_topics.extend(additional_topics)
        
        for topic in selected_topics[:count]:
            templates = QUESTION_TEMPLATES.get(qtype, [f"Describe {topic}."])
            question_text = random.choice(templates).format(topic=topic)
            
            marks_map = {"MCQ": 1, "Short Answer": 3, "Long Answer": 8, "Case Study": 10}
            marks = marks_map.get(qtype, 5)
            
            questions.append({
                'question': question_text,
                'type': qtype,
                'topic': topic,
                'marks': marks,
                'bloom_level': random.choice(BLOOM_LEVELS)
            })
    
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

def analyze_patterns(subject):
    """Analyze patterns from past papers"""
    papers = SAMPLE_PAST_PAPERS.get(subject, [])
    if not papers:
        return {}
    
    all_questions = []
    for paper in papers:
        all_questions.extend(paper['questions'])
    
    # Analyze patterns
    type_distribution = {}
    bloom_distribution = {}
    marks_distribution = {}
    topic_frequency = {}
    
    for q in all_questions:
        qtype = q['type']
        bloom = q['bloom']
        marks = q['marks']
        topic = q['topic']
        
        type_distribution[qtype] = type_distribution.get(qtype, 0) + 1
        bloom_distribution[bloom] = bloom_distribution.get(bloom, 0) + 1
        marks_distribution[marks] = marks_distribution.get(marks, 0) + 1
        topic_frequency[topic] = topic_frequency.get(topic, 0) + 1
    
    return {
        'type_distribution': type_distribution,
        'bloom_distribution': bloom_distribution,
        'marks_distribution': marks_distribution,
        'topic_frequency': topic_frequency,
        'total_papers': len(papers),
        'total_questions': len(all_questions)
    }

def manual_creation_page():
    st.markdown("## 📝 Manual Question Creation")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📄 Upload Syllabus")
        uploaded_file = st.file_uploader(
            "Upload your syllabus (PDF, DOCX, TXT)",
            type=['pdf', 'docx', 'txt']
        )
        
        if uploaded_file is not None:
            st.success(f"✅ File uploaded: {uploaded_file.name}")
            # For now, we'll use a text area for content
            st.info("Please paste the syllabus content below for processing.")
    
    with col2:
        st.markdown("### 📋 Paste Syllabus Content")
        syllabus_text = st.text_area(
            "Paste your syllabus content here",
            height=200,
            placeholder="Paste your syllabus topics, chapters, or content here..."
        )
    
    if syllabus_text:
        # Extract topics from the text
        extracted_topics = extract_topics_from_text(syllabus_text)
        
        st.markdown("### 🎯 Extracted Topics")
        if extracted_topics:
            st.write(f"Found {len(extracted_topics)} potential topics:")
            for i, topic in enumerate(extracted_topics, 1):
                st.write(f"{i}. {topic}")
        else:
            st.warning("No topics could be extracted. Please check your text format.")
            return
        
        st.markdown("### ⚙️ Question Generation Settings")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_questions = st.slider("Total Questions", 5, 30, 15)
            question_types = st.multiselect(
                "Question Types",
                ['MCQ', 'Short Answer', 'Long Answer', 'Case Study'],
                default=['MCQ', 'Short Answer', 'Long Answer']
            )
        
        with col2:
            difficulty = st.selectbox("Difficulty Level", ['Easy', 'Medium', 'Hard', 'Mixed'])
            exam_title = st.text_input("Exam Title", "Custom Generated Paper")
        
        with col3:
            duration = st.number_input("Duration (minutes)", 60, 300, 180)
            subject = st.text_input("Subject", "Custom Subject")
        
        if st.button("🚀 Generate Questions from Syllabus", type="primary"):
            if not question_types:
                st.error("Please select at least one question type!")
                return
            
            with st.spinner("🤖 Generating questions from your syllabus..."):
                questions = generate_questions_from_topics(extracted_topics, total_questions, question_types)
                analysis = analyze_questions(questions)
                
                st.success("✅ Questions generated successfully!")
                
                st.markdown("## 📄 Generated Question Paper")
                st.markdown(f"**{exam_title}**")
                st.markdown(f"**Subject:** {subject} | **Total Marks:** {analysis.get('total_marks', 0)} | **Duration:** {duration} minutes")
                st.markdown(f"**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
                st.subheader("📝 Questions")
                for i, question in enumerate(questions, 1):
                    with st.expander(f"Q{i} ({question['type']}, {question['topic']}, {question['marks']} marks, {question['bloom_level']})"):
                        st.write(f"**Question:** {question['question']}")
                        st.write(f"**Bloom's Level:** {question['bloom_level']}")
                
                st.subheader("📊 Analytics")
                col1, col2 = st.columns(2)
                
                with col1:
                    if analysis.get('type_counts'):
                        type_df = pd.DataFrame([{'Type': k, 'Count': v} for k, v in analysis['type_counts'].items()])
                        fig1 = px.pie(type_df, values='Count', names='Type', title='Question Type Distribution')
                        st.plotly_chart(fig1, use_container_width=True)
                
                with col2:
                    if analysis.get('topic_counts'):
                        topic_df = pd.DataFrame([{'Topic': k, 'Count': v} for k, v in analysis['topic_counts'].items()])
                        fig2 = px.bar(topic_df, x='Topic', y='Count', title='Topic Distribution')
                        fig2.update_xaxes(tickangle=45)
                        st.plotly_chart(fig2, use_container_width=True)
                
                st.subheader("📤 Export Options")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    export_text = f"{exam_title}\nSubject: {subject}\nTotal Marks: {analysis.get('total_marks', 0)}\nDuration: {duration} minutes\n\n"
                    for i, q in enumerate(questions, 1):
                        export_text += f"Q{i} ({q['type']}, {q['marks']} marks): {q['question']}\n\n"
                    st.download_button('📄 Download as Text', export_text, file_name=f'{subject}_question_paper.txt', mime='text/plain')
                
                with col2:
                    export_data = {'exam_title': exam_title, 'subject': subject, 'questions': questions, 'analysis': analysis}
                    st.download_button('📊 Download as JSON', json.dumps(export_data, indent=2), file_name=f'{subject}_question_paper.json', mime='application/json')
                
                with col3:
                    questions_df = pd.DataFrame(questions)
                    csv_data = questions_df.to_csv(index=False)
                    st.download_button('📋 Download as CSV', csv_data, file_name=f'{subject}_questions.csv', mime='text/csv')
    
    if st.button("← Back to Home"):
        st.session_state.show_manual_creation = False
        st.rerun()

def pattern_analysis_page():
    st.markdown("## 📊 Pattern Analysis")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📚 Select Subject for Analysis")
        subject = st.selectbox(
            "Choose subject to analyze patterns",
            list(SAMPLE_PAST_PAPERS.keys()),
            index=0
        )
        
        if subject:
            patterns = analyze_patterns(subject)
            
            if patterns:
                st.markdown("### 📈 Analysis Summary")
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("Total Papers", patterns.get('total_papers', 0))
                    st.metric("Total Questions", patterns.get('total_questions', 0))
                with col_b:
                    st.metric("Question Types", len(patterns.get('type_distribution', {})))
                    st.metric("Bloom's Levels", len(patterns.get('bloom_distribution', {})))
    
    with col2:
        st.markdown("### 📋 Sample Past Papers")
        papers = SAMPLE_PAST_PAPERS.get(subject, [])
        if papers:
            for paper in papers:
                with st.expander(f"📄 {subject} - {paper['year']}"):
                    for i, q in enumerate(paper['questions'], 1):
                        st.write(f"Q{i}: {q['type']} - {q['topic']} ({q['marks']} marks, {q['bloom']})")
        else:
            st.info("No past papers available for this subject.")
    
    if patterns:
        st.markdown("### 📊 Detailed Pattern Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Question Type Distribution
            if patterns.get('type_distribution'):
                type_df = pd.DataFrame([
                    {'Type': k, 'Count': v} for k, v in patterns['type_distribution'].items()
                ])
                fig1 = px.pie(type_df, values='Count', names='Type', title='Question Type Pattern')
                st.plotly_chart(fig1, use_container_width=True)
            
            # Bloom's Taxonomy Distribution
            if patterns.get('bloom_distribution'):
                bloom_df = pd.DataFrame([
                    {'Level': k, 'Count': v} for k, v in patterns['bloom_distribution'].items()
                ])
                fig3 = px.bar(bloom_df, x='Level', y='Count', title="Bloom's Taxonomy Pattern")
                st.plotly_chart(fig3, use_container_width=True)
        
        with col2:
            # Topic Frequency
            if patterns.get('topic_frequency'):
                topic_df = pd.DataFrame([
                    {'Topic': k, 'Frequency': v} for k, v in patterns['topic_frequency'].items()
                ])
                fig2 = px.bar(topic_df, x='Topic', y='Frequency', title='Topic Frequency Pattern')
                fig2.update_xaxes(tickangle=45)
                st.plotly_chart(fig2, use_container_width=True)
            
            # Marks Distribution
            if patterns.get('marks_distribution'):
                marks_df = pd.DataFrame([
                    {'Marks': k, 'Count': v} for k, v in patterns['marks_distribution'].items()
                ])
                fig4 = px.bar(marks_df, x='Marks', y='Count', title='Marks Distribution Pattern')
                st.plotly_chart(fig4, use_container_width=True)
        
        st.markdown("### 💡 Pattern Insights")
        insights = []
        
        if patterns.get('type_distribution'):
            most_common_type = max(patterns['type_distribution'], key=patterns['type_distribution'].get)
            insights.append(f"**Most common question type:** {most_common_type}")
        
        if patterns.get('bloom_distribution'):
            most_common_bloom = max(patterns['bloom_distribution'], key=patterns['bloom_distribution'].get)
            insights.append(f"**Most common Bloom's level:** {most_common_bloom}")
        
        if patterns.get('topic_frequency'):
            most_common_topic = max(patterns['topic_frequency'], key=patterns['topic_frequency'].get)
            insights.append(f"**Most frequently tested topic:** {most_common_topic}")
        
        for insight in insights:
            st.write(f"• {insight}")
        
        st.markdown("### 🎯 Recommended Question Distribution")
        if patterns.get('type_distribution') and patterns.get('total_questions'):
            total_q = patterns['total_questions']
            recommendations = []
            
            for qtype, count in patterns['type_distribution'].items():
                percentage = (count / total_q) * 100
                recommendations.append(f"**{qtype}:** {percentage:.1f}% ({count}/{total_q} questions)")
            
            for rec in recommendations:
                st.write(f"• {rec}")
    
    if st.button("← Back to Home"):
        st.session_state.show_pattern_analysis = False
        st.rerun()

def auto_generation_page():
    st.markdown("## 🤖 Auto Question Generation")
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        subject = st.selectbox("Select Subject", list(SYLLABUS_TOPICS.keys()), index=0)
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
    
    if st.button("🚀 Generate Question Paper Automatically", type="primary"):
        if not question_types:
            st.error("Please select at least one question type!")
            return
        
        with st.spinner("🤖 AI is generating your question paper..."):
            questions = generate_auto_questions(subject, total_questions, question_types)
            analysis = analyze_questions(questions)
            
            st.success("✅ Question paper generated successfully!")
            
            st.markdown("## 📄 Generated Question Paper")
            st.markdown(f"**{exam_title}**")
            st.markdown(f"**Subject:** {subject} | **Total Marks:** {analysis.get('total_marks', 0)} | **Duration:** {duration} minutes")
            st.markdown(f"**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            st.subheader("📝 Questions")
            for i, question in enumerate(questions, 1):
                with st.expander(f"Q{i} ({question['type']}, {question['topic']}, {question['marks']} marks, {question['bloom_level']})"):
                    st.write(f"**Question:** {question['question']}")
                    st.write(f"**Bloom's Level:** {question['bloom_level']}")
            
            st.markdown("## 📊 Analytics")
            col1, col2 = st.columns(2)
            
            with col1:
                if analysis.get('type_counts'):
                    type_df = pd.DataFrame([{'Type': k, 'Count': v} for k, v in analysis['type_counts'].items()])
                    fig1 = px.pie(type_df, values='Count', names='Type', title='Question Type Distribution')
                    st.plotly_chart(fig1, use_container_width=True)
            
            with col2:
                if analysis.get('topic_counts'):
                    topic_df = pd.DataFrame([{'Topic': k, 'Count': v} for k, v in analysis['topic_counts'].items()])
                    fig2 = px.bar(topic_df, x='Topic', y='Count', title='Topic Distribution')
                    fig2.update_xaxes(tickangle=45)
                    st.plotly_chart(fig2, use_container_width=True)
            
            st.subheader("📤 Export Options")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                export_text = f"{exam_title}\nSubject: {subject}\nTotal Marks: {analysis.get('total_marks', 0)}\nDuration: {duration} minutes\n\n"
                for i, q in enumerate(questions, 1):
                    export_text += f"Q{i} ({q['type']}, {q['marks']} marks): {q['question']}\n\n"
                st.download_button('📄 Download as Text', export_text, file_name=f'{subject}_question_paper.txt', mime='text/plain')
            
            with col2:
                export_data = {'exam_title': exam_title, 'subject': subject, 'questions': questions, 'analysis': analysis}
                st.download_button('📊 Download as JSON', json.dumps(export_data, indent=2), file_name=f'{subject}_question_paper.json', mime='application/json')
            
            with col3:
                questions_df = pd.DataFrame(questions)
                csv_data = questions_df.to_csv(index=False)
                st.download_button('📋 Download as CSV', csv_data, file_name=f'{subject}_questions.csv', mime='text/csv')
    
    if st.button("← Back to Home"):
        st.session_state.show_auto_generation = False
        st.rerun()

def main():
    if st.session_state.show_auto_generation:
        auto_generation_page()
        return
    elif st.session_state.show_manual_creation:
        manual_creation_page()
        return
    elif st.session_state.show_pattern_analysis:
        pattern_analysis_page()
        return
    
    st.markdown("""
    # Welcome to Question Paper Maker!

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
        st.metric("Subjects Available", len(SYLLABUS_TOPICS), "📚")

    with col2:
        total_topics = sum(len(topics) for topics in SYLLABUS_TOPICS.values())
        st.metric("Total Topics", total_topics, "🎯")

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

if __name__ == "__main__":
    main() 