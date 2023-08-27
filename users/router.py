import json
from fastapi import APIRouter, HTTPException, Response, status

from app.users.auth import authenticate_user, get_hashed_password, create_access_token
from app.users.dao import UsersDao
from app.users.schemes import SUserRegister


router = APIRouter(prefix='/auth', tags=['Регистрация и авторизация'])


@router.post('/register', status_code=201)
async def register_user(user_data: SUserRegister) -> Response:
    """Register User"""
    email, password = user_data.email, user_data.password
    bug = await UsersDao.get_one_data_by_filter(email=email)
    if bug is not None:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='Пользователь с таким именем существует')
    hash_password = get_hashed_password(password)
    res = await UsersDao.insert_data(email=email, hashed_password=hash_password)
    return {'Success': 'User create succesfully', 'user_id': res}


@router.post('/login', status_code=200)
async def login_user(user_data: SUserRegister, response: Response) -> dict:
    user = await authenticate_user(password=user_data.password,
                                   email=user_data.email)
    if user is None:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)
    access_token = create_access_token({'sub': str(user.id)})
    response.headers.append('access_token', access_token)
    response.set_cookie('access_token', access_token, httponly=True) 
    return {"access_token": access_token}


@router.post('/logout', status_code=status.HTTP_202_ACCEPTED)
async def logout_user(response: Response) -> dict:
    response.delete_cookie('access_token')
    return {'Success': 'User logout successfully'}
