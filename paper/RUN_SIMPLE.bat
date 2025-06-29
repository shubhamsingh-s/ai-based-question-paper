@echo off
echo ========================================
echo Question Paper Maker - Simple Version
echo ========================================
echo.

echo Starting the simple app...
echo.

cd /d "%~dp0"
streamlit run simple_app.py

echo.
echo If the app didn't start, try:
echo 1. python -m streamlit run simple_app.py
echo 2. Make sure you're in the paper directory
echo.

pause 