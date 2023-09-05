from typing import Optional, Union

from fastapi import HTTPException
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.config import settings
from app.users.auth import authenticate_user, create_access_token
from app.users.dependencies import get_current_user
from app.users.models import Users


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> Union[bool, RedirectResponse]:
        form = await request.form()
        email, password = form["username"], form["password"]
        user = await authenticate_user(password, email)
        if user is None:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)
        access_token = create_access_token({'sub': str(user.id)})
        request.session.update({"token": access_token})
        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> Optional[RedirectResponse]:
        try:
            token = request.session.get("token")
            try:
                user: Users = await get_current_user(token=token)
            except Exception:
                raise HTTPException(status_code=403, detail='Информация не доступна')
                
            if token is None or user.is_admin != True:
                return RedirectResponse(request.url_for("admin:login"), status_code=302)
        except Exception:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)


authentication_backend = AdminAuth(secret_key=settings.SECRET_KEY)