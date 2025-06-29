#!/usr/bin/env python3
"""
Test script for production app
"""

def test_imports():
    """Test if all required modules can be imported"""
    try:
        import streamlit as st
        print("✅ Streamlit imported successfully")
    except ImportError as e:
        print(f"❌ Streamlit import failed: {e}")
        return False
    
    try:
        import pandas as pd
        print("✅ Pandas imported successfully")
    except ImportError as e:
        print(f"❌ Pandas import failed: {e}")
        return False
    
    try:
        import plotly.express as px
        print("✅ Plotly imported successfully")
    except ImportError as e:
        print(f"❌ Plotly import failed: {e}")
        return False
    
    try:
        from PIL import Image
        print("✅ Pillow imported successfully")
    except ImportError as e:
        print(f"❌ Pillow import failed: {e}")
        return False
    
    try:
        import sqlite3
        print("✅ SQLite3 imported successfully")
    except ImportError as e:
        print(f"❌ SQLite3 import failed: {e}")
        return False
    
    return True

def test_database():
    """Test database functionality"""
    try:
        import sqlite3
        
        # Test database connection
        conn = sqlite3.connect(':memory:')
        cursor = conn.cursor()
        
        # Test table creation
        cursor.execute('''
            CREATE TABLE test_users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE NOT NULL
            )
        ''')
        
        # Test insert
        cursor.execute('INSERT INTO test_users (username) VALUES (?)', ('test_user',))
        
        # Test select
        cursor.execute('SELECT * FROM test_users')
        result = cursor.fetchone()
        
        conn.close()
        
        if result and result[1] == 'test_user':
            print("✅ Database functionality works")
            return True
        else:
            print("❌ Database test failed")
            return False
            
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def main():
    print("🧪 Testing Production App Components")
    print("=" * 40)
    
    # Test imports
    imports_ok = test_imports()
    
    # Test database
    db_ok = test_database()
    
    print("\n" + "=" * 40)
    if imports_ok and db_ok:
        print("🎉 All tests passed! App is ready to run.")
        print("\nTo launch the website:")
        print("1. Run: LAUNCH_WEBSITE.bat")
        print("2. Or: streamlit run production_app.py")
        print("3. Open: http://localhost:8501")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        print("\nTo fix:")
        print("1. Run: pip install streamlit pandas plotly pillow")
        print("2. Try the tests again")

if __name__ == "__main__":
    main() 