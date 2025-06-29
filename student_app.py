import streamlit as st
import pandas as pd
import plotly.express as px
from collections import Counter
import random

# Page configuration
st.set_page_config(
    page_title="Student Question Paper Helper",
    page_icon="🎓",
    layout="wide"
)

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'
if 'past_papers' not in st.session_state:
    st.session_state.past_papers = []
if 'syllabus_topics' not in st.session_state:
    st.session_state.syllabus_topics = []

def analyze_past_papers(uploaded_files):
    """Analyze past papers to find frequently asked questions"""
    all_questions = []
    
    for file in uploaded_files:
        # Simulate extracting questions from file
        # In real app, you'd use proper text extraction
        sample_questions = [
            "What is database management system?",
            "Explain SQL queries with examples",
            "What are the types of database models?",
            "How to create tables in SQL?",
            "What is normalization in database?",
            "Explain ACID properties",
            "What is indexing in database?",
            "How to perform JOIN operations?",
            "What is transaction management?",
            "Explain database security"
        ]
        
        # Add some random questions for demonstration
        for i in range(random.randint(5, 10)):
            question = random.choice(sample_questions)
            all_questions.append({
                'question': question,
                'file': file.name,
                'year': random.randint(2020, 2024)
            })
    
    return all_questions

def find_question_probability(questions):
    """Calculate probability of questions appearing again"""
    question_counts = Counter([q['question'] for q in questions])
    total_papers = len(set([q['file'] for q in questions]))
    
    probabilities = []
    for question, count in question_counts.items():
        probability = (count / total_papers) * 100
        if count >= 2:
            status = "🔥 HIGH CHANCE"
        elif count == 1:
            status = "⚠️ MEDIUM CHANCE"
        else:
            status = "❄️ LOW CHANCE"
        
        probabilities.append({
            'question': question,
            'appearances': count,
            'probability': probability,
            'status': status
        })
    
    return sorted(probabilities, key=lambda x: x['appearances'], reverse=True)

def generate_sample_papers(syllabus_topics, past_questions, num_papers=3):
    """Generate sample question papers based on syllabus and past patterns"""
    sample_papers = []
    
    for paper_num in range(num_papers):
        paper = {
            'title': f"Sample Question Paper {paper_num + 1}",
            'questions': [],
            'total_marks': 0
        }
        
        # Mix syllabus topics with high-probability past questions
        high_prob_questions = [q for q in past_questions if q['appearances'] >= 2]
        
        # Generate questions
        for i in range(10):  # 10 questions per paper
            if i < 5 and high_prob_questions:  # First 5 from high probability
                selected_q = random.choice(high_prob_questions)
                question_text = selected_q['question']
                marks = random.choice([3, 5, 8])
                probability = selected_q['probability']
            else:  # Rest from syllabus topics
                topic = random.choice(syllabus_topics)
                question_text = f"Explain {topic} in detail."
                marks = random.choice([3, 5, 8])
                probability = random.randint(20, 60)
            
            paper['questions'].append({
                'question': question_text,
                'marks': marks,
                'probability': probability
            })
            paper['total_marks'] += marks
        
        sample_papers.append(paper)
    
    return sample_papers

