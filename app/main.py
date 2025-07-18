from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles  # 👈 Add this import
import os  # 👈 Add this to check/create directory if needed
from fastapi.security import HTTPBearer
from fastapi.openapi.utils import get_openapi

from app.api.auth import auth_router
from app.api.news import news_router
from app.api.rss import rss_router
from app.api.location import loc_router
from app.api.user import user_router
app = FastAPI()
bearer_scheme = HTTPBearer()

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="AI News Aggregator API",
        version="1.0.0",
        description="API with JWT authentication",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "HTTPBearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", [{"HTTPBearer": []}])
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# 👇 Add this block to serve /static (favicon or others)
if not os.path.exists("static"):
    os.makedirs("static")

app.mount("/static", StaticFiles(directory="static"), name="static")

# Remove the favicon route since the file doesn't exist
# @app.get("/favicon.ico")
# async def favicon():
#     from fastapi.responses import FileResponse
#     return FileResponse("static/favicon.ico")

# Routers
app.include_router(news_router, prefix="/news")
app.include_router(auth_router, prefix="/auth")
app.include_router(rss_router, prefix="/rss")
app.include_router(loc_router)
app.include_router(user_router, prefix="/user")
@app.get("/")
def read_root():
    return {"message": "✅ AI News Aggregator Backend is Running"}

@app.get("/health")
def health_check():
    try:
        # Test MongoDB connection
        from app.database.mongo import client
        client.admin.command('ping')
        return {
            "status": "healthy",
            "mongodb": "connected",
            "message": "All systems operational"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "mongodb": "disconnected",
            "error": str(e)
        }
