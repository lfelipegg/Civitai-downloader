#!/usr/bin/env python3
"""
GUI Launcher for CivitAI Model Downloader
Simple launcher script to start the GUI version
"""

import sys
import os
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    missing_deps = []
    
    try:
        import tkinter
    except ImportError:
        missing_deps.append("tkinter")
    
    try:
        import requests
    except ImportError:
        missing_deps.append("requests")
    
    try:
        import tqdm
    except ImportError:
        missing_deps.append("tqdm")
    
    try:
        from dotenv import load_dotenv
    except ImportError:
        missing_deps.append("python-dotenv")
    
    return missing_deps

def main():
    """Main launcher function"""
    print("CivitAI Model Downloader - GUI Launcher")
    print("=" * 50)
    
    # Check dependencies
    missing = check_dependencies()
    if missing:
        print(f"❌ Missing dependencies: {', '.join(missing)}")
        print("\nPlease install missing dependencies:")
        print(f"pip install {' '.join(missing)}")
        return 1
    
    print("✅ All dependencies found")
    
    # Check if we're in the right directory
    current_dir = Path.cwd()
    required_files = ['config.py', 'gui.py', 'model_processor.py']
    
    missing_files = [f for f in required_files if not (current_dir / f).exists()]
    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        print("\nPlease run this script from the CivitAI downloader directory")
        print("that contains all the modular files.")
        return 1
    
    print("✅ All required files found")
    
    # Launch GUI
    try:
        print("\n🚀 Launching GUI...")
        from gui import main as gui_main
        gui_main()
        return 0
    except Exception as e:
        print(f"❌ Error launching GUI: {e}")
        print("\nTry running the GUI directly:")
        print("python gui.py")
        return 1

if __name__ == "__main__":
    sys.exit(main())