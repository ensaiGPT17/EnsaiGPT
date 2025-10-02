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
        try:
            success = self.user_service.create_user(username, password)
            if success:
                return {"success": True, "message": "Utilisateur créé."}
            return {"success": False, "error": "L'utilisateur n'a pas été créé."}
        except ValueError as e:
            return {"success": False, "error": str(e)}

    def change_password(self, username: str, old_password: str, old_password_confirm,
                        new_password: str) -> dict:
        if old_password != old_password_confirm:
            return {"success": False,
                    "error": "Les mots de passe actuels ne correspondent pas."}

        try:
            success = self.user_service.change_password(username, old_password,
                                                        new_password)
            if success:
                return {"success": True, "message": "Mot de passe mis à jour."}
            return {"success": False, "error": "Impossible de changer le mot de passe."}
        except ValueError as e:
            return {"success": False, "error": str(e)}

    def change_username(self, username: str, new_username: str) -> dict:
        try:
            success = self.user_service.change_username(username, new_username)
            if success:
                return {"success": True, "message": "Nom d'utilisateur mis à jour."}
            return {"success": False, "error": "Impossible de changer le nom "
                                               "d'utilisateur."}
        except ValueError as e:
            return {"success": False, "error": str(e)}
