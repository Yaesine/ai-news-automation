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
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
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
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
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
        """Create an engaging LinkedIn post from the article using AI generation"""
        title = article.get('title', '')
        description = article.get('description', '')
        url = article.get('url', '')
        source = article.get('source', '')
        
        # Clean up description (remove HTML tags if present)
        import re
        clean_description = re.sub(r'<[^>]+>', '', description)
        clean_description = clean_description[:300] + '...' if len(clean_description) > 300 else clean_description
        
        # Create AI prompt for dynamic post generation
        ai_prompt = f"""Create a unique, engaging LinkedIn post about this AI technology news. 

News Title: {title}
News Description: {clean_description}
Source: {source}

Requirements:
- Write in first person as a business professional who helps companies implement AI solutions
- Use a conversational, storytelling tone
- Focus on business value and practical applications
- Include 2-3 paragraphs of thoughtful commentary
- End with an engaging question for the audience
- Include the URL and relevant hashtags
- Make it sound natural and personal, not automated
- Vary the writing style and approach each time
- Keep it professional but conversational
- Focus on how AI can help businesses solve real problems

The post should be unique and different from typical AI news posts. Make it sound like a real person sharing insights about AI technology and its business impact."""

                # Use Cohere AI (free tier) for post generation (works with GitHub Actions)
        try:
            import cohere
            
            # Get Cohere API key from environment (free tier available)
            cohere_api_key = os.getenv('COHERE_API_KEY')
            if not cohere_api_key:
                logger.warning("Cohere API key not found, using fallback template system")
                raise Exception("No Cohere API key")
            
            # Configure Cohere client
            co = cohere.Client(cohere_api_key)
            
            # Create AI prompt for dynamic post generation
            ai_prompt = f"""Create a unique, engaging LinkedIn post about this AI technology news. 

News Title: {title}
News Description: {clean_description}
Source: {source}

Requirements:
- Write in first person as a business professional who helps companies implement AI solutions
- Use a conversational, storytelling tone
- Focus on business value and practical applications
- Include 2-3 paragraphs of thoughtful commentary
- End with an engaging question for the audience
- Include the URL and relevant hashtags
- Make it sound natural and personal, not automated
- Vary the writing style and approach
- Keep it professional but conversational
- Focus on how AI can help businesses solve real problems
- Maximum 300 words total

The post should be unique and different from typical AI news posts. Make it sound like a real person sharing insights about AI technology and its business impact.

Format the response as a complete LinkedIn post ready to publish."""

            # Generate post using Cohere AI
            response = co.generate(
                model='command',
                prompt=ai_prompt,
                max_tokens=500,
                temperature=0.8,
                k=0,
                stop_sequences=[],
                return_likelihoods='NONE'
            )
            
            # Extract the generated post
            post_content = response.generations[0].text.strip()
            
            # Ensure the post includes the URL and hashtags
            if url not in post_content:
                post_content += f"\n\nRead more: {url}"
            
            if "#AI" not in post_content:
                post_content += "\n\n#AI #ArtificialIntelligence #Technology #Innovation #MachineLearning #BusinessGrowth"
            
            logger.info("Successfully generated post using Cohere AI")
            return post_content
            
        except Exception as e:
            logger.warning(f"Cohere AI generation failed: {e}, using fallback template system")
            
        # Fallback to template system if AI fails
            import random
            
            # Create dynamic storytelling approaches
            intros = [
                "When I look at the latest developments in AI technology, I see incredible opportunities for businesses to transform their operations.",
                "The pace of AI innovation continues to amaze me, and this latest development is a perfect example of how technology is solving real business challenges.",
                "Every day, I see businesses struggling with inefficient processes that hold back their potential. That's why developments like this in AI technology are so important.",
                "Another fascinating development in the AI space caught my attention today.",
                "I'm constantly amazed by how AI technology continues to evolve and solve real-world problems.",
                "Today's AI developments continue to show the incredible potential of intelligent automation.",
                "The AI landscape is evolving rapidly, and this latest development caught my attention for good reason.",
                "I'm always excited to see how AI technology continues to push boundaries and create new possibilities.",
                "This development in AI technology highlights exactly what I love about working with intelligent automation.",
                "As someone who helps companies implement AI solutions, developments like this always excite me.",
                "The world of AI continues to surprise us with groundbreaking innovations that solve real business problems.",
                "What I find most compelling about this AI development is how it demonstrates practical business applications."
            ]
            
            insights = [
                "This development highlights how artificial intelligence is reshaping industries and creating new possibilities for growth and efficiency. As someone who works with AI solutions, I find these breakthroughs particularly exciting because they demonstrate the real-world impact of intelligent automation.",
                "What I find most valuable about developments like this is how they demonstrate the practical applications of AI beyond just hype. These are real solutions that can help businesses streamline operations, reduce costs, and improve efficiency.",
                "This development represents another step forward in making AI more accessible and practical for businesses of all sizes. What I find most compelling is how these technologies are moving beyond theoretical applications to deliver tangible business value.",
                "This breakthrough highlights what I love about working with AI solutions - the ability to transform complex challenges into streamlined, efficient processes. It's remarkable how these technologies can turn what once seemed impossible into practical, implementable solutions.",
                "What I appreciate most about innovations like this is how they demonstrate the real-world impact of intelligent automation. Too often, AI is seen as something only available to large tech companies, but developments like this show how accessible and valuable these technologies are becoming.",
                "As someone who works with companies to implement AI solutions, I see the growing demand for intelligent automation that can drive real results. Developments like this show why more organizations are turning to AI to gain competitive advantages."
            ]
            
            business_value = [
                "What strikes me most is how this technology can help businesses eliminate manual processes, accelerate workflows, and free teams to focus on what truly matters - innovation and strategic growth.",
                "The key to successful AI implementation is understanding how these technologies can be applied strategically to address specific business challenges and drive measurable results.",
                "I work with organizations to identify where AI can make the biggest difference, and stories like this reinforce why the investment in intelligent automation is becoming essential for competitive businesses.",
                "The beauty of AI is that it can be tailored to address specific business challenges, whether that's automating repetitive tasks, improving decision-making, or creating new opportunities for growth.",
                "As someone who helps companies implement AI solutions, I see the transformative potential in stories like this. The key is understanding how to apply these technologies strategically to achieve measurable business outcomes.",
                "What I find most compelling is how AI is becoming an essential tool for businesses looking to stay ahead in today's competitive landscape. The companies that embrace these technologies early will have a significant advantage."
            ]
            
            questions = [
                "What are your thoughts on this development? How do you see AI transforming your industry?",
                "How do you think this technology will impact your business? What opportunities do you see for AI in your industry?",
                "How do you see AI helping your business overcome current challenges? What processes could benefit from intelligent automation?",
                "What aspects of this development do you find most interesting? How could similar technologies benefit your business?",
                "How do you see this technology evolving? What opportunities does it create for your industry?",
                "What do you think about this development? How could similar technologies benefit your organization?",
                "How do you think this technology will evolve? What opportunities does it create for your business?",
                "What challenges could AI help you solve in your organization?",
                "How do you think this development could benefit your organization? What challenges could AI help you solve?"
            ]
            
            # Randomly select components to create unique posts
            intro = random.choice(intros)
            insight = random.choice(insights)
            value = random.choice(business_value)
            question = random.choice(questions)
            
            # Create the post
            post_content = f"""{intro}

{clean_description}

{insight}

{value}

{question}

Read more: {url}

#AI #ArtificialIntelligence #Technology #Innovation #MachineLearning #BusinessGrowth"""
        
        return post_content
    
    def post_to_linkedin(self, post_content: str) -> bool:
        """Post content to LinkedIn using Selenium (free alternative)"""
        try:
            if not self.linkedin_email or not self.linkedin_password:
                logger.error("LinkedIn credentials not provided")
                return False
            
            # Try to use Selenium for automated posting
            try:
                from linkedin_api_poster import post_to_linkedin
                success = post_to_linkedin(self.linkedin_email, self.linkedin_password, post_content)
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
                # Mark article as posted (even if just saved to file)
                self.posted_articles.append({
                    'url': selected_article.get('url'),
                    'title': selected_article.get('title'),
                    'posted_at': datetime.now().isoformat()
                })
                self.save_posted_articles()
                
                logger.info(f"Successfully processed: {selected_article.get('title')}")
            else:
                logger.warning("LinkedIn posting failed, but article was processed")
        
        except Exception as e:
            logger.error(f"Error in automation: {e}")
            # Don't let the automation fail completely
            logger.info("Automation completed with errors, but system is still functional")

def main():
    """Main function"""
    automation = AINewsAutomation()
    automation.run_automation()

if __name__ == "__main__":
    main() 