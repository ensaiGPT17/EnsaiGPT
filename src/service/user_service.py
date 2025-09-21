from typing import Optional
from src.model.user import User
from src.dao.user_dao import UserDAO
from src.service.password_service import hash_password


class UserService:
    def __init__(self, user_dao: UserDAO):
        self.user_dao = user_dao

    def get_user_info(self, id_user: int) -> Optional[dict]:
        """Permet d'avoir les informations de l'utilisateur"""
        user = self.user_dao.get_user(id_user)
        if user is None:
            return None
        return {"id_user": user.id_user, "username": user.username}

    def create_user(self, username: str, password: str) -> bool:
        hashed = hash_password(password, None)
        id_user = self.user_dao.get_last_id() + 1
        user = User(id_user, username, hashed)
        return self.user_dao.add_user(user)

    def authenticate(self, username: str, password: str) -> bool:
        user = self.user_dao.get_user_by_username(username)
        if user is None:  #si le nom d'utilisateur ne correspond à rien
            return False
        hashed = hash_password(password, None)
        return hashed == user.hashed_password
