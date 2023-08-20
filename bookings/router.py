from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status

from app.bookings.dao import BookingsDAO
from app.users.dependencies import get_current_user
from app.users.models import Users


router: APIRouter = APIRouter(prefix='/bookings', tags=['Бронирование'])


@router.get("")
async def get_boking(user: Users = Depends(get_current_user)):
    """all Bookings"""
    return await BookingsDAO.get_all_data(user_id=user.id)
    

@router.post('/create_boking')
async def create_boking(date_from: date, date_to: date, room_id: int,
                         user: Users = Depends(get_current_user)):
    return await BookingsDAO.create_booking_db(
        date_from=date_from,
        date_to=date_to,
        room_id=room_id,
        user_id=user.id
    )
    

@router.delete('/delete_booking/{booking_id}')
async def delete_booking(booking_id: int):
    boking = await BookingsDAO.get_one_data(model_id=booking_id)
    if boking is not None:
        return await BookingsDAO.delete_data(model_id=booking_id)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail='Обьект не найден')


@router.put('/update_booking/{booking_id}')
async def update_boking(booking_id: int):
    boking = await BookingsDAO.get_one_data(model_id=booking_id)
    if boking is not None:
        return await BookingsDAO.update_booking(booking_id=booking_id)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail='Обьект не найден')