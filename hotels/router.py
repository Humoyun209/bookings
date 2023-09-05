import asyncio
from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from app.hotels.dao import HotelsDAO
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(prefix="/hotels", tags=["Отелы"])


@router.get('') 
# @cache(expire=300)
async def get_hotels(location: str, date_from: date, date_to: date, user: Users = Depends(get_current_user)):
    result = await HotelsDAO.get_all_rooms_with_staticstics(date_from, date_to, location)
    return result