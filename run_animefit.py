"""
AnimeFit Startup Script
Launches the anime-themed push-up tracking application
"""

import sys
import os
import subprocess
import webbrowser
import time
from pathlib import Path

def check_requirements():
    """Check if required packages are installed"""
    required_packages = [
        'flask',
        'flask_socketio',
        'ultralytics',
        'cv2',
        'numpy',
        'PIL'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'cv2':
                import cv2
            elif package == 'PIL':
                import PIL
            else:
                __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    return missing_packages

def install_requirements():
    """Install required packages"""
    print("🔧 Installing required packages...")
    try:
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
        ])
        print("✅ All packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False

def check_model_file():
    """Check if YOLO model file exists"""
    model_path = Path('yolov8n-pose.pt')
    if not model_path.exists():
        print("🤖 YOLO pose model not found. Downloading...")
        try:
            from ultralytics import YOLO
            # This will automatically download the model
            YOLO('yolov8n-pose.pt')
            print("✅ YOLO model downloaded successfully!")
        except Exception as e:
            print(f"❌ Error downloading model: {e}")
            return False
    else:
        print("✅ YOLO model found!")
    
    return True

def create_static_symlinks():
    """Create symbolic links for static files"""
    try:
        # Create static directory if it doesn't exist
        static_dir = Path('static')
        static_dir.mkdir(exist_ok=True)
        
        # Create subdirectories
        (static_dir / 'styles').mkdir(exist_ok=True)
        (static_dir / 'js').mkdir(exist_ok=True)
        
        # Copy files to static directory (Windows compatible)
        import shutil
        
        # Copy CSS files
        if Path('styles/main.css').exists():
            shutil.copy2('styles/main.css', 'static/styles/main.css')
        
        # Copy JS files
        js_files = ['main.js', 'camera.js', 'pose-detection.js', 'animations.js']
        for js_file in js_files:
            if Path(f'js/{js_file}').exists():
                shutil.copy2(f'js/{js_file}', f'static/js/{js_file}')
        
        print("✅ Static files organized!")
        return True
    except Exception as e:
        print(f"❌ Error organizing static files: {e}")
        return False

def main():
    """Main startup function"""
    print("🎌 AnimeFit - Push-Up Tracker Startup 🎌")
    print("========================================")
    
    # Check current directory
    if not Path('backend.py').exists():
        print("❌ Please run this script from the pushup_counter directory")
        sys.exit(1)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    
    print(f"🐍 Python version: {sys.version}")
    
    # Check and install requirements
    missing = check_requirements()
    if missing:
        print(f"📦 Missing packages: {', '.join(missing)}")
        if not install_requirements():
            print("❌ Failed to install requirements. Please install manually:")
            print("   pip install -r requirements.txt")
            sys.exit(1)
    else:
        print("✅ All required packages are installed!")
    
    # Check model file
    if not check_model_file():
        print("❌ Failed to download YOLO model")
        sys.exit(1)
    
    # Organize static files
    if not create_static_symlinks():
        print("⚠️ Warning: Could not organize static files")
    
    print("\n🚀 Starting AnimeFit server...")
    print("🌐 Opening browser in 3 seconds...")
    
    # Start the Flask server in a subprocess
    try:
        # Open browser after a short delay
        def open_browser():
            time.sleep(3)
            webbrowser.open('http://localhost:5000')
        
        import threading
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        # Start Flask server
        subprocess.run([sys.executable, 'backend.py'])
        
    except KeyboardInterrupt:
        print("\n👋 AnimeFit server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()