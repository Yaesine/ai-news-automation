#!/usr/bin/env python3
"""
LinkedIn Poster using LinkedIn API
More reliable than browser automation
"""

import os
import time
import logging
import requests
from linkedin_api import Linkedin

logger = logging.getLogger(__name__)

def post_to_linkedin_api(email, password, post_content):
    """Post to LinkedIn using LinkedIn API"""
    try:
        print("🔐 Authenticating with LinkedIn API...")
        
        # Authenticate with LinkedIn
        api = Linkedin(email, password)
        
        print("✅ Successfully authenticated with LinkedIn")
        
        # Post content
        print("📝 Creating post...")
        result = api.post(post_content)
        
        if result:
            print("✅ Successfully posted to LinkedIn!")
            return True
        else:
            print("❌ Failed to post to LinkedIn")
            return False
            
    except Exception as e:
        print(f"❌ Error posting to LinkedIn: {e}")
        
        # Handle LinkedIn challenge
        if "CHALLENGE" in str(e):
            print("⚠️ LinkedIn requires additional verification")
            print("💡 This is normal for new automated logins")
            print("🔄 Trying alternative method...")
            return False
        
        return False

def post_to_linkedin_rest_api(email, password, post_content):
    """Alternative method using LinkedIn REST API"""
    try:
        print("🔐 Using LinkedIn REST API...")
        
        # LinkedIn REST API endpoint
        url = "https://api.linkedin.com/v2/ugcPosts"
        
        headers = {
            "Authorization": f"Bearer {get_linkedin_token(email, password)}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0"
        }
        
        data = {
            "author": f"urn:li:person:{get_linkedin_person_id(email, password)}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": post_content
                    },
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }
        
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 201:
            print("✅ Successfully posted to LinkedIn via REST API!")
            return True
        else:
            print(f"❌ Failed to post: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error with REST API: {e}")
        return False

def get_linkedin_token(email, password):
    """Get LinkedIn access token (simplified)"""
    # This would require OAuth2 flow in production
    # For now, we'll use the LinkedIn API library
    return None

def get_linkedin_person_id(email, password):
    """Get LinkedIn person ID (simplified)"""
    # This would require API call to get user profile
    # For now, we'll use the LinkedIn API library
    return None

def post_to_linkedin_selenium(email, password, post_content):
    """Fallback to Selenium if API fails"""
    try:
        from linkedin_poster import post_to_linkedin_selenium as selenium_post
        return selenium_post(email, password, post_content)
    except Exception as e:
        print(f"❌ Selenium fallback failed: {e}")
        return False

def post_to_linkedin(email, password, post_content):
    """Main function to post to LinkedIn with multiple fallback methods"""
    
    print("🚀 Attempting to post to LinkedIn...")
    
    # Try LinkedIn API first
    try:
        if post_to_linkedin_api(email, password, post_content):
            return True
    except Exception as e:
        print(f"LinkedIn API failed: {e}")
    
    # Try REST API
    try:
        if post_to_linkedin_rest_api(email, password, post_content):
            return True
    except Exception as e:
        print(f"REST API failed: {e}")
    
    # Fallback to Selenium
    print("🔄 Falling back to Selenium...")
    return post_to_linkedin_selenium(email, password, post_content)

if __name__ == "__main__":
    # Test the LinkedIn posting
    email = os.getenv('LINKEDIN_EMAIL')
    password = os.getenv('LINKEDIN_PASSWORD')
    
    if not email or not password:
        print("Please set LINKEDIN_EMAIL and LINKEDIN_PASSWORD environment variables")
        exit(1)
    
    test_post = "Test post from AI automation system"
    success = post_to_linkedin(email, password, test_post)
    
    if success:
        print("🎉 LinkedIn posting test successful!")
    else:
        print("❌ LinkedIn posting test failed") 