#!/usr/bin/env python3
"""
AI News Automation Script
Fetches AI technology news daily and posts to LinkedIn
"""

import os
import json
import requests
import random
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import logging
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ai_news_automation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AINewsAutomation:
    def __init__(self):
        self.linkedin_email = os.getenv('LINKEDIN_EMAIL')
        self.linkedin_password = os.getenv('LINKEDIN_PASSWORD')
        self.news_api_key = os.getenv('NEWS_API_KEY', 'demo')  # Free tier key
        self.posted_articles_file = 'posted_articles.json'
        self.load_posted_articles()
        
    def load_posted_articles(self):
        """Load previously posted articles to avoid duplicates"""
        try:
            if os.path.exists(self.posted_articles_file):
                with open(self.posted_articles_file, 'r') as f:
                    self.posted_articles = json.load(f)
            else:
                self.posted_articles = []
        except Exception as e:
            logger.error(f"Error loading posted articles: {e}")
            self.posted_articles = []
    
    def save_posted_articles(self):
        """Save posted articles to avoid duplicates"""
        try:
            with open(self.posted_articles_file, 'w') as f:
                json.dump(self.posted_articles, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving posted articles: {e}")
    
    def fetch_ai_news(self) -> List[Dict]:
        """Fetch AI technology news from multiple sources"""
        news_sources = [
            self._fetch_from_newsapi,
            self._fetch_from_techcrunch,
            self._fetch_from_venturebeat
        ]
        
        all_news = []
        
        for source_func in news_sources:
            try:
                news = source_func()
                if news:
                    all_news.extend(news)
                time.sleep(1)  # Be respectful to APIs
            except Exception as e:
                logger.error(f"Error fetching from {source_func.__name__}: {e}")
        
        # Remove duplicates and filter for AI-related content
        unique_news = self._deduplicate_news(all_news)
        ai_filtered_news = self._filter_ai_news(unique_news)
        
        logger.info(f"Fetched {len(ai_filtered_news)} AI-related news articles")
        return ai_filtered_news
    
    def _fetch_from_newsapi(self) -> List[Dict]:
        """Fetch news from NewsAPI (free tier)"""
        try:
            url = "https://newsapi.org/v2/everything"
            params = {
                'q': 'artificial intelligence OR machine learning OR AI technology',
                'language': 'en',
                'sortBy': 'publishedAt',
                'pageSize': 20,
                'apiKey': self.news_api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            articles = []
            
            for article in data.get('articles', []):
                articles.append({
                    'title': article.get('title', ''),
                    'description': article.get('description', ''),
                    'url': article.get('url', ''),
                    'source': article.get('source', {}).get('name', ''),
                    'published_at': article.get('publishedAt', ''),
                    'content': article.get('content', '')
                })
            
            return articles
            
        except Exception as e:
            logger.error(f"Error fetching from NewsAPI: {e}")
            return []
    
    def _fetch_from_techcrunch(self) -> List[Dict]:
        """Fetch AI news from TechCrunch RSS feed"""
        try:
            url = "https://techcrunch.com/feed/"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            # Simple XML parsing for RSS feed
            import xml.etree.ElementTree as ET
            root = ET.fromstring(response.content)
            
            articles = []
            ai_keywords = ['ai', 'artificial intelligence', 'machine learning', 'deep learning', 'neural network']
            
            for item in root.findall('.//item'):
                title = item.find('title').text if item.find('title') is not None else ''
                description = item.find('description').text if item.find('description') is not None else ''
                link = item.find('link').text if item.find('link') is not None else ''
                pub_date = item.find('pubDate').text if item.find('pubDate') is not None else ''
                
                # Check if article is AI-related
                if any(keyword in title.lower() or keyword in description.lower() for keyword in ai_keywords):
                    articles.append({
                        'title': title,
                        'description': description,
                        'url': link,
                        'source': 'TechCrunch',
                        'published_at': pub_date,
                        'content': description
                    })
            
            return articles[:10]  # Limit to 10 articles
            
        except Exception as e:
            logger.error(f"Error fetching from TechCrunch: {e}")
            return []
    
    def _fetch_from_venturebeat(self) -> List[Dict]:
        """Fetch AI news from VentureBeat RSS feed"""
        try:
            url = "https://venturebeat.com/feed/"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            import xml.etree.ElementTree as ET
            root = ET.fromstring(response.content)
            
            articles = []
            ai_keywords = ['ai', 'artificial intelligence', 'machine learning', 'deep learning', 'neural network']
            
            for item in root.findall('.//item'):
                title = item.find('title').text if item.find('title') is not None else ''
                description = item.find('description').text if item.find('description') is not None else ''
                link = item.find('link').text if item.find('link') is not None else ''
                pub_date = item.find('pubDate').text if item.find('pubDate') is not None else ''
                
                # Check if article is AI-related
                if any(keyword in title.lower() or keyword in description.lower() for keyword in ai_keywords):
                    articles.append({
                        'title': title,
                        'description': description,
                        'url': link,
                        'source': 'VentureBeat',
                        'published_at': pub_date,
                        'content': description
                    })
            
            return articles[:10]  # Limit to 10 articles
            
        except Exception as e:
            logger.error(f"Error fetching from VentureBeat: {e}")
            return []
    
    def _deduplicate_news(self, news_list: List[Dict]) -> List[Dict]:
        """Remove duplicate articles based on URL"""
        seen_urls = set()
        unique_news = []
        
        for article in news_list:
            if article.get('url') and article['url'] not in seen_urls:
                seen_urls.add(article['url'])
                unique_news.append(article)
        
        return unique_news
    
    def _filter_ai_news(self, news_list: List[Dict]) -> List[Dict]:
        """Filter news to ensure they are AI-related"""
        ai_keywords = [
            'artificial intelligence', 'ai', 'machine learning', 'ml', 'deep learning',
            'neural network', 'chatgpt', 'gpt', 'llm', 'large language model',
            'computer vision', 'natural language processing', 'nlp', 'robotics',
            'autonomous', 'algorithm', 'data science', 'automation'
        ]
        
        filtered_news = []
        
        for article in news_list:
            title = article.get('title', '').lower()
            description = article.get('description', '').lower()
            content = article.get('content', '').lower()
            
            # Check if any AI keyword is present
            if any(keyword in title or keyword in description or keyword in content for keyword in ai_keywords):
                filtered_news.append(article)
        
        return filtered_news
    
    def select_best_article(self, news_list: List[Dict]) -> Optional[Dict]:
        """Select the best article to post (not previously posted)"""
        if not news_list:
            return None
        
        # Filter out previously posted articles
        available_articles = [
            article for article in news_list 
            if article.get('url') not in [posted.get('url') for posted in self.posted_articles]
        ]
        
        if not available_articles:
            logger.info("No new articles available to post")
            return None
        
        # Select a random article from the top 5 (to add variety)
        top_articles = available_articles[:5]
        selected_article = random.choice(top_articles)
        
        return selected_article
    
    def create_linkedin_post(self, article: Dict) -> str:
        """Create an engaging LinkedIn post from the article"""
        title = article.get('title', '')
        description = article.get('description', '')
        url = article.get('url', '')
        source = article.get('source', '')
        
        # Clean up description (remove HTML tags if present)
        import re
        clean_description = re.sub(r'<[^>]+>', '', description)
        clean_description = clean_description[:250] + '...' if len(clean_description) > 250 else clean_description
        
        # Create different storytelling styles
        import random
        story_templates = [
            f"""AI Technology Update: {title}

{clean_description}

This development represents another milestone in the AI revolution. As we witness these technological breakthroughs, it's remarkable to see how artificial intelligence continues to transform our world in unexpected ways.

The pace of innovation in AI is accelerating, and stories like this remind us of the profound impact these technologies will have on our future.

What are your thoughts on this development? How do you see this technology shaping the industry?

Read more: {url}

#AI #ArtificialIntelligence #Technology #Innovation #MachineLearning #TechNews

---
Source: {source} | Posted via AI News Automation""",

            f"""AI Technology Update: {title}

{clean_description}

In the ever-evolving landscape of artificial intelligence, developments like this showcase the incredible potential of AI to solve real-world challenges. As technology continues to advance, we're seeing AI applications that were once science fiction become reality.

This story highlights the growing intersection between AI and various industries, demonstrating how these technologies are reshaping the way we work and live.

What are your thoughts on this development? How do you think this will impact the industry?

Read more: {url}

#AI #ArtificialIntelligence #Technology #Innovation #MachineLearning #TechNews

---
Source: {source} | Posted via AI News Automation""",

            f"""AI Technology Update: {title}

{clean_description}

The world of artificial intelligence continues to surprise us with groundbreaking developments. This story illustrates how AI is becoming an integral part of our technological landscape, driving innovation across multiple sectors.

As we move forward, it's fascinating to observe how these technologies evolve and create new opportunities for growth and advancement.

What are your thoughts on this development? How do you see this technology progressing?

Read more: {url}

#AI #ArtificialIntelligence #Technology #Innovation #MachineLearning #TechNews

---
Source: {source} | Posted via AI News Automation"""
        ]
        
        # Select a random storytelling style
        post_content = random.choice(story_templates)
        
        return post_content
    
    def post_to_linkedin(self, post_content: str) -> bool:
        """Post content to LinkedIn using Selenium (free alternative)"""
        try:
            if not self.linkedin_email or not self.linkedin_password:
                logger.error("LinkedIn credentials not provided")
                return False
            
            # Try to use Selenium for automated posting
            try:
                from linkedin_poster import post_to_linkedin_selenium
                success = post_to_linkedin_selenium(self.linkedin_email, self.linkedin_password, post_content)
                if success:
                    logger.info("Successfully posted to LinkedIn using Selenium")
                    return True
            except Exception as e:
                logger.warning(f"Selenium posting failed: {e}")
            
            # Fallback: save post content to file for manual posting
            logger.info("Saving post content to file for manual posting...")
            with open('linkedin_post.txt', 'w') as f:
                f.write(post_content)
            
            logger.info("Post content saved to linkedin_post.txt")
            return True
                
        except Exception as e:
            logger.error(f"Error posting to LinkedIn: {e}")
            return False
    
    def run_automation(self):
        """Main automation function"""
        logger.info("Starting AI News Automation...")
        
        try:
            # Fetch AI news
            news_list = self.fetch_ai_news()
            
            if not news_list:
                logger.warning("No AI news found today")
                return
            
            # Select best article
            selected_article = self.select_best_article(news_list)
            
            if not selected_article:
                logger.info("No suitable article to post today")
                return
            
            # Create LinkedIn post
            post_content = self.create_linkedin_post(selected_article)
            
            # Post to LinkedIn
            success = self.post_to_linkedin(post_content)
            
            if success:
                # Mark article as posted
                self.posted_articles.append({
                    'url': selected_article.get('url'),
                    'title': selected_article.get('title'),
                    'posted_at': datetime.now().isoformat()
                })
                self.save_posted_articles()
                
                logger.info(f"Successfully posted: {selected_article.get('title')}")
            else:
                logger.error("Failed to post to LinkedIn")
        
        except Exception as e:
            logger.error(f"Error in automation: {e}")

def main():
    """Main function"""
    automation = AINewsAutomation()
    automation.run_automation()

if __name__ == "__main__":
    main() 