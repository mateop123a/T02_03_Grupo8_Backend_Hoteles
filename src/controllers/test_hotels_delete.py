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


def test_delete_hotel_204_or_200(client):
    with patch(f"{PATCH_TARGET}.delete_hotel", return_value=True):
        resp = client.delete(f"{BASE}/1")

    assert resp.status_code in (204, 200)


def test_delete_hotel_not_found(client):
    with patch(f"{PATCH_TARGET}.delete_hotel", return_value=False):
        resp = client.delete(f"{BASE}/999")

    assert resp.status_code in (404, 400)
