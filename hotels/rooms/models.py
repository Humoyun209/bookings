from sqlalchemy import JSON, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Rooms(Base):
    __tablename__ = 'rooms'
    
    id = Column(Integer, primary_key=True)
    hotel_id = Column(ForeignKey('hotels.id'), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    services = Column(JSON)
    quantity = Column(Integer, nullable=False)
    
    bookings = relationship('Bookings', back_populates='room')
    hotel = relationship('Hotels', back_populates='rooms')
    
    def __str__(self) -> str:
        return f"Комната - {self.name}"