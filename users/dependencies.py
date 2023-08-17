from datetime import datetime
from fastapi import Depends, HTTPException, Request, status
from jose import JWTError, jwt

from app.config import settings
from app.users.dao import UsersDao


def get_token(request: Request):
    token = request.cookies.get('access_token')
    if token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                      detail="User is unauthorized")
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token=token,
            key=settings.PUBLIC_KEY,
            algorithms=settings.ALGORITHM
        )
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Ошибка при декодировании токена')
    expire = payload.get('exp')
    user_id = payload.get('sub')
    if expire is None or user_id is None:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail="Токен не действителен")
    if int(expire) < datetime.utcnow().timestamp():
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail="Срок действия токена окончен")
    user = await UsersDao.get_one_data(model_id=int(user_id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Пользователь таким идентификатором не существует")
    return user
