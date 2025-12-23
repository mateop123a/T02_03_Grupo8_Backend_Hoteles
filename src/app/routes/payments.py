from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity
from ..schemas import PaymentCreateSchema
from ..services.finance_service import FinanceService
from ..utils.permissions import require_roles, ROLE_ADMIN, ROLE_ACCOUNTANT

bp = Blueprint("payments", __name__, url_prefix="/payments")

@bp.post("")
@require_roles(ROLE_ADMIN, ROLE_ACCOUNTANT)
def add_payment():
    data = PaymentCreateSchema().load(request.json or {})
    user_id = int(get_jwt_identity())
    pay = FinanceService.add_payment(
        reservation_id=data["reservation_id"],
        amount=data["amount"],
        method=data["method"],
        reference=data.get("reference"),
        created_by_user_id=user_id
    )
    return {
        "id": pay.id,
        "reservation_id": pay.reservation_id,
        "amount": pay.amount,
        "method": pay.method,
        "reference": pay.reference,
        "paid_at": pay.paid_at.isoformat(),
    }, 201
