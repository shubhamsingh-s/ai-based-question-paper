@echo off
echo ========================================
echo Question Paper Maker - Complete Setup
echo ========================================
echo.

echo Step 1: Checking Python versions...
echo.

echo Python 3.4 (old):
py --version

echo.
echo Python 3.12 (new):
"C:\Users\shubh\AppData\Local\Microsoft\WindowsApps\python3.12.exe" --version

echo.
echo ========================================
echo Step 2: Installing Streamlit...
echo ========================================

echo Installing Streamlit with Python 3.12...
"C:\Users\shubh\AppData\Local\Microsoft\WindowsApps\python3.12.exe" -m pip install streamlit pandas plotly

echo.
echo ========================================
echo Step 3: Running the App...
echo ========================================

echo Starting the Question Paper Maker...
echo.
echo The app will open in your browser automatically.
echo If it doesn't open, go to: http://localhost:8501
echo.
echo Press Ctrl+C to stop the app when you're done.
echo.

"C:\Users\shubh\AppData\Local\Microsoft\WindowsApps\python3.12.exe" -m streamlit run simple_app.py

echo.
echo App stopped.
pause 