# 🚀 Setup Guide - Enhanced Question Paper Maker System

## 📋 Prerequisites

Before installing the system, make sure you have:

1. **Python 3.8 or higher** installed on your system
2. **pip** (Python package installer) available
3. **Windows Command Prompt** or **PowerShell** access

## 🔧 Installation Methods

### Method 1: Automated Setup (Recommended)

1. **Navigate to the project directory:**
   ```bash
   cd paper
   ```

2. **Run the automated setup script:**
   ```bash
   setup_and_run.bat
   ```

3. **Follow the interactive prompts** to install dependencies and run the application.

### Method 2: Manual Installation

1. **Navigate to the project directory:**
   ```bash
   cd paper
   ```

2. **Install Streamlit:**
   ```bash
   pip install streamlit
   ```

3. **Install other dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Test the installation:**
   ```bash
   python test_system.py
   ```

5. **Run the application:**
   ```bash
   streamlit run web_app.py
   ```

### Method 3: Step-by-step Installation

If you encounter issues with the above methods, try installing dependencies one by one:

```bash
# Core dependencies
pip install streamlit
pip install pandas
pip install plotly
pip install matplotlib
pip install seaborn

# Document processing
pip install pdfplumber
pip install python-docx
pip install pymupdf

# Machine learning and analysis
pip install scikit-learn
pip install numpy
pip install scipy

# Additional utilities
pip install nltk
pip install textblob
pip install wordcloud
pip install networkx
pip install openpyxl
pip install reportlab
pip install Pillow
```

## 🧪 Testing the Installation

### Test 1: Console Demo (No Streamlit Required)
```bash
python demo_console.py
```

This will run a console-based demo showing:
- Question generation
- Analysis functionality
- Classification capabilities
- Advanced features (if available)

### Test 2: System Test
```bash
python test_system.py
```

This will test all core modules and provide detailed feedback.

### Test 3: Streamlit Test
```bash
python -c "import streamlit; print('Streamlit is working!')"
```

## 🚀 Running the Application

### Option 1: Basic Web Application
```bash
streamlit run web_app.py
```

### Option 2: Enhanced Web Application
```bash
streamlit run enhanced_web_app.py
```

### Option 3: Using the Batch File
```bash
setup_and_run.bat
```

## 🌐 Accessing the Application

Once the application starts successfully, it will automatically open in your web browser at:
```
http://localhost:8501
```

If it doesn't open automatically, manually navigate to the URL in your browser.

## 🔍 Troubleshooting

### Issue 1: "streamlit is not recognized"
**Solution:**
```bash
# Try these commands in order:
python -m pip install streamlit
pip install streamlit
python -m streamlit run web_app.py
```

### Issue 2: "No module named 'pandas'"
**Solution:**
```bash
pip install pandas
```

### Issue 3: "Permission denied" errors
**Solution:**
- Run Command Prompt as Administrator
- Or use: `pip install --user streamlit`

### Issue 4: Python not found
**Solution:**
- Make sure Python is installed and added to PATH
- Try: `python --version` to verify installation
- Download Python from: https://www.python.org/downloads/

### Issue 5: Port 8501 already in use
**Solution:**
```bash
# Kill existing process
taskkill /f /im streamlit.exe

# Or use a different port
streamlit run web_app.py --server.port 8502
```

## 📁 File Structure

```
paper/
├── src/                          # Core modules
│   ├── ingest.py                 # Document processing
│   ├── generate.py               # Question generation
│   ├── analyze.py                # Pattern analysis
│   ├── classify.py               # Question classification
│   ├── advanced_analyzer.py      # Enhanced analysis
│   ├── advanced_generator.py     # Enhanced generation
│   ├── model_answer_generator.py # Answer generation
│   └── report_generator.py       # Report creation
├── web_app.py                    # Basic Streamlit app
├── enhanced_web_app.py           # Enhanced Streamlit app
├── setup_and_run.bat             # Automated setup script
├── test_system.py                # System test script
├── demo_console.py               # Console demo
├── requirements.txt              # Dependencies
├── README.md                     # Basic documentation
├── README_ENHANCED.md            # Comprehensive documentation
├── SYSTEM_OVERVIEW.md            # System overview
└── SETUP_GUIDE.md                # This file
```

## 🎯 Quick Start Commands

### For First-Time Users:
```bash
cd paper
setup_and_run.bat
```

### For Experienced Users:
```bash
cd paper
pip install -r requirements.txt
streamlit run enhanced_web_app.py
```

### For Testing Only:
```bash
cd paper
python demo_console.py
```

## 📞 Getting Help

If you encounter any issues:

1. **Check the console output** for error messages
2. **Run the test script** to identify specific problems
3. **Try the console demo** to verify core functionality
4. **Check Python and pip versions** are compatible
5. **Ensure you're in the correct directory** (paper/)

## 🔄 Updating the System

To update the system:

1. **Update dependencies:**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

2. **Test the update:**
   ```bash
   python test_system.py
   ```

3. **Run the application:**
   ```bash
   streamlit run enhanced_web_app.py
   ```

## 🎉 Success Indicators

You'll know the system is working correctly when:

✅ **Console Demo runs without errors**
✅ **Test script shows all green checkmarks**
✅ **Streamlit application opens in browser**
✅ **You can upload files and generate questions**
✅ **Analytics and reports work properly**

---

**Happy Question Paper Making! 🎓** 