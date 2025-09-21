from src.dao.user_dao import UserDAO
from password_service import hash_password


class UserService:
    def __init__(self, user_dao: UserDAO):
        self.user_dao = user_dao

    def get_user_info(self, id_user: int) -> dict:
        """Permet d'avoir les informations de l'utilisateur"""
        user = self.user_dao.get_user(id_user)
        return {"id_user": user["id_user"], "username": user["username"]}

    def create_user(self, username: str, password: str):
        hashed = hash_password(password, None)
        id_user = self.user_dao.get_last_id() + 1
        success = self.user_dao.add_user(id_user, username, hashed)
        if success:
            return {"id_user": id_user, "username": username}
        else:
            return None

    def authenticate(self, username: str, password: str) -> bool:
        user = self.user_dao.get_user_by_username(username)
        hashed = hash_password(password, None)
        return hashed == user["password"]
