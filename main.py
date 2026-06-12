import os
import requests
import feedparser
import google.generativeai as genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
WP_URL = os.getenv("WP_URL")
WP_USERNAME = os.getenv("WP_USERNAME")
WP_PASSWORD = os.getenv("WP_PASSWORD")

genai.configure(api_key=GEMINI_API_KEY)

def get_news():
    feed = feedparser.parse("https://news.google.com/rss")
    news_list = []

    for entry in feed.entries[:5]:
        news_list.append(entry.title + " - " + entry.link)

    return "\n".join(news_list)

def generate_article(news):
    model = genai.GenerativeModel("gemini-1.5-pro")

    prompt = f"""
You are a professional news writer.

Read these news headlines:
{news}

Write a NEW original English news article.

Requirements:
- 800+ words
- SEO friendly title
- Human tone
- No copying sentences
- Add introduction, key points, conclusion
"""

    response = model.generate_content(prompt)
    return response.text

def post_to_wordpress(title, content):
    url = f"{WP_URL}/wp-json/wp/v2/posts"

    data = {
        "title": title,
        "content": content,
        "status": "draft"
    }

    res = requests.post(url, auth=(WP_USERNAME, WP_PASSWORD), json=data)

    print(res.text)

def main():
    news = get_news()
    article = generate_article(news)

    title = "AI Daily News"

    post_to_wordpress(title, article)

main()
