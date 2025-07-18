from app.database.mongo import news_collection
from app.services.summarizer import summarize_text
from datetime import datetime

def save_articles_to_db(articles: list, user_country: str | None = None):
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

        # ✏️ Choose content or description for summarization
        content = article.get("content") or article.get("description") or ""

        # 🧠 Generate summary
        summary = summarize_text(content)
        print("🧠 Summary generated:", summary)

        # 📦 Add summary and metadata
        article["summary"] = summary
        article["saved_at"] = datetime.utcnow()

        if user_country:
            article["userCountry"] = user_country.upper()

        # 💾 Save to MongoDB
        news_collection.insert_one(article)
        saved += 1

    print(f"✅ Total saved with summaries: {saved}")
    return saved
