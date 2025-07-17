from pymongo import MongoClient
import os

MONGO_URL = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URL)

db = client["newsdb"]
users_collection = db["users"]
news_collection = db["news"]
