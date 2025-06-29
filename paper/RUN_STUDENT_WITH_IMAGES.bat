@echo off
echo ========================================
echo Student Question Paper Helper (with Images)
echo ========================================
echo.

echo Starting the enhanced student app with image upload support...
echo.

cd /d "%~dp0"
streamlit run student_helper.py

echo.
echo If the app didn't start, try:
echo 1. python -m streamlit run student_helper.py
echo 2. Make sure you're in the paper directory
echo.

pause 