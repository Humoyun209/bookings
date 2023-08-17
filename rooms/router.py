from fastapi import APIRouter

from app.rooms.dao import RoomsDAO

router = APIRouter(prefix='/rooms', tags=['Комнаты'])


@router.get('/room/{hotel_id}')
async def get_rooms_by_hotel(hotel_id: int):
    result = await RoomsDAO.get_all_data(hotel_id=hotel_id)
    return result