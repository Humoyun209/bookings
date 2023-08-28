from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status

from app.bookings.dao import BookingsDAO
from app.bookings.schemes import SBooking
from app.tasks.tasks import get_mail_text, send_message
from app.users.dependencies import get_current_user
from app.users.models import Users

router: APIRouter = APIRouter(prefix='/bookings', tags=['Бронирование'])


@router.get("")
async def get_bokings(user: Users = Depends(get_current_user)):
    """all Bookings"""
    return await BookingsDAO.get_all_data(user_id=user.id)
    

@router.post('/create_boking', status_code=201)
async def create_boking(date_from: date, date_to: date, room_id: int,
                         user: Users = Depends(get_current_user)):
    result =  await BookingsDAO.create_booking_db(
        date_from=date_from,
        date_to=date_to,
        room_id=room_id,
        user_id=user.id
    )
    if result is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Ошибка при вводе даты')
        
    booking_dict = {'date_from': result.date_from, 'date_to': result.date_to}
    # send_message.delay(booking_dict, user.email)
    return result
    

@router.delete('/delete_booking/{booking_id}')
async def delete_booking(booking_id: int,
                         user: Users = Depends(get_current_user)):
    boking = await BookingsDAO.get_one_data(model_id=booking_id, user_id=user.id)
    if boking is not None:
        return await BookingsDAO.delete_data(model_id=booking_id)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail='Обьект не найден')


@router.put('/update_booking/{booking_id}')
async def update_boking(booking_id: int, date_from: Optional[date] = None, date_to: Optional[date] = None,
                        room_id: Optional[int] = None,user: Users = Depends(get_current_user)):
    booking = await BookingsDAO.get_one_data_by_filter(id=booking_id, user_id=user.id)
    if booking is not None:
        result = await BookingsDAO.update_booking(booking_id=booking_id,
                                                room_id=room_id,
                                                date_from=date_from,
                                                date_to=date_to)
        if result is None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                        detail='Вы не можете обновить брона такими параметрами')
        return result
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail='Обьект не найден')
