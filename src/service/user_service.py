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

    def get_user_info_by_username(self, username: str) -> Optional[dict]:
        """Permet d'avoir les informations de l'utilisateur par son username"""
        user = self.user_dao.get_user_by_username(username)
        if user is None:
            return None
        return {"id_user": user.id_user, "username": user.username}

    def create_user(self, username: str, password: str) -> bool:
        if self.user_dao.username_exists(username):
            return False
        hashed = hash_password(password)
        id_user = self.user_dao.get_max_id() + 1
        user = User(id_user, username, hashed)
        return self.user_dao.add_user(user)

    def authenticate(self, username: str, password: str) -> bool:
        user = self.user_dao.get_user_by_username(username)
        if user is None:  #si le nom d'utilisateur ne correspond à rien
            return False
        hashed = hash_password(password)
        return hashed == user.hashed_password

    def count_users(self):  #surtout utile pour les tests
        """
        Renvoie le nombre d'utilisateurs inscrits.
        """
        return self.user_dao.count_users()
