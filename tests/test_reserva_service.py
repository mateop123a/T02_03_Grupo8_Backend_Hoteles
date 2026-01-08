import pytest
from src.services.reserva_service import ReservaService

class FakeReservaRepository:
    def save(sel, reserva):
        return reserva

class FakeHabitacionRepository:
    def obtener_por_id(self, id):
        if id == 1:
            return {
                "id" : 1,
                "precio" : 50,
                "estado" : "Disponible"
            }
        return None

def test_reserva_correcta():
    service = ReservaService(FakeReservaRepository(), FakeHabitacionRepository())
    data = {
        "habitacion_id" : 1,
        "huesped_id" : 2,
        "fecha_entrada" : "2025-01-10",
        "fecha_salida" : "2025-01-15"
    }
    reserva = service.crear_reserva(data)
    assert reserva["total"] == 250

def test_reserva_invalida():
    service = ReservaService(FakeReservaRepository(), FakeHabitacionRepository())
    data = {
        "habitacion_id" : 1,
        "huesped_id" : 2,
        "fecha_entrada" : "2025-01-10",
        "fecha_salida" : "2025-01-15"
    }

    with pytest.raises(ValueError):
        service.crear_reserva(data)
        
def test_habitacion_no_disponible():
    class FakeHabitacionHotelNoDisponible:
        def obtener_por_id(self, id):
            return {"precio" : 50, "estado": "Ocupada"}
    service = ReservaService(FakeReservaRepository(), FakeHabitacionHotelNoDisponible())
    data = {
        "habitacion_id" : 1,
        "huesped_id" : 2,
        "fecha_entrada" : "2025-01-10",
        "fecha_salida" : "2025-01-15"
    }

    with pytest.raises(ValueError):
        service.crear_reserva(data)