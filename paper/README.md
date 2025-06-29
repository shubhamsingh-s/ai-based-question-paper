# AI-powered Question Paper Generator & Exam Pattern Analyzer

## Project Vision
Design an AI-powered system to generate balanced, syllabus-aligned question papers with customizable difficulty, question types (MCQs, short/long answers, case studies), and Bloom's Taxonomy-based cognitive levels. The system will also analyze previous papers (PDF/Word/Text), extract topic trends, topic-wise weightage, question frequency, and predict likely questions with confidence scores. Outputs include formatted question papers, answer keys, and analytical comparison reports with visual analytics.

## Main Modules
- **Document Ingestion & Parsing**: Extract questions and structure from PDF, Word, and text files.
- **Question Classification & Tagging**: Classify question types, map to Bloom's Taxonomy, extract topics, and estimate difficulty.
- **Exam Pattern Analysis**: Analyze topic trends, weightage, frequency, and predict likely questions.
- **Question Paper Generation**: Generate customizable, balanced question papers.
- **Model Answers & Marking Scheme**: Auto-generate model answers and marking schemes.
- **Reporting & Visualization**: Visual analytics and comparison reports.

## Tech Stack
- Python, pdfplumber, python-docx, PyMuPDF, pytesseract, spaCy, transformers, scikit-learn, matplotlib, seaborn, plotly, pandas, jinja2

---

## Getting Started
1. Install dependencies: `pip install -r requirements.txt`
2. Run the main app: `python app.py` 