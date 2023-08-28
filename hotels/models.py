from sqlalchemy import JSON, Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Hotels(Base):
    """Hotels table"""
    __tablename__ = 'hotels'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    services = Column(JSON)
    rooms_quantity = Column(Integer, nullable=False)
    
    rooms = relationship('Rooms', back_populates='hotel')
    images = relationship('Images', back_populates='hotel')
    
    def __str__(self) -> str:
        return f"Отель - {self.name}"
    
    
class Images(Base):
    """Images table"""
    __tablename__ = 'images'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    is_main = Column(Boolean, default=False)
    hotel_id = Column(Integer, ForeignKey('hotels.id'), nullable=False)
    
    hotel = relationship('Hotels', back_populates='images')
    
    def __str__(self) -> str:
        return f"Фото - {self.name}"
