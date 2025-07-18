from app.database.mongo import news_collection
from datetime import datetime, timedelta

def get_trending_articles(limit=10, hours=48):
    # Only consider articles from the last X hours (if publishedAt or saved_at exists)
    time_filter = {}
    now = datetime.utcnow()
    if news_collection.find_one({"saved_at": {"$exists": True}}):
        since = now - timedelta(hours=hours)
        time_filter = {"saved_at": {"$gte": since}}
    # Compute engagement score: likes + shares + dislikes (optionally weight likes/shares higher)
    pipeline = [
        {"$match": time_filter} if time_filter else {},
        {"$addFields": {"engagement": {"$add": [
            {"$ifNull": ["$like_count", 0]},
            {"$ifNull": ["$share_count", 0]},
            {"$ifNull": ["$dislike_count", 0]}
        ]}}},
        {"$sort": {"engagement": -1, "saved_at": -1}},
        {"$limit": limit}
    ]
    # Remove empty $match if not needed
    if not time_filter:
        pipeline = pipeline[1:]
    articles = list(news_collection.aggregate(pipeline))
    for a in articles:
        a["like_count"] = a.get("like_count", 0)
        a["dislike_count"] = a.get("dislike_count", 0)
        a["share_count"] = a.get("share_count", 0)
        a["engagement"] = a.get("engagement", 0)
    return articles

def search_articles(
    keywords: str = "",
    start_date: str = None,
    end_date: str = None,
    source: str = None,
    limit: int = 20
):
    query = {}
    if keywords:
        query["$text"] = {"$search": keywords}
    if start_date or end_date:
        date_filter = {}
        if start_date:
            date_filter["$gte"] = start_date
        if end_date:
            date_filter["$lte"] = end_date
        query["publishedAt"] = date_filter
    if source:
        query["channel"] = source

    projection = {"score": {"$meta": "textScore"}}
    cursor = news_collection.find(query, projection)
    if keywords:
        cursor = cursor.sort([("score", {"$meta": "textScore"})])
    else:
        cursor = cursor.sort("publishedAt", -1)
    cursor = cursor.limit(limit)
    articles = list(cursor)
    for a in articles:
        a["like_count"] = a.get("like_count", 0)
        a["dislike_count"] = a.get("dislike_count", 0)
        a["share_count"] = a.get("share_count", 0)
    return articles 