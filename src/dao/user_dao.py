from typing import Optional, List
from model.user import User
from dao.db_connection import DBConnection
from utils.singleton import Singleton


class UserDAO (metaclass=Singleton):
    def __init__(self, schema: str = "ensaiGPT"):
        """
        Parameters
        ----------
        schema : str
            Nom du schéma PostgreSQL contenant la table des utilisateurs.
        """
        self.schema = schema

    def get_user(self, id_user: int) -> Optional[User]:
        """
        Récupère un utilisateur selon son ID.

        Parameters
        ----------
        id_user : int
            Identifiant unique de l'utilisateur.

        Returns
        -------
        user : Optional[User]
            L'utilisateur correspondant ou None s'il n'existe pas.
        """
        query = f"""
            SELECT id_user, username, hashed_password
            FROM {self.schema}.users
            WHERE id_user = %s
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (id_user,))
                result = cursor.fetchone()

        if result is None:
            return None

        return User(id_user=result['id_user'], username=result['username'],
                    hashed_password=result['hashed_password'])

    def get_user_by_username(self, username: str) -> Optional[User]:
        """
        Récupère un utilisateur grâce à son nom d'utilisateur.

        Parameters
        ----------
        username : str
            Nom d'utilisateur recherché.

        Returns
        -------
        user : Optional[User]
            L'utilisateur correspondant ou None s'il n'existe pas.
        """
        query = f"""
            SELECT id_user, username, hashed_password
            FROM {self.schema}.users
            WHERE username = %s
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (username,))
                result = cursor.fetchone()

        if result is None:
            return None

        return User(id_user=result['id_user'], username=result['username'],
                    hashed_password=result['hashed_password'])

    def insert(self, user: User) -> Optional[User]:
        """
        Insère un utilisateur dans la base de données.

        Parameters
        ----------
        user : User
            L'utilisateur à ajouter.

        Returns
        -------
        user : Optional[User]
            L'utilisateur avec son id_user mis à jour, ou None si l'insertion échoue.
        """
        query = f"""
            INSERT INTO {self.schema}.users (username, hashed_password)
            VALUES (%s, %s)
            RETURNING id_user
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (user.username, user.hashed_password))
                result = cursor.fetchone()
        if result is None:
            return None  # utilisateur n'a pas été créé

        user.id_user = result['id_user']
        return user

    def delete(self, id_user: int) -> bool:
        """
        Supprime un utilisateur de la base de données.

        Parameters
        ----------
        id_user : int
            Identifiant de l'utilisateur à supprimer.

        Returns
        -------
        deleted : bool
            True si un utilisateur a été supprimé, False sinon.
        """
        query = f"DELETE FROM {self.schema}.users WHERE id_user = %s"
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (id_user,))
            connection.commit()
            changes = cursor.rowcount
        return changes > 0

    def update(self, id_user: int, user_updated: User) -> Optional[User]:
        """
        Met à jour les informations d’un utilisateur.

        Parameters
        ----------
        id_user : int
            Identifiant de l'utilisateur à modifier.

        user_updated : User
            Objet User contenant les nouvelles valeurs.

        Returns
        -------
        user : Optional[User]
            L'utilisateur mis à jour, ou None si aucune modification n'a eu lieu.
        """
        query = f"""
            UPDATE {self.schema}.users
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
        """
        Renvoie la liste de tous les utilisateurs.

        Returns
        -------
        users : Optional[List[User]]
            Liste des utilisateurs ou None si la requête échoue.
        """
        users = []
        query = f"""
            SELECT id_user, username, hashed_password
            FROM {self.schema}.users
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
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
        """
        Vérifie si un nom d'utilisateur est déjà utilisé.

        Parameters
        ----------
        username : str
            Nom à vérifier.

        Returns
        -------
        exists : bool
            True si le nom existe déjà, False sinon.
        """
        query = f"""
            SELECT 1 FROM {self.schema}.users
            WHERE username = %s
            LIMIT 1;
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (username,))
                result = cursor.fetchone()
        return result is not None

    def count_users(self) -> Optional[int]:
        """
        Renvoie le nombre total d'utilisateurs.

        Returns
        -------
        count : Optional[int]
            Nombre d'utilisateurs ou None en cas d'erreur.
        """
        query = f"""
            SELECT COUNT(*) FROM {self.schema}.users ;
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchone()

        if result is None:
            return None
        return result['count']
