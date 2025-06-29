# 🚀 Quick Start Guide - Question Paper Maker

## Problem: Streamlit Not Found
If you see `'streamlit' is not recognized as an internal or external command`, follow these steps:

## Solution Options

### Option 1: Use the Complete Setup (Recommended)
```bash
# Double-click or run:
INSTALL_AND_RUN.bat
```

### Option 2: Use Python Setup Script
```bash
# Run the Python setup script:
python setup_and_run.py
```

### Option 3: Manual Installation
```bash
# 1. Install Streamlit
python -m pip install streamlit pandas plotly

# 2. Run the app
python -m streamlit run simple_app.py
```

### Option 4: Use Python 3.12 Directly
```bash
# If you have Python 3.12 installed:
"C:\Users\shubh\AppData\Local\Microsoft\WindowsApps\python3.12.exe" -m pip install streamlit pandas plotly
"C:\Users\shubh\AppData\Local\Microsoft\WindowsApps\python3.12.exe" -m streamlit run simple_app.py
```

## What You'll See
- **Welcome to Question Paper Maker!** header
- Feature cards showing:
  - 📚 Syllabus-Based
  - 🎯 Multiple Types  
  - 📊 Smart Analysis
- Navigation buttons
- System overview metrics

## Troubleshooting

### If Python is not found:
1. Make sure Python is installed
2. Try using the full path to Python 3.12
3. Check if Python is in your PATH

### If packages fail to install:
1. Try upgrading pip: `python -m pip install --upgrade pip`
2. Install packages one by one
3. Check your internet connection

### If the app doesn't open in browser:
1. Go to `http://localhost:8501` manually
2. Check if the port is available
3. Try a different port: `streamlit run simple_app.py --server.port 8502`

## Success!
Once running, you should see the beautiful welcome page with all the features you mentioned! 🎉 