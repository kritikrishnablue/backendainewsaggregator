from fastapi import APIRouter, Query
from typing import Optional
from app.services.news_fetcher import fetch_news
from app.services.news_saver import save_articles_to_db

news_router = APIRouter()

@news_router.get("/top-headlines")
def get_top_headlines(country: str = "in", category: Optional[str] = None, q: Optional[str] = None):
    articles = fetch_news(country=country, category=category, q=q)
    return {"articles": articles}

@news_router.post("/save")
def save_news_to_db(country: str = "in", category: Optional[str] = None, q: Optional[str] = None):
    articles = fetch_news(country=country, category=category, q=q)
    count = save_articles_to_db(articles)
    return {"saved": count, "message": f"{count} articles saved to MongoDB"}
