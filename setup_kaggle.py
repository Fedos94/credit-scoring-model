#!/usr/bin/env python3
"""
Setup script for Kaggle API configuration
"""

import os
import json
from pathlib import Path

def setup_kaggle():
    """Setup Kaggle API configuration if kaggle.json exists"""
    kaggle_dir = Path.home() / '.kaggle'
    kaggle_json = kaggle_dir / 'kaggle.json'
    
    # Create .kaggle directory if it doesn't exist
    kaggle_dir.mkdir(exist_ok=True)
    
    # Check if kaggle.json exists in current directory
    if Path('kaggle.json').exists():
        print("Found kaggle.json in current directory, copying to ~/.kaggle/")
        import shutil
        shutil.copy('kaggle.json', kaggle_json)
        
        # Set appropriate permissions
        kaggle_json.chmod(0o600)
        kaggle_dir.chmod(0o700)
        
        print("Kaggle API configured successfully!")
    else:
        print("No kaggle.json found. You can:")
        print("1. Place kaggle.json in the project directory")
        print("2. Or set KAGGLE_USERNAME and KAGGLE_KEY environment variables")
        print("3. Or the code will use kagglehub which doesn't require authentication for public datasets")

if __name__ == "__main__":
    setup_kaggle()