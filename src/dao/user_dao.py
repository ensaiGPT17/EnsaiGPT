from src.model.user import User


class UserDAO:
    def __init__(self):
        pass

    def get_user(self, id_user) -> User:
        pass

    def get_user_by_username(self, username) -> User:
        """Permet d'avoir l'utilisateur grâce à son nom d'utilisateur"""
        pass

    def add_user(self, user: User) -> bool:
        pass

    def get_last_id(self) -> int:
        """
        Donne le plus le dernier id associé à un utilisateur.
        Retourne 0 si aucun utilisateur existe.
        """
        pass  #ici un SELECT id_user, ORDER BY id_user DESC, LIMIT 1
