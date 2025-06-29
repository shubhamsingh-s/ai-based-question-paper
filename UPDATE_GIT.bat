@echo off
echo ========================================
echo Updating Git Repository
echo ========================================
echo.

echo Step 1: Checking Git status...
git status

echo.
echo Step 2: Adding all new files...
git add .

echo.
echo Step 3: Checking what will be committed...
git status

echo.
echo Step 4: Committing changes...
git commit -m "Enhanced Student Question Paper Helper with Image Upload Support

- Added comprehensive image upload functionality
- Enhanced student app with file and image tabs
- Added image processing and OCR simulation
- Created multiple batch files for easy setup
- Added student-focused documentation
- Improved user interface with better navigation
- Added probability scoring for questions
- Enhanced sample paper generation with image support"

echo.
echo Step 5: Pushing to remote repository...
git push

echo.
echo ========================================
echo Git Repository Updated Successfully!
echo ========================================
echo.

echo Changes committed:
echo - Enhanced student app with image upload
echo - New batch files for easy setup
echo - Updated documentation
echo - Improved user interface
echo.

pause 