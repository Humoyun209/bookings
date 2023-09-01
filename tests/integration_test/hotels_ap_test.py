from httpx import AsyncClient
import pytest

@pytest.mark.smoke
async def test_get_all_hotels(ac: AsyncClient):
    response = await ac.get('/hotels', params={
        'location': 'Алтай',
        'date_from': '2023-11-09',
        'date_to': '2023-11-25'
    })
    
    assert response.status_code == 200