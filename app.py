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
/* Main background styling */
.main {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
}

/* Background for the entire app */
.stApp {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
    background-attachment: fixed;
}

/* Container background with glass effect */
.main .block-container {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 2rem;
    margin: 1rem;
    border: 1px solid rgba(255, 255, 255, 0.2);
    box-shadow: 0 8px 32px rgba(0,0,0,0.1);
}

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
    background: rgba(255, 255, 255, 0.98) !important;
    border-radius: 20px !important;
    padding: 2rem !important;
    margin: 1rem 0.5rem !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.1) !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    transition: all 0.3s ease !important;
    backdrop-filter: blur(10px) !important;
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

/* Text color adjustments for better readability */
p, h2, h3, h4, h5, h6 {
    color: #2c3e50 !important;
    font-weight: 500 !important;
}

/* Make all text containers have white background */
div[data-testid="stMarkdown"] {
    background: rgba(255, 255, 255, 0.95) !important;
    padding: 1rem !important;
    border-radius: 10px !important;
    margin: 0.5rem 0 !important;
}

/* Streamlit elements background */
.stTextInput > div > div > input {
    background: rgba(255, 255, 255, 0.95) !important;
    border-radius: 10px !important;
    border: 2px solid #e0e0e0 !important;
}

.stSelectbox > div > div > div {
    background: rgba(255, 255, 255, 0.95) !important;
    border-radius: 10px !important;
    border: 2px solid #e0e0e0 !important;
}

.stSlider > div > div > div > div {
    background: rgba(255, 255, 255, 0.95) !important;
}

/* Success and info boxes */
.stAlert {
    background: rgba(255, 255, 255, 0.98) !important;
    border-radius: 15px !important;
    backdrop-filter: blur(10px) !important;
    border: 2px solid #e0e0e0 !important;
}

/* Make expandable sections more visible */
.streamlit-expanderHeader {
    background: rgba(255, 255, 255, 0.95) !important;
    border-radius: 10px !important;
    padding: 1rem !important;
    margin: 0.5rem 0 !important;
    border: 2px solid #e0e0e0 !important;
}

.streamlit-expanderContent {
    background: rgba(255, 255, 255, 0.95) !important;
    border-radius: 10px !important;
    padding: 1rem !important;
    margin: 0.5rem 0 !important;
    border: 2px solid #e0e0e0 !important;
}

/* Make tabs more visible */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255, 255, 255, 0.95) !important;
    border-radius: 10px !important;
    padding: 0.5rem !important;
    margin: 0.5rem 0 !important;
}

.stTabs [data-baseweb="tab"] {
    background: rgba(255, 255, 255, 0.95) !important;
    border-radius: 8px !important;
    margin: 0.2rem !important;
}

/* Make file uploader more visible */
.stFileUploader {
    background: rgba(255, 255, 255, 0.95) !important;
    border-radius: 15px !important;
    padding: 1rem !important;
    border: 2px solid #e0e0e0 !important;
}

/* Make text areas more visible */
.stTextArea textarea {
    background: rgba(255, 255, 255, 0.95) !important;
    border-radius: 10px !important;
    border: 2px solid #e0e0e0 !important;
}

/* Make multiselect more visible */
.stMultiSelect > div > div > div {
    background: rgba(255, 255, 255, 0.95) !important;
    border-radius: 10px !important;
    border: 2px solid #e0e0e0 !important;
}

/* Ensure all text is readable */
* {
    color: #2c3e50 !important;
}

/* Make links more visible */
a {
    color: #3498db !important;
    font-weight: 600 !important;
}

/* Make success/error messages more visible */
.stSuccess {
    background: rgba(46, 204, 113, 0.1) !important;
    border: 2px solid #2ecc71 !important;
    color: #27ae60 !important;
}

.stError {
    background: rgba(231, 76, 60, 0.1) !important;
    border: 2px solid #e74c3c !important;
    color: #c0392b !important;
}

.stWarning {
    background: rgba(241, 196, 15, 0.1) !important;
    border: 2px solid #f1c40f !important;
    color: #f39c12 !important;
}

