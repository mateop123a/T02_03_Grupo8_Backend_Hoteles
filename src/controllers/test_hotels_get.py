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


def test_get_hotels_200(client):
    fake_list = [{"id": 1, "name": "Hotel A"}, {"id": 2, "name": "Hotel B"}]

    with patch(f"{PATCH_TARGET}.list_hotels", return_value=fake_list):
        resp = client.get(BASE)

    assert resp.status_code == 200
    assert resp.is_json
    assert resp.get_json() == fake_list


def test_get_hotel_by_id_200(client):
    fake_hotel = {"id": 1, "name": "Hotel A"}

    with patch(f"{PATCH_TARGET}.get_hotel_by_id", return_value=fake_hotel):
        resp = client.get(f"{BASE}/1")

    assert resp.status_code == 200
    assert resp.is_json
    assert resp.get_json()["id"] == 1


def test_get_hotel_by_id_404(client):
    with patch(f"{PATCH_TARGET}.get_hotel_by_id", return_value=None):
        resp = client.get(f"{BASE}/999")

    assert resp.status_code in (404, 400)
