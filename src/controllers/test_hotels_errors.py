import pytest
from unittest.mock import patch
from main import app

BASE = "/hotels"
PATCH_TARGET = "hotel_controller.hotel_service"


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def test_service_exception_on_list(client):
    # Si el controller captura excepciones y responde 500, perfecto.
    # Si no captura, puede devolver 500 por defecto.
    with patch(f"{PATCH_TARGET}.list_hotels", side_effect=Exception("boom")):
        resp = client.get(BASE)

    assert resp.status_code in (500,)


def test_create_hotel_wrong_content_type(client):
    # Enviar texto en vez de JSON (muchos controllers responden 400/415)
    resp = client.post(BASE, data="no-json", content_type="text/plain")
    assert resp.status_code in (400, 415, 422)


def test_update_hotel_empty_body(client):
    # PUT sin body (debería fallar con 400/422)
    resp = client.put(f"{BASE}/1")
    assert resp.status_code in (400, 415, 422)
