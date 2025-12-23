from sqlalchemy.exc import IntegrityError
from ..extensions import db
from ..models import Payment, Reservation, Expense
from ..utils.validators import validate_positive_amount

ALLOWED_METHODS = {"cash", "card", "transfer"}

class FinanceService:
    @staticmethod
    def add_payment(reservation_id: int, amount: float, method: str, reference=None, created_by_user_id=None) -> Payment:
        validate_positive_amount(amount)
        if method not in ALLOWED_METHODS:
            raise ValueError("Método inválido: use cash/card/transfer.")

        res = Reservation.query.get(reservation_id)
        if not res:
            raise ValueError("Reserva no existe.")
        if res.status in ("cancelled",):
            raise ValueError("No se puede pagar una reserva cancelada.")

        balance = res.total_amount - res.paid_amount
        if amount > balance + 1e-9:
            raise ValueError(f"Pago excede el saldo. Saldo actual: {balance:.2f}")

        pay = Payment(
            reservation_id=reservation_id,
            amount=amount,
            method=method,
            reference=reference,
            created_by_user_id=created_by_user_id
        )
        db.session.add(pay)

        res.paid_amount += amount
        if abs(res.paid_amount - res.total_amount) < 1e-6:
            res.status = "completed"

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise ValueError("No se pudo registrar el pago.")
        return pay

    @staticmethod
    def add_expense(category: str, amount: float, description=None, created_by_user_id=None) -> Expense:
        validate_positive_amount(amount)
        if not category or len(category) < 3:
            raise ValueError("Categoría inválida (mínimo 3 caracteres).")

        exp = Expense(
            category=category.strip().lower(),
            amount=amount,
            description=description,
            created_by_user_id=created_by_user_id
        )
        db.session.add(exp)
        db.session.commit()
        return exp
