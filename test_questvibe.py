import unittest
import sqlite3
import tempfile
import os
import sys
from unittest.mock import patch, MagicMock
import json

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the classes we want to test
from streamlit_app import QuestVibeChatGPT, QuestVibeAIDatabase, init_database, save_user_to_database

class TestQuestVibeSystem(unittest.TestCase):
    """Test suite for QuestVibe AI Question Paper Generation System"""
    
    def setUp(self):
        """Set up test environment before each test"""
        # Create a temporary database for testing
        self.test_db_path = tempfile.mktemp(suffix='.db')
        self.original_db_path = 'user_data.db'
        
        # Backup original database if it exists
        if os.path.exists(self.original_db_path):
            import shutil
            shutil.copy2(self.original_db_path, f"{self.original_db_path}.backup")
        
        # Initialize test database
        self.init_test_database()
        
        # Initialize test instances
        self.chatgpt_instance = QuestVibeChatGPT(api_key="test_key")
        self.ai_database = QuestVibeAIDatabase()
    
    def tearDown(self):
        """Clean up after each test"""
        # Remove test database
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)
        
        # Restore original database
        if os.path.exists(f"{self.original_db_path}.backup"):
            import shutil
            shutil.move(f"{self.original_db_path}.backup", self.original_db_path)
    
    def init_test_database(self):
        """Initialize test database with required tables"""
        conn = sqlite3.connect(self.test_db_path)
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                institution TEXT NOT NULL,
                role TEXT DEFAULT 'user',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                session_start TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                session_end TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Create question_generations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS question_generations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                subject TEXT,
                num_questions INTEGER,
                question_types TEXT,
                generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def test_database_initialization(self):
        """Test database initialization"""
        # Test that database tables are created correctly
        conn = sqlite3.connect(self.test_db_path)
        cursor = conn.cursor()
        
        # Check if tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        expected_tables = ['users', 'sessions', 'question_generations']
        for table in expected_tables:
            self.assertIn(table, tables)
        
        conn.close()
    
    def test_user_creation(self):
        """Test user creation and retrieval"""
        # Test user creation
        user_id = save_user_to_database("Test User", "Test University")
        self.assertIsInstance(user_id, int)
        self.assertGreater(user_id, 0)
        
        # Test user retrieval
        user = get_user_by_id(user_id)
        self.assertIsNotNone(user)
        self.assertEqual(user['name'], "Test User")
        self.assertEqual(user['institution'], "Test University")
        self.assertEqual(user['role'], "user")
    
    def test_chatgpt_initialization(self):
        """Test ChatGPT class initialization"""
        # Test with API key
        chatgpt = QuestVibeChatGPT(api_key="test_key")
        self.assertEqual(chatgpt.api_key, "test_key")
        
        # Test without API key
        chatgpt_no_key = QuestVibeChatGPT()
        self.assertIsNone(chatgpt_no_key.api_key)
    
    @patch('streamlit_app.openai.ChatCompletion.create')
    def test_chatgpt_api_call(self, mock_openai):
        """Test ChatGPT API call functionality"""
        # Mock successful API response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Test response"
        mock_openai.return_value = mock_response
        
        # Test API call
        response = self.chatgpt_instance.call_chatgpt_api("Test prompt")
        self.assertEqual(response, "Test response")
        mock_openai.assert_called_once()
    
    def test_fallback_question_generation(self):
        """Test fallback question generation when ChatGPT is not available"""
        # Test fallback generation
        topics = ["Database Management", "SQL", "Normalization"]
        questions = self.chatgpt_instance.generate_fallback_questions(
            "Database Systems", topics, 5, ["MCQ", "Short Answer"]
        )
        
        # Verify questions are generated
        self.assertIsInstance(questions, list)
        self.assertGreater(len(questions), 0)
        
        # Verify question structure
        for question in questions:
            self.assertIn('question', question)
            self.assertIn('type', question)
            self.assertIn('difficulty', question)
            self.assertIn('topic', question)
    
    def test_question_quality_analysis(self):
        """Test question quality analysis functionality"""
        # Create sample questions
        sample_questions = [
            {
                'question': 'What is a database?',
                'type': 'MCQ',
                'difficulty': 'Easy',
                'topic': 'Database Basics',
                'options': ['A', 'B', 'C', 'D'],
                'correct_answer': 'A'
            },
            {
                'question': 'Explain normalization.',
                'type': 'Short Answer',
                'difficulty': 'Medium',
                'topic': 'Database Design'
            }
        ]
        
        # Test quality analysis
        analysis = self.chatgpt_instance.analyze_question_quality(sample_questions)
        
        # Verify analysis structure
        self.assertIn('quality_score', analysis)
        self.assertIn('topic_coverage', analysis)
        self.assertIn('type_distribution', analysis)
        self.assertIn('difficulty_distribution', analysis)
        
        # Verify quality score is within expected range
        self.assertGreaterEqual(analysis['quality_score'], 0)
        self.assertLessEqual(analysis['quality_score'], 100)
    
    def test_ai_database_initialization(self):
        """Test AI Database class initialization"""
        # Test database initialization
        self.assertIsNotNone(self.ai_database)
        
        # Test database connection
        conn = sqlite3.connect('question_paper_analytics.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        # Should have at least some tables
        self.assertGreater(len(tables), 0)
    
    def test_topic_extraction(self):
        """Test topic extraction from content"""
        from streamlit_app import extract_topics_from_content
        
        # Test with structured content
        content = """
        Topic: Database Management Systems
        Unit 1: Introduction to Databases
        • Relational Model
        • SQL Basics
        Chapter 2: Advanced SQL
        """
        
        topics = extract_topics_from_content(content)
        
        # Should extract topics
        self.assertIsInstance(topics, list)
        self.assertGreater(len(topics), 0)
        
        # Should contain expected topics
        topic_texts = [topic.lower() for topic in topics]
        self.assertTrue(any('database' in topic for topic in topic_texts))
    
    def test_error_handling(self):
        """Test error handling in various scenarios"""
        # Test with invalid API key
        chatgpt_invalid = QuestVibeChatGPT(api_key="invalid_key")
        
        # Should handle API errors gracefully
        with patch('streamlit_app.openai.ChatCompletion.create') as mock_openai:
            mock_openai.side_effect = Exception("API Error")
            
            # Should fall back to local generation
            questions = chatgpt_invalid.generate_questions(
                "Test Subject", ["Test Topic"], 3, ["MCQ"]
            )
            
            # Should still return questions (fallback)
            self.assertIsInstance(questions, list)
            self.assertGreater(len(questions), 0)
    
    def test_data_validation(self):
        """Test data validation in various functions"""
        # Test with empty topics
        questions = self.chatgpt_instance.generate_fallback_questions(
            "Test Subject", [], 5, ["MCQ"]
        )
        
        # Should handle empty topics gracefully
        self.assertIsInstance(questions, list)
        
        # Test with invalid question types
        questions = self.chatgpt_instance.generate_fallback_questions(
            "Test Subject", ["Test Topic"], 5, ["Invalid Type"]
        )
        
        # Should handle invalid types gracefully
        self.assertIsInstance(questions, list)

class TestQuestVibeIntegration(unittest.TestCase):
    """Integration tests for QuestVibe system"""
    
    def setUp(self):
        """Set up integration test environment"""
        self.chatgpt = QuestVibeChatGPT()
        self.ai_database = QuestVibeAIDatabase()
    
    def test_end_to_end_question_generation(self):
        """Test complete question generation workflow"""
        # Test the complete workflow
        subject = "Computer Science"
        topics = ["Programming", "Data Structures", "Algorithms"]
        question_types = ["MCQ", "Short Answer"]
        num_questions = 5
        
        # Generate questions
        questions = self.chatgpt.generate_questions(
            subject, topics, num_questions, question_types
        )
        
        # Verify results
        self.assertIsInstance(questions, list)
        self.assertGreater(len(questions), 0)
        
        # Analyze quality
        analysis = self.chatgpt.analyze_question_quality(questions)
        self.assertIsInstance(analysis, dict)
        self.assertIn('quality_score', analysis)
    
    def test_database_operations(self):
        """Test database operations integration"""
        # Test user operations
        user_id = save_user_to_database("Integration Test User", "Test University")
        user = get_user_by_id(user_id)
        
        self.assertIsNotNone(user)
        self.assertEqual(user['name'], "Integration Test User")
    
    def test_chatgpt_fallback_mechanism(self):
        """Test ChatGPT fallback mechanism integration"""
        # Test with no API key
        chatgpt_no_key = QuestVibeChatGPT()
        
        questions = chatgpt_no_key.generate_questions(
            "Test Subject", ["Test Topic"], 3, ["MCQ"]
        )
        
        # Should work without API key (fallback)
        self.assertIsInstance(questions, list)
        self.assertGreater(len(questions), 0)

def run_tests():
    """Run all tests and return results"""
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_suite.addTest(unittest.makeSuite(TestQuestVibeSystem))
    test_suite.addTest(unittest.makeSuite(TestQuestVibeIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    return result

if __name__ == '__main__':
    # Run tests
    result = run_tests()
    
    # Print summary
    print(f"\n{'='*50}")
    print(f"TEST SUMMARY")
    print(f"{'='*50}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print(f"\nFAILURES:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print(f"\nERRORS:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    print(f"\n{'='*50}")
