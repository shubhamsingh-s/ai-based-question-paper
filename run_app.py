#!/usr/bin/env python3
"""
Simple launcher for the Question Paper Maker Streamlit app
"""

import os
import sys
import subprocess

def main():
    print("🚀 Launching Question Paper Maker...")
    print("=" * 50)
    
    # Check if we're in the right directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(current_dir)
    
    # Check if streamlit_app.py exists
    if not os.path.exists("streamlit_app.py"):
        print("❌ Error: streamlit_app.py not found!")
        print("Current directory:", os.getcwd())
        print("Files in directory:", os.listdir("."))
        return
    
    print("✅ Found streamlit_app.py")
    print("📁 Working directory:", os.getcwd())
    
    # Try to run the app
    try:
        print("🌐 Starting Streamlit server...")
        print("📱 The app will open in your browser automatically")
        print("🔗 If it doesn't open, go to: http://localhost:8501")
        print("=" * 50)
        
        # Run streamlit
        subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app.py"], check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running Streamlit: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure Streamlit is installed: pip install streamlit")
        print("2. Try running: streamlit run streamlit_app.py")
        print("3. Check if Python path is correct")
        
    except KeyboardInterrupt:
        print("\n👋 App stopped by user")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main() 