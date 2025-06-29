# 🎓 Student Question Paper Helper - User Guide

## What This App Does

This is a **simple, student-friendly** app that helps you prepare for exams by:

1. **📊 Analyzing Past Papers** - Upload past question papers and see which questions are likely to come again
2. **📝 Generating Sample Papers** - Upload your syllabus and get multiple sample question papers with probability scores

## 🚀 How to Start

### Option 1: Easy Setup (Recommended)
```bash
# Double-click this file:
STUDENT_SETUP.bat
```

### Option 2: Manual Setup
```bash
cd paper
python -m pip install streamlit pandas plotly
streamlit run student_helper.py
```

## 📊 Feature 1: Past Paper Analysis

### What it does:
- Upload past question papers (PDF, DOCX, TXT)
- AI analyzes which questions appear most frequently
- Shows you probability scores for each question
- Tells you which questions are likely to come again

### How to use:
1. Click "🔍 Analyze Past Papers"
2. Upload your past question papers
3. Click "🔍 Analyze Papers"
4. See results:
   - **🔥 HIGH CHANCE** - Questions that appeared 2+ times (study these!)
   - **⚠️ MEDIUM CHANCE** - Questions that appeared once
   - **❄️ LOW CHANCE** - Questions that appeared rarely

### Example Output:
```
🔥 What is database management system?
   - Appeared 3 times
   - 75.0% chance to appear again
   - HIGH PRIORITY for study!
```

## 📝 Feature 2: Sample Question Paper Generation

### What it does:
- Upload your syllabus (topics you need to study)
- Optionally upload past papers for better predictions
- AI creates multiple sample question papers
- Each question comes with probability scores

### How to use:
1. Click "📄 Create Sample Papers"
2. Enter your syllabus topics (one per line)
3. Optionally upload past papers
4. Configure settings (number of papers, questions per paper)
5. Click "🎯 Generate Sample Papers"
6. Get multiple sample papers with probability scores

### Example Syllabus Input:
```
Database Management
SQL Queries
Data Modeling
Normalization
ACID Properties
Indexing
Transaction Management
```

### Example Output:
```
📄 Sample Question Paper 1
Total Marks: 45

Q1 (5 marks): Explain Database Management in detail.
🎯 Probability: 75.2% (HIGH CHANCE)

Q2 (3 marks): Explain SQL Queries in detail.
⚠️ Probability: 45.1% (MEDIUM CHANCE)
```

## 🎯 Understanding Probability Scores

- **🎯 HIGH CHANCE (50%+)** - Very likely to appear in exam
- **⚠️ MEDIUM CHANCE (30-50%)** - Moderate chance to appear
- **❄️ LOW CHANCE (<30%)** - Less likely to appear

## 📤 Export Options

- Download sample papers as text files
- Save analysis results for later reference
- Print or share with classmates

## 💡 Tips for Best Results

1. **Upload more past papers** = Better predictions
2. **Include recent papers** = More accurate probabilities
3. **Be specific with syllabus topics** = Better question generation
4. **Use the probability scores** to prioritize your study

## 🆘 Troubleshooting

### If the app doesn't start:
1. Make sure you're in the `paper` directory
2. Try running `STUDENT_SETUP.bat`
3. Check if Python is installed

### If upload doesn't work:
1. Make sure files are PDF, DOCX, or TXT format
2. Try smaller files first
3. Check your internet connection

## 🎉 Success!

Once you're using the app, you'll have:
- ✅ Smart predictions about exam questions
- ✅ Multiple sample papers to practice with
- ✅ Probability scores to guide your study
- ✅ Better exam preparation strategy

**Good luck with your exams! 🎓** 