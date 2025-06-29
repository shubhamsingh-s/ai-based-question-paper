# 🚀 Git Setup Guide for Question Paper Maker

## 📋 **Overview**
This guide will help you move your complete Question Paper Maker system to the GitHub repository: [https://github.com/shubhamsingh-s/ai-based-question-paper](https://github.com/shubhamsingh-s/ai-based-question-paper)

## 🔧 **Step 1: Install Git (if not installed)**

### **Option A: Download Git**
1. Go to: https://git-scm.com/download/win
2. Download Git for Windows
3. Run the installer
4. Use default settings

### **Option B: Use Chocolatey (if available)**
```bash
choco install git
```

### **Option C: Use Winget**
```bash
winget install Git.Git
```

## ⚙️ **Step 2: Configure Git**

```bash
# Set your name and email
git config --global user.name "shubhamsingh-s"
git config --global user.email "your-email@example.com"

# Verify configuration
git config --list
```

## 📁 **Step 3: Initialize Git Repository**

```bash
# Navigate to your project directory
cd C:\Users\shubh\paper

# Initialize Git repository
git init

# Check status
git status
```

## 📄 **Step 4: Create .gitignore File**

Create a `.gitignore` file with the following content:

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Temporary files
*.tmp
*.temp

# Streamlit
.streamlit/

# Jupyter
.ipynb_checkpoints/
```

## 📦 **Step 5: Add Files to Git**

```bash
# Add all files
git add .

# Check what will be committed
git status

# Make initial commit
git commit -m "Initial commit: Complete Question Paper Maker System

- Core question generation functionality
- Simple demo application
- Web interface with Streamlit
- Comprehensive documentation
- Python 3.12 compatibility
- Analysis and classification features"
```

## 🔗 **Step 6: Connect to GitHub Repository**

```bash
# Add remote repository
git remote add origin https://github.com/shubhamsingh-s/ai-based-question-paper.git

# Verify remote
git remote -v

# Push to GitHub
git push -u origin main
```

## 📋 **Step 7: Update README.md**

Create a comprehensive README.md file:

```markdown
# 🤖 AI-Based Question Paper Maker

An intelligent system for generating comprehensive question papers based on syllabus topics, with advanced analysis and classification capabilities.

## ✨ Features

- 📝 **Question Generation**: Create questions from syllabus topics
- 🎯 **Multiple Question Types**: MCQ, Short Answer, Long Answer
- 📊 **Smart Analysis**: Question distribution and topic analysis
- 🏷️ **Classification**: Automatic topic-based categorization
- 🌐 **Web Interface**: Beautiful Streamlit-based UI
- 💾 **Export Options**: JSON and CSV export capabilities
- 📈 **Visual Analytics**: Interactive charts and graphs

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/shubhamsingh-s/ai-based-question-paper.git
   cd ai-based-question-paper
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the simple demo**
   ```bash
   python simple_demo.py
   ```

4. **Launch web interface**
   ```bash
   streamlit run simple_web_app.py
   ```

## 📁 Project Structure

```
ai-based-question-paper/
├── simple_demo.py          # Console demo application
├── simple_web_app.py       # Streamlit web interface
├── web_app.py             # Full-featured web application
├── src/                   # Core modules
│   ├── generate.py        # Question generation
│   ├── analyze.py         # Analysis engine
│   ├── classify.py        # Classification system
│   └── ingest.py          # Document ingestion
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── docs/                 # Documentation
```

## 🎯 Usage

### Console Demo
```bash
python simple_demo.py
```

### Web Interface
```bash
streamlit run simple_web_app.py
```

## 📊 Features in Detail

### Question Generation
- Syllabus-based question creation
- Multiple difficulty levels
- Bloom's taxonomy integration
- Topic-specific question types

### Analysis Engine
- Question type distribution
- Topic coverage analysis
- Mark allocation optimization
- Cognitive level assessment

### Classification System
- Automatic topic identification
- Question categorization
- Difficulty level assessment
- Content tagging

## 🔧 Configuration

### Customizing Topics
Edit the topics in `simple_demo.py` or use the web interface to configure:
- Database Management Systems
- SQL Queries
- Normalization
- Transaction Management
- And more...

### Question Parameters
- Number of questions
- Question types
- Mark distribution
- Difficulty levels

## 📈 Analytics

The system provides comprehensive analytics:
- Question type distribution charts
- Topic coverage visualization
- Mark allocation analysis
- Performance metrics

## 💾 Export Options

- **JSON Export**: Complete question paper with metadata
- **CSV Export**: Tabular format for spreadsheet analysis
- **PDF Generation**: Professional question paper format

## 🛠️ Development

### Adding New Features
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

### Testing
```bash
python test_system.py
```

## 📞 Support

For issues and questions:
- Create an issue on GitHub
- Check the documentation in the `docs/` folder
- Review troubleshooting guides

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

**Built with ❤️ for educational excellence**
```

## 🔄 **Step 8: Push Updates**

```bash
# Add README
git add README.md
git commit -m "Add comprehensive README with features and usage guide"

# Push to GitHub
git push origin main
```

## ✅ **Step 9: Verify on GitHub**

1. Go to: https://github.com/shubhamsingh-s/ai-based-question-paper
2. Verify all files are uploaded
3. Check README.md is displayed correctly
4. Test the repository structure

## 🎯 **Files to Include**

### **Core System Files**
- `simple_demo.py` - Working console demo
- `simple_web_app.py` - Streamlit web interface
- `web_app.py` - Full-featured web app
- `src/` - All source modules

### **Documentation**
- `README.md` - Comprehensive project guide
- `PYTHON_UPGRADE_GUIDE.md` - Python setup guide
- `FIX_PYTHON_PATH.md` - PATH configuration
- `SOLUTION_SUMMARY.md` - Solution overview
- `FINAL_STATUS.md` - Project status

### **Configuration**
- `requirements.txt` - Python dependencies
- `.gitignore` - Git ignore rules
- `LAUNCH_WEB_APP.bat` - Windows launcher

## 🚀 **Next Steps After Git Setup**

1. **Share the Repository**: Share the GitHub link with others
2. **Collaborate**: Invite collaborators to contribute
3. **Deploy**: Consider deploying the web app to platforms like Streamlit Cloud
4. **Documentation**: Keep documentation updated
5. **Issues**: Use GitHub Issues for bug reports and feature requests

---

**Your Question Paper Maker system will be professionally hosted on GitHub!** 🎉 