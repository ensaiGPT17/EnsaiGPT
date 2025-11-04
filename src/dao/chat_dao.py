from typing import Optional, List
from model.chat import Chat
from dao.db_connection import DBConnection
from utils.singleton import Singleton


class ChatDAO(metaclass=Singleton):
    def __init__(self):
        pass

    def get_chat(self, id_chat: int) -> Optional[Chat]:
        """Récupère une conversation par son id."""
        query = """
            SELECT id_chat, id_user, title, date_start, last_date
            FROM ensaiGPT.chats
            WHERE id_chat = %s
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (id_chat,))
                result = cursor.fetchone()

        if result is None:
            return None

        return Chat(
            id_chat=result["id_chat"],
            id_user=result["id_user"],
            title=result["title"],
            date_start=result["date_start"],
            last_date=result["last_date"],
            max_tokens=result["max_tokens"],
            temperature=result['temperature'],
            top_p=result["top_p"]
        )

    def insert(self, chat: Chat) -> Optional[Chat]:
        """Insère une nouvelle conversation et renvoie l'objet avec son id."""
        query = """
            INSERT INTO ensaiGPT.chats (id_user, title, date_start, last_date)
            VALUES (%s, %s, NOW(), NOW())
            RETURNING id_chat, date_start, last_date
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (chat.id_user, chat.title))
                result = cursor.fetchone()

        if result is None:
            return None

        chat.id_chat = result["id_chat"]
        chat.date_start = result["date_start"]
        chat.last_date = result["last_date"]
        return chat

    def delete(self, id_chat: int) -> bool:
        """Supprime une conversation."""
        query = "DELETE FROM ensaiGPT.chats WHERE id_chat = %s"
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (id_chat,))
            connection.commit()
            return cursor.rowcount > 0

    def update(self, id_chat: int, chat_updated: Chat) -> Optional[Chat]:
        """Met à jour le titre d’une conversation."""
        query = """
            UPDATE ensaiGPT.chats
            SET title = %s, last_date = NOW()
            WHERE id_chat = %s
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (chat_updated.title, id_chat))
            connection.commit()

            if cursor.rowcount == 0:
                return None
        return chat_updated

    def get_all(self) -> Optional[List[Chat]]:
        """Retourne toutes les conversations."""
        query = """
            SELECT id_chat, id_user, title, date_start, last_date
            FROM ensaiGPT.chats
            ORDER BY last_date DESC
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                results = cursor.fetchall()

        if not results:
            return None

        chats = []
        for row in results:
            chats.append(Chat(
                id_chat=row["id_chat"],
                id_user=row["id_user"],
                title=row["title"],
                date_start=row["date_start"],
                last_date=row["last_date"],
                max_tokens=row["max_tokens"],
                temperature=row['temperature'],
                top_p=row["top_p"]
            ))
        return chats

    def list_chats_id_user(self, id_user: int) -> Optional[List[Chat]]:
        """Liste toutes les conversations d’un utilisateur."""
        query = """
            SELECT id_chat, id_user, title, date_start, last_date
            FROM ensaiGPT.chats
            WHERE id_user = %s
            ORDER BY last_date DESC
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (id_user,))
                results = cursor.fetchall()

        if not results:
            return None

        chats = []
        for row in results:
            chats.append(Chat(
                id_chat=row["id_chat"],
                id_user=row["id_user"],
                title=row["title"],
                date_start=row["date_start"],
                last_date=row["last_date"],
                max_tokens=row["max_tokens"],
                temperature=row['temperature'],
                top_p=row["top_p"]
            ))
        return chats

    def count_chats(self) -> Optional[int]:
        """Compte le nombre total de conversations."""
        query = "SELECT COUNT(*) FROM ensaiGPT.chats"
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchone()

        if result is None:
            return None
        return result["count"]
