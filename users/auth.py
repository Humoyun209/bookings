from datetime import datetime, timedelta
from passlib.context import CryptContext

from pydantic import EmailStr
from jose import jwt
from app.config import settings

from app.users.dao import UsersDao


PWD_CONTEXT = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_hashed_password(password: str) -> str:
    """hasher password"""
    return PWD_CONTEXT.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """verify password"""
    return PWD_CONTEXT.verify(password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expired_data = datetime.utcnow() + timedelta(days=10)
    
    to_encode.update(exp=expired_data)
    encoded_jwt = jwt.encode(to_encode, settings.PUBLIC_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def authenticate_user(password: str, email: EmailStr):
    """get user from db"""
    user = await UsersDao.get_one_data_by_filter(email=email)
    if user is None or not verify_password(password=password,
                       hashed_password=user.hashed_password):
        return None
    return user
