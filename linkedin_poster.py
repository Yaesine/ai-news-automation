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
        
        # Uncomment the line below if you want to run headless (no browser window)
        # chrome_options.add_argument("--headless")
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            return True
        except Exception as e:
            logger.error(f"Error setting up Chrome driver: {e}")
            return False
    
    def login_to_linkedin(self):
        """Login to LinkedIn"""
        try:
            self.driver.get("https://www.linkedin.com/login")
            
            # Wait for page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            
            # Enter email
            email_field = self.driver.find_element(By.ID, "username")
            email_field.send_keys(self.email)
            
            # Enter password
            password_field = self.driver.find_element(By.ID, "password")
            password_field.send_keys(self.password)
            
            # Click sign in button
            sign_in_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            sign_in_button.click()
            
            # Wait for login to complete
            WebDriverWait(self.driver, 15).until(
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