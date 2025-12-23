from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from ..extensions import db
from ..models import Room
from ..schemas import RoomSchema
from ..utils.permissions import require_roles, ROLE_ADMIN, ROLE_RECEPTIONIST

bp = Blueprint("rooms", __name__, url_prefix="/rooms")

@bp.post("")
@require_roles(ROLE_ADMIN, ROLE_RECEPTIONIST)
def create_room():
    data = RoomSchema().load(request.json or {})
    room = Room(**data)
    db.session.add(room)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return {"error": "number ya existe."}, 400
    return RoomSchema().dump(room), 201

@bp.get("")
@require_roles(ROLE_ADMIN, ROLE_RECEPTIONIST)
def list_rooms():
    status = request.args.get("status")
    query = Room.query
    if status:
        query = query.filter(Room.status == status)
    rooms = query.order_by(Room.number.asc()).all()
    return RoomSchema(many=True).dump(rooms), 200

@bp.get("/<int:room_id>")
@require_roles(ROLE_ADMIN, ROLE_RECEPTIONIST)
def get_room(room_id):
    room = Room.query.get_or_404(room_id)
    return RoomSchema().dump(room), 200

@bp.put("/<int:room_id>")
@require_roles(ROLE_ADMIN, ROLE_RECEPTIONIST)
def update_room(room_id):
    room = Room.query.get_or_404(room_id)
    data = RoomSchema(partial=True).load(request.json or {})
    for k, v in data.items():
        setattr(room, k, v)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return {"error": "number ya existe."}, 400
    return RoomSchema().dump(room), 200
