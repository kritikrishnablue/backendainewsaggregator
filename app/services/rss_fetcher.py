import feedparser
from datetime import datetime
from app.database.mongo import news_collection
from app.services.summarizer import summarize_text

# 🌍 List of global RSS feeds and their source names
FEEDS = [
    ("https://feeds.bbci.co.uk/news/world/rss.xml", "BBC World"),
    ("https://rss.cnn.com/rss/edition_world.rss", "CNN World"),
    ("https://www.aljazeera.com/xml/rss/all.xml", "Al Jazeera"),
    ("https://www.reutersagency.com/feed/?best-topics=world&post_type=best", "Reuters World"),
    ("https://rss.nytimes.com/services/xml/rss/nyt/World.xml", "New York Times"),
    ("https://feeds.a.dj.com/rss/RSSWorldNews.xml", "Wall Street Journal"),
    ("https://www.cnbc.com/id/100727362/device/rss/rss.html", "CNBC World"),
    ("https://www.npr.org/rss/rss.php?id=1004", "NPR World"),
    ("https://feeds.skynews.com/feeds/rss/world.xml", "Sky News"),
    ("https://www.dw.com/en/top-stories/s-9097/rss", "Deutsche Welle"),
    ("https://timesofindia.indiatimes.com/rssfeeds/296589292.cms", "Times of India"),
    ("https://www.abc.net.au/news/feed/51120/rss.xml", "ABC News Australia"),
("https://www.theguardian.com/au/rss", "The Guardian Australia"),
("https://www.sbs.com.au/news/feed", "SBS News"),
("https://www.smh.com.au/rss/feed.xml", "Sydney Morning Herald"),
]

def safe_to_str(val):
    if isinstance(val, list):
        return " ".join(str(v) for v in val)
    if val is None:
        return ""
    return str(val)

def fetch_rss_articles():
    total_saved = 0

    for rss_url, channel_name in FEEDS:
        print(f"\n🌍 Fetching from {channel_name}...")
        feed = feedparser.parse(rss_url)
        print(f"📡 Found {len(feed.entries)} entries.")

        for entry in feed.entries:
            url = entry.get("link")
            if not url or news_collection.find_one({"url": url}):
                continue

            title = safe_to_str(entry.get("title", "")).strip()
            summary_text = safe_to_str(entry.get("summary", "")) or safe_to_str(entry.get("description", "")) or title
            published_at = safe_to_str(entry.get("published", datetime.utcnow().isoformat()))

            try:
                ai_summary = summarize_text(summary_text)
            except Exception as e:
                print(f"⚠️ Error summarizing article: {title[:50]}... | Error: {e}")
                ai_summary = safe_to_str(summary_text)[:150] + "..."  # fallback

            article = {
                "title": title,
                "url": url,
                "original_summary": summary_text,
                "summary": ai_summary,
                "publishedAt": published_at,
                "channel": channel_name,
                "source": "RSS",
                "saved_at": datetime.utcnow(),
            }

            try:
                news_collection.insert_one(article)
                print(f"✅ Saved: {title}")
                total_saved += 1
            except Exception as db_err:
                print(f"❌ DB Insert Failed: {title[:50]}... | Error: {db_err}")

    print(f"\n🎉 Total RSS articles saved: {total_saved}")
    return total_saved
