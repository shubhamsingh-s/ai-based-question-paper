#!/usr/bin/env python3
"""
Simple Question Paper Maker Web App
==================================

A simplified version that works with basic dependencies.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json

# Page configuration
st.set_page_config(
    page_title="Question Paper Maker",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .feature-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #c3e6cb;
    }
</style>
""", unsafe_allow_html=True)

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

def analyze_questions(questions):
    """Analyze generated questions"""
    if not questions:
        return {}
    
    # Question type distribution
    type_counts = {}
    topic_counts = {}
    total_marks = 0
    
    for q in questions:
        qtype = q['type']
        topic = q['topic']
        marks = q['marks']
        
        type_counts[qtype] = type_counts.get(qtype, 0) + 1
        topic_counts[topic] = topic_counts.get(topic, 0) + 1
        total_marks += marks
    
    return {
        'type_counts': type_counts,
        'topic_counts': topic_counts,
        'total_marks': total_marks,
        'total_questions': len(questions)
    }

def create_charts(analysis):
    """Create visualization charts"""
    charts = {}
    
    if 'type_counts' in analysis and analysis['type_counts']:
        # Question type pie chart
        fig_type = px.pie(
            values=list(analysis['type_counts'].values()),
            names=list(analysis['type_counts'].keys()),
            title="Question Type Distribution",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        charts['type_distribution'] = fig_type
    
    if 'topic_counts' in analysis and analysis['topic_counts']:
        # Topic distribution bar chart
        fig_topic = px.bar(
            x=list(analysis['topic_counts'].keys()),
            y=list(analysis['topic_counts'].values()),
            title="Topic Distribution",
            labels={'x': 'Topics', 'y': 'Number of Questions'},
            color=list(analysis['topic_counts'].values()),
            color_continuous_scale='viridis'
        )
        charts['topic_distribution'] = fig_topic
    
    return charts

def main():
    """Main application function"""
    
    # Header
    st.markdown('<h1 class="main-header">📝 Question Paper Maker</h1>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("⚙️ Configuration")
    
    # Topic input
    st.sidebar.subheader("📚 Syllabus Topics")
    default_topics = [
        "Database Management Systems",
        "SQL Queries", 
        "Normalization",
        "Transaction Management",
        "Indexing and Performance",
        "Data Modeling"
    ]
    
    topics_input = st.sidebar.text_area(
        "Enter topics (one per line):",
        value="\n".join(default_topics),
        height=150
    )
    topics = [topic.strip() for topic in topics_input.split('\n') if topic.strip()]
    
    # Question parameters
    st.sidebar.subheader("📊 Question Parameters")
    num_questions = st.sidebar.slider("Number of Questions", 5, 50, 20)
    
    question_types = st.sidebar.multiselect(
        "Question Types",
        ["MCQ", "Short Answer", "Long Answer"],
        default=["MCQ", "Short Answer", "Long Answer"]
    )
    
    # Generate button
    if st.sidebar.button("🚀 Generate Question Paper", type="primary"):
        if not topics:
            st.error("Please enter at least one topic!")
            return
        
        if not question_types:
            st.error("Please select at least one question type!")
            return
        
        # Generate questions
        with st.spinner("Generating questions..."):
            questions = generate_questions(topics, num_questions, question_types)
        
        # Analyze questions
        analysis = analyze_questions(questions)
        
        # Display results
        st.success(f"✅ Generated {len(questions)} questions successfully!")
        
        # Create tabs for different views
        tab1, tab2, tab3, tab4 = st.tabs(["📄 Questions", "📊 Analysis", "📈 Charts", "💾 Export"])
        
        with tab1:
            st.subheader("Generated Questions")
            
            # Display questions in a nice format
            for i, q in enumerate(questions, 1):
                with st.expander(f"Q{i}: {q['question'][:50]}..."):
                    st.write(f"**Question:** {q['question']}")
                    st.write(f"**Type:** {q['type']}")
                    st.write(f"**Topic:** {q['topic']}")
                    st.write(f"**Marks:** {q['marks']}")
                    st.write(f"**Bloom Level:** {q['bloom_level']}")
        
        with tab2:
            st.subheader("Question Analysis")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Questions", analysis['total_questions'])
            
            with col2:
                st.metric("Total Marks", analysis['total_marks'])
            
            with col3:
                st.metric("Question Types", len(analysis['type_counts']))
            
            with col4:
                st.metric("Topics Covered", len(analysis['topic_counts']))
            
            # Detailed breakdown
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Question Type Breakdown")
                type_df = pd.DataFrame(list(analysis['type_counts'].items()), 
                                     columns=['Type', 'Count'])
                st.dataframe(type_df, use_container_width=True)
            
            with col2:
                st.subheader("Topic Breakdown")
                topic_df = pd.DataFrame(list(analysis['topic_counts'].items()), 
                                      columns=['Topic', 'Count'])
                st.dataframe(topic_df, use_container_width=True)
        
        with tab3:
            st.subheader("Visual Analytics")
            
            charts = create_charts(analysis)
            
            if 'type_distribution' in charts:
                st.plotly_chart(charts['type_distribution'], use_container_width=True)
            
            if 'topic_distribution' in charts:
                st.plotly_chart(charts['topic_distribution'], use_container_width=True)
        
        with tab4:
            st.subheader("Export Options")
            
            # Export as JSON
            if st.button("📄 Export as JSON"):
                export_data = {
                    'questions': questions,
                    'analysis': analysis,
                    'generated_at': datetime.now().isoformat(),
                    'parameters': {
                        'topics': topics,
                        'num_questions': num_questions,
                        'question_types': question_types
                    }
                }
                
                st.download_button(
                    label="💾 Download JSON",
                    data=json.dumps(export_data, indent=2),
                    file_name=f"question_paper_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
            
            # Export as CSV
            if st.button("📊 Export as CSV"):
                questions_df = pd.DataFrame(questions)
                csv_data = questions_df.to_csv(index=False)
                
                st.download_button(
                    label="💾 Download CSV",
                    data=csv_data,
                    file_name=f"question_paper_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
    
    # Information section
    st.sidebar.markdown("---")
    st.sidebar.subheader("ℹ️ About")
    st.sidebar.markdown("""
    This is a simplified version of the Question Paper Maker system.
    
    **Features:**
    - 📝 Question generation
    - 📊 Analysis and statistics
    - 📈 Interactive charts
    - 💾 Export capabilities
    
    **Note:** This version works with basic dependencies and doesn't require file uploads.
    """)
    
    # Main content area
    if not st.session_state.get('questions_generated', False):
        st.markdown("""
        <div class="feature-card">
            <h3>🎯 Welcome to Question Paper Maker!</h3>
            <p>This intelligent system helps you create comprehensive question papers based on your syllabus topics.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="feature-card">
                <h4>📚 Syllabus-Based</h4>
                <p>Generate questions from your specific syllabus topics</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="feature-card">
                <h4>🎯 Multiple Types</h4>
                <p>Support for MCQ, Short Answer, and Long Answer questions</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="feature-card">
                <h4>📊 Smart Analysis</h4>
                <p>Get detailed analytics and visualizations</p>
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 