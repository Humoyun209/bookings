from datetime import date

from fastapi import HTTPException
from fastapi import status

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.rooms.models import Rooms

from sqlalchemy import between, func, or_, select, and_


def get_left_rooms(date_from: date, date_to: date):
    return select(Rooms.id.label('room_id'), func.count(Bookings.room_id).label('cnt_bk')).select_from(Rooms)\
                .join(Bookings, Bookings.room_id == Rooms.id, isouter=True).where(or_(
                    and_(date_to > Bookings.date_to, date_from < Bookings.date_from),
                    between(date_from, Bookings.date_from, Bookings.date_to),
                    between(date_to, Bookings.date_from, Bookings.date_to)
                )).group_by(Rooms.id).order_by(Rooms.id).cte('left_rooms')


class BokingsDAO(BaseDAO):
    """Data axios object for Bookings"""
    model = Bookings
    @classmethod
    async def create_booking_db(cls, date_from: date, date_to: date, room_id: int, user_id: int) -> Bookings:
        async with async_session_maker() as session:
            left_rooms = get_left_rooms(date_from, date_to) 
            
            query = select(Rooms.id, Rooms.price, func.coalesce(Rooms.quantity - left_rooms.c.cnt_bk, Rooms.quantity).\
                            label('empty_rooms')).select_from(Rooms).join(left_rooms, left_rooms.c.room_id ==Rooms.id, isouter=True)
                
            data = await session.execute(query)
            result  = list(map(list, list(data.iterator)))
            booking = cnt_rooms = None
            
            for ls in result: 
                if ls[0] == room_id:
                    cnt_rooms, room_price = ls[2], ls[1]
        
            if cnt_rooms > 0:
                booking = await cls.insert_data(
                    room_id=room_id, 
                    user_id=user_id,
                    date_from=date_from, 
                    date_to=date_to,
                    price=room_price
                ) 
            else:
                raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                    detail='Все комнаты заняты')
            return booking