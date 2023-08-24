from sqlalchemy import Column, Computed, ForeignKey, Integer, Numeric, Date
from sqlalchemy.orm import relationship
from app.database import Base


class Bookings(Base):
    __tablename__ = 'bookings'
    
    id = Column(Integer,primary_key=True)
    room_id = Column(ForeignKey('rooms.id'), nullable=False)
    user_id = Column(ForeignKey('users.id'), nullable=False)
    date_from = Column(Date, nullable=False)
    date_to = Column(Date, nullable=False)
    price = Column(Integer, nullable=False)
    total_cost = Column(Numeric, Computed("(date_to - date_from) * price"))
    total_days = Column(Integer, Computed("date_to - date_from"))
    
    user = relationship('Users', back_populates='bookings')
    room = relationship('Rooms', back_populates='bookings')
    
    def __str__(self) -> str:
        return f"Брон #{self.id}"
    