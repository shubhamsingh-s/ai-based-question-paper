import os
print("PYTHON PATH:", os.environ['PATH'])

import streamlit as st

from src.ingest import DocumentIngestor
from src.generate import generate_questions, generate_model_answer, assign_marks, format_export_text, format_export_docx
from src.analyze import compute_analytics, compute_topic_frequency
from src.classify import tag_questions_by_topic

def save_uploaded_file(uploaded_file):
    with open(uploaded_file.name, 'wb') as f:
        f.write(uploaded_file.getbuffer())
    return uploaded_file.name

st.title('AI Exam Assistant')

mode = st.sidebar.selectbox('Select Mode', ['Syllabus Mode', 'Pattern Mode'])

if mode == 'Syllabus Mode':
    st.header('Syllabus Mode')
    st.write('Upload your syllabus or enter it below. Set exam parameters and generate a question paper.')

    # Syllabus upload or text entry
    syllabus_file = st.file_uploader('Upload Syllabus (TXT, DOCX, PDF)', type=['txt', 'docx', 'pdf'])
    syllabus_text = ''
    if syllabus_file is not None:
        file_path = syllabus_file.name
        with open(file_path, 'wb') as f:
            f.write(syllabus_file.getbuffer())
        ingestor = DocumentIngestor(file_path)
        ext = os.path.splitext(file_path)[-1].lower()
        if ext == '.pdf':
            text_list = ingestor.parse_pdf()
        elif ext in ['.docx', '.doc']:
            text_list = ingestor.parse_word()
        elif ext in ['.txt', '.text']:
            text_list = ingestor.parse_text()
        else:
            text_list = []
        syllabus_text = '\n'.join(text_list)
    else:
        syllabus_text = st.text_area('Or paste your syllabus here:')

    # Exam parameters
    st.subheader('Exam Parameters')
    total_marks = st.number_input('Total Marks', min_value=10, max_value=500, value=100)
    duration = st.number_input('Exam Duration (minutes)', min_value=30, max_value=300, value=180)
    difficulty = st.selectbox('Difficulty Level', ['Easy', 'Medium', 'Hard', 'Mixed'])
    question_types = st.multiselect('Question Types', ['MCQ', 'Short Answer', 'Long Answer', 'Case Study'], default=['MCQ', 'Short Answer', 'Long Answer'])
    num_questions = st.number_input('Number of Questions', min_value=1, max_value=50, value=10)

    if st.button('Generate Question Paper'):
        # Parse topics from syllabus text (split by lines, ignore empty)
        topics = [line.strip() for line in syllabus_text.split('\n') if line.strip()]
        if not topics:
            st.warning('No topics found in syllabus!')
        else:
            questions = generate_questions(topics, question_types, num_questions)
            st.success('Generated Question Paper:')
            total_assigned_marks = 0
            for idx, q in enumerate(questions, 1):
                marks = assign_marks(q)
                total_assigned_marks += marks
                st.markdown(f'**Q{idx} ({q["type"]}, {q["bloom_level"]}, {q["topic"]}, {marks} marks):** {q["question"]}')
                model_answer = generate_model_answer(q)
                st.markdown(f'*Model Answer:* {model_answer}')
            st.info(f'Total Assigned Marks: {total_assigned_marks}')
            # Export options
            st.subheader('Export')
            export_text = format_export_text(questions)
            st.download_button('Download as Text', export_text, file_name='question_paper.txt')
            docx_filename = 'question_paper.docx'
            format_export_docx(questions, docx_filename)
            with open(docx_filename, 'rb') as f:
                st.download_button('Download as Word (.docx)', f, file_name=docx_filename)
            # Analytics
            st.subheader('Analytics')
            analytics = compute_analytics(questions)
            st.write('**Question Type Distribution:**')
            st.bar_chart(analytics['type_counts'])
            st.write('**Bloom\'s Level Distribution:**')
            st.bar_chart(analytics['bloom_counts'])
            st.write('**Topic Coverage:**')
            st.bar_chart(analytics['topic_counts'])

elif mode == 'Pattern Mode':
    st.header('Pattern Mode')
    st.write('Upload multiple past question papers (PDF, DOCX, TXT) to analyze trends and predict high-probability questions.')
    uploaded_files = st.file_uploader('Upload Past Papers', type=['pdf', 'docx', 'txt'], accept_multiple_files=True)
    if uploaded_files:
        topics_text = st.text_area('Enter topics for tagging (one per line):')
        topics = [line.strip() for line in topics_text.split('\n') if line.strip()]
        if st.button('Process Papers'):
            all_questions = []
            for file in uploaded_files:
                file_path = file.name
                with open(file_path, 'wb') as f:
                    f.write(file.getbuffer())
                ingestor = DocumentIngestor(file_path)
                ext = os.path.splitext(file_path)[-1].lower()
                if ext == '.pdf':
                    text_list = ingestor.parse_pdf()
                elif ext in ['.docx', '.doc']:
                    text_list = ingestor.parse_word()
                elif ext in ['.txt', '.text']:
                    text_list = ingestor.parse_text()
                else:
                    text_list = []
                questions = ingestor.extract_questions(text_list)
                all_questions.extend(questions)
                st.markdown(f'**{file.name}: {len(questions)} questions extracted**')
                for idx, q in enumerate(questions, 1):
                    st.markdown(f'Q{idx}: {q}')
            st.success(f'Total questions extracted from all files: {len(all_questions)}')
            if topics:
                tagged = tag_questions_by_topic(all_questions, topics)
                st.subheader('Tagged Questions by Topic')
                for idx, (q, topic) in enumerate(tagged, 1):
                    st.markdown(f'Q{idx} [{topic}]: {q}')
                # Analytics: topic frequency
                st.subheader('Topic Frequency Analytics')
                topic_counts = compute_topic_frequency(tagged)
                st.bar_chart(topic_counts)
            else:
                st.info('Enter topics above to enable tagging.')
    else:
        st.write('Please upload at least one past paper.')

uploaded_file = st.file_uploader('Upload a question paper (PDF, DOCX, or TXT)', type=['pdf', 'docx', 'txt'])

if uploaded_file is not None:
    file_path = save_uploaded_file(uploaded_file)
    ingestor = DocumentIngestor(file_path)
    ext = os.path.splitext(file_path)[-1].lower()
    if ext == '.pdf':
        text_list = ingestor.parse_pdf()
    elif ext in ['.docx', '.doc']:
        text_list = ingestor.parse_word()
    elif ext in ['.txt', '.text']:
        text_list = ingestor.parse_text()
    else:
        text_list = []
    st.subheader('Extracted Text:')
    for i, page in enumerate(text_list, 1):
        st.markdown(f'**Page {i}:**')
        st.write(page)
    # Extract and display questions
    questions = ingestor.extract_questions(text_list)
    st.subheader('Extracted Questions:')
    if questions:
        for idx, q in enumerate(questions, 1):
            st.markdown(f'**Q{idx}:** {q}')
    else:
        st.write('No questions found.') 