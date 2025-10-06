from typing import Optional
from model.user import User
from dao.db_connection import DBConnection
from utils.singleton import Singleton

class UserDAO (metaclass = Singleton):
    def __init__(self):
        pass

    def get_user(self, id_user) -> Optional[User]:
        pass

    def get_user_by_username(self, username) -> Optional[User]:
        """Permet d'avoir l'utilisateur grâce à son nom d'utilisateur"""
        pass

    def insert(self, user: User) -> Optional[User]:
        """
        Ajoute un utilisateur à la base de données.
        """
        #new_id = self.get_max_id() + 1
        #user.id_user = new_id
        pass

    def delete(self, id_user: int) -> bool:
        """Supprime un utilisateur de la bdd."""
        pass

    def update(self, id_user: int, user_updated: User) -> Optional[User]:
        """Modifie un utilisateur de la bdd."""
        pass

    def get_all(self):
        """Renvoie la liste des utilisateurs."""
        pass

    def username_exists(self, username: str) -> bool:
        # Juste pour tester si les requettes fonctionne
        """Permet de savoir si un nom d'utilisateur est déjà pris."""
        query = """
            SELECT 1 FROM ensaiGPT.user
            WHERE username = %s
            LIMIT 1;
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (username,))
                result = cursor.fetchone()
                return result is not None

    def get_max_id(self) -> int:
        """
        Donne le plus grand id associé à un utilisateur.
        Retourne 0 si aucun utilisateur n'existe.
        """
        """ ici un SELECT id_user, ORDER BY id_user DESC, LIMIT 1  
              # ==> par Bruno, haha :) : ensuite, renvoyer l'id de l'utilisateur """
        pass

    def count_users(self) -> int:
        """Renvoie le nombre d'utilisateurs dans la base de données."""
        pass
