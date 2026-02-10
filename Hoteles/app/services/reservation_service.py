from __future__ import annotations
from datetime import date
from typing import Dict, Optional, Tuple, List

from app.repositories.reservation_repository import ReservationRepository
from app.repositories.hotel_repository import HotelRepository


class ReservationService:
    def __init__(self, repo: ReservationRepository, hotel_repo: HotelRepository) -> None:
        self.repo = repo
        self.hotel_repo = hotel_repo

    def list_reservations(self) -> List[Dict]:
        return [self._to_dict(r) for r in self.repo.list_all()]

    def list_reservations_by_user_id(self, user_id: int) -> List[Dict]:
        return [self._to_dict(r) for r in self.repo.list_by_user_id(user_id)]

    def get_reservation(self, reservation_id: str) -> Tuple[Optional[Dict], Optional[str]]:
        r = self.repo.get(reservation_id)
        if not r:
            return None, "Reserva no encontrada"
        return self._to_dict(r), None

    def create_reservation(self, payload: Dict) -> Tuple[Optional[Dict], Optional[str]]:
        try:
            user_id = int(payload.get("user_id", 0))
        except Exception:
            user_id = 0

        hotel_id = str(payload.get("hotel_id", "")).strip()
        full_name = str(payload.get("full_name", "")).strip()
        email = str(payload.get("email", "")).strip().lower()
        check_in = str(payload.get("check_in", "")).strip()
        check_out = str(payload.get("check_out", "")).strip()

        payment_method = str(payload.get("payment_method", "")).strip().lower()

        try:
            guests = int(payload.get("guests", 1))
        except Exception:
            return None, "guests debe ser entero"

        if user_id <= 0:
            return None, "Debes iniciar sesión para reservar"
        if not hotel_id:
            return None, "hotel_id es requerido"

        hotel = self.hotel_repo.get(hotel_id)
        if not hotel:
            return None, "Hotel no encontrado"

        if not full_name:
            return None, "full_name es requerido"
        if "@" not in email:
            return None, "email inválido"
        if not check_in or not check_out:
            return None, "check_in y check_out son requeridos"
        if guests < 1:
            return None, "guests debe ser >= 1"

        # ✅ validar forma de pago
        allowed = {"card", "transfer", "cash"}
        if payment_method not in allowed:
            return None, "payment_method inválido (card, transfer, cash)"

        nights = self._calc_nights(check_in, check_out)
        if nights <= 0:
            return None, "check_out debe ser mayor a check_in"

        price = float(getattr(hotel, "price_per_person_night", 0) or 0)
        if price <= 0:
            return None, "El hotel no tiene precio configurado"

        total_paid = round(price * nights * guests, 2)

        r = self.repo.create(
            hotel_id=hotel_id,
            user_id=user_id,
            full_name=full_name,
            email=email,
            check_in=check_in,
            check_out=check_out,
            guests=guests,
            price_per_person_night=price,
            nights=nights,
            total_paid=total_paid,
            payment_method=payment_method,      # ✅ faltaba
            payment_status="paid",
        )

        return self._to_dict(r), None

    def _calc_nights(self, check_in: str, check_out: str) -> int:
        try:
            y1, m1, d1 = map(int, check_in.split("-"))
            y2, m2, d2 = map(int, check_out.split("-"))
            in_date = date(y1, m1, d1)
            out_date = date(y2, m2, d2)
            return (out_date - in_date).days
        except Exception:
            return 0

    def _to_dict(self, r) -> Dict:
        return {
            "id": r.id,
            "hotel_id": r.hotel_id,
            "user_id": r.user_id,
            "full_name": r.full_name,
            "email": r.email,
            "check_in": r.check_in,
            "check_out": r.check_out,
            "guests": int(r.guests),
            "nights": int(r.nights),
            "price_per_person_night": float(r.price_per_person_night),
            "total_paid": float(r.total_paid),
            "payment_method": r.payment_method,
            "payment_status": r.payment_status,
        }
