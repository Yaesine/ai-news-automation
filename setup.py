#!/usr/bin/env python3
"""
Setup script for AI News Automation
Helps users configure the automation system
"""

import os
import sys

def create_env_file():
    """Create .env file with user input"""
    print("🔧 Setting up AI News Automation...")
    print("=" * 50)
    
    # Check if .env already exists
    if os.path.exists('.env'):
        overwrite = input("⚠️  .env file already exists. Overwrite? (y/N): ").lower()
        if overwrite != 'y':
            print("❌ Setup cancelled.")
            return False
    
    print("\n📝 Please provide the following information:")
    print("(Press Enter to skip any field)")
    
    # Get user input
    linkedin_email = input("\nLinkedIn Email: ").strip()
    linkedin_password = input("LinkedIn Password: ").strip()
    news_api_key = input("NewsAPI Key (optional - press Enter to use demo): ").strip()
    openai_api_key = input("OpenAI API Key (for AI post generation): ").strip()
    
    # Create .env content
    env_content = []
    
    if linkedin_email:
        env_content.append(f"LINKEDIN_EMAIL={linkedin_email}")
    
    if linkedin_password:
        env_content.append(f"LINKEDIN_PASSWORD={linkedin_password}")
    
    if news_api_key:
        env_content.append(f"NEWS_API_KEY={news_api_key}")
    
    if openai_api_key:
        env_content.append(f"OPENAI_API_KEY={openai_api_key}")
    
    # Write .env file
    try:
        with open('.env', 'w') as f:
            f.write('\n'.join(env_content))
        
        print("\n✅ .env file created successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False

def install_dependencies():
    """Install Python dependencies"""
    print("\n📦 Installing dependencies...")
    
    try:
        import subprocess
        result = subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Dependencies installed successfully!")
            return True
        else:
            print(f"❌ Error installing dependencies: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def show_next_steps():
    """Show next steps for setup"""
    print("\n📋 Next Steps:")
    print("=" * 50)
    print("1. 🧪 Test the automation:")
    print("   python test_script.py")
    print()
    print("2. 🐙 Set up GitHub repository:")
    print("   git init")
    print("   git add .")
    print("   git commit -m 'Initial commit'")
    print("   git branch -M main")
    print("   git remote add origin https://github.com/yourusername/ai-news-automation.git")
    print("   git push -u origin main")
    print()
    print("3. 🔐 Configure GitHub Secrets:")
    print("   - Go to your GitHub repository")
    print("   - Settings → Secrets and variables → Actions")
    print("   - Add: LINKEDIN_EMAIL, LINKEDIN_PASSWORD, NEWS_API_KEY")
    print()
    print("4. ⏰ The automation will run daily at 9:00 AM UTC")
    print()
    print("📚 For detailed instructions, see README.md")

def main():
    """Main setup function"""
    print("🤖 AI News Automation Setup")
    print("=" * 50)
    
    # Create .env file
    env_created = create_env_file()
    if not env_created:
        return
    
    # Install dependencies
    deps_installed = install_dependencies()
    if not deps_installed:
        print("⚠️  Dependencies installation failed. You may need to install them manually:")
        print("   pip install -r requirements.txt")
    
    # Show next steps
    show_next_steps()
    
    print("\n🎉 Setup complete!")

if __name__ == "__main__":
    main() 