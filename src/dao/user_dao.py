from typing import Optional
from src.model.user import User


class UserDAO:
    def __init__(self):
        pass

    def get_user(self, id_user) -> Optional[User]:
        pass

    def get_user_by_username(self, username) -> Optional[User]:
        """Permet d'avoir l'utilisateur grâce à son nom d'utilisateur"""
        pass

    def username_exists(self, username: str) -> bool:
        """Permet de savoir si un nom d'utilisateur est deja pris."""
        pass

    def add_user(self, user: User) -> bool:
        """
        Ajoute un utilisateur à la base de données.
        """
        #new_id = self.get_max_id() + 1
        #user.id_user = new_id
        pass

    def get_max_id(self) -> int:
        """
        Donne le plus grand id associé à un utilisateur.
        Retourne 0 si aucun utilisateur n'existe.
        """
        pass  #ici un SELECT id_user, ORDER BY id_user DESC, LIMIT 1

    def count_users(self) -> int:
        """Renvoie le nombre d'utilisateurs dans la base de données."""
        pass
