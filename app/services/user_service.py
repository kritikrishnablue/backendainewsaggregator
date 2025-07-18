from app.database.mongo import users_collection, news_collection
from fastapi import HTTPException
import urllib.parse

# Like an article

def like_article(user_email: str, article_id: str):
    if not article_id:
        raise HTTPException(status_code=400, detail="Missing article_id or url")
    users_collection.update_one(
        {"email": user_email},
        {"$addToSet": {"liked_articles": article_id}, "$pull": {"disliked_articles": article_id}}
    )
    news_collection.update_one(
        {"url": article_id},
        {"$inc": {"like_count": 1, "dislike_count": -1}},
        upsert=True
    )
    return {"message": "Article liked", "article": article_id}

# Dislike an article

def dislike_article(user_email: str, article_id: str):
    if not article_id:
        raise HTTPException(status_code=400, detail="Missing article_id or url")
    users_collection.update_one(
        {"email": user_email},
        {"$addToSet": {"disliked_articles": article_id}, "$pull": {"liked_articles": article_id}}
    )
    news_collection.update_one(
        {"url": article_id},
        {"$inc": {"dislike_count": 1, "like_count": -1}},
        upsert=True
    )
    return {"message": "Article disliked", "article": article_id}

# Share an article (returns share URLs for social media)
def share_article(article_url: str, title: str = ""):
    if not article_url:
        raise HTTPException(status_code=400, detail="Missing article url")
    encoded_url = urllib.parse.quote_plus(article_url)
    encoded_title = urllib.parse.quote_plus(title)
    news_collection.update_one(
        {"url": article_url},
        {"$inc": {"share_count": 1}},
        upsert=True
    )
    return {
        "share_url": article_url,
        "twitter": f"https://twitter.com/intent/tweet?url={encoded_url}&text={encoded_title}",
        "facebook": f"https://www.facebook.com/sharer/sharer.php?u={encoded_url}",
        "linkedin": f"https://www.linkedin.com/shareArticle?mini=true&url={encoded_url}&title={encoded_title}",
        "whatsapp": f"https://api.whatsapp.com/send?text={encoded_title}%20{encoded_url}",
        "telegram": f"https://t.me/share/url?url={encoded_url}&text={encoded_title}",
        "email": f"mailto:?subject={encoded_title}&body={encoded_url}"
    } 