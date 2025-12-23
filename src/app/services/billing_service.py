from datetime import datetime
from sqlalchemy.exc import IntegrityError
from ..extensions import db
from ..models import Invoice, Reservation

class BillingService:
    @staticmethod
    def generate_invoice_for_reservation(reservation_id: int) -> Invoice:
        res = Reservation.query.get(reservation_id)
        if not res:
            raise ValueError("Reserva no existe.")
        if res.status == "cancelled":
            raise ValueError("No se factura una reserva cancelada.")

        if res.invoice:
            return res.invoice

        # número simple: INV-YYYYMMDD-<id>
        invoice_number = f"INV-{datetime.utcnow().strftime('%Y%m%d')}-{reservation_id}"

        inv = Invoice(
            reservation_id=reservation_id,
            invoice_number=invoice_number,
            total=res.total_amount
        )
        db.session.add(inv)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise ValueError("No se pudo generar la factura.")
        return inv
