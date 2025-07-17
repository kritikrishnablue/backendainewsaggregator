import httpx
import os

NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
print("Loaded NEWSAPI_KEY:", NEWSAPI_KEY)  # Debug print

BASE_URL = "https://newsapi.org/v2/top-headlines"

def fetch_news(country="in", category=None, q=None):
    params = {
        "apiKey": NEWSAPI_KEY,
        "country": country,
        "pageSize": 10,
    }

    if category:
        params["category"] = category
    if q:
        params["q"] = q

    try:
        response = httpx.get(BASE_URL, params=params)
        response.raise_for_status()
        print("NewsAPI response:", response.json())  # Debug print
        return response.json().get("articles", [])
    except Exception as e:
        print("❌ Error fetching news:", e)
        return []
