@echo off
echo ========================================
echo    QuestVibe Test Runner
echo ========================================
echo.

echo Running basic functionality tests...
python -c "import streamlit_app; print('✅ All imports successful')"

echo.
echo Running test suite...
python test_questvibe.py

echo.
echo ========================================
echo    Test Complete
echo ========================================
pause 