from datetime import date, datetime

from fastapi import HTTPException
from fastapi import status

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.models import Hotels
from app.hotels.rooms.dao import RoomsDAO
from app.hotels.rooms.models import Rooms

from sqlalchemy import between, func, or_, select, and_, update
from sqlalchemy.orm import joinedload


def get_left_rooms(date_from: date, date_to: date):
    return select(Rooms.id.label('room_id'), func.count(Bookings.room_id).label('cnt_bk')).select_from(Rooms)\
                .join(Bookings, Bookings.room_id == Rooms.id, isouter=True).where(or_(
                    and_(date_to > Bookings.date_to, date_from < Bookings.date_from),
                    between(date_from, Bookings.date_from, Bookings.date_to),
                    between(date_to, Bookings.date_from, Bookings.date_to)
                )).group_by(Rooms.id).order_by(Rooms.id).cte('left_rooms')


class BookingsDAO(BaseDAO):
    """Data axios object for Bookings"""
    model = Bookings
    
    @staticmethod
    def get_update_data(booking: Bookings, **kwargs) -> dict:
        result = {}
        for key in kwargs:
            if kwargs[key] is None:
                result[key] = booking.__dict__[key]
            else:
                result[key] = kwargs[key]
        return result
                
    
    @classmethod
    async def create_booking_db(cls, date_from: date, date_to: date, room_id: int, user_id: int) -> Bookings:
        async with async_session_maker() as session:
            if date_from < datetime.now().date():
                return None
            left_rooms = get_left_rooms(date_from, date_to) 
            print(date_from)
            
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
        
    @classmethod
    async def update_booking(cls, booking_id: int, room_id: int, **kwargs):
        async with async_session_maker() as session:
            
            booking = await cls.get_one_data(model_id=booking_id)
            
            query1 = select(Hotels.id).select_from(Hotels).\
                    join(Rooms, Rooms.hotel_id == Hotels.id).\
                    join(Bookings, Bookings.room_id == Rooms.id).\
                    where(Bookings.id == booking_id)
                    
            hotel_id = await session.execute(query1)
            
            query2 = select(Rooms.id).where(Rooms.hotel_id == hotel_id.scalar())
            
            room_ids = await session.execute(query2)
            if room_id not in room_ids.scalars().all():
                return None
            
            query = update(Bookings).where(Bookings.id == booking_id).values(
                **cls.get_update_data(booking, **kwargs)
            ).returning(Bookings)
            
            result = await session.execute(query)
            await session.commit()

            return result.scalar()
        
    
        
        