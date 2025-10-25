from typing import Optional, List
from model.user import User
from dao.db_connection import DBConnection
from utils.singleton import Singleton


class UserDAO (metaclass=Singleton):
    def __init__(self):
        pass

    def get_user(self, id_user: int) -> Optional[User]:
        query = """
            SELECT id_user, username, hashed_password
            FROM ensaiGPT.user
            WHERE id_user = %s
        """
        with DBConnection().connection as connection:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute(query, (id_user,))
                result = cursor.fetchone()

        if result is None:
            return None

        return User(id_user=result['id_user'], username=result['username'],
                    hashed_password=result['hashed_password'])

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Permet d'avoir l'utilisateur grâce à son nom d'utilisateur"""
        query = """
            SELECT id_user, username, hashed_password
            FROM ensaiGPT.user
            WHERE username = %s
        """
        with DBConnection().connection as connection:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute(query, (username,))
                result = cursor.fetchone()

        if result is None:
            return None

        return User(id_user=result['id_user'], username=result['username'],
                    hashed_password=result['hashed_password'])

    def insert(self, user: User) -> Optional[User]:
        """
        Ajoute un utilisateur à la base de données et met à jour son id_user.
        """
        query = """
            INSERT INTO ensaiGPT.user (username, hashed_password)
            VALUES (%s, %s)
            RETURNING id_user
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (user.username, user.hashed_password))
                result = cursor.fetchone()
        if result is None or result[0] is None:
            return None  # utilisateur n'a pas été créé

        user.id_user = result[0]
        return user

    def delete(self, id_user: int) -> bool:
        """Supprime un utilisateur de la bdd."""
        query = "DELETE FROM ensaiGPT.user WHERE id_user = %s"
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (id_user,))
            connection.commit()
            changes = cursor.rowcount
        return changes > 0

    def update(self, id_user: int, user_updated: User) -> Optional[User]:
        """Modifie un utilisateur de la bdd."""
        query = """
            UPDATE ensaiGPT.user
            SET username = %s, hashed_password = %s
            WHERE id_user = %s
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (
                    user_updated.username,
                    user_updated.hashed_password,
                    id_user
                ))
            changes = cursor.rowcount
            connection.commit()
        if changes == 0:
            return None
        return user_updated

    def get_all(self) -> Optional[List[User]]:
        """Renvoie la liste des utilisateurs."""
        users = []
        query = """
            SELECT id_user, username, hashed_password
            FROM ensaiGPT.user
        """
        with DBConnection().connection as connection:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute(query)
                result = cursor.fetchall()

        if result is None:
            return None

        for row in result:
            user = User(id_user=row['id_user'], username=row['username'],
                        hashed_password=row['hashed_password'])
            users.append(user)

        return users

    def username_exists(self, username: str) -> bool:
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

    def count_users(self) -> Optional[int]:
        """Renvoie le nombre d'utilisateurs dans la base de données."""
        query = """
            SELECT COUNT(*) FROM ensaiGPT.user ;
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchone()
        if result is None:
            return None
        return result[0]
