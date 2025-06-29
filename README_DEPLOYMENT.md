# 🚀 Deployment Guide - Student Question Paper Helper

## 🌐 Launch Website Locally

### Quick Start
1. **Run the batch file:**
   ```bash
   LAUNCH_WEBSITE.bat
   ```

2. **Or manually:**
   ```bash
   pip install streamlit pandas plotly pillow
   streamlit run production_app.py
   ```

3. **Access the website:**
   - Open your browser
   - Go to: `http://localhost:8501`

## ☁️ Deploy to Cloud Platforms

### 1. Streamlit Cloud (Recommended)
- **Free hosting**
- **Automatic deployment**
- **Easy setup**

**Steps:**
1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with GitHub
4. Select your repository
5. Set main file path: `production_app.py`
6. Deploy!

### 2. Heroku
1. Install Heroku CLI
2. Run: `heroku create your-app-name`
3. Run: `git add .`
4. Run: `git commit -m "Deploy app"`
5. Run: `git push heroku main`

### 3. Railway
1. Go to [railway.app](https://railway.app)
2. Connect your GitHub repository
3. Deploy automatically

### 4. Render
1. Go to [render.com](https://render.com)
2. Create new Web Service
3. Connect your GitHub repository
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `streamlit run production_app.py`

## 🗄️ Database Features

The app includes SQLite database with:

### Tables:
- **users**: User accounts and login history
- **analyses**: Past paper analysis results
- **papers**: Generated sample papers

### Features:
- ✅ User registration and login
- ✅ Save analysis history
- ✅ Save generated papers
- ✅ Track user activity
- ✅ Export data

## 🔧 Configuration

### Environment Variables:
```bash
# For production
export STREAMLIT_SERVER_PORT=8501
export STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

### Database Location:
- Local: `student_app.db` (SQLite)
- Cloud: Configure external database (PostgreSQL, MySQL)

## 📱 Features

### For Students:
- 📊 **Past Paper Analysis**: Upload files/images, get probability scores
- 📝 **Sample Paper Generation**: Create practice papers with AI
- 🗄️ **Database Tracking**: Save all your work and history
- 📈 **Analytics**: View your progress and patterns
- 📤 **Export**: Download papers and results

### Technical Features:
- 🔐 **User Authentication**: Login/register system
- 📁 **File Upload**: Support for PDF, DOCX, TXT, Images
- 🎯 **AI Analysis**: Question frequency and probability scoring
- 📊 **Visualizations**: Charts and graphs
- 💾 **Data Persistence**: SQLite database
- 🌐 **Web Interface**: Responsive Streamlit app

## 🚀 Quick Launch Commands

### Windows:
```bash
LAUNCH_WEBSITE.bat
```

### Mac/Linux:
```bash
chmod +x LAUNCH_WEBSITE.sh
./LAUNCH_WEBSITE.sh
```

### Manual:
```bash
pip install -r requirements.txt
streamlit run production_app.py
```

## 🔍 Troubleshooting

### Common Issues:

1. **Port already in use:**
   ```bash
   streamlit run production_app.py --server.port 8502
   ```

2. **Database errors:**
   - Delete `student_app.db` file
   - Restart the app

3. **Import errors:**
   ```bash
   pip install --upgrade streamlit pandas plotly pillow
   ```

4. **Permission errors:**
   - Run as administrator (Windows)
   - Use `sudo` (Mac/Linux)

## 📞 Support

If you encounter issues:
1. Check the error messages
2. Verify Python version (3.8+)
3. Reinstall dependencies
4. Check file permissions

## 🎯 Next Steps

After deployment:
1. Test all features
2. Add more questions to the database
3. Customize the UI
4. Add more analysis features
5. Integrate with external APIs

---

**🎓 Happy Studying! Your AI-powered exam preparation assistant is ready!** 