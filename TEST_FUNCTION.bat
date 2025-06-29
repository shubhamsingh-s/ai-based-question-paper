@echo off
echo ========================================
echo Testing Question Paper Maker Function
echo ========================================
echo.

cd /d "%~dp0"
python test_app.py

echo.
echo Test completed!
pause 