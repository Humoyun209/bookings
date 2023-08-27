from sqladmin import ModelView
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class Users(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    
    bookings = relationship('Bookings', back_populates='user')
    
    def __str__(self) -> str:
        return f'Пользователь - {self.email}'