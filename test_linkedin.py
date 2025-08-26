#!/usr/bin/env python3
"""
Test LinkedIn login functionality
"""

import os
from dotenv import load_dotenv
from linkedin_poster import LinkedInPoster

def test_linkedin_login():
    """Test LinkedIn login step by step"""
    load_dotenv()
    
    email = os.getenv('LINKEDIN_EMAIL')
    password = os.getenv('LINKEDIN_PASSWORD')
    
    print(f"Email: {email}")
    print(f"Password: {'*' * len(password) if password else 'NOT SET'}")
    
    if not email or not password:
        print("❌ LinkedIn credentials not found in .env file")
        return False
    
    print("\n🔧 Testing LinkedIn login...")
    
    try:
        poster = LinkedInPoster(email, password)
        
        # Test driver setup
        print("1. Setting up Chrome driver...")
        driver_success = poster.setup_driver()
        print(f"   Driver setup: {'✅ Success' if driver_success else '❌ Failed'}")
        
        if not driver_success:
            print("❌ Failed to setup Chrome driver")
            return False
        
        # Test login
        print("2. Attempting LinkedIn login...")
        login_success = poster.login_to_linkedin()
        print(f"   Login result: {'✅ Success' if login_success else '❌ Failed'}")
        
        if login_success:
            print("3. Testing post creation...")
            post_success = poster.create_post("Test post from AI automation")
            print(f"   Post creation: {'✅ Success' if post_success else '❌ Failed'}")
        
        return login_success
        
    except Exception as e:
        print(f"❌ Error during LinkedIn test: {e}")
        return False
    finally:
        if hasattr(poster, 'driver') and poster.driver:
            poster.driver.quit()

if __name__ == "__main__":
    test_linkedin_login() 