from datetime import date

from fastapi import HTTPException
from fastapi import status

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.rooms.models import Rooms

from sqlalchemy import between, func, or_, select, and_


"""booked_rooms = select(func.count(cls.model.id).label('cnt')).where(
                                and_(
                                    cls.model.room_id == Rooms.id,
                                    or_(
                                        between(date_from, cls.model.date_from, cls.model.date_to),
                                        between(date_to, cls.model.date_from, cls.model.date_to)
                                    ))
                                ).cte('boked_rooms')
            query = select(Rooms.id, Rooms.quantity - booked_rooms.c.cnt)
            result = await session.execute(query)
            lst = list(result.iterator)
            
            room_price = await session.execute(
                select(Rooms.price).where(Rooms.id==room_id)
            )
            
            cnt_rooms = None
            
            for ls in lst: 
                if ls[0] == room_id:
                    cnt_rooms = ls[1]
            
            booking_id = None
            
            if cnt_rooms > 0:
                booking_id = await cls.insert_data(
                    room_id=room_id,
                    user_id=user_id,
                    date_from=date_from,
                    date_to=date_to,
                    price=room_price.scalar_one_or_none()
                ) 
            else:
                raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                    detail='Все комнаты заняты')

            return booking_id"""

class BokingsDAO(BaseDAO):
    """Data axios object for Bookings"""
    model = Bookings
    
    @classmethod
    async def create_booking_db(cls, date_from: date, date_to: date, room_id: int, user_id: int):
        async with async_session_maker() as session:
            query1 = select(cls.model.room_id, func.count(cls.model.id).label('count_bookings')).\
                    where(or_(
                        between(cls.model.date_from, date_from, date_to),
                        between(cls.model.date_to, date_from, date_to)
                    )).group_by(cls.model.room_id)
            
            query2 = select(Rooms.id, Rooms.quantity, Rooms.price)
                    
            booking_rooms_session = await session.execute(query1)
            booking_rooms_count = list(map(list, list(booking_rooms_session.iterator)))
            
            all_rooms_session = await session.execute(query2)
            all_rooms_count = list(map(list, list(all_rooms_session.iterator)))
            
            for b_rooms in booking_rooms_count:
                for a_rooms in all_rooms_count:
                    if b_rooms[0] == a_rooms[0]:
                        a_rooms[1] -= b_rooms[1]
            cnt_rooms, room_price = None, None
            for ls in all_rooms_count: 
                if ls[0] == room_id:
                    cnt_rooms, room_price = ls[1], ls[2]
            
            if cnt_rooms > 0:
                booking_id = await cls.insert_data(
                    room_id=room_id,
                    user_id=user_id,
                    date_from=date_from,
                    date_to=date_to,
                    price=room_price
                ) 
            else:
                raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                    detail='Все комнаты заняты')
            return booking_id