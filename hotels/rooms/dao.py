from app.dao.base import BaseDAO
from app.hotels.rooms.models import Rooms
from app.database import async_session_maker

from sqlalchemy import select


class RoomsDAO(BaseDAO):
    model = Rooms
    
    @classmethod
    async def filter_rooms(cls, hotel_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).where(hotel_id == hotel_id)
            result = await session.execute(query)
            return result.scalars.all()
