from sqlalchemy import insert, select
from app.database import  async_session_maker


class BaseDAO:
    """Base Data Axios Object"""
    model = None
    
    @classmethod
    async def insert_data(cls, **data) -> int:
        """Insert data"""
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data).returning(cls.model)
            result = await session.execute(query)
            await session.commit()
            return result.scalars().all()[0]
    
    @classmethod
    async def get_one_data(cls, model_id: int) -> dict:
        """Base get one data"""
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()
        
    @classmethod
    async def get_one_data_by_filter(cls, **data) -> list[dict]:
        """Base get all data"""
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**data)
            result = await session.execute(query)
            return result.scalar_one_or_none()
    
    @classmethod
    async def get_all_data(cls, **data) -> list[dict]:
        """Base get all data"""
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**data)
            result = await session.execute(query)
            return result.scalars().all()
