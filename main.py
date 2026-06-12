import os
import requests
import feedparser
import google.generativeai as genai
from datetime import datetime

# ======================
# ENV VARIABLES
# ======================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
WP_URL = os.getenv("WP_URL")
WP_USERNAME = os.getenv("WP_USERNAME")
WP_PASSWORD = os.getenv("WP_PASSWORD")

# ======================
# GEMINI SETUP
# ======================
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")


# ======================
# GET NEWS (RSS)
# ======================
def get_news():
    feed = feedparser.parse("https://news.google.com/rss")
    
    news_items = []
    for entry in feed.entries[:5]:
        news_items.append(entry.title)

    return "\n".join(news_items)


# ======================
# GENERATE ARTICLE
# ======================
def generate_article(news):
    prompt = f"""
You are a professional English news writer.

Read these headlines:
{news}

Write a unique SEO-friendly news article.

Requirements:
- 800+ words
- Human tone
- No copy-paste
- Add introduction, key points, conclusion
"""

    response = model.generate_content(prompt)
    return response.text


# ======================
# POST TO WORDPRESS
# ======================
def post_to_wordpress(title, content):
    url = f"{WP_URL}/wp-json/wp/v2/posts"

    data = {
        "title": title,
        "content": content,
        "status": "draft"   # আগে draft রাখলাম safe এর জন্য
    }

    res = requests.post(
        url,
        auth=(WP_USERNAME, WP_PASSWORD),
        json=data
    )

    # 🔥 DEBUG (সবচেয়ে গুরুত্বপূর্ণ অংশ)
    print("STATUS CODE:", res.status_code)
    print("RESPONSE TEXT:", res.text)

    return res


# ======================
# MAIN FUNCTION
# ======================
def main():
    print("Bot started...")

    news = get_news()
    print("News fetched")

    article = generate_article(news)
    print("Article generated")

    title = "AI Daily News - " + datetime.now().strftime("%Y-%m-%d")

    res = post_to_wordpress(title, article)

    print("Finished")


# ======================
# RUN
# ======================
if __name__ == "__main__":
    main()
