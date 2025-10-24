#!/usr/bin/env python3
"""
Update all Streamlit app versions with comprehensive application form
"""

import shutil
import os

def update_all_versions():
    """Update all versions with comprehensive application form"""
    
    # Files to update
    files_to_update = [
        "streamlit_app_ultra_secure.py",
        "streamlit_app_working.py", 
        "streamlit_app_simple.py"
    ]
    
    # Source file with comprehensive form
    source_file = "streamlit_app.py"
    
    print("🔄 Updating all versions with comprehensive application form...")
    
    for file in files_to_update:
        if os.path.exists(file):
            print(f"✅ Updating {file}...")
            shutil.copy2(source_file, file)
            print(f"✅ {file} updated successfully!")
        else:
            print(f"❌ {file} not found, skipping...")
    
    print("\n🎉 All versions updated with comprehensive application form!")
    print("\n📋 Updated files:")
    for file in files_to_update:
        if os.path.exists(file):
            print(f"✅ {file} - COMPLETE")
        else:
            print(f"❌ {file} - NOT FOUND")

if __name__ == "__main__":
    update_all_versions()
