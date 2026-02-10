from __future__ import annotations
from typing import List, Optional
from uuid import uuid4

from app.db import db
from app.domain.models.hotel import Hotel


class HotelRepository:
    def list_all(self) -> List[Hotel]:
        return Hotel.query.all()

    def get(self, hotel_id: str) -> Optional[Hotel]:
        return Hotel.query.get(hotel_id)

    def create(
        self,
        name: str,
        city: str,
        stars: int,
        price_per_person_night: float,
        image_url: str,
    ) -> Hotel:
        h = Hotel(
            id=str(uuid4()),
            name=name,
            city=city,
            stars=stars,
            price_per_person_night=price_per_person_night,
            image_url=image_url,
        )
        db.session.add(h)
        db.session.commit()
        return h

    def update(
        self,
        hotel_id: str,
        name: str,
        city: str,
        stars: int,
        price_per_person_night: float,
        image_url: str,
    ) -> Optional[Hotel]:
        h = Hotel.query.get(hotel_id)
        if not h:
            return None

        h.name = name
        h.city = city
        h.stars = stars
        h.price_per_person_night = price_per_person_night
        h.image_url = image_url

        db.session.commit()
        return h

    def delete(self, hotel_id: str) -> bool:
        h = Hotel.query.get(hotel_id)
        if not h:
            return False
        db.session.delete(h)
        db.session.commit()
        return True
