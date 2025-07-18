import httpx
from functools import lru_cache
import asyncio

# 🌍 IPAPI endpoint (no API key needed)
GEO_URL = "https://ipapi.co/{ip}/json/"

# Remove @lru_cache and make geo_cached async
async def geo_cached(ip: str):
    return await get_geo(ip)


# 🌐 Get location info using ipapi.co
async def get_geo(ip: str) -> dict | None:
    if ip == "127.0.0.1" or ip.startswith("192.168."):
        ip = ""  # Let API auto-detect server public IP in local dev

    try:
        async with httpx.AsyncClient(timeout=3) as client:
            response = await client.get(GEO_URL.format(ip=ip))
            response.raise_for_status()
            data = response.json()

            return {
                "ip": ip or "auto",
                "country": data.get("country_name"),
                "country_code": data.get("country_code"),
                "city": data.get("city"),
                "lat": data.get("latitude"),
                "lon": data.get("longitude"),
                "timezone": data.get("timezone")
            }

    except Exception as e:
        print("❌ IP location fetch failed:", e)
        return None
