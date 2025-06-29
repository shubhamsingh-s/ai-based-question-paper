import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
from collections import Counter, defaultdict
import json
import tempfile

# Import existing modules
from src.ingest import DocumentIngestor
from src.generate import generate_questions, generate_model_answer, assign_marks, format_export_text, format_export_docx
from src.analyze import compute_analytics, compute_topic_frequency
from src.classify import tag_questions_by_topic

# Page configuration
st.set_page_config(
    page_title="AI Question Paper Maker & Exam Pattern Analyzer",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #c3e6cb;
    }
    .warning-message {
        background-color: #fff3cd;
        color: #856404;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #ffeaa7;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'question_database' not in st.session_state:
    st.session_state.question_database = []
if 'syllabus_topics' not in st.session_state:
    st.session_state.syllabus_topics = []
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = {}

class AdvancedAnalyzer:
    def __init__(self):
        self.question_database = []
        self.topic_weights = {}
        self.trend_analysis = {}
    
    def add_question_paper(self, questions, metadata=None):
        paper_data = {
            'questions': questions,
            'metadata': metadata or {},
            'timestamp': datetime.now()
        }
        self.question_database.append(paper_data)
    
    def analyze_topic_distribution(self):
        all_topics = []
        topic_marks = defaultdict(int)
        topic_frequency = Counter()
        
        for paper in self.question_database:
            for q in paper['questions']:
                topic = q.get('topic', 'Unknown')
                marks = q.get('marks', 1)
                all_topics.append(topic)
                topic_marks[topic] += marks
                topic_frequency[topic] += 1
        
        total_marks = sum(topic_marks.values())
        topic_weightage = {topic: (marks/total_marks)*100 for topic, marks in topic_marks.items()} if total_marks > 0 else {}
        
        return {
            'topic_frequency': dict(topic_frequency),
            'topic_weightage': topic_weightage,
            'total_questions': len(all_topics),
            'unique_topics': len(set(all_topics))
        }
    
    def predict_likely_questions(self, syllabus_topics, num_predictions=10):
        topic_analysis = self.analyze_topic_distribution()
        predictions = []
        
        for topic in syllabus_topics:
            topic_freq = topic_analysis['topic_frequency'].get(topic, 0)
            total_questions = topic_analysis['total_questions']
            topic_probability = (topic_freq / total_questions) * 100 if total_questions > 0 else 0
            
            # Get most common question types for this topic
            topic_questions = []
            for paper in self.question_database:
                for q in paper['questions']:
                    if q.get('topic', '').lower() == topic.lower():
                        topic_questions.append(q)
            
            if topic_questions:
                type_counts = Counter(q.get('type', 'Unknown') for q in topic_questions)
                most_common_type = type_counts.most_common(1)[0][0] if type_counts else 'Short Answer'
                confidence = min(95, topic_probability + 20)
                
                predictions.append({
                    'topic': topic,
                    'question_type': most_common_type,
                    'probability': topic_probability,
                    'confidence': confidence,
                    'historical_frequency': topic_freq,
                    'recommended_marks': self._get_recommended_marks(most_common_type)
                })
        
        predictions.sort(key=lambda x: x['probability'], reverse=True)
        return predictions[:num_predictions]
    
    def _get_recommended_marks(self, question_type):
        type_marks = []
        for paper in self.question_database:
            for q in paper['questions']:
                if q.get('type') == question_type:
                    type_marks.append(q.get('marks', 1))
        
        if type_marks:
            return int(np.mean(type_marks))
        else:
            defaults = {'MCQ': 1, 'Short Answer': 3, 'Long Answer': 8, 'Case Study': 10}
            return defaults.get(question_type, 2)
    
    def identify_hot_topics(self, threshold_percentage=10.0):
        topic_analysis = self.analyze_topic_distribution()
        hot_topics = []
        
        for topic, weightage in topic_analysis['topic_weightage'].items():
            if weightage >= threshold_percentage:
                hot_topics.append({
                    'topic': topic,
                    'weightage': weightage,
                    'frequency': topic_analysis['topic_frequency'].get(topic, 0),
                    'status': 'Hot Topic'
                })
        
        return sorted(hot_topics, key=lambda x: x['weightage'], reverse=True)

# Initialize analyzer
if 'analyzer' not in st.session_state:
    st.session_state.analyzer = AdvancedAnalyzer()

def main():
    st.markdown('<h1 class="main-header">🤖 AI Question Paper Maker & Exam Pattern Analyzer</h1>', unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    mode = st.sidebar.selectbox(
        "Select Mode",
        ["📊 Pattern Analysis", "📝 Question Paper Generation", "📈 Analytics Dashboard", "📋 Report Generation"]
    )
    
    if mode == "📊 Pattern Analysis":
        pattern_analysis_page()
    elif mode == "📝 Question Paper Generation":
        question_generation_page()
    elif mode == "📈 Analytics Dashboard":
        analytics_dashboard_page()
    elif mode == "📋 Report Generation":
        report_generation_page()

def pattern_analysis_page():
    st.markdown('<h2 class="section-header">📊 Exam Pattern Analysis</h2>', unsafe_allow_html=True)
    
    st.write("Upload multiple previous question papers to analyze patterns and predict future questions.")
    
    # File upload section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_files = st.file_uploader(
            "Upload Previous Question Papers",
            type=['pdf', 'docx', 'txt'],
            accept_multiple_files=True,
            help="Upload multiple files to get better pattern analysis"
        )
    
    with col2:
        st.markdown("### Analysis Parameters")
        years_back = st.slider("Analysis Period (Years)", 1, 10, 5)
        confidence_threshold = st.slider("Confidence Threshold (%)", 50, 95, 70)
    
    if uploaded_files:
        st.markdown('<div class="success-message">📁 Files uploaded successfully!</div>', unsafe_allow_html=True)
        
        # Process uploaded files
        if st.button("🔍 Analyze Patterns", type="primary"):
            with st.spinner("Analyzing question papers..."):
                process_uploaded_files(uploaded_files)
                st.success("Analysis completed!")
        
        # Display analysis results
        if st.session_state.analyzer.question_database:
            display_pattern_analysis_results(years_back, confidence_threshold)

def process_uploaded_files(uploaded_files):
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i, file in enumerate(uploaded_files):
        status_text.text(f"Processing {file.name}...")
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.name)[1]) as tmp_file:
            tmp_file.write(file.getbuffer())
            tmp_file_path = tmp_file.name
        
        try:
            # Extract text from file
            ingestor = DocumentIngestor(tmp_file_path)
            ext = os.path.splitext(file.name)[-1].lower()
            
            if ext == '.pdf':
                text_list = ingestor.parse_pdf()
            elif ext in ['.docx', '.doc']:
                text_list = ingestor.parse_word()
            elif ext in ['.txt', '.text']:
                text_list = ingestor.parse_text()
            else:
                text_list = []
            
            # Extract questions
            questions = ingestor.extract_questions(text_list)
            
            # Convert to structured format
            structured_questions = []
            for q in questions:
                structured_questions.append({
                    'question': q,
                    'type': 'Unknown',
                    'topic': 'Unknown',
                    'bloom_level': 'Unknown',
                    'marks': 1
                })
            
            # Add to analyzer
            paper_metadata = {
                'filename': file.name,
                'year': datetime.now().year,
                'total_questions': len(structured_questions)
            }
            
            st.session_state.analyzer.add_question_paper(structured_questions, paper_metadata)
            
        except Exception as e:
            st.error(f"Error processing {file.name}: {str(e)}")
        finally:
            os.unlink(tmp_file_path)
        
        progress_bar.progress((i + 1) / len(uploaded_files))
    
    status_text.text("Processing completed!")
    progress_bar.empty()

