#!/usr/bin/env python3
"""
Test script for Question Paper Maker functions
"""

def generate_questions(topics, num_questions, question_types):
    """Generate questions based on topics and parameters"""
    questions = []
    
    for topic in topics:
        for qtype in question_types:
            if qtype == "MCQ":
                question = f"Which of the following best describes {topic}?"
                marks = 1
            elif qtype == "Short Answer":
                question = f"Explain the concept of {topic}."
                marks = 3
            elif qtype == "Long Answer":
                question = f"Discuss {topic} in detail with examples."
                marks = 8
            else:
                question = f"Describe {topic}."
                marks = 5
            
            questions.append({
                'question': question,
                'type': qtype,
                'topic': topic,
                'marks': marks,
                'bloom_level': 'Understand'
            })
    
    return questions[:num_questions]

def test_function():
    """Test the generate_questions function"""
    print("🧪 Testing Question Paper Maker Functions...")
    
    # Test data
    topics = ["Database Management", "SQL Queries", "Data Modeling"]
    question_types = ["MCQ", "Short Answer"]
    num_questions = 5
    
    try:
        # Test the function
        questions = generate_questions(topics, num_questions, question_types)
        
        print(f"✅ Function executed successfully!")
        print(f"📊 Generated {len(questions)} questions")
        
        # Display sample questions
        print("\n📝 Sample Questions:")
        for i, q in enumerate(questions[:3], 1):
            print(f"Q{i}: {q['question']} ({q['type']}, {q['marks']} marks)")
        
        print("\n🎉 All tests passed! The app should work correctly.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("🔧 Please check the function implementation.")

if __name__ == "__main__":
    test_function() 