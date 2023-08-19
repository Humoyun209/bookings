from sqlalchemy import Boolean, Column, Integer, String, JSON, ForeignKey
from app.database import Base


class Hotels(Base):
    """Hotels table"""
    __tablename__ = 'hotels'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    services = Column(JSON)
    rooms_quantity = Column(Integer, nullable=False)
    
    
class Images(Base):
    """Images table"""
    __tablename__ = 'images'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    is_main = Column(Boolean, default=False)
    hotel_id = Column(Integer, ForeignKey('hotels.id'), nullable=False)
