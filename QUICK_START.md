# 🚀 Quick Start Guide

Get your AI News Automation running in 5 minutes!

## Step 1: Setup (2 minutes)

```bash
# Run the setup script
python setup.py
```

This will:
- Create your `.env` file
- Install dependencies
- Guide you through configuration

## Step 2: Test (1 minute)

```bash
# Test the automation
python test_script.py
```

This will:
- Fetch AI news from multiple sources
- Generate a sample LinkedIn post
- Save it to `test_post.txt`

## Step 3: GitHub Setup (2 minutes)

```bash
# Initialize git repository
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/ai-news-automation.git
git push -u origin main
```

## Step 4: Configure GitHub Secrets

1. Go to your GitHub repository
2. Settings → Secrets and variables → Actions
3. Add these secrets:
   - `LINKEDIN_EMAIL`: Your LinkedIn email
   - `LINKEDIN_PASSWORD`: Your LinkedIn password  
   - `NEWS_API_KEY`: Your NewsAPI key (optional)

## Step 5: Done! 🎉

Your automation will now run daily at 9:00 AM UTC and post AI news to LinkedIn!

## Manual Testing

Want to test posting right now?

```bash
# Run the full automation
python main.py
```

## Troubleshooting

- **No news found**: Check your internet connection
- **LinkedIn login issues**: Verify your credentials
- **GitHub Actions failing**: Check the Actions tab for logs

## Need Help?

- Check the full `README.md` for detailed instructions
- Look at the logs in `ai_news_automation.log`
- GitHub Actions logs are in the Actions tab

---

**That's it! Your AI news automation is ready to go! 🤖📰** 