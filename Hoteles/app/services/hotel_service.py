from __future__ import annotations
from typing import Dict, List, Tuple, Optional

from app.repositories.hotel_repository import HotelRepository


class HotelService:
    def __init__(self, repo: HotelRepository) -> None:
        self.repo = repo

    def list_hotels(self) -> List[Dict]:
        return [self._to_dict(h) for h in self.repo.list_all()]

    def get_hotel(self, hotel_id: str) -> Tuple[Optional[Dict], Optional[str]]:
        h = self.repo.get(hotel_id)
        if not h:
            return None, "Hotel no encontrado"
        return self._to_dict(h), None

    def create_hotel(self, payload: Dict) -> Tuple[Optional[Dict], Optional[str]]:
        name, city, stars, price, image_url, err = self._validate(payload)
        if err:
            return None, err

        h = self.repo.create(
            name=name,
            city=city,
            stars=stars,
            price_per_person_night=price,
            image_url=image_url,
        )
        return self._to_dict(h), None

    def update_hotel(self, hotel_id: str, payload: Dict) -> Tuple[Optional[Dict], Optional[str]]:
        name, city, stars, price, image_url, err = self._validate(payload)
        if err:
            return None, err

        h = self.repo.update(
            hotel_id,
            name=name,
            city=city,
            stars=stars,
            price_per_person_night=price,
            image_url=image_url,  # ✅ faltaba en tu update
        )
        if not h:
            return None, "Hotel no encontrado"

        return self._to_dict(h), None

    def delete_hotel(self, hotel_id: str) -> Tuple[bool, Optional[str]]:
        ok = self.repo.delete(hotel_id)
        if not ok:
            return False, "Hotel no encontrado"
        return True, None

    def _validate(self, payload: Dict):
        name = str(payload.get("name", "")).strip()
        city = str(payload.get("city", "")).strip()
        image_url = str(payload.get("image_url", "")).strip()

        try:
            stars = int(payload.get("stars", 0))
        except Exception:
            return "", "", 0, 0.0, "", "stars debe ser un número entero"

        try:
            price = float(payload.get("price_per_person_night", 0))
        except Exception:
            return "", "", 0, 0.0, "", "price_per_person_night debe ser un número"

        if not name:
            return "", "", 0, 0.0, "", "name es requerido"
        if not city:
            return "", "", 0, 0.0, "", "city es requerido"
        if stars < 1 or stars > 5:
            return "", "", 0, 0.0, "", "stars debe estar entre 1 y 5"
        if price <= 0:
            return "", "", 0, 0.0, "", "price_per_person_night debe ser > 0"
        if not image_url:
            return "", "", 0, 0.0, "", "image_url es requerido"

        return name, city, stars, price, image_url, None

    def _to_dict(self, h) -> Dict:
        return {
            "id": h.id,
            "name": h.name,
            "city": h.city,
            "stars": int(h.stars),
            "price_per_person_night": float(h.price_per_person_night),
            "image_url": h.image_url,
        }
