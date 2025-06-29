#!/usr/bin/env python3
"""
Quick Start Script for Question Paper Maker
Handles installation and running the app
"""

import os
import sys
import subprocess
import platform

def print_header():
    print("=" * 60)
    print("🚀 Question Paper Maker - Quick Start")
    print("=" * 60)

def check_directory():
    """Check and fix directory"""
    current_dir = os.getcwd()
    print(f"📍 Current directory: {current_dir}")
    
    # If we're in paper/paper, go up one level
    if current_dir.endswith("paper\\paper"):
        os.chdir("..")
        print(f"📁 Moved to: {os.getcwd()}")
    
    return os.getcwd()

def find_python():
    """Find the best Python installation"""
    python_paths = [
        "python",
        "python3",
        "py",
        r"C:\Users\shubh\AppData\Local\Microsoft\WindowsApps\python3.12.exe",
        r"C:\Python312\python.exe",
        r"C:\Python311\python.exe",
        r"C:\Python310\python.exe"
    ]
    
    for path in python_paths:
        try:
            result = subprocess.run([path, "--version"], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print(f"✅ Found Python: {path}")
                print(f"   Version: {result.stdout.strip()}")
                return path
        except:
            continue
    
    print("❌ No Python found!")
    return None

def install_packages(python_path):
    """Install required packages"""
    packages = ["streamlit", "pandas", "plotly"]
    
    print("\n📦 Installing required packages...")
    for package in packages:
        try:
            print(f"   Installing {package}...")
            subprocess.run([python_path, "-m", "pip", "install", package], 
                         check=True, capture_output=True)
            print(f"   ✅ {package} installed")
        except subprocess.CalledProcessError as e:
            print(f"   ❌ Failed to install {package}: {e}")
            return False
    
    return True

def run_app(python_path):
    """Run the Streamlit app"""
    app_file = "enhanced_simple_app.py"
    
    if not os.path.exists(app_file):
        print(f"❌ {app_file} not found!")
        print(f"Available files: {os.listdir('.')}")
        return False
    
    print(f"\n🌐 Starting Streamlit app: {app_file}")
    print("📱 The app will open in your browser automatically")
    print("🔗 If it doesn't open, go to: http://localhost:8501")
    print("=" * 60)
    print("Press Ctrl+C to stop the app")
    print("=" * 60)
    
    try:
        subprocess.run([python_path, "-m", "streamlit", "run", app_file], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running Streamlit: {e}")
        return False
    except KeyboardInterrupt:
        print("\n👋 App stopped by user")
        return True
    
    return True

def main():
    print_header()
    
    # Check directory
    directory = check_directory()
    
    # Find Python
    python_path = find_python()
    if not python_path:
        print("❌ Cannot continue without Python")
        return
    
    # Install packages
    if not install_packages(python_path):
        print("❌ Failed to install packages")
        return
    
    # Run app
    print("\n✅ Setup complete! Starting app...")
    run_app(python_path)

if __name__ == "__main__":
    main() 