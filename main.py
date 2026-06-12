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
# GET NEWS FROM TRUSTED SOURCES
# ======================
def get_news():
    feeds = [
        "http://feeds.bbci.co.uk/news/rss.xml",
        "http://rss.cnn.com/rss/edition.rss",
        "https://www.aljazeera.com/xml/rss/all.xml",
        "https://feeds.reuters.com/reuters/topNews"
    ]

    news_items = []

    for url in feeds:
        feed = feedparser.parse(url)

        for entry in feed.entries[:3]:
            news_items.append(entry.title)

    return "\n".join(news_items)


# ======================
# GENERATE ARTICLE
# ======================
def generate_article(news):
    prompt = f"""
You are a professional international news writer.

Use these headlines from BBC, CNN, Al Jazeera, Reuters:

{news}

Write a NEW original news article.

Requirements:
- 900+ words
- SEO optimized title
- Human journalism style
- Do NOT copy sentences
- Combine similar news and remove duplicates
- Add sections: Introduction, Details, Analysis, Conclusion
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
        "status": "draft"   # safe mode
    }

    res = requests.post(
        url,
        auth=(WP_USERNAME, WP_PASSWORD),
        json=data
    )

    print("STATUS CODE:", res.status_code)
    print("RESPONSE:", res.text)

    return res


# ======================
# MAIN
# ======================
def main():
    print("Bot started...")

    news = get_news()
    print("News collected")

    article = generate_article(news)
    print("Article generated")

    title = "Global News Update - " + datetime.now().strftime("%Y-%m-%d")

    post_to_wordpress(title, article)

    print("Done")


# ======================
# RUN
# ======================
if __name__ == "__main__":
    main()
