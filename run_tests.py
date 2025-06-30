#!/usr/bin/env python3
"""
QuestVibe Test Runner
Run this script to execute all tests for the QuestVibe system.
"""

import subprocess
import sys
import os

def run_tests():
    """Run all tests and display results"""
    print("🧪 Running QuestVibe Tests...")
    print("=" * 50)
    
    try:
        # Run the test suite
        result = subprocess.run([
            sys.executable, "test_questvibe.py"
        ], capture_output=True, text=True, timeout=300)
        
        # Print output
        if result.stdout:
            print(result.stdout)
        
        if result.stderr:
            print("Errors/Warnings:")
            print(result.stderr)
        
        # Return exit code
        return result.returncode
        
    except subprocess.TimeoutExpired:
        print("❌ Tests timed out after 5 minutes")
        return 1
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return 1

def run_simple_tests():
    """Run basic functionality tests"""
    print("🔍 Running Basic Functionality Tests...")
    print("=" * 50)
    
    try:
        # Import and test basic functionality
        import streamlit_app
        
        # Test imports
        print("✅ All modules imported successfully")
        
        # Test database initialization
        streamlit_app.init_database()
        print("✅ Database initialization successful")
        
        # Test ChatGPT class
        chatgpt = streamlit_app.QuestVibeChatGPT()
        print("✅ ChatGPT class initialized")
        
        # Test AI Database class
        ai_db = streamlit_app.QuestVibeAIDatabase()
        print("✅ AI Database class initialized")
        
        print("✅ All basic tests passed!")
        return 0
        
    except Exception as e:
        print(f"❌ Basic test failed: {e}")
        return 1

def main():
    """Main test runner"""
    print("🚀 QuestVibe Test Suite")
    print("=" * 50)
    
    # Check if test file exists
    if not os.path.exists("test_questvibe.py"):
        print("❌ test_questvibe.py not found. Running basic tests only.")
        return run_simple_tests()
    
    # Run comprehensive tests
    test_result = run_tests()
    
    if test_result == 0:
        print("\n🎉 All tests passed successfully!")
    else:
        print("\n❌ Some tests failed. Check the output above.")
    
    return test_result

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 