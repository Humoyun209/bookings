from fastapi import FastAPI, Request
import uvicorn
from app.bookings.router import router as bookings_router
from app.users.router import router as users_router
from app.hotels.router import router as hotels_router
from app.rooms.router import router as rooms_roter


app = FastAPI()

app.include_router(bookings_router)
app.include_router(users_router)
app.include_router(hotels_router)
app.include_router(rooms_roter)


@app.get("/home/")
def get_home(request: Request) -> dict:
    return {'Message': 'Welcome to UFC'}
