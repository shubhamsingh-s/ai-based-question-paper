@echo off
echo ========================================
echo Student Question Paper Helper - Setup
echo ========================================
echo.

echo Step 1: Checking current directory...
echo Current directory: %CD%
echo.

echo Step 2: Navigating to correct directory...
cd /d "C:\Users\shubh\paper"
echo Now in: %CD%
echo.

echo Step 3: Installing required packages...
echo.

echo Installing Streamlit and dependencies...
"C:\Users\shubh\AppData\Local\Microsoft\WindowsApps\python3.12.exe" -m pip install streamlit pandas plotly

echo.
echo ========================================
echo Step 4: Starting Student App...
echo ========================================

echo Starting the Student Question Paper Helper...
echo.
echo Features:
echo - 📊 Past Paper Analysis
echo - 📝 Sample Question Paper Generation
echo - 🎯 Probability Scores for Questions
echo.
echo The app will open in your browser automatically.
echo If it doesn't open, go to: http://localhost:8501
echo.
echo Press Ctrl+C to stop the app when you're done.
echo.

"C:\Users\shubh\AppData\Local\Microsoft\WindowsApps\python3.12.exe" -m streamlit run student_helper.py

echo.
echo App stopped.
pause 