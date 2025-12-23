from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..schemas import UserCreateSchema, LoginSchema, UserOutSchema
from ..services.auth_service import AuthService
from ..utils.permissions import require_roles, ROLE_ADMIN

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.post("/register")
@require_roles(ROLE_ADMIN)
def register():
    data = UserCreateSchema().load(request.json or {})
    user = AuthService.register_user(**data)
    return UserOutSchema().dump(user), 201

@bp.post("/login")
def login():
    data = LoginSchema().load(request.json or {})
    token = AuthService.login(data["username"], data["password"])
    return {"access_token": token}, 200
