from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from ..extensions import db
from ..models import Client
from ..schemas import ClientSchema
from ..utils.permissions import require_roles, ROLE_ADMIN, ROLE_RECEPTIONIST

bp = Blueprint("clients", __name__, url_prefix="/clients")

@bp.post("")
@require_roles(ROLE_ADMIN, ROLE_RECEPTIONIST)
def create_client():
    data = ClientSchema().load(request.json or {})
    client = Client(**data)
    db.session.add(client)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return {"error": "doc_id ya existe."}, 400
    return ClientSchema().dump(client), 201

@bp.get("")
@require_roles(ROLE_ADMIN, ROLE_RECEPTIONIST)
def list_clients():
    q = request.args.get("q", "").strip()
    query = Client.query
    if q:
        like = f"%{q}%"
        query = query.filter((Client.full_name.ilike(like)) | (Client.doc_id.ilike(like)))
    clients = query.order_by(Client.created_at.desc()).all()
    return ClientSchema(many=True).dump(clients), 200

@bp.get("/<int:client_id>")
@require_roles(ROLE_ADMIN, ROLE_RECEPTIONIST)
def get_client(client_id):
    client = Client.query.get_or_404(client_id)
    return ClientSchema().dump(client), 200

@bp.put("/<int:client_id>")
@require_roles(ROLE_ADMIN, ROLE_RECEPTIONIST)
def update_client(client_id):
    client = Client.query.get_or_404(client_id)
    data = ClientSchema(partial=True).load(request.json or {})
    for k, v in data.items():
        setattr(client, k, v)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return {"error": "doc_id ya existe."}, 400
    return ClientSchema().dump(client), 200

@bp.delete("/<int:client_id>")
@require_roles(ROLE_ADMIN)
def delete_client(client_id):
    client = Client.query.get_or_404(client_id)
    db.session.delete(client)
    db.session.commit()
    return {"ok": True}, 200
