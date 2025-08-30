#!/usr/bin/env python3
"""
GitHub Repository Setup Script
Cattle Breed Identifier - SIH 2025

This script helps set up the GitHub repository with proper initialization.
"""

import os
import subprocess
import sys

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_git_installed():
    """Check if git is installed"""
    try:
        subprocess.run(["git", "--version"], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def setup_git_repository():
    """Set up the git repository"""
    print("🚀 Setting up GitHub Repository for Cattle Breed Identifier")
    print("=" * 60)
    
    # Check if git is installed
    if not check_git_installed():
        print("❌ Git is not installed. Please install Git first.")
        print("Download from: https://git-scm.com/downloads")
        return False
    
    # Initialize git repository
    if not run_command("git init", "Initializing git repository"):
        return False
    
    # Add all files
    if not run_command("git add .", "Adding files to git"):
        return False
    
    # Create initial commit
    if not run_command('git commit -m "feat: initial commit - Cattle Breed Identifier SIH 2025"', "Creating initial commit"):
        return False
    
    print("\n📋 Next Steps:")
    print("1. Create a new repository on GitHub:")
    print("   - Go to https://github.com/new")
    print("   - Name: cattle-breed-identifier")
    print("   - Description: AI-powered cattle breed recognition system for SIH 2025")
    print("   - Make it Public")
    print("   - Don't initialize with README (we already have one)")
    
    print("\n2. Connect your local repository to GitHub:")
    print("   git remote add origin https://github.com/YOUR_USERNAME/cattle-breed-identifier.git")
    print("   git branch -M main")
    print("   git push -u origin main")
    
    print("\n3. Set up repository features:")
    print("   - Enable Issues")
    print("   - Enable Discussions")
    print("   - Set up branch protection rules")
    print("   - Configure GitHub Actions")
    
    print("\n4. Add repository topics:")
    print("   - ai, machine-learning, computer-vision, flask, python")
    print("   - agriculture, cattle, livestock, india, sih2025")
    print("   - tensorflow, opencv, bootstrap, responsive-design")
    
    return True

def create_github_workflow():
    """Create GitHub workflow files"""
    print("\n🔧 Creating GitHub workflow files...")
    
    # The workflow file is already created in .github/workflows/ci.yml
    print("✅ GitHub Actions workflow created")
    print("   - Automated testing on multiple Python versions")
    print("   - Security checks with bandit and safety")
    print("   - Automated deployment package creation")

def print_repository_info():
    """Print repository information"""
    print("\n📊 Repository Information:")
    print("=" * 40)
    print("Project: Cattle Breed Identifier")
    print("Event: Smart India Hackathon 2025")
    print("Ministry: Fisheries, Animal Husbandry & Dairying")
    print("Technology: AI/ML, Flask, TensorFlow")
    print("Language: Python, HTML, CSS, JavaScript")
    
    print("\n🎯 Key Features:")
    print("- AI-powered cattle breed identification")
    print("- Comprehensive breed information cards")
    print("- Government scheme integration")
    print("- Livestock registration system")
    print("- Explainable AI with heatmaps")
    print("- Responsive web interface")

def main():
    """Main function"""
    print("🐄 Cattle Breed Identifier - GitHub Repository Setup")
    print("SIH 2025 - Smart India Hackathon")
    print("=" * 60)
    
    # Set up git repository
    if not setup_git_repository():
        print("\n❌ Repository setup failed. Please check the errors above.")
        return
    
    # Create GitHub workflow
    create_github_workflow()
    
    # Print repository information
    print_repository_info()
    
    print("\n🎉 Repository setup completed!")
    print("Your project is ready for GitHub!")
    print("\nNext: Follow the steps above to create and connect your GitHub repository.")

if __name__ == "__main__":
    main()

