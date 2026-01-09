from sqlalchemy import Column, Integer, String, ForeignKey
from src.database.database import Base

class Habitacion(Base):
    __tablename__ = "habitaciones"

    id = Column(Integer, primary_key=True, index=True)
    numero = Column(String, nullable=False)
    tipo = Column(String, nullable=False)
    precio = Column(Integer, nullable=False)
    hotel_id = Column(Integer, ForeignKey("hoteles.id"))
