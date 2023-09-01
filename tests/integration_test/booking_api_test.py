from datetime import date, datetime

import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "date_from,date_to,room_id,status",
    [*[("2030-11-09", "2030-11-25", 1, 201)] * 5, 
     ("2030-11-09", "2030-11-25", 1, 406)],
)
@pytest.mark.authorized
async def test_create_booking(
    authenticate_ac: AsyncClient,
    date_from: date,
    date_to: date,
    room_id: int,
    status: int,
):
    print(authenticate_ac.cookies.get("access_token"))
    response = await authenticate_ac.post(
        "/bookings/create_booking",
        params={'date_from': date_from,
                'date_to': date_to,
                'room_id': room_id},
    )

    assert response.status_code == status
    


