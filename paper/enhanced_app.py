import streamlit as st
import pandas as pd
import numpy as np
from typing import List, Dict, Optional
import os
import tempfile
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Import our custom modules
from src.ingest import DocumentIngestor
from src.advanced_analyzer import AdvancedExamAnalyzer
from src.advanced_generator import AdvancedQuestionGenerator
from src.model_answer_generator import ModelAnswerGenerator
from src.report_generator import ReportGenerator

# Page configuration
st.set_page_config(
    page_title="AI Question Paper Maker & Exam Pattern Analyzer",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
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
if 'analyzer' not in st.session_state:
    st.session_state.analyzer = AdvancedExamAnalyzer()
if 'generator' not in st.session_state:
    st.session_state.generator = AdvancedQuestionGenerator()
if 'answer_generator' not in st.session_state:
    st.session_state.answer_generator = ModelAnswerGenerator()
if 'report_generator' not in st.session_state:
    st.session_state.report_generator = ReportGenerator()

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
    """Process uploaded files and extract questions"""
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
                'year': datetime.now().year,  # You could extract this from filename
                'total_questions': len(structured_questions)
            }
            
            st.session_state.analyzer.add_question_paper(structured_questions, paper_metadata)
            
        except Exception as e:
            st.error(f"Error processing {file.name}: {str(e)}")
        finally:
            # Clean up temporary file
            os.unlink(tmp_file_path)
        
        progress_bar.progress((i + 1) / len(uploaded_files))
    
    status_text.text("Processing completed!")
    progress_bar.empty()

