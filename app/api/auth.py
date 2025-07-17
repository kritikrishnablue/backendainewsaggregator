from fastapi import APIRouter, HTTPException
from app.models.user import UserCreate, UserLogin, UserOut
from app.database.mongo import users_collection
from app.core.auth import get_password_hash, verify_password, create_access_token

auth_router = APIRouter()

@auth_router.post("/register", response_model=UserOut)
def register(user: UserCreate):
    if users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_pw = get_password_hash(user.password)
    users_collection.insert_one({"email": user.email, "password": hashed_pw})
    token = create_access_token({"sub": user.email})
    return {"email": user.email, "token": token}

@auth_router.post("/login", response_model=UserOut)
def login(user: UserLogin):
    db_user = users_collection.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.email})
    return {"email": user.email, "token": token}
