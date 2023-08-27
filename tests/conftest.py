import asyncio
import json
from fastapi import Request, Response
import pytest
from datetime import datetime
from sqlalchemy import insert


from app.config import settings 
from app.database import Base, engine
from app.database import async_session_maker
from app.main import app as fastapi_app

from app.bookings.models import Bookings
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.hotels.models import Hotels, Images
from app.hotels.rooms.models import Rooms


from fastapi.testclient import TestClient
from httpx import AsyncClient


@pytest.fixture(scope='session', autouse=True)
async def prepare_database():
    assert settings.MODE == 'TEST'
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def load_json_to_db(table_name: str):
        with open(f'app/tests/test_json_data/{table_name}.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    
    add_bookings = load_json_to_db('bookings')
    
    for booking in add_bookings:
        booking['date_from'] = datetime.strptime(booking['date_from'], '%Y-%m-%d')
        booking['date_to'] = datetime.strptime(booking['date_to'], '%Y-%m-%d')
        
    async with async_session_maker() as session:
        # bookings = insert(Bookings).values(add_bookings)
        hotels = insert(Hotels).values(load_json_to_db('hotels'))
        rooms = insert(Rooms).values(load_json_to_db('rooms'))
        users = insert(Users).values(load_json_to_db('users'))
        
        await session.execute(users)
        await session.execute(hotels)
        await session.execute(rooms)
        # await session.execute(bookings)
        
        await session.commit()
    print('\n start .... \n')
        

@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
    

@pytest.fixture(scope="function")
async def ac():
    async with AsyncClient(app=fastapi_app, base_url='http://test') as as_cl:
        yield as_cl
        

@pytest.fixture(scope="function")
async def session():
    async with async_session_maker() as ses:
        yield ses


@pytest.fixture(scope="session")
async def authenticate_ac():
    async with AsyncClient(app=fastapi_app, base_url='http://test') as as_cl:
        await as_cl.post('/auth/login', json={
            "email": "humoyun209@gmail.com",
            "password": "humo6050"
        })
        assert as_cl.cookies.get("access_token") is not None
        yield as_cl