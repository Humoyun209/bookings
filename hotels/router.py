import asyncio
from datetime import date
from typing import Annotated
from fastapi import APIRouter, Depends
from app.hotels.dao import HotelsDAO

from fastapi_cache.decorator import cache




router = APIRouter(prefix="/hotel", tags=["Отелы"])


@router.get('/hotels')
async def get_hotels(date_from: date, date_to: date):
    result = await HotelsDAO.get_all_rooms_with_staticstics(date_from, date_to)
    return result