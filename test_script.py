#!/usr/bin/env python3
"""
Test script for AI News Automation
Tests the news fetching functionality without posting to LinkedIn
"""

import os
import json
from main import AINewsAutomation

def test_news_fetching():
    """Test the news fetching functionality"""
    print("🤖 Testing AI News Automation...")
    
    # Create automation instance
    automation = AINewsAutomation()
    
    # Test news fetching
    print("📰 Fetching AI news...")
    news_list = automation.fetch_ai_news()
    
    if not news_list:
        print("❌ No news found!")
        return False
    
    print(f"✅ Found {len(news_list)} AI-related articles")
    
    # Display first 3 articles
    print("\n📋 Sample articles:")
    for i, article in enumerate(news_list[:3], 1):
        print(f"\n{i}. {article.get('title', 'No title')}")
        print(f"   Source: {article.get('source', 'Unknown')}")
        print(f"   URL: {article.get('url', 'No URL')}")
        print(f"   Description: {article.get('description', 'No description')[:100]}...")
    
    # Test article selection
    print("\n🎯 Testing article selection...")
    selected_article = automation.select_best_article(news_list)
    
    if selected_article:
        print(f"✅ Selected article: {selected_article.get('title', 'No title')}")
        
        # Test post creation
        print("\n📝 Testing post creation...")
        post_content = automation.create_linkedin_post(selected_article)
        print("✅ Post content generated:")
        print("-" * 50)
        print(post_content)
        print("-" * 50)
        
        # Save test post
        with open('test_post.txt', 'w') as f:
            f.write(post_content)
        print("\n💾 Test post saved to 'test_post.txt'")
        
    else:
        print("❌ No suitable article selected")
        return False
    
    return True

def test_configuration():
    """Test configuration and environment"""
    print("\n⚙️ Testing configuration...")
    
    # Check environment variables
    linkedin_email = os.getenv('LINKEDIN_EMAIL')
    linkedin_password = os.getenv('LINKEDIN_PASSWORD')
    news_api_key = os.getenv('NEWS_API_KEY')
    
    print(f"LinkedIn Email: {'✅ Set' if linkedin_email else '❌ Not set'}")
    print(f"LinkedIn Password: {'✅ Set' if linkedin_password else '❌ Not set'}")
    print(f"News API Key: {'✅ Set' if news_api_key else '❌ Not set (using demo)'}")
    
    # Check if files exist
    files_to_check = ['main.py', 'requirements.txt', '.github/workflows/daily-ai-news.yml']
    
    print("\n📁 Checking required files:")
    for file_path in files_to_check:
        exists = os.path.exists(file_path)
        print(f"{file_path}: {'✅ Exists' if exists else '❌ Missing'}")
    
    return True

def main():
    """Main test function"""
    print("🧪 AI News Automation Test Suite")
    print("=" * 50)
    
    # Test configuration
    config_ok = test_configuration()
    
    if not config_ok:
        print("\n❌ Configuration test failed!")
        return
    
    # Test news fetching
    news_ok = test_news_fetching()
    
    if news_ok:
        print("\n🎉 All tests passed! Your automation is ready to use.")
        print("\n📋 Next steps:")
        print("1. Set up your GitHub repository")
        print("2. Configure GitHub Secrets")
        print("3. Push your code to GitHub")
        print("4. The automation will run daily at 9:00 AM UTC")
    else:
        print("\n❌ News fetching test failed!")
        print("Check your internet connection and API keys.")

if __name__ == "__main__":
    main() 