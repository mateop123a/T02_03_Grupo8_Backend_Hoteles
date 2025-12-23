from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity
from ..schemas import ExpenseCreateSchema
from ..services.finance_service import FinanceService
from ..utils.permissions import require_roles, ROLE_ADMIN, ROLE_ACCOUNTANT

bp = Blueprint("expenses", __name__, url_prefix="/expenses")

@bp.post("")
@require_roles(ROLE_ADMIN, ROLE_ACCOUNTANT)
def add_expense():
    data = ExpenseCreateSchema().load(request.json or {})
    user_id = int(get_jwt_identity())
    exp = FinanceService.add_expense(
        category=data["category"],
        amount=data["amount"],
        description=data.get("description"),
        created_by_user_id=user_id
    )
    return {
        "id": exp.id,
        "category": exp.category,
        "amount": exp.amount,
        "description": exp.description,
        "incurred_at": exp.incurred_at.isoformat(),
    }, 201
