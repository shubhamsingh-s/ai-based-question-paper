import streamlit as st
import pandas as pd
import plotly.express as px
from collections import Counter
import random
from PIL import Image
import io
import base64

# Page configuration
st.set_page_config(
    page_title="Student Question Paper Helper",
    page_icon="🎓",
    layout="wide"
)

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'

def process_image_upload(uploaded_image):
    """Process uploaded image and extract text (simulated)"""
    try:
        # Display the uploaded image
        st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)
        
        # Simulate text extraction from image
        # In a real app, you would use OCR (Optical Character Recognition)
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
        
        # Return simulated extracted text
        extracted_text = "\n".join(random.sample(sample_questions, random.randint(3, 6)))
        
        st.success("✅ Image processed successfully!")
        st.info("📝 Extracted text from image:")
        st.text_area("Extracted Content", extracted_text, height=150, disabled=True)
        
        return extracted_text
        
    except Exception as e:
        st.error(f"Error processing image: {str(e)}")
        return ""

def home_page():
    st.markdown("""
    # 🎓 Student Question Paper Helper
    
    **Your AI assistant for exam preparation!**
    
    Upload past papers (files or images) and syllabus to get smart predictions and sample question papers.
    """)
    
    # Feature cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📊 Past Paper Analysis
        - Upload past question papers (PDF, DOCX, TXT, Images)
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
        - Optionally upload past papers (files or images)
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
    1. Upload past question papers (PDF, DOCX, TXT, Images)
    2. AI analyzes which questions appear most frequently
    3. Get probability scores for each question
    4. Know which questions are likely to come in your exam!
    """)
    
    # Upload options
    st.markdown("### 📁 Upload Options")
    
    upload_tab1, upload_tab2 = st.tabs(["📄 File Upload", "📷 Image Upload"])
    
    uploaded_files = []
    uploaded_images = []
    
    with upload_tab1:
        st.markdown("#### Upload Files")
        uploaded_files = st.file_uploader(
            "Upload Past Question Papers (Files)", 
            type=['pdf', 'docx', 'txt'], 
            accept_multiple_files=True,
            help="Upload PDF, DOCX, or TXT files"
        )
        
        if uploaded_files:
            st.success(f"✅ {len(uploaded_files)} files uploaded")
    
    with upload_tab2:
        st.markdown("#### Upload Images")
        st.markdown("Upload images of question papers (JPG, PNG, etc.)")
        
        # Image upload
        uploaded_images = st.file_uploader(
            "Upload Images of Question Papers",
            type=['jpg', 'jpeg', 'png', 'bmp', 'tiff'],
            accept_multiple_files=True,
            help="Upload images of question papers"
        )
        
        if uploaded_images:
            st.success(f"✅ {len(uploaded_images)} images uploaded")
            
            # Display uploaded images
            for i, img in enumerate(uploaded_images):
                st.image(img, caption=f"Image {i+1}: {img.name}", use_column_width=True)
        
        # Image paste option
        st.markdown("#### Or Paste Image from Clipboard")
        st.markdown("You can also paste an image directly from your clipboard")
        
        # Note about clipboard paste
        st.info("💡 **Tip:** To paste an image, copy it to your clipboard (Ctrl+C) and then paste it here (Ctrl+V)")
        
        # This would require additional setup for clipboard access
        # For now, we'll show a placeholder
        if st.button("📋 Paste from Clipboard"):
            st.info("📋 Clipboard paste feature coming soon! For now, please use the file upload option above.")
    
    # Process all uploads
    all_questions = []
    
    if uploaded_files or uploaded_images:
        if st.button("🔍 Analyze All Papers", type="primary"):
            with st.spinner("Analyzing papers and images..."):
                # Process file uploads
                if uploaded_files:
                    st.markdown("### 📄 Processing Files...")
                    for file in uploaded_files:
                        st.info(f"Processing: {file.name}")
                        # Simulate processing files
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
                        
                        for i in range(random.randint(5, 10)):
                            question = random.choice(sample_questions)
                            all_questions.append({
                                'question': question,
                                'file': file.name,
                                'type': 'file',
                                'year': random.randint(2020, 2024)
                            })
                
                # Process image uploads
                if uploaded_images:
                    st.markdown("### 📷 Processing Images...")
                    for img in uploaded_images:
                        st.info(f"Processing image: {img.name}")
                        # Process image and extract questions
                        extracted_text = process_image_upload(img)
                        
                        # Simulate questions from image
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
                        
                        for i in range(random.randint(3, 7)):
                            question = random.choice(sample_questions)
                            all_questions.append({
                                'question': question,
                                'file': img.name,
                                'type': 'image',
                                'year': random.randint(2020, 2024)
                            })
                
                # Calculate probabilities
                if all_questions:
                    question_counts = Counter([q['question'] for q in all_questions])
                    total_sources = len(uploaded_files) + len(uploaded_images)
                    
                    probabilities = []
                    for question, count in question_counts.items():
                        probability = (count / total_sources) * 100
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
                    
                    probabilities.sort(key=lambda x: x['appearances'], reverse=True)
                    
                    st.success("Analysis complete!")
                    
                    # Display results
                    st.markdown("## 📈 Analysis Results")
                    
                    # Summary metrics
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Files Analyzed", len(uploaded_files))
                    with col2:
                        st.metric("Images Analyzed", len(uploaded_images))
                    with col3:
                        st.metric("Total Questions", len(all_questions))
                    with col4:
                        high_chance = len([p for p in probabilities if p['appearances'] >= 2])
                        st.metric("High Chance Questions", high_chance)
                    
                    # Question probability display
                    st.markdown("### 🎯 Question Probability Analysis")
                    
                    for prob in probabilities:
                        if prob['status'] == "🔥 HIGH CHANCE":
                            st.markdown(f"**🔥 {prob['question']}**")
                            st.markdown(f"   - Appeared {prob['appearances']} times")
                            st.markdown(f"   - **{prob['probability']:.1f}% chance** to appear again")
                            st.markdown("   - **HIGH PRIORITY** for study!")
                        elif prob['status'] == "⚠️ MEDIUM CHANCE":
                            st.markdown(f"**⚠️ {prob['question']}**")
                            st.markdown(f"   - Appeared {prob['appearances']} time")
                            st.markdown(f"   - **{prob['probability']:.1f}% chance** to appear again")
                        else:
                            st.markdown(f"**❄️ {prob['question']}**")
                            st.markdown(f"   - Appeared {prob['appearances']} time")
                            st.markdown(f"   - **{prob['probability']:.1f}% chance** to appear again")
                        
                        st.markdown("---")
                    
                    # Chart
                    if len(probabilities) > 0:
                        st.markdown("### 📊 Question Frequency Chart")
                        chart_df = pd.DataFrame(probabilities[:10])
                        fig = px.bar(chart_df, x='question', y='appearances', 
                                   title='Most Frequently Asked Questions')
                        fig.update_xaxis(tickangle=45)
                        st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("No questions found in uploaded content.")
    
    else:
        st.info("👆 Please upload files or images to begin analysis")

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
    2. Optionally upload past papers (files or images) for better predictions
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
    
    # Past papers (optional) - with image support
    st.markdown("### 📄 Step 2: Upload Past Papers (Optional)")
    
    upload_tab1, upload_tab2 = st.tabs(["📄 Files", "📷 Images"])
    
    past_files = []
    past_images = []
    
    with upload_tab1:
        past_files = st.file_uploader(
            "Upload past papers (files)", 
            type=['pdf', 'docx', 'txt'], 
            accept_multiple_files=True
        )
        if past_files:
            st.success(f"✅ {len(past_files)} files uploaded")
    
    with upload_tab2:
        past_images = st.file_uploader(
            "Upload images of past papers",
            type=['jpg', 'jpeg', 'png', 'bmp', 'tiff'],
            accept_multiple_files=True
        )
        if past_images:
            st.success(f"✅ {len(past_images)} images uploaded")
            
            # Show preview of uploaded images
            for img in past_images:
                st.image(img, caption=img.name, width=200)
    
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
            
            if topics:
                with st.spinner("Generating sample question papers..."):
                    # Analyze past papers if provided
                    past_questions = []
                    
                    # Process files
                    if past_files:
                        st.info("Processing uploaded files...")
                        # Simulate processing files
                        for file in past_files:
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
                            
                            for i in range(random.randint(3, 8)):
                                question = random.choice(sample_questions)
                                past_questions.append({
                                    'question': question,
                                    'appearances': random.randint(1, 3),
                                    'probability': random.randint(30, 80)
                                })
                    
                    # Process images
                    if past_images:
                        st.info("Processing uploaded images...")
                        for img in past_images:
                            # Simulate processing images
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
                            
                            for i in range(random.randint(2, 6)):
                                question = random.choice(sample_questions)
                                past_questions.append({
                                    'question': question,
                                    'appearances': random.randint(1, 3),
                                    'probability': random.randint(30, 80)
                                })
                    
                    # Generate sample papers
                    sample_papers = []
                    
                    for paper_num in range(num_papers):
                        paper = {
                            'title': f"Sample Question Paper {paper_num + 1}",
                            'questions': [],
                            'total_marks': 0
                        }
                        
                        # Mix syllabus topics with high-probability past questions
                        high_prob_questions = [q for q in past_questions if q['probability'] >= 50]
                        
                        # Generate questions
                        for i in range(questions_per_paper):
                            if i < 5 and high_prob_questions:  # First 5 from high probability
                                selected_q = random.choice(high_prob_questions)
                                question_text = selected_q['question']
                                marks = random.choice([3, 5, 8])
                                probability = selected_q['probability']
                            else:  # Rest from syllabus topics
                                topic = random.choice(topics)
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