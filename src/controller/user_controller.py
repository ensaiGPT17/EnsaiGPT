from src.service.user_service import UserService


class UserController:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def get_user(self, username: str):
        return self.user_service.get_user_by_username(username)

    def login(self, username: str, password: str) -> bool:
        """Retourne True si authentification réussie, False sinon"""
        return self.user_service.authenticate(username, password)

    def register(self, username: str, password: str) -> bool:
        """Retourne True si création de User est réussie, False sinon"""
        return self.user_service.create_user(username, password)

    def change_password(self, username: str, old_password: str, new_password: str) -> \
            bool:
        return self.user_service.change_password(username, old_password, new_password)

    def change_username(self, username: str, new_username: str) -> bool:
        return self.user_service.change_username(username, new_username)
