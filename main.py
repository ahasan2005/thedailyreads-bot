from google import genai
import os

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_article(news):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"""
Write a professional English news article based on this:

{news}

- 800+ words
- SEO friendly
- No copy paste
"""
    )
    return response.text