def display_pattern_analysis_results(years_back, confidence_threshold):
    """Display pattern analysis results"""
    st.markdown('<h3 class="section-header">📊 Analysis Results</h3>', unsafe_allow_html=True)
    
    # Get analysis data
    topic_analysis = st.session_state.analyzer.analyze_topic_distribution()
    type_analysis = st.session_state.analyzer.analyze_question_types()
    bloom_analysis = st.session_state.analyzer.analyze_bloom_levels()
    temporal_trends = st.session_state.analyzer.analyze_temporal_trends(years_back)
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Papers", topic_analysis.get('total_questions', 0))
    
    with col2:
        st.metric("Unique Topics", topic_analysis.get('unique_topics', 0))
    
    with col3:
        st.metric("Question Types", len(type_analysis.get('type_distribution', {})))
    
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
    
    # Question type distribution
    st.subheader("📊 Question Type Distribution")
    if type_analysis.get('type_distribution'):
        type_df = pd.DataFrame([
            {'Type': qtype, 'Count': count}
            for qtype, count in type_analysis['type_distribution'].items()
        ])
        
        fig = px.bar(
            type_df,
            x='Type',
            y='Count',
            title='Question Type Distribution',
            color='Count',
            color_continuous_scale='viridis'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Hot topics
    st.subheader("🔥 Hot Topics")
    hot_topics = st.session_state.analyzer.identify_hot_topics(threshold_percentage=10.0)
    if hot_topics:
        hot_topics_df = pd.DataFrame(hot_topics)
        st.dataframe(hot_topics_df, use_container_width=True)
    
    # Declining topics
    st.subheader("📉 Declining Topics")
    declining_topics = st.session_state.analyzer.identify_declining_topics(years_back)
    if declining_topics:
        declining_df = pd.DataFrame(declining_topics)
        st.dataframe(declining_df, use_container_width=True)

def question_generation_page():
    st.markdown('<h2 class="section-header">📝 Question Paper Generation</h2>', unsafe_allow_html=True)
    
    # Syllabus input
    st.subheader("📚 Syllabus Input")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        syllabus_file = st.file_uploader("Upload Syllabus", type=['pdf', 'docx', 'txt'])
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
        
        difficulty_distribution = st.slider("Easy:Medium:Hard Ratio", 0.0, 1.0, 0.3, help="Easy questions percentage")
        medium_percentage = st.slider("Medium questions percentage", 0.0, 1.0, 0.5)
        hard_percentage = 1.0 - difficulty_distribution - medium_percentage
        
        st.write(f"Difficulty Distribution: Easy {difficulty_distribution:.1%}, Medium {medium_percentage:.1%}, Hard {hard_percentage:.1%}")
    
    # Generate question paper
    if st.button("🎯 Generate Question Paper", type="primary"):
        if syllabus_text:
            # Parse topics
            topics = [line.strip() for line in syllabus_text.split('\n') if line.strip()]
            
            if topics:
                with st.spinner("Generating question paper..."):
                    # Prepare exam configuration
                    exam_config = {
                        'title': exam_title,
                        'total_questions': total_questions,
                        'total_marks': total_marks,
                        'duration': duration,
                        'question_types': question_types,
                        'instructions': f"Answer all questions. Total marks: {total_marks}, Duration: {duration} minutes."
                    }
                    
                    difficulty_dist = {
                        'Easy': difficulty_distribution,
                        'Medium': medium_percentage,
                        'Hard': hard_percentage
                    }
                    
                    # Generate question paper
                    question_paper = st.session_state.generator.generate_question_paper(
                        topics, exam_config, difficulty_dist
                    )
                    
                    # Store in session state
                    st.session_state.current_paper = question_paper
                    
                    st.success("Question paper generated successfully!")
                    
                    # Display generated paper
                    display_generated_paper(question_paper)
            else:
                st.error("No topics found in syllabus!")
        else:
            st.error("Please provide syllabus content!")

def display_generated_paper(question_paper):
    """Display the generated question paper"""
    st.markdown('<h3 class="section-header">📄 Generated Question Paper</h3>', unsafe_allow_html=True)
    
    paper_info = question_paper.get('paper_info', {})
    questions = question_paper.get('questions', [])
    
    # Paper header
    st.markdown(f"**{paper_info.get('title', 'Question Paper')}**")
    st.markdown(f"**Total Marks:** {paper_info.get('total_marks', 0)} | **Duration:** {paper_info.get('duration', 0)} minutes")
    st.markdown(f"**Instructions:** {paper_info.get('instructions', '')}")
    
    # Display questions
    st.subheader("Questions")
    
    for i, question in enumerate(questions, 1):
        with st.expander(f"Q{i} ({question['type']}, {question['bloom_level']}, {question['difficulty']}, {question['marks']} marks)"):
            st.write(f"**Question:** {question['question']}")
            
            # Generate model answer
            if st.button(f"Generate Answer for Q{i}", key=f"answer_{i}"):
                model_answer = st.session_state.answer_generator.generate_model_answer(question)
                
                st.markdown("**Model Answer:**")
                st.write(model_answer['main_answer'])
                
                st.markdown("**Key Points:**")
                for point in model_answer['key_points']:
                    st.write(f"• {point}")
                
                st.markdown("**Alternative Approaches:**")
                for approach in model_answer['alternative_approaches']:
                    st.write(f"• {approach}")
    
    # Paper analysis
    analysis = question_paper.get('analysis', {})
    if analysis:
        st.subheader("📊 Paper Analysis")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Coverage %", f"{analysis.get('coverage_percentage', 0):.1f}%")
        
        with col2:
            st.metric("Avg Marks/Question", f"{analysis.get('average_marks_per_question', 0):.1f}")
        
        with col3:
            st.metric("Total Marks", analysis.get('total_marks', 0))
        
        # Export options
        st.subheader("📤 Export Options")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📄 Export as Word"):
                # Generate Word document
                pass
        
        with col2:
            if st.button("📊 Export as PDF"):
                # Generate PDF
                pass
        
        with col3:
            if st.button("📈 Generate Report"):
                # Generate comprehensive report
                pass

def analytics_dashboard_page():
    st.markdown('<h2 class="section-header">📈 Analytics Dashboard</h2>', unsafe_allow_html=True)
    
    if not st.session_state.analyzer.question_database:
        st.warning("No data available for analytics. Please upload question papers first.")
        return
    
    # Get analytics data
    analytics_report = st.session_state.analyzer.generate_analytics_report()
    visualizations = st.session_state.analyzer.create_visualizations()
    
    # Dashboard metrics
    st.subheader("📊 Key Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Papers", analytics_report.get('total_papers_analyzed', 0))
    
    with col2:
        topic_analysis = analytics_report.get('topic_analysis', {})
        st.metric("Unique Topics", topic_analysis.get('unique_topics', 0))
    
    with col3:
        type_analysis = analytics_report.get('type_analysis', {})
        st.metric("Question Types", len(type_analysis.get('type_distribution', {})))
    
    with col4:
        bloom_analysis = analytics_report.get('bloom_analysis', {})
        st.metric("Cognitive Levels", len(bloom_analysis.get('bloom_distribution', {})))
    
    # Visualizations
    st.subheader("📈 Visualizations")
    
    if visualizations:
        # Topic distribution
        if 'topic_distribution' in visualizations:
            st.plotly_chart(visualizations['topic_distribution'], use_container_width=True)
        
        # Question type distribution
        if 'type_distribution' in visualizations:
            st.plotly_chart(visualizations['type_distribution'], use_container_width=True)
        
        # Cognitive levels
        if 'bloom_distribution' in visualizations:
            st.plotly_chart(visualizations['bloom_distribution'], use_container_width=True)
        
        # Temporal trends
        if 'temporal_trends' in visualizations and visualizations['temporal_trends']:
            st.plotly_chart(visualizations['temporal_trends'], use_container_width=True)
    
    # Hot topics and predictions
    st.subheader("🔥 Hot Topics & Predictions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        hot_topics = analytics_report.get('hot_topics', [])
        if hot_topics:
            hot_df = pd.DataFrame(hot_topics)
            st.dataframe(hot_df, use_container_width=True)
    
    with col2:
        # Generate predictions
        if st.button("🔮 Generate Predictions"):
            # Get topics from uploaded papers
            topic_analysis = analytics_report.get('topic_analysis', {})
            topics = list(topic_analysis.get('topic_frequency', {}).keys())
            
            if topics:
                predictions = st.session_state.analyzer.predict_likely_questions(topics, num_predictions=10)
                pred_df = pd.DataFrame(predictions)
                st.dataframe(pred_df, use_container_width=True)

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
        include_recommendations = st.checkbox("Include Recommendations", value=True)
    
    with col2:
        report_format = st.selectbox("Report Format", ["Word Document", "PDF", "JSON"])
        include_historical_comparison = st.checkbox("Include Historical Comparison", value=True)
    
    if st.button("📋 Generate Report", type="primary"):
        with st.spinner("Generating comprehensive report..."):
            # Get analysis data
            analytics_report = st.session_state.analyzer.generate_analytics_report()
            
            # Generate predictions if requested
            predictions = None
            if include_predictions:
                topic_analysis = analytics_report.get('topic_analysis', {})
                topics = list(topic_analysis.get('topic_frequency', {}).keys())
                if topics:
                    predictions = st.session_state.analyzer.predict_likely_questions(topics, num_predictions=10)
            
            # Generate comprehensive report
            report = st.session_state.report_generator.generate_comprehensive_report(
                st.session_state.current_paper,
                analytics_report,
                predictions,
                analytics_report if include_historical_comparison else None
            )
            
            st.success("Report generated successfully!")
            
            # Display report summary
            display_report_summary(report)
            
            # Export options
            st.subheader("📤 Export Report")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if report_format == "Word Document":
                    if st.button("📄 Download Word Report"):
                        filename = st.session_state.report_generator.export_report_to_docx(report)
                        with open(filename, 'rb') as f:
                            st.download_button(
                                label="Download Word Report",
                                data=f.read(),
                                file_name=filename,
                                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                            )
            
            with col2:
                if report_format == "JSON":
                    if st.button("📊 Download JSON Report"):
                        filename = st.session_state.report_generator.export_report_to_json(report)
                        with open(filename, 'r') as f:
                            st.download_button(
                                label="Download JSON Report",
                                data=f.read(),
                                file_name=filename,
                                mime="application/json"
                            )

def display_report_summary(report):
    """Display a summary of the generated report"""
    st.subheader("📋 Report Summary")
    
    metadata = report.get('metadata', {})
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Report Information:**")
        st.write(f"• Generated: {metadata.get('generated_at', 'Unknown')}")
        st.write(f"• Paper Title: {metadata.get('paper_title', 'Unknown')}")
        st.write(f"• Total Questions: {metadata.get('total_questions', 0)}")
        st.write(f"• Total Marks: {metadata.get('total_marks', 0)}")
    
    with col2:
        st.markdown("**Analysis Coverage:**")
        st.write(f"• Topic Analysis: ✅")
        st.write(f"• Cognitive Analysis: ✅")
        st.write(f"• Difficulty Analysis: ✅")
        st.write(f"• Historical Comparison: ✅")
    
    # Recommendations
    recommendations = report.get('recommendations', [])
    if recommendations:
        st.subheader("💡 Key Recommendations")
        for i, rec in enumerate(recommendations[:5], 1):  # Show top 5
            st.markdown(f"**{i}. {rec['type'].title()}:** {rec['issue']}")
            st.markdown(f"   *Recommendation:* {rec['recommendation']}")
            st.markdown(f"   *Priority:* {rec['priority']}")

if __name__ == "__main__":
    main() 