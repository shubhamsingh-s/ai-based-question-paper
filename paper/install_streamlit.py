#!/usr/bin/env python3
"""
Streamlit Installation Script
============================

This script installs Streamlit and tests the installation.
"""

import subprocess
import sys
import os

def run_command(command):
    """Run a command and return the result"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def install_streamlit():
    """Install Streamlit using different methods"""
    print("🚀 Installing Streamlit...")
    print("=" * 50)
    
    # Method 1: pip install streamlit
    print("Method 1: pip install streamlit")
    success, stdout, stderr = run_command("pip install streamlit")
    if success:
        print("✅ Streamlit installed successfully!")
        return True
    else:
        print(f"❌ Failed: {stderr}")
    
    # Method 2: python -m pip install streamlit
    print("\nMethod 2: python -m pip install streamlit")
    success, stdout, stderr = run_command("python -m pip install streamlit")
    if success:
        print("✅ Streamlit installed successfully!")
        return True
    else:
        print(f"❌ Failed: {stderr}")
    
    # Method 3: py -m pip install streamlit
    print("\nMethod 3: py -m pip install streamlit")
    success, stdout, stderr = run_command("py -m pip install streamlit")
    if success:
        print("✅ Streamlit installed successfully!")
        return True
    else:
        print(f"❌ Failed: {stderr}")
    
    # Method 4: pip3 install streamlit
    print("\nMethod 4: pip3 install streamlit")
    success, stdout, stderr = run_command("pip3 install streamlit")
    if success:
        print("✅ Streamlit installed successfully!")
        return True
    else:
        print(f"❌ Failed: {stderr}")
    
    return False

def test_streamlit():
    """Test if Streamlit is working"""
    print("\n🧪 Testing Streamlit installation...")
    print("=" * 50)
    
    try:
        import streamlit
        print("✅ Streamlit imported successfully!")
        print(f"   Version: {streamlit.__version__}")
        return True
    except ImportError as e:
        print(f"❌ Streamlit import failed: {e}")
        return False

def test_other_dependencies():
    """Test other required dependencies"""
    print("\n📦 Testing other dependencies...")
    print("=" * 50)
    
    dependencies = [
        'pandas', 'plotly', 'matplotlib', 'seaborn',
        'pdfplumber', 'docx', 'fitz', 'sklearn', 'numpy'
    ]
    
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"✅ {dep} - OK")
        except ImportError:
            print(f"❌ {dep} - Missing")
    
    print("\n💡 If any dependencies are missing, install them with:")
    print("pip install pandas plotly matplotlib seaborn pdfplumber python-docx pymupdf scikit-learn numpy")

def main():
    """Main installation function"""
    print("🤖 Streamlit Installation Script")
    print("=" * 50)
    
    # Check Python version
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    
    # Install Streamlit
    if install_streamlit():
        print("\n🎉 Streamlit installation completed!")
    else:
        print("\n❌ Streamlit installation failed!")
        print("\n📋 Manual installation steps:")
        print("1. Open Command Prompt as Administrator")
        print("2. Run: pip install streamlit")
        print("3. Or run: python -m pip install streamlit")
        return False
    
    # Test Streamlit
    if test_streamlit():
        print("\n🎉 Streamlit is working correctly!")
    else:
        print("\n❌ Streamlit test failed!")
        return False
    
    # Test other dependencies
    test_other_dependencies()
    
    print("\n🚀 Ready to run the application!")
    print("Run: streamlit run web_app.py")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ Installation failed. Please try manual installation.")
        sys.exit(1)
    else:
        print("\n✅ Installation successful!") 