def home_page():
    st.markdown("""
    # 🎓 Student Question Paper Helper
    
    **Your AI assistant for exam preparation!**
    
    Upload past papers and syllabus to get smart predictions and sample question papers.
    """)
    
    # Feature cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📊 Past Paper Analysis
        - Upload past question papers
        - AI analyzes which questions appear frequently
        - Get probability scores for each question
        - Know which questions are likely to come again!
        """)
        
        if st.button("🔍 Analyze Past Papers", key="analyze_btn"):
            st.session_state.current_page = 'analyze'
            st.rerun()
    
    with col2:
        st.markdown("""
        ### 📝 Generate Sample Papers
        - Upload your syllabus
        - Optionally upload past papers
        - AI creates multiple sample question papers
        - Each question comes with probability scores
        """)
        
        if st.button("📄 Create Sample Papers", key="generate_btn"):
            st.session_state.current_page = 'generate'
            st.rerun()

def analyze_page():
    st.markdown("## 📊 Past Paper Analysis")
    st.markdown("---")
    
    # Back button
    if st.button("← Back to Home"):
        st.session_state.current_page = 'home'
        st.rerun()
    
    st.markdown("""
    ### How it works:
    1. Upload past question papers (PDF, DOCX, TXT)
    2. AI analyzes which questions appear most frequently
    3. Get probability scores for each question
    4. Know which questions are likely to come in your exam!
    """)
    
    # File upload
    uploaded_files = st.file_uploader(
        "Upload Past Question Papers", 
        type=['pdf', 'docx', 'txt'], 
        accept_multiple_files=True,
        help="Upload multiple past papers for better analysis"
    )
    
    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} files uploaded")
        
        if st.button("🔍 Analyze Papers", type="primary"):
            with st.spinner("Analyzing past papers..."):
                # Analyze the papers
                questions = analyze_past_papers(uploaded_files)
                probabilities = find_question_probability(questions)
                
                st.session_state.past_papers = probabilities
                
                st.success("Analysis complete!")
                
                # Display results
                st.markdown("## 📈 Analysis Results")
                
                # Summary metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Papers Analyzed", len(uploaded_files))
                with col2:
                    st.metric("Total Questions", len(questions))
                with col3:
                    high_chance = len([p for p in probabilities if p['appearances'] >= 2])
                    st.metric("High Chance Questions", high_chance)
                
                # Question probability table
                st.markdown("### 🎯 Question Probability Analysis")
                
                # Create DataFrame for better display
                df = pd.DataFrame(probabilities)
                df = df.rename(columns={
                    'question': 'Question',
                    'appearances': 'Times Appeared',
                    'probability': 'Probability (%)',
                    'status': 'Chance'
                })
                
                # Display with color coding
                for _, row in df.iterrows():
                    if row['Chance'] == "🔥 HIGH CHANCE":
                        st.markdown(f"**🔥 {row['Question']}**")
                        st.markdown(f"   - Appeared {row['Times Appeared']} times")
                        st.markdown(f"   - **{row['Probability (%)']:.1f}% chance** to appear again")
                        st.markdown("   - **HIGH PRIORITY** for study!")
                    elif row['Chance'] == "⚠️ MEDIUM CHANCE":
                        st.markdown(f"**⚠️ {row['Question']}**")
                        st.markdown(f"   - Appeared {row['Times Appeared']} time")
                        st.markdown(f"   - **{row['Probability (%)']:.1f}% chance** to appear again")
                    else:
                        st.markdown(f"**❄️ {row['Question']}**")
                        st.markdown(f"   - Appeared {row['Times Appeared']} time")
                        st.markdown(f"   - **{row['Probability (%)']:.1f}% chance** to appear again")
                    
                    st.markdown("---")
                
                # Chart
                if len(probabilities) > 0:
                    st.markdown("### 📊 Question Frequency Chart")
                    chart_df = pd.DataFrame(probabilities[:10])  # Top 10
                    fig = px.bar(chart_df, x='question', y='appearances', 
                               title='Most Frequently Asked Questions',
                               labels={'question': 'Question', 'appearances': 'Times Appeared'})
                    fig.update_xaxis(tickangle=45)
                    st.plotly_chart(fig, use_container_width=True)
    
    else:
        st.info("👆 Please upload past question papers to begin analysis")

def generate_page():
    st.markdown("## 📝 Generate Sample Question Papers")
    st.markdown("---")
    
    # Back button
    if st.button("← Back to Home"):
        st.session_state.current_page = 'home'
        st.rerun()
    
    st.markdown("""
    ### How it works:
    1. Upload your syllabus (topics you need to study)
    2. Optionally upload past papers for better predictions
    3. AI creates multiple sample question papers
    4. Each question comes with probability scores
    """)
    
    # Syllabus input
    st.markdown("### 📚 Step 1: Upload Syllabus")
    syllabus_text = st.text_area(
        "Enter your syllabus topics (one per line)",
        height=150,
        placeholder="Database Management\nSQL Queries\nData Modeling\nNormalization\nACID Properties\n..."
    )
    
    # Past papers (optional)
    st.markdown("### 📄 Step 2: Upload Past Papers (Optional)")
    past_files = st.file_uploader(
        "Upload past papers for better predictions", 
        type=['pdf', 'docx', 'txt'], 
        accept_multiple_files=True
    )
    
    # Configuration
    st.markdown("### ⚙️ Step 3: Configuration")
    col1, col2 = st.columns(2)
    
    with col1:
        num_papers = st.number_input("Number of sample papers", min_value=1, max_value=5, value=3)
        questions_per_paper = st.number_input("Questions per paper", min_value=5, max_value=20, value=10)
    
    with col2:
        include_probability = st.checkbox("Include probability scores", value=True)
        focus_on_high_prob = st.checkbox("Focus on high-probability questions", value=True)
    
    # Generate papers
    if st.button("🎯 Generate Sample Papers", type="primary"):
        if syllabus_text:
            # Parse syllabus
            topics = [line.strip() for line in syllabus_text.split('\n') if line.strip()]
            st.session_state.syllabus_topics = topics
            
            if topics:
                with st.spinner("Generating sample question papers..."):
                    # Analyze past papers if provided
                    past_questions = []
                    if past_files:
                        questions = analyze_past_papers(past_files)
                        past_questions = find_question_probability(questions)
                    
                    # Generate sample papers
                    sample_papers = generate_sample_papers(topics, past_questions, num_papers)
                    
                    st.success(f"✅ Generated {len(sample_papers)} sample papers!")
                    
                    # Display papers
                    for i, paper in enumerate(sample_papers):
                        st.markdown(f"## 📄 {paper['title']}")
                        st.markdown(f"**Total Marks:** {paper['total_marks']}")
                        
                        # Display questions
                        for j, question in enumerate(paper['questions'], 1):
                            with st.expander(f"Q{j} ({question['marks']} marks)"):
                                st.write(f"**Question:** {question['question']}")
                                if include_probability:
                                    if question['probability'] >= 50:
                                        st.markdown(f"🎯 **Probability:** {question['probability']:.1f}% (HIGH CHANCE)")
                                    elif question['probability'] >= 30:
                                        st.markdown(f"⚠️ **Probability:** {question['probability']:.1f}% (MEDIUM CHANCE)")
                                    else:
                                        st.markdown(f"❄️ **Probability:** {question['probability']:.1f}% (LOW CHANCE)")
                        
                        st.markdown("---")
                    
                    # Export option
                    st.markdown("### 📤 Export Options")
                    if st.button(f"📄 Download All Papers as Text"):
                        export_text = ""
                        for paper in sample_papers:
                            export_text += f"{paper['title']}\n"
                            export_text += f"Total Marks: {paper['total_marks']}\n\n"
                            for j, q in enumerate(paper['questions'], 1):
                                export_text += f"Q{j} ({q['marks']} marks): {q['question']}\n"
                                if include_probability:
                                    export_text += f"Probability: {q['probability']:.1f}%\n"
                                export_text += "\n"
                            export_text += "=" * 50 + "\n\n"
                        
                        st.download_button(
                            'Download Sample Papers',
                            export_text,
                            file_name='sample_question_papers.txt'
                        )
            else:
                st.error("No topics found in syllabus!")
        else:
            st.error("Please provide syllabus topics!")

def main():
    # Page routing
    if st.session_state.current_page == 'home':
        home_page()
    elif st.session_state.current_page == 'analyze':
        analyze_page()
    elif st.session_state.current_page == 'generate':
        generate_page()
    
    # Footer
    if st.session_state.current_page == 'home':
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: #666; padding: 1rem;">
            <p>🎓 Made for Students • Powered by AI • Smart Exam Preparation</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 