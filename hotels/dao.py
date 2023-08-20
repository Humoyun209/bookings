from datetime import date
from app.bookings.dao import get_left_rooms
from app.dao.base import BaseDAO
from app.hotels.models import Hotels
from app.database import async_session_maker

from sqlalchemy import func, select

from app.hotels.rooms.models import Rooms


class HotelsDAO(BaseDAO):
    model = Hotels
    
    async def get_all_rooms_with_staticstics(date_from: date, date_to: date):
        async with async_session_maker() as session:
            left_rooms = get_left_rooms(date_from, date_to)
            
            query = select(Hotels.id, Hotels.name, Hotels.location, Hotels.services, Hotels.rooms_quantity, func.coalesce(
                Rooms.quantity - left_rooms.c.cnt_bk, Rooms.quantity).label('empty_rooms')
            ).select_from(Rooms).join(left_rooms, left_rooms.c.room_id == Rooms.id, isouter=True)\
             .join(Hotels, Hotels.id == Rooms.hotel_id, isouter=True)
            
            data = await session.execute(query)
            arr = list(map(list, data.fetchall()))
            
            without_doubles, doubles, result = [], [], []
            
            for row in arr:
                if row[0] in doubles:
                    for r in without_doubles:
                        if r[0] == row[0]:
                            r[5] = row[5] + r[5]
                else:
                    doubles.append(row[0])
                    without_doubles.append(row)
            
            for row in without_doubles:
                result.append({
                    'hotel_id': row[0],
                    'name': row[1],
                    'location': row[2],
                    'services': row[3],
                    'rooms_quantity': row[4],
                    'empty_rooms': row[5]
                })
               
            return result
