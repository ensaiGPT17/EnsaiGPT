from typing import Optional
from src.model.user import User
from src.dao.user_dao import UserDAO


class UserDAOMock(UserDAO):
    def __init__(self):
        super().__init__()
        self.users = []  #simule la base SQL des utilisateurs

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

    def username_exists(self, username: str) -> bool:
        """Permet de savoir si un certain nom d'utilisateur existe dans la base."""
        for user in self.users:
            if username == user.username:
                return True
        return False

    def add_user(self, user: User) -> bool:
        new_id = self.get_max_id() + 1
        user.id_user = new_id
        self.users.append(user)
        return True

    def get_max_id(self) -> int:
        """
        Donne le plus grand id associé à un utilisateur.
        Retourne 0 si aucun utilisateur n'existe.
        """
        if len(self.users) == 0:
            return 0
        return max(user.id_user for user in self.users)

    def count_users(self) -> int:
        """Renvoie le nombre d'utilisateurs dans la base de données."""
        return len(self.users)
