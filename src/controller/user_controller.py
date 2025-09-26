from src.service.user_service import UserService
from src.service.password_service import password_is_secure


class UserController:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def get_user(self, username: str):
        return self.user_service.get_user_by_username(username)

    def login(self, username: str, password: str) -> bool:
        """Retourne True si authentification réussie, False sinon"""
        return self.user_service.authenticate(username, password)

    def register(self, username: str, password: str) -> dict:
        if not password_is_secure(password):
            return {"success": False,
                    "error": "Le mot de passe doit [être sécurisé]."}

        success = self.user_service.create_user(username, password)
        if success:
            return {"success": True, "message": "Utilisateur créé."}
        else:
            return {"success": False, "error": "Ce nom d'utilisateur est déjà pris."}

    def change_password(self, username: str, old_password: str, new_password: str) -> \
            bool:
        return self.user_service.change_password(username, old_password, new_password)

    def change_username(self, username: str, new_username: str) -> bool:
        return self.user_service.change_username(username, new_username)
