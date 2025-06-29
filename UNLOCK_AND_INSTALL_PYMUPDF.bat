@echo off
REM =====================================
REM  UNLOCK AND INSTALL PYMUPDF SCRIPT
REM =====================================

echo Stopping all Python processes...
taskkill /F /IM python.exe /T >nul 2>&1
taskkill /F /IM pythonw.exe /T >nul 2>&1

echo.
echo All Python processes stopped.
echo Installing/Repairing PyMuPDF...
pip install --upgrade --force-reinstall pymupdf

echo.
echo If you see 'Successfully installed', PyMuPDF is ready!
echo If you see an error, please restart your computer and run this script again.
pause 