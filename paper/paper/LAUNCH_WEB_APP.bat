@echo off
echo ========================================
echo Question Paper Maker - Web App Launcher
echo ========================================
echo.

echo Checking Python versions...
echo.

echo Python 3.4 (old):
py --version

echo.
echo Python 3.12 (new):
"C:\Users\shubh\AppData\Local\Microsoft\WindowsApps\python3.12.exe" --version

echo.
echo ========================================
echo SOLUTION OPTIONS:
echo ========================================

echo.
echo OPTION 1: Use Simple Demo (Works Now!)
echo python simple_demo.py
echo.

echo OPTION 2: Fix Python Environment
echo 1. Close this window
echo 2. Open NEW command prompt
echo 3. Run: python --version
echo 4. If shows 3.12, run: python -m pip install streamlit pandas plotly
echo 5. Run: streamlit run simple_web_app.py
echo.

echo OPTION 3: Manual Python 3.12 Usage
echo "C:\Users\shubh\AppData\Local\Microsoft\WindowsApps\python3.12.exe" -m streamlit run simple_web_app.py
echo.

echo ========================================
echo CURRENT STATUS:
echo ========================================
echo ✅ Python 3.12.10 installed
echo ✅ Streamlit installed
echo ❌ PATH configuration issue
echo ✅ Simple demo works: python simple_demo.py
echo.

echo Press any key to try launching the web app...
pause

echo.
echo Attempting to launch web app with Python 3.12...
"C:\Users\shubh\AppData\Local\Microsoft\WindowsApps\python3.12.exe" -m streamlit run simple_web_app.py

echo.
echo If the above failed, try:
echo 1. Close this window
echo 2. Open NEW command prompt  
echo 3. Run: python --version
echo 4. If shows 3.12, run: streamlit run simple_web_app.py
echo.

pause 