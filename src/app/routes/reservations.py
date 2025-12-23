from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity
from ..models import Reservation
from ..schemas import ReservationCreateSchema, ReservationOutSchema
from ..services.reservation_service import ReservationService
from ..utils.permissions import require_roles, ROLE_ADMIN, ROLE_RECEPTIONIST

bp = Blueprint("reservations", __name__, url_prefix="/reservations")

@bp.post("")
@require_roles(ROLE_ADMIN, ROLE_RECEPTIONIST)
def create_reservation():
    data = ReservationCreateSchema().load(request.json or {})
    user_id = int(get_jwt_identity())
    res = ReservationService.create_reservation(
        client_id=data["client_id"],
        room_id=data["room_id"],
        check_in=data["check_in"],
        check_out=data["check_out"],
        created_by_user_id=user_id
    )
    return ReservationOutSchema().dump(res), 201

@bp.get("")
@require_roles(ROLE_ADMIN, ROLE_RECEPTIONIST)
def list_reservations():
    status = request.args.get("status")
    client_id = request.args.get("client_id", type=int)
    query = Reservation.query
    if status:
        query = query.filter(Reservation.status == status)
    if client_id:
        query = query.filter(Reservation.client_id == client_id)
    res = query.order_by(Reservation.created_at.desc()).all()
    return ReservationOutSchema(many=True).dump(res), 200

@bp.put("/<int:reservation_id>/dates")
@require_roles(ROLE_ADMIN, ROLE_RECEPTIONIST)
def update_dates(reservation_id):
    payload = request.json or {}
    check_in = payload.get("check_in")
    check_out = payload.get("check_out")
    if not check_in or not check_out:
        return {"error": "check_in y check_out son requeridos."}, 400

    # marshmallow no parsea aquí; simple:
    from datetime import date
    try:
        ci = date.fromisoformat(check_in)
        co = date.fromisoformat(check_out)
    except ValueError:
        return {"error": "Formato de fecha inválido. Use YYYY-MM-DD."}, 400

    res = ReservationService.update_dates(reservation_id, ci, co)
    return ReservationOutSchema().dump(res), 200

@bp.put("/<int:reservation_id>/cancel")
@require_roles(ROLE_ADMIN, ROLE_RECEPTIONIST)
def cancel_reservation(reservation_id):
    res = ReservationService.cancel_reservation(reservation_id)
    return ReservationOutSchema().dump(res), 200
