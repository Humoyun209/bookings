from typing import Annotated
from fastapi import APIRouter, Depends
from app.hotels.dao import HotelsDAO


router = APIRouter(prefix="/hotel", tags=["Отелы"])


@router.get('/hotels')
async def get_hotels():
    result =  await HotelsDAO.get_all_data()
    return result