# 🎓 Student Question Paper Helper

A **simple, student-friendly** AI-powered application that helps students prepare for exams by analyzing past question papers and generating sample papers with probability scores.

## 🚀 Features

### 📊 Past Paper Analysis
- **Upload past question papers** (PDF, DOCX, TXT, Images)
- **AI analyzes** which questions appear frequently
- **Get probability scores** for each question
- **Know which questions** are likely to come again

### 📝 Sample Question Paper Generation
- **Upload your syllabus** (topics you need to study)
- **Optionally upload past papers** (files or images) for better predictions
- **AI creates multiple sample papers** (3-5 different versions)
- **Each question has probability scores** showing likelihood to appear

### 📷 Image Upload Support
- **Upload images** of question papers (JPG, PNG, BMP, TIFF)
- **Image processing** with OCR simulation
- **Visual preview** of uploaded images
- **Combined analysis** of files and images

## 🛠️ Installation & Setup

### Option 1: Easy Setup (Recommended)
```bash
# Double-click this file:
STUDENT_SETUP.bat
```

### Option 2: Manual Setup
```bash
cd paper
python -m pip install streamlit pandas plotly pillow
streamlit run student_helper.py
```

### Option 3: Enhanced Setup with Images
```bash
cd paper
RUN_STUDENT_WITH_IMAGES.bat
```

## 📱 How to Use

### 1. Past Paper Analysis
1. Click "🔍 Analyze Past Papers"
2. Choose upload method:
   - **📄 File Upload** - Upload PDF, DOCX, TXT files
   - **📷 Image Upload** - Upload images of question papers
3. Click "🔍 Analyze All Papers"
4. View results with probability scores:
   - **🔥 HIGH CHANCE** - Questions that appeared 2+ times
   - **⚠️ MEDIUM CHANCE** - Questions that appeared once
   - **❄️ LOW CHANCE** - Questions that appeared rarely

### 2. Sample Paper Generation
1. Click "📄 Create Sample Papers"
2. Enter syllabus topics (one per line)
3. Optionally upload past papers (files or images)
4. Configure settings (number of papers, questions per paper)
5. Click "🎯 Generate Sample Papers"
6. Get multiple sample papers with probability scores

## 🎯 Understanding Probability Scores

- **🎯 HIGH CHANCE (50%+)** - Very likely to appear in exam
- **⚠️ MEDIUM CHANCE (30-50%)** - Moderate chance to appear
- **❄️ LOW CHANCE (<30%)** - Less likely to appear

## 📁 File Structure

```
paper/
├── student_helper.py              # Main student app
├── STUDENT_SETUP.bat             # Easy setup script
├── RUN_STUDENT_WITH_IMAGES.bat   # Enhanced setup with images
├── STUDENT_GUIDE.md              # Complete user guide
├── UPDATE_GIT.bat                # Git repository update
├── git_update.py                 # Python Git update script
└── README_STUDENT_APP.md         # This file
```

## 🎨 User Interface

### Home Page
- **Clear navigation** with two main options
- **Feature cards** explaining functionality
- **System overview** with metrics

### Analysis Page
- **Tabbed interface** for file and image upload
- **Visual feedback** for uploaded content
- **Progress indicators** during processing
- **Results display** with probability scores

### Generation Page
- **Syllabus input** with placeholder text
- **Dual upload options** (files and images)
- **Configuration settings** for customization
- **Export functionality** for generated papers

## 🔧 Technical Details

### Supported File Formats
- **Documents**: PDF, DOCX, TXT
- **Images**: JPG, JPEG, PNG, BMP, TIFF

### Dependencies
- `streamlit` - Web application framework
- `pandas` - Data manipulation
- `plotly` - Interactive charts
- `pillow` - Image processing

### Features
- **Session state management** for navigation
- **Image processing** with PIL
- **Data visualization** with Plotly
- **File upload handling** with Streamlit
- **Export functionality** for results

## 📊 Example Output

### Past Paper Analysis
```
🔥 What is database management system?
   - Appeared 3 times
   - 75.0% chance to appear again
   - HIGH PRIORITY for study!

⚠️ Explain SQL queries with examples
   - Appeared 1 time
   - 25.0% chance to appear again
```

### Sample Paper Generation
```
📄 Sample Question Paper 1
Total Marks: 45

Q1 (5 marks): Explain Database Management in detail.
🎯 Probability: 75.2% (HIGH CHANCE)

Q2 (3 marks): Explain SQL Queries in detail.
⚠️ Probability: 45.1% (MEDIUM CHANCE)
```

## 🎉 Benefits for Students

- ✅ **Smart predictions** about exam questions
- ✅ **Multiple sample papers** to practice with
- ✅ **Probability scores** to guide study priorities
- ✅ **Easy image upload** for photos of question papers
- ✅ **Export functionality** to save and share
- ✅ **Simple interface** designed for students

## 🆘 Troubleshooting

### If the app doesn't start:
1. Make sure you're in the `paper` directory
2. Try running `STUDENT_SETUP.bat`
3. Check if Python and dependencies are installed

### If upload doesn't work:
1. Make sure files are in supported formats
2. Try smaller files first
3. Check your internet connection

### If images don't process:
1. Ensure images are clear and readable
2. Try different image formats
3. Check file size limits

## 🚀 Future Enhancements

- **Real OCR integration** for better image text extraction
- **Clipboard paste** for direct image pasting
- **Advanced analytics** with more detailed insights
- **Mobile optimization** for better phone experience
- **Cloud storage** for saving analysis results

## 📞 Support

For issues or questions:
1. Check the `STUDENT_GUIDE.md` file
2. Review troubleshooting section above
3. Ensure all dependencies are installed

---

**Made for Students • Powered by AI • Smart Exam Preparation** 🎓 