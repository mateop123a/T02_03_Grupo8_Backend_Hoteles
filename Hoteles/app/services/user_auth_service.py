from werkzeug.security import generate_password_hash, check_password_hash
from app.repositories.user_repository import UserRepository

class UserAuthService:
    def __init__(self, repo: UserRepository) -> None:
        self.repo = repo

    def register(self, email: str, password: str):
        email = (email or "").strip().lower()
        password = (password or "").strip()

        if "@" not in email:
            return "Email inválido"
        if len(password) < 4:
            return "La contraseña debe tener al menos 4 caracteres"
        if self.repo.get_by_email(email):
            return "El usuario ya existe"

        self.repo.create(email=email, password_hash=generate_password_hash(password))
        return None

    def validate(self, email: str, password: str) -> bool:
        email = (email or "").strip().lower()
        u = self.repo.get_by_email(email)
        if not u:
            return False
        return check_password_hash(u.password_hash, password)
