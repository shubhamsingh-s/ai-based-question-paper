#!/usr/bin/env python3
"""
Git Repository Update Script
Updates the repository with all new changes
"""

import os
import subprocess
import sys

def run_command(command, description):
    """Run a git command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            if result.stdout:
                print(result.stdout)
            return True
        else:
            print(f"❌ {description} failed:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error during {description}: {e}")
        return False

def main():
    print("🚀 Git Repository Update")
    print("=" * 50)
    
    # Check if we're in a git repository
    if not os.path.exists(".git"):
        print("❌ Not in a git repository!")
        print("Please navigate to the correct directory.")
        return
    
    # Step 1: Check status
    if not run_command("git status", "Checking Git status"):
        return
    
    # Step 2: Add all files
    if not run_command("git add .", "Adding all files"):
        return
    
    # Step 3: Check what will be committed
    if not run_command("git status", "Checking what will be committed"):
        return
    
    # Step 4: Commit changes
    commit_message = """Enhanced Student Question Paper Helper with Image Upload Support

- Added comprehensive image upload functionality
- Enhanced student app with file and image tabs
- Added image processing and OCR simulation
- Created multiple batch files for easy setup
- Added student-focused documentation
- Improved user interface with better navigation
- Added probability scoring for questions
- Enhanced sample paper generation with image support"""
    
    if not run_command(f'git commit -m "{commit_message}"', "Committing changes"):
        return
    
    # Step 5: Push to remote
    if not run_command("git push", "Pushing to remote repository"):
        return
    
    print("\n🎉 Git Repository Updated Successfully!")
    print("=" * 50)
    print("Changes committed:")
    print("- Enhanced student app with image upload")
    print("- New batch files for easy setup")
    print("- Updated documentation")
    print("- Improved user interface")
    print("- Added probability scoring system")

if __name__ == "__main__":
    main() 