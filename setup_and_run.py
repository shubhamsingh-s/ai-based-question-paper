#!/usr/bin/env python3
"""
Setup and Run Script for Question Paper Maker
"""

import os
import sys
import subprocess
import importlib.util

def check_python_version():
    """Check Python version"""
    print(f"🐍 Python version: {sys.version}")
    if sys.version_info >= (3, 8):
        print("✅ Python version is compatible")
        return True
    else:
        print("❌ Python version is too old. Need Python 3.8+")
        return False

def install_package(package):
    """Install a package using pip"""
    try:
        print(f"📦 Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ {package} installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {package}: {e}")
        return False

def check_package(package):
    """Check if a package is installed"""
    spec = importlib.util.find_spec(package)
    if spec is None:
        print(f"❌ {package} is not installed")
        return False
    else:
        print(f"✅ {package} is installed")
        return True

def main():
    print("🚀 Question Paper Maker - Setup and Run")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Check and install required packages
    required_packages = ['streamlit', 'pandas', 'plotly']
    
    for package in required_packages:
        if not check_package(package):
            if not install_package(package):
                print(f"❌ Cannot continue without {package}")
                return
    
    print("\n✅ All packages are ready!")
    
    # Check if the app file exists
    app_file = "simple_app.py"
    if not os.path.exists(app_file):
        print(f"❌ {app_file} not found!")
        print("Current directory:", os.getcwd())
        print("Available files:", os.listdir("."))
        return
    
    print(f"✅ Found {app_file}")
    
    # Run the app
    print("\n🌐 Starting Streamlit app...")
    print("📱 The app will open in your browser automatically")
    print("🔗 If it doesn't open, go to: http://localhost:8501")
    print("=" * 50)
    print("Press Ctrl+C to stop the app")
    print("=" * 50)
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", app_file], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running Streamlit: {e}")
    except KeyboardInterrupt:
        print("\n👋 App stopped by user")

if __name__ == "__main__":
    main() 