def display_pattern_analysis_results(years_back, confidence_threshold):
    st.markdown('<h3 class="section-header">📊 Analysis Results</h3>', unsafe_allow_html=True)
    
    # Get analysis data
    topic_analysis = st.session_state.analyzer.analyze_topic_distribution()
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Papers", len(st.session_state.analyzer.question_database))
    
    with col2:
        st.metric("Total Questions", topic_analysis.get('total_questions', 0))
    
    with col3:
        st.metric("Unique Topics", topic_analysis.get('unique_topics', 0))
    
    with col4:
        st.metric("Analysis Period", f"{years_back} years")
    
    # Topic distribution
    st.subheader("📈 Topic Distribution")
    if topic_analysis.get('topic_weightage'):
        topic_df = pd.DataFrame([
            {'Topic': topic, 'Weightage (%)': weight}
            for topic, weight in topic_analysis['topic_weightage'].items()
        ])
        
        fig = px.pie(
            topic_df,
            values='Weightage (%)',
            names='Topic',
            title='Topic Weightage Distribution'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Hot topics
    st.subheader("🔥 Hot Topics")
    hot_topics = st.session_state.analyzer.identify_hot_topics(threshold_percentage=10.0)
    if hot_topics:
        hot_topics_df = pd.DataFrame(hot_topics)
        st.dataframe(hot_topics_df, use_container_width=True)
    
    # Predictions
    st.subheader("🔮 Predictions")
    if st.button("Generate Predictions"):
        if st.session_state.syllabus_topics:
            predictions = st.session_state.analyzer.predict_likely_questions(st.session_state.syllabus_topics, num_predictions=10)
            if predictions:
                pred_df = pd.DataFrame(predictions)
                st.dataframe(pred_df, use_container_width=True)
        else:
            st.warning("Please provide syllabus topics for predictions")

def question_generation_page():
    st.markdown('<h2 class="section-header">📝 Question Paper Generation</h2>', unsafe_allow_html=True)
    
    # Syllabus input
    st.subheader("📚 Syllabus Input")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        syllabus_file = st.file_uploader("Upload Syllabus", type=['pdf', 'docx', 'txt'])
        syllabus_text = ""
        
        if syllabus_file:
            # Process syllabus file
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(syllabus_file.name)[1]) as tmp_file:
                tmp_file.write(syllabus_file.getbuffer())
                tmp_file_path = tmp_file.name
            
            try:
                ingestor = DocumentIngestor(tmp_file_path)
                ext = os.path.splitext(syllabus_file.name)[-1].lower()
                
                if ext == '.pdf':
                    text_list = ingestor.parse_pdf()
                elif ext in ['.docx', '.doc']:
                    text_list = ingestor.parse_word()
                elif ext in ['.txt', '.text']:
                    text_list = ingestor.parse_text()
                else:
                    text_list = []
                
                syllabus_text = '\n'.join(text_list)
                st.text_area("Extracted Syllabus", syllabus_text, height=200)
                
            except Exception as e:
                st.error(f"Error processing syllabus: {str(e)}")
            finally:
                os.unlink(tmp_file_path)
        else:
            syllabus_text = st.text_area("Or paste syllabus topics (one per line)", height=200)
    
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
            st.session_state.syllabus_topics = topics
            
            if topics:
                with st.spinner("Generating question paper..."):
                    # Generate questions using existing function
                    questions = generate_questions(topics, question_types, total_questions)
                    
                    # Calculate total marks
                    total_assigned_marks = sum(assign_marks(q) for q in questions)
                    
                    # Store in session state
                    st.session_state.current_paper = {
                        'paper_info': {
                            'title': exam_title,
                            'total_questions': len(questions),
                            'total_marks': total_assigned_marks,
                            'duration': duration
                        },
                        'questions': questions
                    }
                    
                    st.success("Question paper generated successfully!")
                    
                    # Display generated paper
                    display_generated_paper(st.session_state.current_paper)
            else:
                st.error("No topics found in syllabus!")
        else:
            st.error("Please provide syllabus content!")

