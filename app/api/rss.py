from fastapi import APIRouter, Depends
from app.services.rss_fetcher import fetch_rss_articles
from app.dependencies.geo_dep import geo_dep

# 🚀 Define RSS router
rss_router = APIRouter()

# 📡 Route to fetch RSS feeds, tagged with user country
@rss_router.post("/fetch")
async def fetch_rss(geo=Depends(geo_dep)):
    user_country = geo.get("country_code") if geo else None
    print(f"🌐 Detected user country: {user_country}")

    total = fetch_rss_articles(user_country=user_country)

    return {
        "message": f"✅ Total RSS articles saved: {total}",
        "userCountry": user_country
    }
