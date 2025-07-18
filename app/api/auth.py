from fastapi import APIRouter, HTTPException, Depends, Header
from app.models.user import UserCreate, UserLogin, UserOut
from app.database.mongo import users_collection
from app.core.auth import get_password_hash, verify_password, create_access_token
from typing import Optional
import os

auth_router = APIRouter()

def get_current_user(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")
    token = authorization.split(" ", 1)[1]
    try:
        from jose import jwt
        payload = jwt.decode(token, os.getenv("SECRET_KEY", "supersecret"), algorithms=["HS256"])
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        user = users_collection.find_one({"email": email})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

@auth_router.post("/register", response_model=UserOut)
def register(user: UserCreate):
    if users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_pw = get_password_hash(user.password)
    user_doc = {
        "email": user.email,
        "password": hashed_pw,
        "preferences": user.preferences or {"topics": [], "sources": [], "countries": []},
        "reading_history": [],
        "bookmarks": user.bookmarks or [],
        "liked_articles": user.liked_articles or []
    }
    users_collection.insert_one(user_doc)
    token = create_access_token({"sub": user.email})
    return {
        "email": user.email,
        "token": token,
        "preferences": user_doc["preferences"],
        "reading_history": user_doc["reading_history"],
        "bookmarks": user_doc["bookmarks"],
        "liked_articles": user_doc["liked_articles"]
    }

@auth_router.post("/login", response_model=UserOut)
def login(user: UserLogin):
    db_user = users_collection.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.email})
    return {
        "email": user.email,
        "token": token,
        "preferences": db_user.get("preferences", {"topics": [], "sources": [], "countries": []}),
        "reading_history": db_user.get("reading_history", []),
        "bookmarks": db_user.get("bookmarks", []),
        "liked_articles": db_user.get("liked_articles", [])
    }
