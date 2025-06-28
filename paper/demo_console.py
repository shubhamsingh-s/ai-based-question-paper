#!/usr/bin/env python3
"""
Console Demo for Enhanced Question Paper Maker System
====================================================

This demo shows the core functionality without requiring Streamlit.
"""

import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def demo_question_generation():
    """Demo question generation functionality"""
    print("\n" + "="*60)
    print("📝 QUESTION PAPER GENERATION DEMO")
    print("="*60)
    
    try:
        from generate import generate_questions, generate_model_answer, assign_marks
        
        # Sample syllabus topics
        syllabus_topics = [
            "Database Management Systems",
            "SQL Queries",
            "Normalization",
            "Transaction Management",
            "Indexing and Performance"
        ]
        
        print(f"📚 Syllabus Topics: {len(syllabus_topics)} topics")
        for i, topic in enumerate(syllabus_topics, 1):
            print(f"   {i}. {topic}")
        
        # Generate questions
        question_types = ["MCQ", "Short Answer", "Long Answer"]
        num_questions = 10
        
        print(f"\n🎯 Generating {num_questions} questions...")
        questions = generate_questions(syllabus_topics, question_types, num_questions)
        
        print(f"✅ Generated {len(questions)} questions successfully!")
        
        # Display sample questions
        print("\n📄 Sample Generated Questions:")
        print("-" * 40)
        
        for i, question in enumerate(questions[:5], 1):
            marks = assign_marks(question)
            print(f"\nQ{i} ({question['type']}, {question['bloom_level']}, {marks} marks)")
            print(f"Topic: {question['topic']}")
            print(f"Question: {question['question']}")
            
            # Generate model answer
            model_answer = generate_model_answer(question)
            print(f"Model Answer: {model_answer}")
        
        return questions
        
    except Exception as e:
        print(f"❌ Error in question generation demo: {e}")
        return []

def demo_analysis():
    """Demo analysis functionality"""
    print("\n" + "="*60)
    print("📊 ANALYSIS DEMO")
    print("="*60)
    
    try:
        from analyze import compute_analytics
        
        # Sample questions for analysis
        sample_questions = [
            {'type': 'MCQ', 'bloom_level': 'Remember', 'topic': 'Database Management Systems'},
            {'type': 'MCQ', 'bloom_level': 'Understand', 'topic': 'SQL Queries'},
            {'type': 'Short Answer', 'bloom_level': 'Apply', 'topic': 'Normalization'},
            {'type': 'Short Answer', 'bloom_level': 'Analyze', 'topic': 'Transaction Management'},
            {'type': 'Long Answer', 'bloom_level': 'Evaluate', 'topic': 'Indexing and Performance'},
            {'type': 'Long Answer', 'bloom_level': 'Create', 'topic': 'Database Management Systems'}
        ]
        
        print(f"📈 Analyzing {len(sample_questions)} sample questions...")
        
        # Compute analytics
        analytics = compute_analytics(sample_questions)
        
        print("✅ Analysis completed!")
        print("\n📊 Analysis Results:")
        print("-" * 30)
        
        print("Question Type Distribution:")
        for qtype, count in analytics['type_counts'].items():
            print(f"   {qtype}: {count} questions")
        
        print("\nCognitive Level Distribution:")
        for level, count in analytics['bloom_counts'].items():
            print(f"   {level}: {count} questions")
        
        print("\nTopic Distribution:")
        for topic, count in analytics['topic_counts'].items():
            print(f"   {topic}: {count} questions")
        
        return analytics
        
    except Exception as e:
        print(f"❌ Error in analysis demo: {e}")
        return {}

def demo_classification():
    """Demo classification functionality"""
    print("\n" + "="*60)
    print("🏷️ CLASSIFICATION DEMO")
    print("="*60)
    
    try:
        from classify import tag_questions_by_topic
        
        # Sample questions
        questions = [
            "What is a database management system?",
            "Explain the concept of SQL queries with examples.",
            "How does normalization help in database design?",
            "Describe transaction management in databases.",
            "What are the benefits of indexing in database performance?"
        ]
        
        # Topics for classification
        topics = ["Database Management Systems", "SQL Queries", "Normalization", "Transaction Management", "Indexing"]
        
        print(f"📝 Classifying {len(questions)} questions into {len(topics)} topics...")
        
        # Tag questions
        tagged_questions = tag_questions_by_topic(questions, topics)
        
        print("✅ Classification completed!")
        print("\n🏷️ Classification Results:")
        print("-" * 30)
        
        for i, (question, topic) in enumerate(tagged_questions, 1):
            print(f"Q{i} [{topic}]: {question}")
        
        return tagged_questions
        
    except Exception as e:
        print(f"❌ Error in classification demo: {e}")
        return []

def demo_advanced_features():
    """Demo advanced features if available"""
    print("\n" + "="*60)
    print("🚀 ADVANCED FEATURES DEMO")
    print("="*60)
    
    # Test advanced analyzer
    try:
        from advanced_analyzer import AdvancedExamAnalyzer
        print("✅ Advanced Exam Analyzer available")
        
        analyzer = AdvancedExamAnalyzer()
        print("   - Pattern analysis capabilities")
        print("   - Predictive analytics")
        print("   - Hot topic identification")
        
    except ImportError:
        print("⚠️ Advanced Exam Analyzer not available")
    
    # Test advanced generator
    try:
        from advanced_generator import AdvancedQuestionGenerator
        print("✅ Advanced Question Generator available")
        
        generator = AdvancedQuestionGenerator()
        print("   - Template-based generation")
        print("   - Difficulty level control")
        print("   - Cognitive level classification")
        
    except ImportError:
        print("⚠️ Advanced Question Generator not available")
    
    # Test model answer generator
    try:
        from model_answer_generator import ModelAnswerGenerator
        print("✅ Model Answer Generator available")
        
        answer_gen = ModelAnswerGenerator()
        print("   - Comprehensive answer generation")
        print("   - Marking scheme creation")
        print("   - Alternative approach suggestions")
        
    except ImportError:
        print("⚠️ Model Answer Generator not available")

def main():
    """Main demo function"""
    print("🤖 Enhanced Question Paper Maker System - Console Demo")
    print("=" * 60)
    print("This demo shows the core functionality without requiring Streamlit.")
    print("=" * 60)
    
    # Demo 1: Question Generation
    questions = demo_question_generation()
    
    # Demo 2: Analysis
    analytics = demo_analysis()
    
    # Demo 3: Classification
    tagged_questions = demo_classification()
    
    # Demo 4: Advanced Features
    demo_advanced_features()
    
    # Summary
    print("\n" + "="*60)
    print("📋 DEMO SUMMARY")
    print("="*60)
    print(f"✅ Questions Generated: {len(questions)}")
    print(f"✅ Analysis Completed: {len(analytics)} metrics")
    print(f"✅ Questions Classified: {len(tagged_questions)}")
    
    print("\n🎉 Demo completed successfully!")
    print("\n📋 To use the full system with web interface:")
    print("1. Install Streamlit: pip install streamlit")
    print("2. Run: streamlit run web_app.py")
    print("3. Or run: streamlit run enhanced_web_app.py")
    
    print("\n📋 Alternative setup:")
    print("1. Run the batch file: setup_and_run.bat")
    print("2. Follow the interactive prompts")
    
    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        print("Please check your Python installation and dependencies.") 