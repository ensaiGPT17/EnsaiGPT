from typing import Optional
from src.model.user import User
from src.dao.user_dao import UserDAO
from src.service.password_service import hash_password, password_is_secure
from src.service.response_service import ResponseService


class UserService:
    # --- Constantes avec code et message ---
    USER_CREATED = (201, "Utilisateur créé avec succès")
    PASSWORD_WEAK = (400, "Mot de passe trop faible")
    USERNAME_EXISTS = (409, "Nom d'utilisateur déjà utilisé")
    CREATION_ERROR = (500, "Erreur interne lors de la création de l'utilisateur")
    AUTH_FAILED = (401, "Nom d'utilisateur ou mot de passe incorrect")
    AUTH_SUCCESS = (200, "Authentification réussie")
    PASSWORD_CHANGE_SUCCESS = (200, "Mot de passe modifié avec succès")
    PASSWORD_CHANGE_ERROR = (500, "Impossible de modifier le mot de passe")
    USER_NOT_FOUND = (404, "Utilisateur non trouvé")
    USERNAME_CHANGE_SUCCESS = (200, "Nom d'utilisateur modifié avec succès")
    USERNAME_CHANGE_ERROR = (500, "Impossible de modifier le nom d'utilisateur")

    def __init__(self, user_dao: UserDAO):
        self.user_dao = user_dao

    def get_user(self, id_user: int) -> Optional[User]:
        return self.user_dao.get_user(id_user)

    def get_user_by_username(self, username: str) -> Optional[User]:
        return self.user_dao.get_user_by_username(username)

    # ------------------- Création -------------------
    def create_user(self, username: str, password: str) -> ResponseService:
        if self.user_dao.username_exists(username):
            return ResponseService(*self.USERNAME_EXISTS)
        if not password_is_secure(password):
            return ResponseService(*self.PASSWORD_WEAK)

        hashed = hash_password(password)
        user = self.user_dao.insert_user(User(0, username, hashed))
        if user is None:
            return ResponseService(*self.CREATION_ERROR)

        return ResponseService(*self.USER_CREATED)

    # ------------------- Authentification -------------------
    def authenticate(self, username: str, password: str) -> ResponseService:
        user = self.user_dao.get_user_by_username(username)
        if user is None:
            return ResponseService(*self.AUTH_FAILED)

        hashed = hash_password(password)
        if hashed != user.hashed_password:
            return ResponseService(*self.AUTH_FAILED)

        return ResponseService(*self.AUTH_SUCCESS)

    # ------------------- Changement de mot de passe -------------------
    def change_password(self, username: str, password: str, new_password: str) -> ResponseService:
        if not password_is_secure(new_password):
            return ResponseService(*self.PASSWORD_WEAK)

        user = self.user_dao.get_user_by_username(username)
        if user is None:
            return ResponseService(*self.USER_NOT_FOUND)

        auth_response = self.authenticate(username, password)
        if auth_response.code != 200:
            return ResponseService(*self.AUTH_FAILED)

        user.hashed_password = hash_password(new_password)
        updated_user = self.user_dao.update(user.id_user, user)
        if updated_user is None:
            return ResponseService(*self.PASSWORD_CHANGE_ERROR)

        return ResponseService(*self.PASSWORD_CHANGE_SUCCESS)

    # ------------------- Changement de nom d'utilisateur -------------------
    def change_username(self, username: str, new_username: str) -> ResponseService:
        user = self.user_dao.get_user_by_username(username)
        if user is None:
            return ResponseService(*self.USER_NOT_FOUND)

        new_username_user = self.user_dao.get_user_by_username(new_username)
        if new_username_user is not None:
            return ResponseService(*self.USERNAME_EXISTS)

        user.username = new_username
        updated_user = self.user_dao.update(user.id_user, user)
        if updated_user is None:
            return ResponseService(*self.USERNAME_CHANGE_ERROR)

        return ResponseService(*self.USERNAME_CHANGE_SUCCESS)

    # ------------------- Compteur -------------------
    def count_users(self) -> int:
        return self.user_dao.count_users()