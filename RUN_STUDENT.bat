@echo off
echo ========================================
echo Student Question Paper Helper
echo ========================================
echo.

echo Starting the student app...
echo.

cd paper
streamlit run student_helper.py

echo.
echo If the app didn't start, try:
echo 1. cd paper
echo 2. streamlit run student_helper.py
echo.

pause 