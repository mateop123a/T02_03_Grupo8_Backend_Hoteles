from __future__ import annotations
import os


class AuthService:
    """
    Auth simple para ADMIN (demo).
    - Usuario y contraseña salen de variables de entorno si existen.
    - Si no existen, usa valores por defecto.
    """

    def __init__(self) -> None:
        self.admin_user = os.getenv("ADMIN_USER", "admin")
        self.admin_pass = os.getenv("ADMIN_PASS", "admin123")

    def validate_admin(self, username: str, password: str) -> bool:
        u = (username or "").strip()
        p = (password or "").strip()
        return u == self.admin_user and p == self.admin_pass
