from typing import Optional, List
from datetime import datetime
from model.message import Message
from dao.db_connection import DBConnection
from utils.singleton import Singleton


class MessageDAO(metaclass=Singleton):

    def create_message(self, id_chat: int, date_sending: datetime, role_author: str, content: str) -> Optional[Message]:
        """Ajouter un nouveau message à la base de données

        Parameters
        ----------
        id_chat : int
            L'id de la conversation à laquelle le message appartient
        date_sending : datetime
            La date d'envoi du message
        role_author : str
            L'auteur du message
        content : str
            Le contenu du message

        Returns
        -------
        Optional[Message]
            L'objet Message créé ou None en cas d'erreur
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                query = """
                    INSERT INTO message (id_chat, date_sending, role_author, content)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id_message;
                """
                cursor.execute(query, (id_chat, date_sending, role_author, content))
                res = cursor.fetchone()

        # Construction de l’objet Message si insertion réussie
        if res:
            new_id = res[0]
            return Message(
                id_message=new_id,
                id_chat=id_chat,
                date_sending=date_sending,
                role_author=role_author,
                content=content
            )

        # En cas d’échec
        return None

    def delete_message(self, id_message: int) -> bool:
        """Supprimer un message de la base de données

        Parameters
        ----------
        id_message : int
            L'id du message à supprimer

        Returns
        -------
        bool
            True si le message a bien été supprimé, False sinon
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                query = """
                    DELETE FROM message
                    WHERE id_message = %s
                """
                cursor.execute(query, (id_message,))
                rows_deleted = cursor.rowcount
        # Retourne True si au moins une ligne a été supprimée
        return rows_deleted > 0

    def get_message_by_id(self, id_message: int) -> Optional[Message]:
        """Récupérer un message par son id

        Parameters
        ----------
        id_message : int
            L'identifiant du message

        Returns
        -------
        Optional[Message]
            Un objet Message s'il existe, None sinon
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                query = """
                    SELECT id_message, id_chat, date_sending, role_author, content
                    FROM message
                    WHERE id_message = %s
                """
                cursor.execute(query, (id_message,))
                res = cursor.fetchone()

        if res:
            return Message(
                id_message=res[0],
                id_chat=res[1],
                date_sending=res[2],
                role_author=res[3],
                content=res[4]
            )
        return None

    def get_messages_by_chat(self, id_chat: int) -> List[Message]:
        """Récupérer tous les messages d'une conversation donnée

        Parameters
        ----------
        id_chat : int
            L'identifiant du chat dont on veut les messages

        Returns
        -------
        List[Message]
            La liste des messages appartenant à ce chat par ordre de date croissante
            Liste vide si aucun message trouvé
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                query = """
                    SELECT id_message, id_chat, date_sending, role_author, content
                    FROM message
                    WHERE id_chat = %s
                    ORDER BY date_sending ASC;
                """
                cursor.execute(query, (id_chat,))
                res = cursor.fetchall()

        messages = [
            Message(
                id_message=row[0],
                id_chat=row[1],
                date_sending=row[2],
                role_author=row[3],
                content=row[4]
            )
            for row in res
        ]

        return messages
