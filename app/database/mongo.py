from pymongo import MongoClient
import os

MONGO_URL = os.getenv("MONGO_URI")
if not MONGO_URL:
    raise ValueError("MONGO_URI environment variable is not set")

try:
    client = MongoClient(MONGO_URL)
    # Test the connection
    client.admin.command('ping')
    print("✅ MongoDB connection successful")
except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")
    raise

db = client["newsdb"]
users_collection = db["users"]
news_collection = db["news"]
