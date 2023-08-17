from decimal import Decimal

from datetime import date
from pydantic import BaseModel


class SBooking(BaseModel):
    """booking pydantic model"""
    id: int
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: Decimal
    total_cost: int
    total_days: int


class BookingCreate(BaseModel):
    room_id: int
    date_from: date
    date_to: date
