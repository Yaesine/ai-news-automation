#!/usr/bin/env python3
"""
Quick test to verify AI News Automation is working
"""

import os
from dotenv import load_dotenv

def test_environment():
    """Test if environment variables are loaded"""
    load_dotenv()
    
    print("🔧 Environment Test")
    print("=" * 40)
    
    linkedin_email = os.getenv('LINKEDIN_EMAIL')
    linkedin_password = os.getenv('LINKEDIN_PASSWORD')
    news_api_key = os.getenv('NEWS_API_KEY')
    
    print(f"LinkedIn Email: {'✅ Set' if linkedin_email else '❌ Not set'}")
    print(f"LinkedIn Password: {'✅ Set' if linkedin_password else '❌ Not set'}")
    print(f"News API Key: {'✅ Set' if news_api_key else '❌ Not set (using demo)'}")
    
    return bool(linkedin_email and linkedin_password)

def test_files():
    """Test if required files exist"""
    print("\n📁 Files Test")
    print("=" * 40)
    
    required_files = [
        'main.py',
        'linkedin_poster.py',
        'requirements.txt',
        '.github/workflows/daily-ai-news.yml',
        '.env'
    ]
    
    all_exist = True
    for file_path in required_files:
        exists = os.path.exists(file_path)
        print(f"{file_path}: {'✅ Exists' if exists else '❌ Missing'}")
        if not exists:
            all_exist = False
    
    return all_exist

def test_news_fetching():
    """Test news fetching functionality"""
    print("\n📰 News Fetching Test")
    print("=" * 40)
    
    try:
        from main import AINewsAutomation
        
        automation = AINewsAutomation()
        news_list = automation.fetch_ai_news()
        
        if news_list:
            print(f"✅ Successfully fetched {len(news_list)} articles")
            print(f"📋 Sample: {news_list[0].get('title', 'No title')[:50]}...")
            return True
        else:
            print("❌ No articles fetched")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 AI News Automation - Quick Test")
    print("=" * 50)
    
    # Test environment
    env_ok = test_environment()
    
    # Test files
    files_ok = test_files()
    
    # Test news fetching
    news_ok = test_news_fetching()
    
    # Summary
    print("\n📊 Test Summary")
    print("=" * 40)
    print(f"Environment: {'✅ OK' if env_ok else '❌ Issues'}")
    print(f"Files: {'✅ OK' if files_ok else '❌ Issues'}")
    print(f"News Fetching: {'✅ OK' if news_ok else '❌ Issues'}")
    
    if env_ok and files_ok and news_ok:
        print("\n🎉 All tests passed! Your automation is working correctly.")
        print("\n📋 Next steps:")
        print("1. Set up GitHub Secrets for automated posting")
        print("2. Test the full automation: python3 main.py")
        print("3. Check GitHub Actions for scheduled runs")
    else:
        print("\n⚠️  Some tests failed. Check the issues above.")
    
    print("\n🔗 Your repository: https://github.com/Yaesine/ai-news-automation")

if __name__ == "__main__":
    main() 