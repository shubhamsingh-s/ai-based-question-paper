@echo off
echo ========================================
echo Python Version Check and Upgrade Guide
echo ========================================
echo.

echo Checking current Python version...
python --version
echo.

echo Checking pip version...
python -m pip --version
echo.

echo ========================================
echo ANALYSIS RESULTS:
echo ========================================

python --version 2>&1 | findstr "3.4" >nul
if %errorlevel% equ 0 (
    echo ❌ You are using Python 3.4 (too old)
    echo.
    echo 🔧 UPGRADE REQUIRED:
    echo 1. Download Python 3.11 from: https://www.python.org/downloads/
    echo 2. Install with "Add to PATH" checked
    echo 3. Close this window and open a new command prompt
    echo 4. Run: python --version (should show 3.11.x)
    echo 5. Run: python -m pip install streamlit
    echo 6. Run: streamlit run web_app.py
    echo.
) else (
    echo ✅ Python version looks good!
    echo.
    echo 🚀 Next steps:
    echo 1. Run: python -m pip install streamlit
    echo 2. Run: streamlit run web_app.py
    echo.
)

echo ========================================
echo CURRENT WORKING OPTIONS:
echo ========================================
echo ✅ Simple Demo: python simple_demo.py
echo 📖 Upgrade Guide: Read PYTHON_UPGRADE_GUIDE.md
echo.

pause 