from __future__ import annotations
from typing import List, Optional
from uuid import uuid4

from app.db import db
from app.domain.models.reservation import Reservation


class ReservationRepository:
    def list_all(self) -> List[Reservation]:
        return Reservation.query.order_by(Reservation.id.desc()).all()

    def list_by_user_id(self, user_id: int) -> List[Reservation]:
        return (
            Reservation.query
            .filter_by(user_id=user_id)
            .order_by(Reservation.id.desc())
            .all()
        )

    def get(self, reservation_id: str) -> Optional[Reservation]:
        return Reservation.query.get(reservation_id)

    def create(
        self,
        hotel_id: str,
        user_id: int,
        full_name: str,
        email: str,
        check_in: str,
        check_out: str,
        guests: int,
        price_per_person_night: float,
        nights: int,
        total_paid: float,
        payment_method: str,
        payment_status: str = "paid",
    ) -> Reservation:
        rid = str(uuid4())  # ✅ antes faltaba

        r = Reservation(
            id=rid,
            hotel_id=hotel_id,
            user_id=user_id,
            full_name=full_name,
            email=email,
            check_in=check_in,
            check_out=check_out,
            guests=guests,
            price_per_person_night=price_per_person_night,
            nights=nights,
            total_paid=total_paid,
            payment_method=payment_method,
            payment_status=payment_status,
        )

        db.session.add(r)
        db.session.commit()
        return r
