import shutil
from fastapi import APIRouter, HTTPException, UploadFile, status
from app.hotels.images.dao import ImagesDAO


router = APIRouter(prefix='/hotels/images', tags=['Загрузка изображений'])


@router.post('/create')
async def create_image(title: str, files: UploadFile, hotel_id: int, is_main: bool = False):
    try:
        with open(f'app/media/hotels/{title}.webp', '+wb') as file_object:
            shutil.copyfileobj(files.file, file_object)
            image_id = await ImagesDAO.insert_data(name=f'{title}.webp', is_main=is_main, hotel_id=hotel_id)
        
        return {"Success": f"Add image successfully. id = {image_id}"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='Ошибка при добавлении файла')
    