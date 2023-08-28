from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqladmin import Admin

from app.admin.admin import (BookingsAdmin, HotelsAdmin, ImagesAdmin,
                             RoomsAdmin, UserAdmin)
from app.admin.auth import authentication_backend
from app.bookings.dao import BookingsDAO
from app.bookings.router import router as bookings_router
from app.dao.base import BaseDAO
from app.database import engine
from app.hotels.dao import HotelsDAO
from app.hotels.images.router import router as images_router
from app.hotels.rooms.dao import RoomsDAO
from app.hotels.rooms.router import router as rooms_roter
from app.hotels.router import router as hotels_router
from app.users.dao import UsersDao
from app.users.router import router as users_router

app = FastAPI()
app.mount("/media", StaticFiles(directory="app/media"), name="static")

app.include_router(bookings_router)
app.include_router(users_router)
app.include_router(hotels_router)
app.include_router(rooms_roter)
app.include_router(images_router)


admin = Admin(app=app, engine=engine, authentication_backend=authentication_backend)

admin.add_view(UserAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(HotelsAdmin)
admin.add_view(RoomsAdmin)
admin.add_view(ImagesAdmin)


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost:6379")
    FastAPICache.init(RedisBackend(redis), prefix="cache")


origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)


@app.get("/all_rooms")
async def get_all_rooms():
    return await RoomsDAO.get_all_data()


@app.get("/all_bookings")
async def get_all_rooms():
    return await BookingsDAO.get_all_data()


@app.get("/all_users")
async def get_all_users():
    return await UsersDao.get_all_data()


@app.get("/all_hotels")
async def get_all_hotels():
    return await HotelsDAO.get_all_data()
