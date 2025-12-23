from sqlalchemy import Column, Integer, String
from src.database.database import Base

class Hotel(Base):
    __tablename__ = "hoteles"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    direccion = Column(String, nullable=False)
    ciudad = Column(String, nullable=False)
    estrellas = Column(Integer, nullable=False)
