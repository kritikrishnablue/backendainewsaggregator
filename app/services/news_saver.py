from app.database.mongo import news_collection
from app.services.summarizer import summarize_text
from datetime import datetime

def save_articles_to_db(articles: list):
    saved = 0
    for article in articles:
        url = article.get("url")
        print("🔍 Checking:", url)

        if not url:
            continue

        exists = news_collection.find_one({"url": url})
        print("🟡 Already exists in DB:", bool(exists))

        if exists:
            continue

        # 👇 Extract content or fallback to description
        content = article.get("content") or article.get("description") or ""

        # 🧠 Generate summary
        summary = summarize_text(content)
        print("🧠 Summary:", summary)

        # ✅ Add fields before saving
        article["summary"] = summary
        article["saved_at"] = datetime.utcnow()

        news_collection.insert_one(article)
        saved += 1

    print(f"✅ Total saved with summaries: {saved}")
    return saved
