from fastapi import Request
from app.services.geo import geo_cached

async def geo_dep(request: Request):
    xff = request.headers.get("X-Forwarded-For", "")
    ip = xff.split(",")[0].strip() if xff else (request.client.host if request.client else "unknown")
    return await geo_cached(ip)
