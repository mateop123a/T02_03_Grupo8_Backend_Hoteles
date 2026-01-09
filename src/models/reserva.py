from pydantic import BaseModel, Field

class Reserva(BaseModel):
    id: int
    hotel_id: int
    noches: int = Field(gt=0)
    precio_total: float = Field(ge=0)

    def es_valida(self) -> bool:
        """
        Valida que la reserva tenga noches > 0.

        >>> r = Reserva(id=1, hotel_id=1, noches=2, precio_total=200)
        >>> r.es_valida()
        True

        >>> r = Reserva(id=2, hotel_id=1, noches=0, precio_total=200)
        >>> r.es_valida()
        False
        """
        return self.noches > 0
