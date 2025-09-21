from src.dao.user_dao import UserDAO
from password_service import hash_password


class UserService:
    def __init__(self, user_dao: UserDAO):
        self.user_dao = user_dao

    def get_user_info(self, id_user: int) -> dict:
        """Permet d'avoir les informations de l'utilisateur"""
        user = self.user_dao.get_user(id_user)
        return {"id_user": user["id_user"], "username": user["username"]}

    def authenticate(self, id_user: str, password: str) -> bool:
        user = self.user_dao.get_user(id_user)
        hashed = hash_password(password)
        return hashed == user["password"]
