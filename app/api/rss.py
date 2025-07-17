from fastapi import APIRouter
from app.services.rss_fetcher import fetch_rss_articles

rss_router = APIRouter()

@rss_router.post("/fetch")
def fetch_rss():
    total = fetch_rss_articles()
    return {"message": f"{total} RSS articles saved from multiple global channels"}
