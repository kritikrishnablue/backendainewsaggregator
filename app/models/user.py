from pydantic import BaseModel, EmailStr
from typing import List, Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    preferences: Optional[dict] = None  # {"topics": List[str], "sources": List[str], "countries": List[str]}
    bookmarks: Optional[List[str]] = None
    liked_articles: Optional[List[str]] = None
    disliked_articles: Optional[List[str]] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    email: EmailStr
    token: str
    preferences: Optional[dict] = None
    reading_history: Optional[List[str]] = None  # List of news article IDs or URLs
    bookmarks: Optional[List[str]] = None
    liked_articles: Optional[List[str]] = None
    disliked_articles: Optional[List[str]] = None
