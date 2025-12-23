from datetime import date
from sqlalchemy.exc import IntegrityError
from ..extensions import db
from ..models import Reservation, Client, Room
from ..utils.validators import validate_date_range

class ReservationService:
    @staticmethod
    def _overlaps(a_start, a_end, b_start, b_end) -> bool:
        # solapamiento: [a_start, a_end) con [b_start, b_end)
        return a_start < b_end and b_start < a_end

    @staticmethod
    def room_is_available(room_id: int, check_in: date, check_out: date, exclude_reservation_id=None) -> bool:
        q = Reservation.query.filter(
            Reservation.room_id == room_id,
            Reservation.status != "cancelled",
        )
        if exclude_reservation_id:
            q = q.filter(Reservation.id != exclude_reservation_id)

        existing = q.all()
        for r in existing:
            if ReservationService._overlaps(check_in, check_out, r.check_in, r.check_out):
                return False
        return True

    @staticmethod
    def create_reservation(client_id: int, room_id: int, check_in: date, check_out: date, created_by_user_id=None) -> Reservation:
        validate_date_range(check_in, check_out)

        client = Client.query.get(client_id)
        if not client:
            raise ValueError("Cliente no existe.")
        room = Room.query.get(room_id)
        if not room or not room.is_active:
            raise ValueError("Habitación no existe o está inactiva.")
        if room.status == "maintenance":
            raise ValueError("Habitación en mantenimiento.")

        if not ReservationService.room_is_available(room_id, check_in, check_out):
            raise ValueError("Habitación no disponible para esas fechas.")

        nights = (check_out - check_in).days
        total = nights * room.price_per_night

        res = Reservation(
            client_id=client_id,
            room_id=room_id,
            check_in=check_in,
            check_out=check_out,
            nights=nights,
            total_amount=total,
            paid_amount=0.0,
            status="confirmed",
            created_by_user_id=created_by_user_id,
        )
        db.session.add(res)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise ValueError("No se pudo crear la reserva.")
        return res

    @staticmethod
    def cancel_reservation(reservation_id: int) -> Reservation:
        res = Reservation.query.get(reservation_id)
        if not res:
            raise ValueError("Reserva no existe.")
        if res.status == "cancelled":
            return res
        if res.status == "completed":
            raise ValueError("No se puede cancelar una reserva completada.")
        res.status = "cancelled"
        db.session.commit()
        return res

    @staticmethod
    def update_dates(reservation_id: int, check_in: date, check_out: date) -> Reservation:
        res = Reservation.query.get(reservation_id)
        if not res:
            raise ValueError("Reserva no existe.")
        if res.status in ("cancelled", "completed"):
            raise ValueError("No se puede modificar una reserva cancelada/completada.")

        validate_date_range(check_in, check_out)

        if not ReservationService.room_is_available(res.room_id, check_in, check_out, exclude_reservation_id=res.id):
            raise ValueError("Habitación no disponible para las nuevas fechas.")

        room = Room.query.get(res.room_id)
        nights = (check_out - check_in).days
        total = nights * room.price_per_night

        if res.paid_amount > total:
            raise ValueError("Ya se pagó más que el nuevo total. Ajuste pagos primero.")

        res.check_in = check_in
        res.check_out = check_out
        res.nights = nights
        res.total_amount = total
        db.session.commit()
        return res
