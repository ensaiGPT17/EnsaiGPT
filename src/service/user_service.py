from typing import Optional
from model.user import User
from dao.user_dao import UserDAO
from service.password_service import hash_password, password_is_secure, check_password
from service.response_service import ResponseService
from utils.log_decorator import log


class UserService:
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
    USER_DELETE_SUCCESS = (200, "Utilisateur supprimé avec succès")
    USER_DELETE_ERROR = (500, "Impossible de supprimer l'utilisateur")

    def __init__(self, user_dao: UserDAO):
        self.user_dao = user_dao

    @log
    def get_user(self, id_user: int) -> Optional[User]:
        return self.user_dao.get_user(id_user)

    @log
    def get_user_by_username(self, username: str) -> Optional[User]:
        return self.user_dao.get_user_by_username(username)

    @log
    def is_username_available(self, username: str) -> ResponseService:
        """
        Vérifie si le nom d'utilisateur est disponible.
        Retourne ResponseService avec code 200 si disponible, sinon 409.
        """
        if self.user_dao.username_exists(username):
            return ResponseService(*self.USERNAME_EXISTS)
        return ResponseService(200, "Nom d'utilisateur disponible")

    @log
    def is_password_secure(self, password: str) -> ResponseService:
        """
        Crée un nouvel utilisateur avec un mot de passe sécurisé.
        Codes de sortie :
        - 201 : "Utilisateur créé avec succès"
        - 400 : "Mot de passe trop faible"
        - 409 : "Nom d'utilisateur déjà utilisé"
        - 500 : "Erreur interne lors de la création de l'utilisateur"
        """
        if not password_is_secure(password):
            return ResponseService(*self.PASSWORD_WEAK)
        return ResponseService(200, "Mot de passe sécurisé")

    @log
    def create_user(self, username: str, password: str) -> ResponseService:

        """
        Crée un nouvel utilisateur avec un mot de passe sécurisé.
        Codes de sortie :
        - 201 : "Utilisateur créé avec succès"
        - 400 : "Mot de passe trop faible"
        - 409 : "Nom d'utilisateur déjà utilisé"
        - 500 : "Erreur interne lors de la création de l'utilisateur"
        """
        if self.user_dao.username_exists(username):
            return ResponseService(*self.USERNAME_EXISTS)
        if not password_is_secure(password):
            return ResponseService(*self.PASSWORD_WEAK)

        hashed = hash_password(password)
        user = self.user_dao.insert(User(0, username, hashed))
        if user is None:
            return ResponseService(*self.CREATION_ERROR)

        return ResponseService(201, "Utilisateur créé avec succès")

    @log
    def authenticate(self, username: str, password: str) -> ResponseService:
        """
        Authentifie un utilisateur via son nom d'utilisateur et mot de passe.
        
        Codes de sortie :
        - 200 : "Authentification réussie"
        - 401 : "Nom d'utilisateur ou mot de passe incorrect"
        """
        user = self.user_dao.get_user_by_username(username)
        if user is None:
            return ResponseService(*self.AUTH_FAILED)
        if not check_password(password, user.hashed_password):
            return ResponseService(*self.AUTH_FAILED)
        return ResponseService(*self.AUTH_SUCCESS)

    @log
    def change_password(self, id_user: int, old_password: str, new_password: str) -> \
            ResponseService:

        """
        Change le mot de passe d'un utilisateur après vérification de l'ancien mot de passe.    
        Codes de sortie :
        - 200 : "Mot de passe modifié avec succès"
        - 400 : "Mot de passe trop faible"
        - 401 : "Nom d'utilisateur ou mot de passe incorrect"
        - 404 : "Utilisateur non trouvé"
        - 500 : "Impossible de modifier le mot de passe"
        """
        if not password_is_secure(new_password):
            return ResponseService(*self.PASSWORD_WEAK)

        user = self.user_dao.get_user(id_user)
        if user is None:
            return ResponseService(*self.USER_NOT_FOUND)

        if not check_password(old_password, user.hashed_password):
            return ResponseService(*self.AUTH_FAILED)

        user.hashed_password = hash_password(new_password)
        if self.user_dao.update(id_user, user) is None:
            return ResponseService(*self.PASSWORD_CHANGE_ERROR)

        return ResponseService(*self.PASSWORD_CHANGE_SUCCESS)

    @log
    def change_username(self, id_user: int, new_username: str) -> ResponseService:

        """
            Change le nom d'utilisateur après vérification de la disponibilité.
            
            Codes de sortie :
            - 200 : "Nom d'utilisateur modifié avec succès"
            - 404 : "Utilisateur non trouvé"
            - 409 : "Nom d'utilisateur déjà utilisé"
            - 500 : "Impossible de modifier le nom d'utilisateur"
        """
        user = self.user_dao.get_user(id_user)
        if user is None:
            return ResponseService(*self.USER_NOT_FOUND)

        if self.user_dao.username_exists(new_username):
            return ResponseService(*self.USERNAME_EXISTS)

        user.username = new_username
        if self.user_dao.update(id_user, user) is None:
            return ResponseService(*self.USERNAME_CHANGE_ERROR)

        return ResponseService(*self.USERNAME_CHANGE_SUCCESS)

    @log
    def delete_user(self, id_user: int, password: str) -> ResponseService:
        """
        Supprime un utilisateur à partir de son nom d'utilisateur.
        Retourne ResponseService avec code 200 si succès, 404 si utilisateur non trouvé,
        500 si erreur.

        Codes de sortie :
            - 200 : "Utilisateur supprimé avec succès"
            - 401 : "Nom d'utilisateur ou mot de passe incorrect"
            - 404 : "Utilisateur non trouvé"
            - 500 : "Impossible de supprimer l'utilisateur"
        """

        user = self.user_dao.get_user(id_user)
        if user is None:
            return ResponseService(*self.USER_NOT_FOUND)

        # Authentification
        if not check_password(password, user.hashed_password):
            return ResponseService(*self.AUTH_FAILED)

        if not self.user_dao.delete(id_user):
            return ResponseService(*self.USER_DELETE_ERROR)

        return ResponseService(*self.USER_DELETE_SUCCESS)

    @log
    def count_users(self) -> int:
        return self.user_dao.count_users()