def display_generated_paper(question_paper):
    st.markdown('<h3 class="section-header">📄 Generated Question Paper</h3>', unsafe_allow_html=True)
    
    paper_info = question_paper.get('paper_info', {})
    questions = question_paper.get('questions', [])
    
    # Paper header
    st.markdown(f"**{paper_info.get('title', 'Question Paper')}**")
    st.markdown(f"**Total Marks:** {paper_info.get('total_marks', 0)} | **Duration:** {paper_info.get('duration', 0)} minutes")
    
    # Display questions
    st.subheader("Questions")
    
    for i, question in enumerate(questions, 1):
        with st.expander(f"Q{i} ({question['type']}, {question['bloom_level']}, {question['topic']}, {assign_marks(question)} marks)"):
            st.write(f"**Question:** {question['question']}")
            
            # Generate model answer
            if st.button(f"Generate Answer for Q{i}", key=f"answer_{i}"):
                model_answer = generate_model_answer(question)
                st.markdown("**Model Answer:**")
                st.write(model_answer)
    
    # Analytics
    st.subheader("📊 Paper Analytics")
    analytics = compute_analytics(questions)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**Question Type Distribution:**")
        type_df = pd.DataFrame([
            {'Type': k, 'Count': v} for k, v in analytics['type_counts'].items()
        ])
        fig1 = px.bar(type_df, x='Type', y='Count', title='Question Types')
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.write("**Bloom's Level Distribution:**")
        bloom_df = pd.DataFrame([
            {'Level': k, 'Count': v} for k, v in analytics['bloom_counts'].items()
        ])
        fig2 = px.bar(bloom_df, x='Level', y='Count', title='Cognitive Levels')
        st.plotly_chart(fig2, use_container_width=True)
    
    with col3:
        st.write("**Topic Coverage:**")
        topic_df = pd.DataFrame([
            {'Topic': k, 'Count': v} for k, v in analytics['topic_counts'].items()
        ])
        fig3 = px.bar(topic_df, x='Topic', y='Count', title='Topic Distribution')
        st.plotly_chart(fig3, use_container_width=True)
    
    # Export options
    st.subheader("📤 Export Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📄 Export as Text"):
            export_text = format_export_text(questions)
            st.download_button('Download as Text', export_text, file_name='question_paper.txt')
    
    with col2:
        if st.button("📊 Export as Word Document"):
            docx_filename = 'question_paper.docx'
            format_export_docx(questions, docx_filename)
            with open(docx_filename, 'rb') as f:
                st.download_button('Download as Word (.docx)', f, file_name=docx_filename)

