from typing import Optional
from src.model.user import User
from src.dao.user_dao import UserDAO


class UserDAOMock(UserDAO):
    def __init__(self):
        super().__init__()
        self.users = []  #simule la base SQL

    def get_user(self, id_user) -> Optional[User]:
        for user in self.users:
            if user.id_user == id_user:
                return user
        return None

    def get_user_by_username(self, username) -> Optional[User]:
        """Permet d'avoir l'utilisateur grâce à son nom d'utilisateur"""
        for user in self.users:
            if user.username == username:
                return user
        return None

    def add_user(self, user: User) -> bool:
        """
        Ajoute un utilisateur à la base de données.
        """
        for other in self.users:
            if other.username == user.username:
                return False
        self.users.append(user)
        return True

    def get_last_id(self) -> int:
        """
        Donne le plus le dernier id associé à un utilisateur.
        Retourne 0 si aucun utilisateur existe.
        """
        if len(self.users) == 0:
            return 0
        return max(user.id_user for user in self.users)
