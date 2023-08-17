from datetime import date
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.bookings.dao import BokingsDAO
from app.bookings.schemes import SBooking
from app.users.dependencies import get_current_user
from app.users.models import Users


router: APIRouter = APIRouter(prefix='/bookings', tags=['Бронирование'])


@router.get("")
async def get_booking(user: Users = Depends(get_current_user)):
    """all bookings"""
    return user
    

@router.post('/create_booking')
async def create_booking(date_from: date, date_to: date, room_id: int,
                         user: Users = Depends(get_current_user)):
    return await BokingsDAO.create_booking_db(
        date_from=date_from,
        date_to=date_to,
        room_id=room_id,
        user_id=user.id
    )