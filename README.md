# 🚀 QuestVibe - AI-Powered Question Paper Generation System

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen.svg)](https://github.com/shubhamsingh-s/ai-based-question-paper/actions)

> **Intelligent Question Paper Generation with AI Integration**

QuestVibe is a comprehensive AI-powered system that generates high-quality question papers from syllabus topics. It features ChatGPT integration, automated question generation, manual creation tools, pattern analysis, and real-time analytics.

## 🌟 Key Features

### 🤖 **AI-Powered Generation**
- **ChatGPT Integration**: Intelligent question generation using OpenAI's GPT models
- **Fallback System**: Seamless local generation when API is unavailable
- **Context-Aware**: Questions based on actual syllabus content
- **Quality Analysis**: AI-powered question quality assessment

### 📚 **Multiple Generation Modes**
- **Auto Generation**: Quick questions from predefined subjects
- **Manual Creation**: Upload or paste syllabus for custom questions
- **Pattern Analysis**: Analyze question distribution and difficulty
- **Syllabus Processing**: Extract topics from uploaded documents

### 🎯 **Question Types & Difficulty**
- **MCQ**: Multiple choice questions with options
- **Short Answer**: Brief explanation questions
- **Long Answer**: Detailed analytical questions
- **Case Study**: Real-world scenario questions
- **Difficulty Levels**: Easy, Medium, Hard with Bloom's Taxonomy

### 📊 **Analytics & Insights**
- **Real-time Dashboard**: Live user activity and generation stats
- **Quality Metrics**: Question quality scores and analysis
- **Usage Analytics**: User behavior and popular subjects
- **Export Options**: PDF, DOCX, and Excel formats

### 🔐 **User Management**
- **Simple Login**: Name and institution-based access
- **Super Admin**: Hidden access for full system control
- **Session Tracking**: User activity monitoring
- **Database Management**: Comprehensive data control

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Internet connection (for ChatGPT features)
- OpenAI API key (optional, for enhanced AI features)

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

3. **Run the application**
   ```bash
   streamlit run streamlit_app.py
   ```

4. **Access the application**
   - Open your browser and go to `http://localhost:8501`
   - Enter your name and institution
   - Start generating questions!

### 🎯 **Quick Demo**

1. **Auto Generation**: Select a subject and generate questions instantly
2. **Manual Creation**: Upload a syllabus file or paste content
3. **ChatGPT Setup**: Use super admin access to configure API key
4. **Export Results**: Download questions in your preferred format

## 📖 Detailed Usage Guide

### 🔧 **Setting Up ChatGPT Integration**

1. **Get OpenAI API Key**
   - Visit [OpenAI Platform](https://platform.openai.com/)
   - Create an account and get your API key
   - Note: Free tier available with limitations

2. **Configure in QuestVibe**
   - Login as super admin (hidden access)
   - Go to Super Admin Dashboard
   - Enter your API key in the ChatGPT section
   - Test the connection

3. **Enhanced Features**
   - Intelligent question generation
   - Context-aware responses
   - Better question quality
   - Advanced topic analysis

### 📝 **Question Generation Workflows**

#### **Auto Generation**
```
Subject Selection → Topic Selection → Question Types → Generate → Export
```

#### **Manual Creation**
```
Upload Syllabus → Extract Topics → Configure Settings → Generate → Analyze
```

#### **Pattern Analysis**
```
Upload Questions → Analyze Patterns → View Insights → Export Report
```

### 🎨 **User Interface Features**

- **Modern Design**: Beautiful gradient backgrounds and animations
- **Responsive Layout**: Works on desktop, tablet, and mobile
- **Intuitive Navigation**: Easy-to-use tabs and sections
- **Real-time Feedback**: Progress indicators and success messages
- **Error Handling**: Graceful error messages and fallbacks

## 🛠️ Development

### **Running Tests**
```bash
# Run all tests
python run_tests.py

# Run specific test file
python test_questvibe.py

# Run with coverage
pytest test_questvibe.py --cov=streamlit_app
```

### **Code Quality**
```bash
# Format code
black streamlit_app.py

# Lint code
flake8 streamlit_app.py

# Sort imports
isort streamlit_app.py
```

### **Development Setup**
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Set up pre-commit hooks
pre-commit install
```

## 📊 **System Architecture**

```
QuestVibe System
├── Frontend (Streamlit)
│   ├── User Interface
│   ├── Form Handling
│   └── Real-time Updates
├── Backend (Python)
│   ├── ChatGPT Integration
│   ├── Question Generation
│   ├── Database Management
│   └── File Processing
├── Database (SQLite)
│   ├── User Data
│   ├── Question Analytics
│   └── Session Tracking
└── External APIs
    ├── OpenAI ChatGPT
    └── File Processing Services
```

## 🔧 **Configuration**

### **Environment Variables**
```bash
# Optional: Set OpenAI API key
export OPENAI_API_KEY="your-api-key-here"

# Optional: Set database path
export QUESTVIBE_DB_PATH="path/to/database.db"
```

### **Super Admin Access**
- **Username**: `admin`
- **Password**: `questvibe2024`
- **Access**: Hidden login option for full system control

## 📈 **Analytics & Metrics**

### **Question Quality Metrics**
- **Quality Score**: 0-100 based on AI analysis
- **Topic Coverage**: Number of syllabus topics covered
- **Difficulty Distribution**: Balance across difficulty levels
- **Type Distribution**: Mix of question types

### **User Analytics**
- **Active Users**: Real-time user count
- **Generation Stats**: Questions generated per session
- **Popular Subjects**: Most frequently used subjects
- **Session Duration**: Average time spent in app

## 🚀 **Deployment**

### **Streamlit Cloud**
1. Connect your GitHub repository
2. Deploy automatically on push to main
3. Configure environment variables
4. Access your live application

### **Local Deployment**
```bash
# Production mode
streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0

# With custom config
streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0 --server.maxUploadSize 200
```

### **Docker Deployment**
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

## 🤝 **Contributing**

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### **Development Workflow**
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Submit a pull request

### **Code Standards**
- Follow PEP 8 style guidelines
- Add docstrings to all functions
- Include type hints where possible
- Write comprehensive tests

## 📋 **Testing**

### **Test Coverage**
- **Unit Tests**: Individual component testing
- **Integration Tests**: End-to-end workflow testing
- **API Tests**: ChatGPT integration testing
- **UI Tests**: User interface functionality

### **Running Tests**
```bash
# All tests
python run_tests.py

# Specific test categories
python -m pytest test_questvibe.py::TestQuestVibeSystem
python -m pytest test_questvibe.py::TestQuestVibeIntegration
```

## 🔒 **Security**

### **Data Protection**
- **No Sensitive Data Storage**: API keys not stored in plain text
- **Session Management**: Secure user session handling
- **Input Validation**: All user inputs validated
- **Error Handling**: No sensitive information in error messages

### **API Security**
- **Rate Limiting**: Built-in protection against abuse
- **Fallback Systems**: Graceful degradation when APIs fail
- **Secure Communication**: HTTPS for all external calls

## 📞 **Support**

### **Getting Help**
- **Documentation**: Check this README and other docs
- **Issues**: Report bugs on GitHub Issues
- **Discussions**: Use GitHub Discussions for questions
- **Email**: Contact the development team

### **Common Issues**

#### **ChatGPT API Errors**
- Check your API key is correct
- Verify you have sufficient credits
- Ensure internet connection is stable
- System will fall back to local generation

#### **File Upload Issues**
- Ensure file is in supported format (.txt, .pdf, .docx)
- Check file size (max 200MB)
- Verify file is not corrupted

#### **Performance Issues**
- Clear browser cache
- Restart the application
- Check system resources

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 **Acknowledgments**

- **OpenAI**: For providing the ChatGPT API
- **Streamlit**: For the amazing web framework
- **Contributors**: All who have helped improve QuestVibe
- **Users**: For valuable feedback and suggestions

## 📊 **Project Status**

- **Version**: 2.0.0
- **Status**: Production Ready
- **Last Updated**: December 2024
- **Maintainer**: QuestVibe Development Team

---

**Made with ❤️ by the QuestVibe Team**

*Empowering educators with AI-driven question paper generation* 