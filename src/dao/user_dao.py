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
            FROM ensaiGPT.users
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
        """Permet d'avoir l'utilisateur grâce à son nom d'utilisateur"""
        query = """
            SELECT id_user, username, hashed_password
            FROM ensaiGPT.users
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
        Ajoute un utilisateur à la base de données et met à jour son id_user.
        """
        query = """
            INSERT INTO ensaiGPT.users (username, hashed_password)
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
        """Supprime un utilisateur de la bdd."""
        query = "DELETE FROM ensaiGPT.users WHERE id_user = %s"
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (id_user,))
            connection.commit()
            changes = cursor.rowcount
        return changes > 0

    def update(self, id_user: int, user_updated: User) -> Optional[User]:
        """Modifie un utilisateur de la bdd."""
        query = """
            UPDATE ensaiGPT.users
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
            FROM ensaiGPT.users
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
        """Permet de savoir si un nom d'utilisateur est déjà pris."""
        query = """
            SELECT 1 FROM ensaiGPT.users
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
            SELECT COUNT(*) FROM ensaiGPT.users ;
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchone()
        
        #print(result)
        if result is None:
            return None
        return result['count']


"""
if __name__ == "__main__":
    # Initialisation du DAO
    user_dao = UserDAO()

    print("=== TEST DE LA CLASSE UserDAO ===")
    new_user = User(id_user=None, username="bruno", hashed_password="1234")
    id_user = 1 
    username = 'bruno'

    #  - Récupération par ID
    print("\n--- Récupération par ID ---")
    user = user_dao.get_user(id_user)
    print(f"Utilisateur récupéré : {user.username if user else 'Aucun utilisateur trouvé'}")

    user_by_name = user_dao.get_user_by_username(username)
    print(f"Utilisateur trouvé : {user_by_name.id_user, user_by_name.username, user_by_name.hashed_password if user_by_name else 'Non trouvé'}")


    # - Vérification de l'existence du username
    print("\n--- Vérification username_exists ---")
    exists = user_dao.username_exists(username)
    print(f"Le nom d'utilisateur {username} existe ? {'Oui' if exists else 'Non'}")

    username1 = 'brun'
    exists = user_dao.username_exists(username1)
    print(f"Le nom d'utilisateur {username1} existe ? {'Oui' if exists else 'Non'}")

    #  - Récupération de tous les utilisateurs
    print("\n--- Liste de tous les utilisateurs ---")
    users = user_dao.get_all()
    if users:
        for u in users:
            print(f"{u.id_user} | {u.username}")
    else:
        print("Aucun utilisateur trouvé")

    #  - Insertion d'un nouvel utilisateur
    print("\n--- Insertion d'un utilisateur ---")
    new_user = User(id_user=None, username="bruno_inserted", hashed_password="1234")
    inserted_user = user_dao.insert(new_user)
    if inserted_user:
        print(f"Utilisateur inséré avec succès : {inserted_user.id_user}, {inserted_user.username}")
    else:
        print("Échec d'insertion")
    

    #  - Mise à jour
    print("\n--- Mise à jour d'un utilisateur ---")
    updated_user = User(id_user=inserted_user.id_user, username="updated_user", hashed_password="new_hashed_pwd")
    result = user_dao.update(inserted_user.id_user, updated_user)
    print(f"Mise à jour réussie : {result.username if result else 'Échec'}")

    #  - Compter le nombre d'utilisateurs
    print("\n--- Compter le nombre d'utilisateurs ---")
    count = user_dao.count_users()
    print(f"Nombre total d'utilisateurs : {count}")

    #  - Suppression
    print("\n--- Suppression d'un utilisateur ---")
    deleted = user_dao.delete(inserted_user.id_user)
    print("Utilisateur supprimé avec succès" if deleted else "Échec de suppression")


    # 5 Récupération de tous les utilisateurs
    print("\n--- Liste de tous les utilisateurs ---")
    users = user_dao.get_all()
    if users:
        for u in users:
            print(f"{u.id_user} | {u.username}")
    else:
        print("Aucun utilisateur trouvé")

"""