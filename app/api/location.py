from fastapi import APIRouter, Depends
from app.dependencies.geo_dep import geo_dep

loc_router = APIRouter()

@loc_router.get("/location")
async def get_location(geo=Depends(geo_dep)):
    return {"location": geo or "unavailable"}
