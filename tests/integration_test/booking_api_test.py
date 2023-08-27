from datetime import date
import pytest
from httpx import AsyncClient

from app.bookings.dao import BookingsDAO
from app.users.dependencies import get_current_user


@pytest.mark.parametrize("date_from,date_to,room_id,status_code", [
    *[("2030-11-11", "2030-11-11", 1, 201)]*5,
    ("2030-11-11", "2030-11-11", 1, 406)
])
async def test_add_booking_in_api(room_id: int, date_from: date, date_to: date, status_code: int,
                                  authenticate_ac: AsyncClient):
    booking = await authenticate_ac.post('/bookings/create_boking', params={
        "room_id": room_id,
        "date_from": date_from,
        "date_to": date_to
    })
    assert booking.status_code == status_code
