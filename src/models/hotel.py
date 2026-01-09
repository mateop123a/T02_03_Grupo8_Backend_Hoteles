from sqlalchemy import Column, Integer, String
from src.database.database import Base
from pydantic import BaseModel, Field

class Hotel(Base):
    __tablename__ = "hoteles"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    direccion = Column(String, nullable=False)
    ciudad = Column(String, nullable=False)
    estrellas = Column(Integer, nullable=False)

class Hotel(BaseModel):
    id: int
    nombre: str
    ciudad: str
    tarifa: float = Field(gt=0)

    def calcular_precio_total(self, noches: int) -> float:
        """
        Calcula el precio total de una estadía.

        >>> hotel = Hotel(id=1, nombre="Test Hotel", ciudad="Quito", tarifa=50)
        >>> hotel.calcular_precio_total(3)
        150
        """
        return self.tarifa * noches
