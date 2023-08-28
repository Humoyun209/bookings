import shutil

from fastapi import (APIRouter, BackgroundTasks, HTTPException, UploadFile,
                     status)

from app.hotels.images.dao import ImagesDAO
from app.tasks.tasks import process_pic

router = APIRouter(prefix='/hotels/images', tags=['Загрузка изображений'])
back_tasks = BackgroundTasks

@router.post('/create')
async def create_image(title: str, files: UploadFile, hotel_id: int, is_main: bool = False,
                       back_tasks: BackgroundTasks = None):
    try:
        path_name = f'app/media/hotels/{title}.webp'
        with open(path_name, '+wb') as file_object:
            shutil.copyfileobj(files.file, file_object)
            image_id = await ImagesDAO.insert_data(name=f'{title}.webp', is_main=is_main, hotel_id=hotel_id)
        
        
        back_tasks.add_task(process_pic, path_name)
        # process_pic.delay(path_name)
        
        return {"Success": f"Add image successfully. id = {image_id}"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='Ошибка при добавлении файла')
    