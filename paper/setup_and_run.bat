@echo off
echo ========================================
echo Enhanced Question Paper Maker System
echo ========================================
echo.

echo Step 1: Installing required dependencies...
echo.

REM Try to install streamlit
echo Installing Streamlit...
python -m pip install streamlit
if %errorlevel% neq 0 (
    echo Failed to install streamlit with python -m pip
    echo Trying with pip directly...
    pip install streamlit
)

echo.
echo Installing other dependencies...
python -m pip install pandas plotly matplotlib seaborn
python -m pip install pdfplumber python-docx pymupdf
python -m pip install scikit-learn numpy scipy

echo.
echo Step 2: Testing the system...
echo.

REM Test if streamlit is installed
python -c "import streamlit; print('Streamlit is installed successfully')"
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Streamlit installation failed!
    echo Please try installing manually:
    echo pip install streamlit
    echo.
    pause
    exit /b 1
)

echo.
echo Step 3: Running the application...
echo.

echo Choose an option:
echo 1. Run Basic Web App (web_app.py)
echo 2. Run Enhanced Web App (enhanced_web_app.py)
echo 3. Run Test Script (test_system.py)
echo 4. Exit
echo.

set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" (
    echo Starting Basic Web App...
    streamlit run web_app.py
) else if "%choice%"=="2" (
    echo Starting Enhanced Web App...
    streamlit run enhanced_web_app.py
) else if "%choice%"=="3" (
    echo Running Test Script...
    python test_system.py
    pause
) else if "%choice%"=="4" (
    echo Exiting...
    exit /b 0
) else (
    echo Invalid choice!
    pause
    exit /b 1
)

pause 