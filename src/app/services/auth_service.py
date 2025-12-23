from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError
from ..extensions import db
from ..models import User
from ..utils.security import hash_password, verify_password
from ..utils.validators import validate_email

ALLOWED_ROLES = {"admin", "recepcionista", "contador"}

class AuthService:
    @staticmethod
    def register_user(username: str, email: str, password: str, role: str) -> User:
        if not username or len(username) < 3:
            raise ValueError("username mínimo 3 caracteres.")
        validate_email(email)
        if not password or len(password) < 6:
            raise ValueError("password mínimo 6 caracteres.")
        if role not in ALLOWED_ROLES:
            raise ValueError("role inválido. Use admin/recepcionista/contador.")

        user = User(
            username=username.strip(),
            email=email.strip().lower(),
            password_hash=hash_password(password),
            role=role,
            is_active=True,
        )
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise ValueError("username o email ya existe.")
        return user

    @staticmethod
    def login(username: str, password: str) -> str:
        user = User.query.filter_by(username=username).first()
        if not user or not user.is_active:
            raise ValueError("Credenciales inválidas.")
        if not verify_password(password, user.password_hash):
            raise ValueError("Credenciales inválidas.")

        token = create_access_token(
            identity=str(user.id),
            additional_claims={"role": user.role, "username": user.username}
        )
        return token