.stInfo {
    background: rgba(52, 152, 219, 0.1) !important;
    border: 2px solid #3498db !important;
    color: #2980b9 !important;
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
if 'custom_paper' not in st.session_state:
    st.session_state.custom_paper = None

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
    # Improved topic extraction with better pattern matching
    lines = text.split('\n')
    topics = []
    
    # Common patterns for syllabus topics
    patterns = [
        r'^\d+\.\s*(.+)$',  # 1. Topic Name
        r'^[A-Z][A-Z\s]+$',  # ALL CAPS TOPICS
        r'^[A-Z][a-z\s]+:$',  # Topic: format
        r'^Chapter\s+\d+[:\s]+(.+)$',  # Chapter 1: Topic
        r'^Unit\s+\d+[:\s]+(.+)$',  # Unit 1: Topic
        r'^Module\s+\d+[:\s]+(.+)$',  # Module 1: Topic
        r'^[A-Z][a-z\s]{3,}$',  # Proper case topics with 3+ chars
    ]
    
    for line in lines:
        line = line.strip()
        if len(line) < 5:  # Skip very short lines
            continue
            
        # Check each pattern
        for pattern in patterns:
            match = re.match(pattern, line)
            if match:
                topic = match.group(1) if len(match.groups()) > 0 else line
                # Clean up the topic
                topic = re.sub(r'[^\w\s\-]', '', topic).strip()
                if len(topic) > 3 and topic not in topics:
                    topics.append(topic)
                break
    
    # If no patterns match, try to extract meaningful phrases
    if not topics:
        words = text.split()
        for i in range(len(words) - 2):
            phrase = ' '.join(words[i:i+3])
            if len(phrase) > 10 and phrase[0].isupper():
                clean_phrase = re.sub(r'[^\w\s]', '', phrase).strip()
                if len(clean_phrase) > 5 and clean_phrase not in topics:
                    topics.append(clean_phrase)
    
    return topics[:15]  # Limit to 15 topics

def generate_questions_from_topics(topics, num_questions, question_types, subject="Custom Subject"):
    """Generate questions from custom topics with better context"""
    if not topics:
        return []
    
    questions = []
    questions_per_type = num_questions // len(question_types)
    remaining = num_questions % len(question_types)
    
    # Enhanced question templates for better context
    enhanced_templates = {
        "MCQ": [
            "Which of the following best describes {topic} in {subject}?",
            "What is the primary purpose of {topic} in the context of {subject}?",
            "Which statement is true about {topic}?",
            "In {subject}, what does {topic} represent?",
            "Which approach is most commonly used for {topic} in {subject}?"
        ],
        "Short Answer": [
            "Explain the concept of {topic} in {subject}.",
            "Describe the key components of {topic}.",
            "What are the main advantages of {topic} in {subject}?",
            "How does {topic} work in {subject}?",
            "List the important features of {topic}."
        ],
        "Long Answer": [
            "Discuss {topic} in detail with examples and applications in {subject}.",
            "Analyze the importance of {topic} in {subject}.",
            "Compare and contrast different approaches to {topic} in {subject}.",
            "Explain the implementation and challenges of {topic} in {subject}.",
            "Describe the evolution and future trends of {topic} in {subject}."
        ],
        "Case Study": [
            "Consider a scenario where {topic} needs to be implemented in {subject}. What would be your approach?",
            "Analyze a real-world problem that can be solved using {topic} in {subject}.",
            "Design a solution using {topic} for a given {subject} requirement.",
            "Evaluate the effectiveness of {topic} in {subject}.",
            "Propose improvements to an existing {topic} implementation in {subject}."
        ]
    }
    
    for qtype in question_types:
        count = questions_per_type + (1 if remaining > 0 else 0)
        remaining -= 1
        
        selected_topics = random.sample(topics, min(count, len(topics)))
        if count > len(topics):
            additional_needed = count - len(topics)
            additional_topics = random.choices(topics, k=additional_needed)
            selected_topics.extend(additional_topics)
        
        for topic in selected_topics[:count]:
            templates = enhanced_templates.get(qtype, [f"Describe {topic} in {subject}."])
            question_text = random.choice(templates).format(topic=topic, subject=subject)
            
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

def parse_uploaded_question_paper(file_content):
    """Parse uploaded question paper and extract question data"""
    try:
        # Try to parse as JSON first
        if isinstance(file_content, str):
            data = json.loads(file_content)
            return data
    except:
        pass
    
    # If not JSON, try to parse as text
    if isinstance(file_content, str):
        lines = file_content.split('\n')
        questions = []
        current_question = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Look for question patterns
            question_match = re.match(r'Q(\d+)[:\s]+(.+)', line, re.IGNORECASE)
            if question_match:
                if current_question:
                    questions.append(current_question)
                
                question_text = question_match.group(2)
                current_question = {
                    'question': question_text,
                    'type': 'Unknown',
                    'topic': 'Unknown',
                    'marks': 5,
                    'bloom': 'Understand'
                }
            else:
                # Look for metadata in the line
                if current_question:
                    if 'marks' in line.lower() or '(' in line and ')' in line:
                        # Extract marks from parentheses
                        marks_match = re.search(r'\((\d+)\s*marks?\)', line, re.IGNORECASE)
                        if marks_match:
                            current_question['marks'] = int(marks_match.group(1))
                    
                    if 'mcq' in line.lower():
                        current_question['type'] = 'MCQ'
                    elif 'short' in line.lower():
                        current_question['type'] = 'Short Answer'
                    elif 'long' in line.lower():
                        current_question['type'] = 'Long Answer'
                    elif 'case' in line.lower():
                        current_question['type'] = 'Case Study'
        
        if current_question:
            questions.append(current_question)
        
        return {
            'questions': questions,
            'year': 'Custom',
            'subject': 'Custom Subject'
        }
    
    return None

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
            placeholder="Paste your syllabus topics, chapters, or content here...\n\nExample formats:\n1. Database Design\n2. SQL Queries\nChapter 1: Introduction\nUnit 2: Advanced Topics"
        )
    
    if syllabus_text:
        # Extract topics from the text
        extracted_topics = extract_topics_from_text(syllabus_text)
        
        st.markdown("### 🎯 Extracted Topics")
        if extracted_topics:
            st.success(f"✅ Successfully extracted {len(extracted_topics)} topics from your syllabus!")
            st.write("**Topics found:**")
            for i, topic in enumerate(extracted_topics, 1):
                st.write(f"{i}. **{topic}**")
            
            # Allow user to edit topics
            st.markdown("### ✏️ Edit Topics (Optional)")
            st.info("You can edit the extracted topics below if needed:")
            
            edited_topics = []
            for i, topic in enumerate(extracted_topics):
                edited_topic = st.text_input(f"Topic {i+1}", value=topic, key=f"topic_{i}")
                if edited_topic.strip():
                    edited_topics.append(edited_topic.strip())
            
            # Use edited topics if provided, otherwise use extracted ones
            final_topics = edited_topics if edited_topics else extracted_topics
            
        else:
            st.warning("⚠️ No topics could be extracted automatically. Please check your text format.")
            st.info("**Tips for better topic extraction:**")
            st.write("• Use numbered lists: 1. Topic Name")
            st.write("• Use chapter format: Chapter 1: Topic Name")
            st.write("• Use unit format: Unit 1: Topic Name")
            st.write("• Use proper capitalization: Topic Name")
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
            subject = st.text_input("Subject Name", value="Custom Subject", help="Enter the subject name (e.g., Database Management, Computer Networks)")
        
        with col3:
            duration = st.number_input("Duration (minutes)", 60, 300, 180)
            exam_title = st.text_input("Exam Title", value=f"{subject} - Custom Generated Paper")
        
        if st.button("🚀 Generate Questions from Syllabus", type="primary"):
            if not question_types:
                st.error("Please select at least one question type!")
                return
            
            if not subject.strip():
                st.error("Please enter a subject name!")
                return
            
            with st.spinner("🤖 Generating questions from your syllabus..."):
                questions = generate_questions_from_topics(final_topics, total_questions, question_types, subject)
                analysis = analyze_questions(questions)
                
                st.success("✅ Questions generated successfully!")
                
                st.markdown("## 📄 Generated Question Paper")
                st.markdown(f"**{exam_title}**")
                st.markdown(f"**Subject:** {subject} | **Total Marks:** {analysis.get('total_marks', 0)} | **Duration:** {duration} minutes")
                st.markdown(f"**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                st.markdown(f"**Topics covered:** {len(final_topics)} topics from your syllabus")
                
                st.subheader("📝 Questions")
                for i, question in enumerate(questions, 1):
                    with st.expander(f"Q{i} ({question['type']}, {question['topic']}, {question['marks']} marks, {question['bloom_level']})"):
                        st.write(f"**Question:** {question['question']}")
                        st.write(f"**Topic:** {question['topic']}")
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
                    export_text = f"{exam_title}\nSubject: {subject}\nTotal Marks: {analysis.get('total_marks', 0)}\nDuration: {duration} minutes\nTopics: {', '.join(final_topics)}\n\n"
                    for i, q in enumerate(questions, 1):
                        export_text += f"Q{i} ({q['type']}, {q['marks']} marks): {q['question']}\n\n"
                    st.download_button('📄 Download as Text', export_text, file_name=f'{subject}_question_paper.txt', mime='text/plain')
                
                with col2:
                    export_data = {
                        'exam_title': exam_title, 
                        'subject': subject, 
                        'topics': final_topics,
                        'questions': questions, 
                        'analysis': analysis
                    }
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
    
    # Add tabs for different analysis options
    tab1, tab2 = st.tabs(["📚 Sample Papers Analysis", "📄 Upload Custom Papers"])
    
    with tab1:
        st.markdown("### 📚 Analyze Sample Past Papers")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📚 Select Subject for Analysis")
            subject = st.selectbox(
                "Choose subject to analyze patterns",
                list(SAMPLE_PAST_PAPERS.keys()),
                index=0,
                key="sample_subject"
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
    
    with tab2:
        st.markdown("### 📄 Upload Custom Question Papers")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📁 Upload Question Paper")
            uploaded_paper = st.file_uploader(
                "Upload your question paper (JSON, TXT)",
                type=['json', 'txt'],
                key="paper_upload"
            )
            
            if uploaded_paper is not None:
                st.success(f"✅ File uploaded: {uploaded_paper.name}")
                
                # Read file content
                try:
                    if uploaded_paper.name.endswith('.json'):
                        content = json.load(uploaded_paper)
                    else:
                        content = uploaded_paper.read().decode('utf-8')
                    
                    # Parse the content
                    parsed_data = parse_uploaded_question_paper(content)
                    
                    if parsed_data and parsed_data.get('questions'):
                        st.session_state.custom_paper = parsed_data
                        st.success(f"✅ Successfully parsed {len(parsed_data['questions'])} questions!")
                    else:
                        st.error("❌ Could not parse questions from the uploaded file.")
                        
                except Exception as e:
                    st.error(f"❌ Error reading file: {str(e)}")
        
        with col2:
            st.markdown("#### 📝 Paste Question Paper")
            pasted_paper = st.text_area(
                "Or paste your question paper content here",
                height=200,
                placeholder="Paste your question paper content here...\n\nExample format:\nQ1: What is database normalization? (5 marks)\nQ2: Explain SQL joins with examples. (8 marks)"
            )
            
            if pasted_paper and st.button("📊 Analyze Pasted Paper"):
                parsed_data = parse_uploaded_question_paper(pasted_paper)
                if parsed_data and parsed_data.get('questions'):
                    st.session_state.custom_paper = parsed_data
                    st.success(f"✅ Successfully parsed {len(parsed_data['questions'])} questions!")
                else:
                    st.error("❌ Could not parse questions from the pasted content.")
        
        # Analyze custom paper if available
        if hasattr(st.session_state, 'custom_paper') and st.session_state.custom_paper:
            custom_paper = st.session_state.custom_paper
            
            st.markdown("### 📊 Custom Paper Analysis")
            
            # Get subject name
            subject_name = st.text_input(
                "Subject Name", 
                value=custom_paper.get('subject', 'Custom Subject'),
                help="Enter the subject name for better analysis"
            )
            
            if st.button("🔍 Analyze Custom Paper"):
                # Analyze the custom paper
                questions = custom_paper['questions']
                
                # Count patterns
                type_counts = {}
                bloom_counts = {}
                marks_counts = {}
                topic_counts = {}
                total_marks = 0
                
                for q in questions:
                    qtype = q.get('type', 'Unknown')
                    bloom = q.get('bloom', 'Understand')
                    marks = q.get('marks', 5)
                    topic = q.get('topic', 'Unknown')
                    
                    type_counts[qtype] = type_counts.get(qtype, 0) + 1
                    bloom_counts[bloom] = bloom_counts.get(bloom, 0) + 1
                    marks_counts[marks] = marks_counts.get(marks, 0) + 1
                    topic_counts[topic] = topic_counts.get(topic, 0) + 1
                    total_marks += marks
                
                # Display analysis
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Total Questions", len(questions))
                    st.metric("Total Marks", total_marks)
                
                with col2:
                    st.metric("Question Types", len(type_counts))
                    st.metric("Topics Covered", len(topic_counts))
                
                # Charts
                col1, col2 = st.columns(2)
                
                with col1:
                    if type_counts:
                        type_df = pd.DataFrame([{'Type': k, 'Count': v} for k, v in type_counts.items()])
                        fig1 = px.pie(type_df, values='Count', names='Type', title=f'{subject_name} - Question Type Distribution')
                        st.plotly_chart(fig1, use_container_width=True)
                    
                    if marks_counts:
                        marks_df = pd.DataFrame([{'Marks': k, 'Count': v} for k, v in marks_counts.items()])
                        fig3 = px.bar(marks_df, x='Marks', y='Count', title=f'{subject_name} - Marks Distribution')
                        st.plotly_chart(fig3, use_container_width=True)
                
                with col2:
                    if topic_counts:
                        topic_df = pd.DataFrame([{'Topic': k, 'Count': v} for k, v in topic_counts.items()])
                        fig2 = px.bar(topic_df, x='Topic', y='Count', title=f'{subject_name} - Topic Distribution')
                        fig2.update_xaxes(tickangle=45)
                        st.plotly_chart(fig2, use_container_width=True)
                    
                    if bloom_counts:
                        bloom_df = pd.DataFrame([{'Level': k, 'Count': v} for k, v in bloom_counts.items()])
                        fig4 = px.bar(bloom_df, x='Level', y='Count', title=f'{subject_name} - Bloom\'s Taxonomy')
                        st.plotly_chart(fig4, use_container_width=True)
                
                # Insights
                st.markdown("### 💡 Custom Paper Insights")
                insights = []
                
                if type_counts:
                    most_common_type = max(type_counts, key=type_counts.get)
                    insights.append(f"**Most common question type:** {most_common_type}")
                
                if marks_counts:
                    most_common_marks = max(marks_counts, key=marks_counts.get)
                    insights.append(f"**Most common marks per question:** {most_common_marks}")
                
                if topic_counts:
                    most_common_topic = max(topic_counts, key=topic_counts.get)
                    insights.append(f"**Most frequently tested topic:** {most_common_topic}")
                
                for insight in insights:
                    st.write(f"• {insight}")
                
                # Export analysis
                st.markdown("### 📤 Export Analysis")
                analysis_data = {
                    'subject': subject_name,
                    'total_questions': len(questions),
                    'total_marks': total_marks,
                    'type_distribution': type_counts,
                    'marks_distribution': marks_counts,
                    'topic_distribution': topic_counts,
                    'bloom_distribution': bloom_counts,
                    'questions': questions
                }
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.download_button(
                        '📊 Download Analysis as JSON',
                        json.dumps(analysis_data, indent=2),
                        file_name=f'{subject_name}_pattern_analysis.json',
                        mime='application/json'
                    )
                
                with col2:
                    # Create CSV of questions
                    questions_df = pd.DataFrame(questions)
                    csv_data = questions_df.to_csv(index=False)
                    st.download_button(
                        '📋 Download Questions as CSV',
                        csv_data,
                        file_name=f'{subject_name}_questions.csv',
                        mime='text/csv'
                    )
    
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
    try:
        # Initialize session state if not already done
        if 'show_auto_generation' not in st.session_state:
            st.session_state.show_auto_generation = False
        if 'show_manual_creation' not in st.session_state:
            st.session_state.show_manual_creation = False
        if 'show_pattern_analysis' not in st.session_state:
            st.session_state.show_pattern_analysis = False
        if 'custom_paper' not in st.session_state:
            st.session_state.custom_paper = None
        
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
    
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.info("Please refresh the page and try again.")
        # Reset session state
        for key in ['show_auto_generation', 'show_manual_creation', 'show_pattern_analysis', 'custom_paper']:
            if key in st.session_state:
                del st.session_state[key]

if __name__ == "__main__":
    main() 