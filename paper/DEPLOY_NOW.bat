@echo off
echo ========================================
echo    Question Paper Maker - Deploy Now
echo ========================================
echo.

echo 🚀 Setting up for public deployment...
echo.

echo 📋 Step 1: Initialize Git Repository
git init
git add .
git commit -m "Initial commit - Question Paper Maker with Database"

echo.
echo ✅ Git repository initialized!
echo.

echo 📋 Step 2: Create GitHub Repository
echo.
echo Please follow these steps:
echo 1. Go to https://github.com/new
echo 2. Create a new repository named: question-paper-maker
echo 3. Don't initialize with README (we already have files)
echo 4. Copy the repository URL
echo.

set /p repo_url="Enter your GitHub repository URL: "

echo.
echo 📋 Step 3: Push to GitHub
git branch -M main
git remote add origin %repo_url%
git push -u origin main

echo.
echo ✅ Code pushed to GitHub!
echo.

echo 📋 Step 4: Deploy on Streamlit Cloud
echo.
echo Please follow these steps:
echo 1. Go to https://share.streamlit.io
echo 2. Sign in with GitHub
echo 3. Click "New app"
echo 4. Select repository: question-paper-maker
echo 5. Set main file path: streamlit_app.py
echo 6. Click "Deploy"
echo.

echo 🎉 Your website will be live in a few minutes!
echo.
echo 📖 For detailed instructions, see: DEPLOYMENT_GUIDE.md
echo.

pause 