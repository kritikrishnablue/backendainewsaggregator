import feedparser
from datetime import datetime
from app.database.mongo import news_collection
from app.services.summarizer import summarize_text

# 🌍 List of global + Australian RSS feeds and their channel names
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

    # 🇦🇺 Australian feeds
    ("https://www.abc.net.au/news/feed/51120/rss.xml", "ABC News Australia"),
    ("https://www.theguardian.com/au/rss", "The Guardian Australia"),
    ("https://www.sbs.com.au/news/feed", "SBS News"),
    ("https://www.smh.com.au/rss/feed.xml", "Sydney Morning Herald"),
    ("https://www.theage.com.au/rss/world.xml", "The Age"),
    ("https://www.theaustralian.com.au/rss/world.xml", "The Australian"),
    ("https://www.theconversation.com/au/rss/world", "The Conversation"),
]

def fetch_rss_articles(user_country: str | None = None):
    total_saved = 0

    for rss_url, channel_name in FEEDS:
        print(f"\n🌍 Fetching from {channel_name}...")
        feed = feedparser.parse(rss_url)
        print(f"📡 Found {len(feed.entries)} entries.")

        for entry in feed.entries:
            url = entry.get("link")
            if not url or news_collection.find_one({"url": url}):
                continue

            # 🧹 Clean title
            title = entry.get("title", "")
            if isinstance(title, list):
                title = " ".join(str(t) for t in title)
            if not title:
                title = "No Title"
            title = title.strip()

            # ✂️ Extract summary text
            summary_text = entry.get("summary", "")
            if isinstance(summary_text, list):
                summary_text = " ".join(str(s) for s in summary_text)
            if not summary_text:
                summary_text = entry.get("description", "")
                if isinstance(summary_text, list):
                    summary_text = " ".join(str(s) for s in summary_text)
            if not summary_text:
                summary_text = title

            # 🧠 Summarize
            try:
                ai_summary = summarize_text(summary_text)
            except Exception as e:
                print(f"⚠️ Error summarizing article: {title[:50]}... | Error: {e}")
                ai_summary = summary_text[:150] + "..."  # fallback

            # 🕒 Published date
            published_at = entry.get("published", datetime.utcnow().isoformat())

            # 📦 Construct the article document
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

            if user_country:
                article["userCountry"] = user_country.upper()

            # 💾 Insert into MongoDB
            try:
                news_collection.insert_one(article)
                print(f"✅ Saved: {title}")
                total_saved += 1
            except Exception as db_err:
                print(f"❌ DB Insert Failed: {title[:50]}... | Error: {db_err}")

    print(f"\n🎉 Total RSS articles saved: {total_saved}")
    return total_saved
