from flask import Blueprint, request
from ..models import User
from ..schemas import UserOutSchema
from ..utils.permissions import require_roles, ROLE_ADMIN

bp = Blueprint("users", __name__, url_prefix="/users")

@bp.get("")
@require_roles(ROLE_ADMIN)
def list_users():
    users = User.query.order_by(User.created_at.desc()).all()
    return UserOutSchema(many=True).dump(users), 200
