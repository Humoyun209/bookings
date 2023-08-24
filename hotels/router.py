import asyncio
from datetime import date
from typing import Annotated
from fastapi import APIRouter, Depends
from app.hotels.dao import HotelsDAO

from fastapi_cache.decorator import cache


router = APIRouter(prefix="/hotel", tags=["Отелы"])


@router.get('/hotels') 
@cache(expire=300)
async def get_hotels(location: str, date_from: date, date_to: date):
    await asyncio.sleep(1)
    result = await HotelsDAO.get_all_rooms_with_staticstics(date_from, date_to, location)
    return result