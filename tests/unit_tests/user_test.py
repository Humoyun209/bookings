from httpx import AsyncClient
from pydantic import EmailStr

import pytest


@pytest.mark.parametrize("email,password,status", [
    ('ufc@mail.ru', 'natediaz', 201),
    ('ufc@mail.ru', 'natediaz', 406),
    ('bellator', 'aaa', 422),
])
async def test_register_user(email: EmailStr,
                             password: str,
                             status: int,
                             ac: AsyncClient):
    response = await ac.post('/auth/register', json={
        'email': email,
        'password': password})
    assert response.status_code == status


@pytest.mark.parametrize("email,password,status", [
    ('h.ahmedov209@gmail.com', 'humo6050', 200),
    ('ufc12@mail.ru', 'natediaz1', 406),
    ('bellator', 'aaa', 422),
])
async def test_login_user(email: EmailStr,
                          password: str,
                          status: int,
                          ac: AsyncClient):
    response = await ac.post('/auth/login', json={
        'email': email,
        'password': password})
    assert response.status_code == status
