from typing import Optional
from app.db import db
from app.domain.models.user import User

class UserRepository:
    def get_by_email(self, email: str) -> Optional[User]:
        return User.query.filter_by(email=email).first()

    def create(self, email: str, password_hash: str) -> User:
        user = User(email=email, password_hash=password_hash)
        db.session.add(user)
        db.session.commit()
        return user
