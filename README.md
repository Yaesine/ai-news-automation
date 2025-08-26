# AI News Automation 🤖

An automated system that fetches AI technology news daily and posts to LinkedIn using free tools and APIs.

## Features

- 🔍 **Multi-source news fetching**: NewsAPI, TechCrunch RSS, VentureBeat RSS
- 🤖 **AI content filtering**: Automatically filters for AI-related articles
- 📝 **Smart post generation**: Creates engaging LinkedIn posts with hashtags
- 🔄 **Duplicate prevention**: Tracks posted articles to avoid repetition
- ⏰ **Automated scheduling**: Runs daily via GitHub Actions
- 🆓 **Free tools only**: Uses free APIs and services

## How It Works

1. **News Fetching**: The script fetches news from multiple sources
2. **Content Filtering**: Filters articles for AI-related content using keywords
3. **Article Selection**: Randomly selects from top 5 articles (adds variety)
4. **Post Creation**: Generates engaging LinkedIn posts with hashtags
5. **Automated Posting**: Posts to LinkedIn using Selenium automation
6. **Tracking**: Saves posted articles to prevent duplicates

## Setup Instructions

### Prerequisites

- Python 3.8+
- Chrome browser (for Selenium automation)
- GitHub account (for free hosting and scheduling)
- LinkedIn account

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd ai-news-automation
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Get Free API Keys

#### NewsAPI (Free Tier)
1. Go to [NewsAPI](https://newsapi.org/)
2. Sign up for a free account
3. Get your API key (1000 requests/day free)

### 4. Set Environment Variables

Create a `.env` file in the project root:

```env
LINKEDIN_EMAIL=your_linkedin_email@example.com
LINKEDIN_PASSWORD=your_linkedin_password
NEWS_API_KEY=your_newsapi_key_here
```

### 5. GitHub Repository Setup

1. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/ai-news-automation.git
   git push -u origin main
   ```

2. **Set GitHub Secrets**:
   - Go to your GitHub repository
   - Navigate to Settings → Secrets and variables → Actions
   - Add the following secrets:
     - `LINKEDIN_EMAIL`: Your LinkedIn email
     - `LINKEDIN_PASSWORD`: Your LinkedIn password
     - `NEWS_API_KEY`: Your NewsAPI key

### 6. Test Locally

```bash
python main.py
```

## Usage

### Manual Execution

```bash
python main.py
```

### Automated Daily Execution

The GitHub Actions workflow runs automatically every day at 9:00 AM UTC. You can also trigger it manually:

1. Go to your GitHub repository
2. Click on "Actions" tab
3. Select "Daily AI News Automation"
4. Click "Run workflow"

## Configuration

### Customizing News Sources

Edit `main.py` to add or modify news sources:

```python
def fetch_ai_news(self) -> List[Dict]:
    news_sources = [
        self._fetch_from_newsapi,
        self._fetch_from_techcrunch,
        self._fetch_from_venturebeat,
        # Add your custom source here
    ]
```

### Customizing AI Keywords

Modify the AI keywords in `main.py`:

```python
ai_keywords = [
    'artificial intelligence', 'ai', 'machine learning', 'ml', 'deep learning',
    'neural network', 'chatgpt', 'gpt', 'llm', 'large language model',
    # Add your custom keywords
]
```

### Customizing Post Format

Edit the `create_linkedin_post` method in `main.py`:

```python
post_content = f"""🤖 AI Technology Update: {title}

{clean_description}

🔗 Read more: {url}

#AI #ArtificialIntelligence #Technology #Innovation #MachineLearning #TechNews

What are your thoughts on this development? Share your insights below! 👇

---
Source: {source} | Posted via AI News Automation 🤖"""
```

## File Structure

```
ai-news-automation/
├── main.py                          # Main automation script
├── linkedin_poster.py              # LinkedIn posting with Selenium
├── requirements.txt                 # Python dependencies
├── .github/workflows/
│   └── daily-ai-news.yml           # GitHub Actions workflow
├── README.md                       # This file
├── .env                           # Environment variables (create this)
├── posted_articles.json           # Tracks posted articles
├── linkedin_post.txt              # Generated post content
└── ai_news_automation.log         # Automation logs
```

## Free Tools Used

- **GitHub**: Repository hosting and GitHub Actions (free tier)
- **NewsAPI**: News aggregation (1000 requests/day free)
- **TechCrunch RSS**: Free RSS feed
- **VentureBeat RSS**: Free RSS feed
- **Selenium**: Free browser automation
- **Python**: Free programming language

## Troubleshooting

### Common Issues

1. **LinkedIn Login Issues**:
   - Ensure your LinkedIn credentials are correct
   - Consider using 2FA and app passwords
   - LinkedIn may detect automation - use sparingly

2. **NewsAPI Rate Limits**:
   - Free tier allows 1000 requests/day
   - The script uses 1 request per run
   - Consider upgrading if you need more

3. **ChromeDriver Issues**:
   - Ensure Chrome browser is installed
   - The GitHub Actions workflow handles this automatically

4. **No Articles Found**:
   - Check your internet connection
   - Verify NewsAPI key is valid
   - RSS feeds might be temporarily unavailable

### Logs

Check the logs for detailed information:
- `ai_news_automation.log`: Detailed automation logs
- GitHub Actions logs: Available in the Actions tab

## Security Notes

- Never commit your `.env` file to version control
- Use GitHub Secrets for sensitive information
- Consider using LinkedIn app passwords instead of your main password
- The script runs in a secure GitHub Actions environment

## Contributing

Feel free to contribute by:
- Adding new news sources
- Improving the post generation algorithm
- Enhancing error handling
- Adding new features

## License

This project is open source and available under the MIT License.

## Support

If you encounter issues:
1. Check the logs for error messages
2. Verify your API keys and credentials
3. Ensure all dependencies are installed
4. Check GitHub Actions status

---

**Note**: This automation tool is for educational purposes. Please respect LinkedIn's terms of service and use responsibly. 