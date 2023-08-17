from sqlalchemy import select
from app.dao.base import BaseDAO
from app.users.models import Users

from app.database import async_session_maker


class UsersDao(BaseDAO):
    """integrate with database on users"""
    model = Users
    
    @classmethod
    async def get_user_without_password(cls, user_id: int):
        async with async_session_maker() as session:
            query = select(cls.model.email, cls.model.id).where(cls.model.id==user_id)
            data = await session.execute(query)
            result = next(data.iterator)
            return {'id': result[1], 'email': result[0]}
