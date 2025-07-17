from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles  # 👈 Add this import
import os  # 👈 Add this to check/create directory if needed

from app.api.auth import auth_router
from app.api.news import news_router
from app.api.rss import rss_router
app = FastAPI()

# 👇 Add this block to serve /static (favicon or others)
if not os.path.exists("static"):
    os.makedirs("static")

app.mount("/static", StaticFiles(directory="static"), name="static")

# 👇 Add this to redirect /favicon.ico to your static folder
@app.get("/favicon.ico")
async def favicon():
    from fastapi.responses import FileResponse
    return FileResponse("static/favicon.ico")

# Routers
app.include_router(news_router, prefix="/news")
app.include_router(auth_router, prefix="/auth")
app.include_router(rss_router, prefix="/rss")
@app.get("/")
def read_root():
    return {"message": "✅ AI News Aggregator Backend is Running"}
