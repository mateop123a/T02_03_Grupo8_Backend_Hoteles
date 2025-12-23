from flask import Blueprint, request
from datetime import date, datetime
from sqlalchemy import func
from ..models import Room, Reservation, Payment, Expense
from ..extensions import db
from ..services.reservation_service import ReservationService
from ..utils.permissions import require_roles, ROLE_ADMIN, ROLE_ACCOUNTANT, ROLE_RECEPTIONIST

bp = Blueprint("reports", __name__, url_prefix="/reports")

@bp.get("/rooms/available")
@require_roles(ROLE_ADMIN, ROLE_RECEPTIONIST)
def rooms_available():
    # /reports/rooms/available?check_in=YYYY-MM-DD&check_out=YYYY-MM-DD
    ci = request.args.get("check_in")
    co = request.args.get("check_out")
    if not ci or not co:
        return {"error": "check_in y check_out requeridos."}, 400
    try:
        check_in = date.fromisoformat(ci)
        check_out = date.fromisoformat(co)
    except ValueError:
        return {"error": "Formato de fecha inválido. Use YYYY-MM-DD."}, 400

    rooms = Room.query.filter(Room.is_active == True, Room.status != "maintenance").all()
    available = []
    for r in rooms:
        if ReservationService.room_is_available(r.id, check_in, check_out):
            available.append({
                "id": r.id,
                "number": r.number,
                "room_type": r.room_type,
                "capacity": r.capacity,
                "price_per_night": r.price_per_night
            })
    return {"rooms": available}, 200

@bp.get("/occupancy")
@require_roles(ROLE_ADMIN, ROLE_RECEPTIONIST, ROLE_ACCOUNTANT)
def occupancy_report():
    # ocupación por rango
    start = request.args.get("start")
    end = request.args.get("end")
    if not start or not end:
        return {"error": "start y end requeridos."}, 400
    try:
        start_d = date.fromisoformat(start)
        end_d = date.fromisoformat(end)
    except ValueError:
        return {"error": "Formato de fecha inválido. Use YYYY-MM-DD."}, 400

    total_rooms = Room.query.filter(Room.is_active == True).count()

    # contar reservas que se solapan con el rango y no canceladas
    reservations = Reservation.query.filter(Reservation.status != "cancelled").all()
    active_count = 0
    for r in reservations:
        if start_d < r.check_out and r.check_in < end_d:
            active_count += 1

    occupancy_rate = (active_count / total_rooms * 100.0) if total_rooms else 0.0
    return {
        "total_rooms": total_rooms,
        "active_reservations": active_count,
        "occupancy_rate_percent": round(occupancy_rate, 2)
    }, 200

@bp.get("/finance/summary")
@require_roles(ROLE_ADMIN, ROLE_ACCOUNTANT)
def finance_summary():
    # /reports/finance/summary?start=YYYY-MM-DD&end=YYYY-MM-DD
    start = request.args.get("start")
    end = request.args.get("end")
    if not start or not end:
        return {"error": "start y end requeridos."}, 400
    try:
        start_dt = datetime.fromisoformat(start + "T00:00:00")
        end_dt = datetime.fromisoformat(end + "T23:59:59")
    except ValueError:
        return {"error": "Formato inválido. Use YYYY-MM-DD."}, 400

    income = db.session.query(func.coalesce(func.sum(Payment.amount), 0.0))\
        .filter(Payment.paid_at >= start_dt, Payment.paid_at <= end_dt).scalar()

    expenses = db.session.query(func.coalesce(func.sum(Expense.amount), 0.0))\
        .filter(Expense.incurred_at >= start_dt, Expense.incurred_at <= end_dt).scalar()

    return {
        "income": float(income),
        "expenses": float(expenses),
        "net": float(income - expenses),
    }, 200
