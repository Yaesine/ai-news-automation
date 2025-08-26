#!/usr/bin/env python3
"""
LinkedIn Poster using Selenium
Automated posting to LinkedIn using browser automation
"""

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

logger = logging.getLogger(__name__)

class LinkedInPoster:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.driver = None
        
    def setup_driver(self):
        """Setup Chrome driver with appropriate options"""
        chrome_options = Options()
        
        # Add options for better automation
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Run with browser window visible for better LinkedIn compatibility
        # chrome_options.add_argument("--headless")
        
        # Add more options to avoid detection
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--allow-running-insecure-content")
        chrome_options.add_argument("--disable-features=VizDisplayCompositor")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36")
        
        try:
            # Try different Chrome paths for GitHub Actions and macOS
            chrome_paths = [
                "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",  # macOS
                "/usr/bin/google-chrome",
                "/usr/bin/chromium-browser",
                "/opt/hostedtoolcache/setup-chrome/chrome/stable/x64/chrome",
                "/usr/bin/chromium",
                "/snap/bin/chromium"
            ]
            
            chrome_found = False
            for chrome_path in chrome_paths:
                if os.path.exists(chrome_path):
                    chrome_options.binary_location = chrome_path
                    logger.info(f"Found Chrome at: {chrome_path}")
                    chrome_found = True
                    break
            
            if not chrome_found:
                logger.warning("Chrome not found in standard paths, trying default")
            
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            return True
        except Exception as e:
            logger.error(f"Error setting up Chrome driver: {e}")
            # Try to install Chrome if not found
            try:
                logger.info("Attempting to install Chrome...")
                import subprocess
                subprocess.run(["sudo", "apt-get", "update"], check=True)
                subprocess.run(["sudo", "apt-get", "install", "-y", "google-chrome-stable"], check=True)
                logger.info("Chrome installed successfully")
                return True
            except Exception as install_error:
                logger.error(f"Failed to install Chrome: {install_error}")
                return False
    
    def login_to_linkedin(self):
        """Login to LinkedIn with improved error handling"""
        try:
            print("🌐 Navigating to LinkedIn login page...")
            self.driver.get("https://www.linkedin.com/login")
            
            # Wait for page to load with longer timeout
            print("⏳ Waiting for login form to load...")
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            
            # Add delay to simulate human behavior
            time.sleep(2)
            
            # Enter email
            print("📧 Entering email...")
            email_field = self.driver.find_element(By.ID, "username")
            email_field.clear()
            email_field.send_keys(self.email)
            time.sleep(1)
            
            # Enter password
            print("🔒 Entering password...")
            password_field = self.driver.find_element(By.ID, "password")
            password_field.clear()
            password_field.send_keys(self.password)
            time.sleep(1)
            
            # Click sign in button
            print("🔘 Clicking sign in button...")
            sign_in_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            sign_in_button.click()
            
            # Wait for login to complete with longer timeout
            print("⏳ Waiting for login to complete...")
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-test-id='nav-home']"))
            )
            
            logger.info("Successfully logged in to LinkedIn")
            return True
            
        except TimeoutException:
            logger.error("Timeout during LinkedIn login")
            return False
        except Exception as e:
            logger.error(f"Error during LinkedIn login: {e}")
            return False
    
    def create_post(self, post_content):
        """Create a new post on LinkedIn"""
        try:
            # Navigate to LinkedIn home page
            self.driver.get("https://www.linkedin.com/feed/")
            time.sleep(3)
            
            # Find and click the "Start a post" button
            start_post_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Start a post']"))
            )
            start_post_button.click()
            
            # Wait for post modal to appear
            post_modal = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-test-id='post-modal']"))
            )
            
            # Find the post text area
            post_text_area = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-test-id='post-modal'] div[role='textbox']"))
            )
            
            # Clear any existing text and enter post content
            post_text_area.clear()
            post_text_area.send_keys(post_content)
            
            # Wait a moment for the post to be processed
            time.sleep(2)
            
            # Click the "Post" button
            post_button = self.driver.find_element(By.CSS_SELECTOR, "button[data-test-id='post-button']")
            post_button.click()
            
            # Wait for post to be published
            time.sleep(5)
            
            logger.info("Successfully posted to LinkedIn")
            return True
            
        except TimeoutException:
            logger.error("Timeout while creating LinkedIn post")
            return False
        except Exception as e:
            logger.error(f"Error creating LinkedIn post: {e}")
            return False
    
    def close_driver(self):
        """Close the browser driver"""
        if self.driver:
            self.driver.quit()
            logger.info("Browser driver closed")

def post_to_linkedin_selenium(email, password, post_content):
    """Main function to post to LinkedIn using Selenium"""
    poster = LinkedInPoster(email, password)
    
    try:
        # Setup driver
        if not poster.setup_driver():
            return False
        
        # Login to LinkedIn
        if not poster.login_to_linkedin():
            return False
        
        # Create post
        success = poster.create_post(post_content)
        
        return success
        
    except Exception as e:
        logger.error(f"Error in LinkedIn posting: {e}")
        return False
    finally:
        poster.close_driver()

if __name__ == "__main__":
    # Example usage
    email = os.getenv('LINKEDIN_EMAIL')
    password = os.getenv('LINKEDIN_PASSWORD')
    
    if not email or not password:
        print("Please set LINKEDIN_EMAIL and LINKEDIN_PASSWORD environment variables")
        exit(1)
    
    # Read post content from file
    try:
        with open('linkedin_post.txt', 'r') as f:
            post_content = f.read()
    except FileNotFoundError:
        print("linkedin_post.txt not found")
        exit(1)
    
    success = post_to_linkedin_selenium(email, password, post_content)
    
    if success:
        print("Successfully posted to LinkedIn!")
    else:
        print("Failed to post to LinkedIn") 