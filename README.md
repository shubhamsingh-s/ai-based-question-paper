# 🤖 Question Paper Maker - AI-Powered Exam Generator

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)
[![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)](https://sqlite.org/)

## 🌟 Live Demo

**🚀 Your website will be live at:** `https://question-paper-maker-YOUR_USERNAME.streamlit.app`

## 📋 Quick Start

### 🎯 Deploy in 5 Minutes

1. **Run the deployment script:**
   ```bash
   DEPLOY_NOW.bat
   ```

2. **Or follow manual steps:**
   - Create GitHub repository
   - Push code to GitHub
   - Deploy on [Streamlit Cloud](https://share.streamlit.io)

## 🎨 Features

### 🤖 Auto Question Generation
- **Pre-loaded Syllabus Topics** for 4 subjects
- **Smart Question Templates** with variety
- **Bloom's Taxonomy Integration** (6 cognitive levels)
- **Automatic Mark Allocation** based on question type

### 📝 Manual Question Creation
- **File Upload Support** (PDF, DOCX, TXT)
- **Custom Syllabus Input** with text area
- **Real-time Analytics** and visualizations
- **Multiple Export Formats** (Text, JSON, CSV)

### 📊 Pattern Analysis
- **Past Paper Analysis** for insights
- **Topic Distribution** visualization
- **Question Pattern Recognition**
- **Trend Analysis** over time

### 🎛️ Admin Dashboard
- **Real-time Analytics** and metrics
- **User Activity Tracking** with IP logging
- **Question Generation Statistics**
- **System Health Monitoring**

### 🗄️ Database Integration
- **SQLite Database** for data persistence
- **User Session Tracking** with unique IDs
- **Generation Request Logging** with timestamps
- **Analytics Data Storage** for insights

## 🚀 Deployment Options

### 1. Streamlit Cloud (Recommended - FREE)
- **Fastest deployment** - 5 minutes
- **Free hosting** with generous limits
- **Automatic HTTPS** and CDN
- **Easy updates** with Git integration

### 2. Railway (FREE Tier)
- **Simple deployment** from GitHub
- **Auto-detection** of Python apps
- **Custom domains** support
- **Real-time logs** and monitoring

### 3. Heroku (Paid)
- **Professional hosting** with scaling
- **Custom domains** and SSL
- **Advanced monitoring** and analytics
- **Team collaboration** features

### 4. Render (FREE)
- **Free tier** available
- **Auto-deployment** from Git
- **Custom domains** support
- **Easy scaling** options

## 📁 Project Structure

```
question-paper-maker/
├── streamlit_app.py          # 🚀 Main entry point for deployment
├── simple_app.py            # 🎯 Core application logic
├── database_manager.py      # 🗄️ Database operations
├── database_setup.py        # 🔧 Database initialization
├── requirements.txt         # 📦 Dependencies
├── .streamlit/
│   └── config.toml         # ⚙️ Streamlit configuration
├── Procfile                # 🐳 For Heroku/Railway
├── runtime.txt             # 🐍 Python version
├── DEPLOY_NOW.bat          # 🚀 Quick deployment script
├── DEPLOYMENT_GUIDE.md     # 📖 Detailed deployment guide
└── README.md               # 📋 This file
```

## 🎯 Subjects Available

### 📚 Database Management System
- Database Design and ER Model
- Relational Algebra and SQL
- Normalization and Database Design
- Transaction Management
- Concurrency Control
- Database Security
- Distributed Databases
- Data Warehousing
- Big Data and NoSQL
- Database Administration

### 📊 Big Data Fundamentals
- Introduction to Big Data
- Hadoop Ecosystem
- MapReduce Programming
- HDFS Architecture
- Spark Framework
- Data Processing Pipelines
- Machine Learning with Big Data
- Data Visualization
- Cloud Computing for Big Data
- Big Data Analytics

### 🌐 Computer Networks
- Network Architecture
- OSI Model and TCP/IP
- Network Protocols
- Routing Algorithms
- Network Security
- Wireless Networks
- Network Management
- Internet Technologies
- Network Performance
- Emerging Network Technologies

### 💻 Operating Systems
- Process Management
- Memory Management
- File Systems
- CPU Scheduling
- Deadlock Prevention
- Virtual Memory
- Device Management
- System Security
- Distributed Systems
- Real-time Systems

## 🎨 Question Types

### 📝 Multiple Choice Questions (MCQ)
- **Marks:** 1 per question
- **Templates:** 5 different patterns
- **Bloom's Levels:** All 6 levels

### ✍️ Short Answer Questions
- **Marks:** 3 per question
- **Templates:** 5 different patterns
- **Focus:** Understanding and application

### 📄 Long Answer Questions
- **Marks:** 8 per question
- **Templates:** 5 different patterns
- **Focus:** Analysis and evaluation

### 📋 Case Study Questions
- **Marks:** 10 per question
- **Templates:** 5 different patterns
- **Focus:** Real-world application

## 🧠 Bloom's Taxonomy Integration

The system automatically assigns cognitive levels:
- **Remember** - Recall facts and basic concepts
- **Understand** - Explain ideas and concepts
- **Apply** - Use information in new situations
- **Analyze** - Draw connections among ideas
- **Evaluate** - Justify a stand or decision
- **Create** - Produce new or original work

## 📊 Analytics & Insights

### 🔍 What You Can Track
- **User Sessions** and unique visitors
- **Generation Requests** by type and subject
- **Question Type Distribution** across subjects
- **Popular Topics** and difficulty preferences
- **Export Format Preferences** (Text, JSON, CSV)
- **System Performance** and response times

### 📈 Real-time Dashboard
- **Live Metrics** showing current usage
- **Activity Timeline** with interactive charts
- **Popular Subjects** visualization
- **Question Type Analysis** with pie charts
- **User Behavior Patterns** and trends

## 🔒 Security & Privacy

- **No Personal Data Collection** - Only anonymous analytics
- **Secure Database** - SQLite with proper access controls
- **HTTPS Enabled** - All platforms provide SSL certificates
- **No API Keys Required** - Self-contained application
- **Session-based Tracking** - No persistent user identification

## 🛠️ Technical Stack

- **Frontend:** Streamlit (Python web framework)
- **Backend:** Python 3.9+
- **Database:** SQLite with SQLAlchemy
- **Visualization:** Plotly for interactive charts
- **Styling:** Custom CSS with animations
- **Deployment:** Streamlit Cloud, Railway, Heroku, Render

## 🚨 Troubleshooting

### Common Issues & Solutions

1. **Import Errors**
   - Ensure all files are in the same directory
   - Check `requirements.txt` has all dependencies

2. **Database Issues**
   - Database will be created automatically
   - Sample data will be loaded on first run

3. **Port Issues**
   - Use `$PORT` environment variable for cloud platforms
   - Local development uses port 8501

4. **Memory Issues**
   - Streamlit Cloud has memory limits
   - Optimize large file uploads

## 📞 Support

### Getting Help
1. **Check Documentation** - See `DEPLOYMENT_GUIDE.md`
2. **Review Logs** - Check platform deployment logs
3. **Verify Files** - Ensure all files are properly uploaded
4. **Test Locally** - Run `streamlit run streamlit_app.py` first

### Community
- **GitHub Issues** - Report bugs and request features
- **Streamlit Community** - Get help with Streamlit-specific issues
- **Documentation** - Comprehensive guides and tutorials

## 🎉 Success Stories

Once deployed, your Question Paper Maker will be:
- **Publicly Accessible** to anyone with the URL
- **Fully Functional** with all features enabled
- **Database Enabled** for comprehensive analytics
- **Mobile Responsive** for all devices
- **Free to Use** (depending on platform)

## 📄 License

This project is open source and available under the MIT License.

---

**🎯 Ready to deploy? Run `DEPLOY_NOW.bat` for the fastest setup!**

**🌟 Star this repository if you find it helpful!** 