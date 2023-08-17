from pydantic import BaseModel, EmailStr


class SUserRegister(BaseModel):
    """Register model"""
    email: EmailStr
    password: str
