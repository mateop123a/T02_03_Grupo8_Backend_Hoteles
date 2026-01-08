import pytest
from src.services.factura_service import FacturaService

class FakeFacturaRepository:
    pass

def calculo_factura_correcto():
    service = FacturaService(FakeFacturaRepository())
    resultado = service.generar_detalle_factura(100)
    assert resultado["subtotal"] == 100
    assert resultado["I.V.A"] == 15
    assert resultado["total"] == 115

def test_factura_monto_invalido():
    service  = FacturaService(FakeFacturaRepository())
    service.generar_detalle_factura(0)