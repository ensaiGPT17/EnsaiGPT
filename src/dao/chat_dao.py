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
            SELECT id_chat, id_user, title, date_start, last_date, max_tokens, temperature, top_p
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
            temperature=result["temperature"],
            top_p=result["top_p"]
        )

    def insert(self, chat: Chat) -> Optional[Chat]:
        """Insère une nouvelle conversation et renvoie l'objet avec son id."""
        query = """
            INSERT INTO ensaiGPT.chats (id_user, title, date_start, last_date, max_tokens, 
            temperature, top_p)
            VALUES (%s, %s, NOW(), NOW(), %s, %s, %s)
            RETURNING id_chat, id_user, title, date_start, last_date, max_tokens, 
            temperature, top_p
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (chat.id_user, chat.title, chat.max_tokens, chat.temperature, 
                chat.top_p))
                result = cursor.fetchone()

        if result is None:
            return None

        return Chat(
                    id_chat=result["id_chat"],
                    title=result["title"],
                    id_user=result["id_user"],
                    date_start=result["date_start"],
                    last_date=result["last_date"],
                    max_tokens=result["max_tokens"],
                    temperature=result["temperature"],
                    top_p=result["top_p"]
        )

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
            SELECT id_chat, id_user, title, date_start, last_date, max_tokens, 
            temperature, top_p
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
            SELECT id_chat, id_user, title, date_start, last_date, max_tokens, 
            temperature, top_p
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

"""
if __name__ == "__main__":
    from datetime import datetime

    print("=== TEST DE LA CLASSE ChatDAO ===")

    chat_dao = ChatDAO()
    #  Recup conversation

    chat1 = chat_dao.get_chat(1)

    print(f"CONV: {chat1.title} -- et derniere fois: {chat1.last_date}")

    # 2. Li
    id_chat = 100
    max_tokens = 500
    temp = 0.5
    top_p = 0.9
    id_user = 3
    title="Coucogdgdfg gdfgdu"

    chat_to_insert = Chat(
        id_chat=id_chat,
        id_user=id_user,
        title=title,
        date_start=datetime.now(),
        last_date=datetime.now(),
        max_tokens=max_tokens,
        temperature=temp,
        top_p=top_p
    )
    chat_dao.insert(chat=chat_to_insert)

    #3 - update chat
    id_chat = 9
    updated_chat = Chat(
        id_chat=id_chat,
        id_user=id_user,
        title="TITRE du nouveau id",
        date_start=datetime.now(),
        last_date=datetime.now(),
        max_tokens=max_tokens,
        temperature=temp,
        top_p=top_p
    )
    chat_dao.update(id_chat=id_chat, chat_updated=updated_chat)

    # Deete chat 
    #chat_dao.delete(9)

    # toutes les conversations
    liste = chat_dao.get_all()

    for conv in liste:
        print(f"ID: {conv.id_chat} --- TITRE: {conv.title}")

    print(" --------- --------------- ----------------")
    
    # toutes les conversations d'un user
    id_user = 2
    liste = chat_dao.list_chats_id_user(id_user=id_user)

    for conv in liste:
        print(f"ID: {conv.id_chat} --- TITRE: {conv.title}")

    print(" --------- --------------- ----------------")
    print(chat_dao.count_chats())
"""