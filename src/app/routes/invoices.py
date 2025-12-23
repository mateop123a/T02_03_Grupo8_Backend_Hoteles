from flask import Blueprint
from ..schemas import InvoiceOutSchema
from ..services.billing_service import BillingService
from ..utils.permissions import require_roles, ROLE_ADMIN, ROLE_ACCOUNTANT, ROLE_RECEPTIONIST

bp = Blueprint("invoices", __name__, url_prefix="/invoices")

@bp.post("/reservation/<int:reservation_id>")
@require_roles(ROLE_ADMIN, ROLE_ACCOUNTANT, ROLE_RECEPTIONIST)
def create_invoice(reservation_id):
    inv = BillingService.generate_invoice_for_reservation(reservation_id)
    return InvoiceOutSchema().dump(inv), 201
