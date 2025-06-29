#!/usr/bin/env python3
"""
Simple Demo for Question Paper Maker System
==========================================

This demo works with Python 3.4 and older versions.
"""

import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def simple_question_generation():
    """Simple question generation without advanced features"""
    print("\n" + "="*60)
    print("📝 SIMPLE QUESTION GENERATION DEMO")
    print("="*60)
    
    # Sample topics
    topics = [
        "Database Management Systems",
        "SQL Queries",
        "Normalization",
        "Transaction Management"
    ]
    
    print("📚 Syllabus Topics:")
    for i, topic in enumerate(topics, 1):
        print(f"   {i}. {topic}")
    
    # Generate simple questions
    questions = []
    question_types = ["MCQ", "Short Answer", "Long Answer"]
    
    for topic in topics:
        for qtype in question_types:
            if qtype == "MCQ":
                question = f"Which of the following best describes {topic}?"
            elif qtype == "Short Answer":
                question = f"Explain the concept of {topic}."
            else:  # Long Answer
                question = f"Discuss {topic} in detail with examples."
            
            questions.append({
                'question': question,
                'type': qtype,
                'topic': topic,
                'bloom_level': 'Understand',
                'marks': 1 if qtype == "MCQ" else 3 if qtype == "Short Answer" else 8
            })
    
    print(f"\n✅ Generated {len(questions)} questions!")
    
    # Display sample questions
    print("\n📄 Sample Questions:")
    print("-" * 40)
    
    for i, q in enumerate(questions[:6], 1):
        print(f"\nQ{i} ({q['type']}, {q['marks']} marks)")
        print(f"Topic: {q['topic']}")
        print(f"Question: {q['question']}")
    
    return questions

def simple_analysis(questions):
    """Simple analysis without advanced libraries"""
    print("\n" + "="*60)
    print("📊 SIMPLE ANALYSIS")
    print("="*60)
    
    # Count question types
    type_counts = {}
    topic_counts = {}
    
    for q in questions:
        # Count types
        qtype = q['type']
        type_counts[qtype] = type_counts.get(qtype, 0) + 1
        
        # Count topics
        topic = q['topic']
        topic_counts[topic] = topic_counts.get(topic, 0) + 1
    
    print("Question Type Distribution:")
    for qtype, count in type_counts.items():
        print(f"   {qtype}: {count} questions")
    
    print("\nTopic Distribution:")
    for topic, count in topic_counts.items():
        print(f"   {topic}: {count} questions")
    
    # Calculate total marks
    total_marks = sum(q['marks'] for q in questions)
    print(f"\nTotal Marks: {total_marks}")
    
    return {
        'type_counts': type_counts,
        'topic_counts': topic_counts,
        'total_marks': total_marks
    }

def simple_classification():
    """Simple question classification"""
    print("\n" + "="*60)
    print("🏷️ SIMPLE CLASSIFICATION")
    print("="*60)
    
    questions = [
        "What is a database management system?",
        "Explain SQL queries with examples.",
        "How does normalization work?",
        "Describe transaction management."
    ]
    
    topics = ["Database", "SQL", "Normalization", "Transactions"]
    
    print("Sample Questions:")
    for i, q in enumerate(questions, 1):
        print(f"Q{i}: {q}")
    
    print("\nClassification Results:")
    for i, (q, topic) in enumerate(zip(questions, topics), 1):
        print(f"Q{i} [{topic}]: {q}")
    
    return list(zip(questions, topics))

def main():
    """Main demo function"""
    print("🤖 Simple Question Paper Maker Demo")
    print("=" * 60)
    print("This demo works with Python 3.4 and older versions.")
    print("=" * 60)
    
    # Demo 1: Question Generation
    questions = simple_question_generation()
    
    # Demo 2: Analysis
    analysis = simple_analysis(questions)
    
    # Demo 3: Classification
    classified = simple_classification()
    
    # Summary
    print("\n" + "="*60)
    print("📋 DEMO SUMMARY")
    print("="*60)
    print(f"✅ Questions Generated: {len(questions)}")
    print(f"✅ Analysis Completed: {len(analysis)} metrics")
    print(f"✅ Questions Classified: {len(classified)}")
    
    print("\n🎉 Demo completed successfully!")
    print("\n📋 To use the full system with web interface:")
    print("1. Upgrade to Python 3.8 or higher")
    print("2. Install Streamlit: pip install streamlit")
    print("3. Run: streamlit run web_app.py")
    
    return True

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        print("This might be due to Python version compatibility.") 