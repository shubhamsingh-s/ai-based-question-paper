#!/usr/bin/env python3
"""
Test Script for Enhanced Question Paper Maker System
===================================================

This script tests the core functionality without requiring Streamlit.
"""

import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing module imports...")
    
    try:
        from ingest import DocumentIngestor
        print("✅ DocumentIngestor imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import DocumentIngestor: {e}")
        return False
    
    try:
        from generate import generate_questions, generate_model_answer, assign_marks
        print("✅ Question generation modules imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import question generation modules: {e}")
        return False
    
    try:
        from analyze import compute_analytics, compute_topic_frequency
        print("✅ Analysis modules imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import analysis modules: {e}")
        return False
    
    try:
        from classify import tag_questions_by_topic
        print("✅ Classification modules imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import classification modules: {e}")
        return False
    
    return True

def test_basic_functionality():
    """Test basic functionality without external dependencies"""
    print("\n🧪 Testing basic functionality...")
    
    # Test question generation
    try:
        from generate import generate_questions, generate_model_answer, assign_marks
        
        # Sample topics
        topics = ["Database Management", "SQL Queries", "Normalization"]
        question_types = ["MCQ", "Short Answer", "Long Answer"]
        
        # Generate questions
        questions = generate_questions(topics, question_types, 5)
        print(f"✅ Generated {len(questions)} questions successfully")
        
        # Test model answer generation
        if questions:
            model_answer = generate_model_answer(questions[0])
            print("✅ Model answer generation works")
            
            # Test mark assignment
            marks = assign_marks(questions[0])
            print(f"✅ Mark assignment works: {marks} marks")
        
        return True
        
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False

def test_analysis_functionality():
    """Test analysis functionality"""
    print("\n📊 Testing analysis functionality...")
    
    try:
        from analyze import compute_analytics
        
        # Sample questions for analysis
        sample_questions = [
            {'type': 'MCQ', 'bloom_level': 'Remember', 'topic': 'Database'},
            {'type': 'Short Answer', 'bloom_level': 'Understand', 'topic': 'SQL'},
            {'type': 'Long Answer', 'bloom_level': 'Apply', 'topic': 'Database'}
        ]
        
        # Compute analytics
        analytics = compute_analytics(sample_questions)
        print("✅ Analytics computation works")
        print(f"   - Type counts: {analytics['type_counts']}")
        print(f"   - Bloom counts: {analytics['bloom_counts']}")
        print(f"   - Topic counts: {analytics['topic_counts']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Analysis functionality test failed: {e}")
        return False

def test_classification_functionality():
    """Test classification functionality"""
    print("\n🏷️ Testing classification functionality...")
    
    try:
        from classify import tag_questions_by_topic
        
        # Sample questions and topics
        questions = [
            "What is a database?",
            "Explain SQL queries",
            "How does normalization work?"
        ]
        topics = ["Database", "SQL", "Normalization"]
        
        # Tag questions
        tagged = tag_questions_by_topic(questions, topics)
        print(f"✅ Tagged {len(tagged)} questions successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Classification functionality test failed: {e}")
        return False

def test_advanced_modules():
    """Test advanced modules if available"""
    print("\n🚀 Testing advanced modules...")
    
    advanced_modules = [
        'advanced_analyzer',
        'advanced_generator', 
        'model_answer_generator',
        'report_generator'
    ]
    
    for module in advanced_modules:
        try:
            __import__(module)
            print(f"✅ {module} imported successfully")
        except ImportError:
            print(f"⚠️ {module} not available (this is optional)")
    
    return True

def main():
    """Main test function"""
    print("🤖 Enhanced Question Paper Maker System - Test Suite")
    print("=" * 60)
    
    # Test imports
    if not test_imports():
        print("\n❌ Import tests failed. Please check your installation.")
        return False
    
    # Test basic functionality
    if not test_basic_functionality():
        print("\n❌ Basic functionality tests failed.")
        return False
    
    # Test analysis functionality
    if not test_analysis_functionality():
        print("\n❌ Analysis functionality tests failed.")
        return False
    
    # Test classification functionality
    if not test_classification_functionality():
        print("\n❌ Classification functionality tests failed.")
        return False
    
    # Test advanced modules
    test_advanced_modules()
    
    print("\n🎉 All core functionality tests passed!")
    print("\n📋 Next Steps:")
    print("1. Install Streamlit: pip install streamlit")
    print("2. Run the web app: streamlit run web_app.py")
    print("3. Or run the enhanced app: streamlit run enhanced_web_app.py")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 