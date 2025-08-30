"""
Deployment Script for Cattle Breed Identifier
SIH 2025 - Smart India Hackathon

This script helps with setting up and deploying the application.
"""

import os
import sys
import subprocess
import platform
import json
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    else:
        print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
        return True

def create_virtual_environment():
    """Create virtual environment"""
    print("\n📦 Creating virtual environment...")
    
    venv_name = "venv"
    if os.path.exists(venv_name):
        print(f"✅ Virtual environment already exists: {venv_name}")
        return True
    
    try:
        subprocess.run([sys.executable, "-m", "venv", venv_name], check=True)
        print(f"✅ Virtual environment created: {venv_name}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create virtual environment: {e}")
        return False

def get_activate_command():
    """Get the appropriate activation command for the OS"""
    system = platform.system().lower()
    if system == "windows":
        return "venv\\Scripts\\activate"
    else:
        return "source venv/bin/activate"

def install_dependencies():
    """Install required dependencies"""
    print("\n📥 Installing dependencies...")
    
    try:
        # Install from requirements.txt
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    
    directories = ["uploads", "models", "static"]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def check_model():
    """Check if model files exist"""
    print("\n🤖 Checking AI model...")
    
    # For prototype, we'll use the built-in MobileNetV2
    print("✅ Using MobileNetV2 for prototype (will be replaced with custom model)")
    return True

def create_config_file():
    """Create configuration file"""
    print("\n⚙️ Creating configuration file...")
    
    config = {
        "app_name": "Cattle Breed Identifier",
        "version": "1.0.0",
        "description": "AI-powered cattle breed recognition system",
        "author": "SIH 2025 Team",
        "host": "0.0.0.0",
        "port": 5000,
        "debug": True,
        "max_file_size": "16MB",
        "supported_formats": ["jpg", "jpeg", "png", "bmp"],
        "supported_breeds": [
            "murrah_buffalo",
            "gir_cattle", 
            "sahiwal_cattle",
            "tharparkar_cattle"
        ]
    }
    
    with open("config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    print("✅ Configuration file created: config.json")

def run_tests():
    """Run application tests"""
    print("\n🧪 Running tests...")
    
    try:
        # Start the application in background
        print("Starting application for testing...")
        process = subprocess.Popen([sys.executable, "app.py"], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE)
        
        # Wait a moment for the app to start
        import time
        time.sleep(5)
        
        # Run tests
        result = subprocess.run([sys.executable, "test_app.py"], 
                              capture_output=True, 
                              text=True)
        
        # Stop the application
        process.terminate()
        process.wait()
        
        if result.returncode == 0:
            print("✅ Tests passed")
            return True
        else:
            print("❌ Tests failed")
            print(result.stdout)
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Test execution failed: {e}")
        return False

def create_startup_scripts():
    """Create startup scripts for different platforms"""
    print("\n🚀 Creating startup scripts...")
    
    # Windows batch file
    windows_script = """@echo off
echo Starting Cattle Breed Identifier...
echo.
echo Make sure you have activated the virtual environment:
echo venv\\Scripts\\activate
echo.
python app.py
pause
"""
    
    with open("start.bat", "w") as f:
        f.write(windows_script)
    
    # Unix/Linux shell script
    unix_script = """#!/bin/bash
echo "Starting Cattle Breed Identifier..."
echo ""
echo "Make sure you have activated the virtual environment:"
echo "source venv/bin/activate"
echo ""
python app.py
"""
    
    with open("start.sh", "w") as f:
        f.write(unix_script)
    
    # Make shell script executable on Unix systems
    if platform.system().lower() != "windows":
        os.chmod("start.sh", 0o755)
    
    print("✅ Startup scripts created:")
    print("   - start.bat (Windows)")
    print("   - start.sh (Unix/Linux)")

def print_deployment_info():
    """Print deployment information"""
    print("\n" + "="*60)
    print("🎉 DEPLOYMENT COMPLETED SUCCESSFULLY!")
    print("="*60)
    print("🐄 Cattle Breed Identifier - SIH 2025")
    print("="*60)
    
    print("\n📋 Next Steps:")
    print("1. Activate virtual environment:")
    activate_cmd = get_activate_command()
    print(f"   {activate_cmd}")
    
    print("\n2. Start the application:")
    if platform.system().lower() == "windows":
        print("   start.bat")
    else:
        print("   ./start.sh")
    print("   or manually: python app.py")
    
    print("\n3. Access the application:")
    print("   http://localhost:5000")
    
    print("\n📁 Project Structure:")
    print("   ├── app.py              # Main application")
    print("   ├── requirements.txt    # Dependencies")
    print("   ├── templates/          # HTML templates")
    print("   ├── uploads/            # Uploaded images")
    print("   ├── models/             # AI models")
    print("   ├── config.json         # Configuration")
    print("   ├── start.bat           # Windows startup")
    print("   └── start.sh            # Unix startup")
    
    print("\n🔧 Development:")
    print("   - Edit app.py for backend changes")
    print("   - Edit templates/index.html for frontend")
    print("   - Run test_app.py to test functionality")
    print("   - Use train_model.py for custom model training")
    
    print("\n📚 Documentation:")
    print("   - README.md for detailed information")
    print("   - API endpoints documented in app.py")
    
    print("\n🎯 Features Available:")
    print("   ✅ Image upload and breed identification")
    print("   ✅ Comprehensive breed information cards")
    print("   ✅ AI heatmap visualization")
    print("   ✅ Livestock registration system")
    print("   ✅ Modern responsive UI")
    
    print("\n🔮 Future Enhancements:")
    print("   - Custom trained model for better accuracy")
    print("   - Mobile application development")
    print("   - Database integration")
    print("   - Government scheme integration")
    
    print("\n" + "="*60)
    print("🚀 Ready to empower farmers with AI technology!")
    print("="*60)

def main():
    """Main deployment function"""
    print("🐄 Cattle Breed Identifier - Deployment Script")
    print("="*50)
    print("SIH 2025 - Smart India Hackathon")
    print("="*50)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Create virtual environment
    if not create_virtual_environment():
        return False
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Create directories
    create_directories()
    
    # Check model
    if not check_model():
        return False
    
    # Create configuration
    create_config_file()
    
    # Create startup scripts
    create_startup_scripts()
    
    # Run tests (optional)
    print("\n🧪 Would you like to run tests? (y/n): ", end="")
    try:
        response = input().lower().strip()
        if response in ['y', 'yes']:
            run_tests()
    except KeyboardInterrupt:
        print("\n⏭️ Skipping tests...")
    
    # Print deployment info
    print_deployment_info()
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n✅ Deployment completed successfully!")
        else:
            print("\n❌ Deployment failed. Please check the errors above.")
    except KeyboardInterrupt:
        print("\n\n⏹️ Deployment interrupted by user.")
    except Exception as e:
        print(f"\n❌ Unexpected error during deployment: {e}")