def analytics_dashboard_page():
    st.markdown('<h2 class="section-header">📈 Analytics Dashboard</h2>', unsafe_allow_html=True)
    
    if not st.session_state.analyzer.question_database:
        st.warning("No data available for analytics. Please upload question papers first.")
        return
    
    # Get analytics data
    topic_analysis = st.session_state.analyzer.analyze_topic_distribution()
    
    # Dashboard metrics
    st.subheader("📊 Key Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Papers", len(st.session_state.analyzer.question_database))
    
    with col2:
        st.metric("Total Questions", topic_analysis.get('total_questions', 0))
    
    with col3:
        st.metric("Unique Topics", topic_analysis.get('unique_topics', 0))
    
    with col4:
        st.metric("Average Questions/Paper", 
                 topic_analysis.get('total_questions', 0) // len(st.session_state.analyzer.question_database) if st.session_state.analyzer.question_database else 0)
    
    # Visualizations
    st.subheader("📈 Visualizations")
    
    # Topic distribution
    if topic_analysis.get('topic_weightage'):
        topic_df = pd.DataFrame([
            {'Topic': topic, 'Weightage (%)': weight}
            for topic, weight in topic_analysis['topic_weightage'].items()
        ])
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig1 = px.pie(
                topic_df,
                values='Weightage (%)',
                names='Topic',
                title='Topic Weightage Distribution'
            )
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            fig2 = px.bar(
                topic_df,
                x='Topic',
                y='Weightage (%)',
                title='Topic Weightage (Bar Chart)',
                color='Weightage (%)',
                color_continuous_scale='viridis'
            )
            st.plotly_chart(fig2, use_container_width=True)

def report_generation_page():
    st.markdown('<h2 class="section-header">📋 Report Generation</h2>', unsafe_allow_html=True)
    
    if not st.session_state.analyzer.question_database:
        st.warning("No data available for report generation. Please upload question papers first.")
        return
    
    if 'current_paper' not in st.session_state:
        st.warning("No question paper available for report generation. Please generate a question paper first.")
        return
    
    st.subheader("📊 Generate Comprehensive Report")
    
    # Report options
    col1, col2 = st.columns(2)
    
    with col1:
        include_predictions = st.checkbox("Include Predictions", value=True)
        include_visualizations = st.checkbox("Include Visualizations", value=True)
    
    with col2:
        report_format = st.selectbox("Report Format", ["JSON", "Text"])
        include_historical_comparison = st.checkbox("Include Historical Comparison", value=True)
    
    if st.button("📋 Generate Report", type="primary"):
        with st.spinner("Generating comprehensive report..."):
            # Generate report
            report = generate_comprehensive_report(
                st.session_state.current_paper,
                include_predictions,
                include_visualizations,
                include_historical_comparison
            )
            
            st.success("Report generated successfully!")
            
            # Display report
            st.subheader("📋 Generated Report")
            st.json(report)
            
            # Export
            if report_format == "JSON":
                report_json = json.dumps(report, indent=2, default=str)
                st.download_button(
                    label="Download JSON Report",
                    data=report_json,
                    file_name="question_paper_report.json",
                    mime="application/json"
                )

def generate_comprehensive_report(question_paper, include_predictions=True, include_visualizations=True, include_historical_comparison=True):
    """Generate a comprehensive report"""
    report = {
        'metadata': {
            'generated_at': datetime.now().isoformat(),
            'paper_title': question_paper.get('paper_info', {}).get('title', 'Generated Question Paper'),
            'total_questions': question_paper.get('paper_info', {}).get('total_questions', 0),
            'total_marks': question_paper.get('paper_info', {}).get('total_marks', 0),
            'duration': question_paper.get('paper_info', {}).get('duration', 180)
        },
        'paper_analysis': analyze_question_paper(question_paper),
        'topic_analysis': st.session_state.analyzer.analyze_topic_distribution(),
        'predictions': [],
        'recommendations': generate_recommendations(question_paper)
    }
    
    if include_predictions and st.session_state.syllabus_topics:
        report['predictions'] = st.session_state.analyzer.predict_likely_questions(st.session_state.syllabus_topics, num_predictions=10)
    
    if include_historical_comparison:
        report['historical_comparison'] = {
            'total_papers_analyzed': len(st.session_state.analyzer.question_database),
            'analysis_period': 'Current session'
        }
    
    return report

def analyze_question_paper(question_paper):
    """Analyze the generated question paper"""
    questions = question_paper.get('questions', [])
    
    if not questions:
        return {}
    
    # Basic statistics
    total_questions = len(questions)
    total_marks = sum(assign_marks(q) for q in questions)
    avg_marks_per_question = total_marks / total_questions if total_questions > 0 else 0
    
    # Question type distribution
    type_distribution = Counter(q.get('type', 'Unknown') for q in questions)
    
    # Topic distribution
    topic_distribution = Counter(q.get('topic', 'Unknown') for q in questions)
    
    # Bloom's level distribution
    bloom_distribution = Counter(q.get('bloom_level', 'Unknown') for q in questions)
    
    return {
        'total_questions': total_questions,
        'total_marks': total_marks,
        'average_marks_per_question': avg_marks_per_question,
        'question_type_distribution': dict(type_distribution),
        'topic_distribution': dict(topic_distribution),
        'bloom_distribution': dict(bloom_distribution)
    }

def generate_recommendations(question_paper):
    """Generate recommendations for improving the question paper"""
    recommendations = []
    
    questions = question_paper.get('questions', [])
    if not questions:
        return recommendations
    
    # Analyze topic coverage
    topic_distribution = Counter(q.get('topic', 'Unknown') for q in questions)
    total_questions = len(questions)
    
    for topic, count in topic_distribution.items():
        percentage = (count / total_questions) * 100
        if percentage > 20:
            recommendations.append({
                'type': 'topic_balance',
                'issue': f'Topic "{topic}" has high coverage ({percentage:.1f}%)',
                'recommendation': f'Consider reducing questions on {topic} to improve balance',
                'priority': 'high' if percentage > 30 else 'medium'
            })
    
    # Analyze cognitive levels
    bloom_distribution = Counter(q.get('bloom_level', 'Unknown') for q in questions)
    higher_order_skills = ['Analyze', 'Evaluate', 'Create']
    higher_order_count = sum(bloom_distribution.get(level, 0) for level in higher_order_skills)
    higher_order_percentage = (higher_order_count / total_questions) * 100
    
    if higher_order_percentage < 30:
        recommendations.append({
            'type': 'cognitive_balance',
            'issue': f'Low coverage of higher-order thinking skills ({higher_order_percentage:.1f}%)',
            'recommendation': 'Increase questions requiring analysis, evaluation, and creation',
            'priority': 'high'
        })
    
    return recommendations

if __name__ == "__main__":
    main() 