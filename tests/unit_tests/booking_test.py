from datetime import date, datetime, timedelta

import pytest

from app.bookings.dao import BookingsDAO
from app.bookings.models import Bookings


def func(delta: int) -> str:
    NOW = datetime.utcnow()
    from_time = NOW + timedelta(days=delta)
    to_time = NOW + timedelta(days=delta+30)
    return (from_time.strftime("%Y-%m-%d"), to_time.strftime("%Y-%m-%d"))


@pytest.mark.parametrize("user_id,date_from,date_to,room_id",[
    (4, datetime.strptime(func(10)[0], "%Y-%m-%d").date(), datetime.strptime(func(10)[1],"%Y-%m-%d").date(), 2),
    (3, datetime.strptime(func(-10)[0], "%Y-%m-%d").date(), datetime.strptime(func(-10)[1], "%Y-%m-%d").date(), 8)
])
async def test_add_booking_to_db(user_id: int, date_from: date, date_to: date, room_id: int):
    booking = await BookingsDAO.create_booking_db(
        date_from=date_from,
        date_to=date_to,
        user_id=user_id,
        room_id=room_id
    )
    if date_from < datetime.now().date():
        assert not booking
    else: assert isinstance(booking, Bookings)
