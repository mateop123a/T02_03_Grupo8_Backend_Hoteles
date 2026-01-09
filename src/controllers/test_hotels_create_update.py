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


def test_create_hotel_201(client):
    payload = {"name": "Hotel Nuevo"}
    created = {"id": 10, **payload}

    with patch(f"{PATCH_TARGET}.create_hotel", return_value=created):
        resp = client.post(BASE, json=payload)

    assert resp.status_code in (201, 200)
    assert resp.is_json
    data = resp.get_json()
    assert data["name"] == "Hotel Nuevo"
    assert "id" in data


def test_create_hotel_invalid_400(client):
    resp = client.post(BASE, json={})
    assert resp.status_code in (400, 422)


def test_update_hotel_200(client):
    payload = {"name": "Hotel Editado"}
    updated = {"id": 1, **payload}

    with patch(f"{PATCH_TARGET}.update_hotel", return_value=updated):
        resp = client.put(f"{BASE}/1", json=payload)

    assert resp.status_code == 200
    assert resp.is_json
    assert resp.get_json()["name"] == "Hotel Editado"


def test_update_hotel_not_found(client):
    payload = {"name": "Hotel X"}

    with patch(f"{PATCH_TARGET}.update_hotel", return_value=None):
        resp = client.put(f"{BASE}/999", json=payload)

    assert resp.status_code in (404, 400)
