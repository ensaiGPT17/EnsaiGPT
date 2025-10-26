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
                    INSERT INTO ensaiGPT.messages (id_chat, date_sending, role_author, content)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id_message;
                """
                cursor.execute(query, (id_chat, date_sending, role_author, content))
                res = cursor.fetchone()

        print(res)
        # Construction de l’objet Message si insertion réussie
        if res:
            new_id = res['id_message']
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
                    DELETE FROM ensaiGPT.messages
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
                    FROM ensaiGPT.messages
                    WHERE id_message = %s
                """
                cursor.execute(query, (id_message,))
                res = cursor.fetchone()

        print(res)
        if res:
            return Message(
                id_message=res['id_message'],
                id_chat=res['id_chat'],
                date_sending=res['date_sending'],
                role_author=res['role_author'],
                content=res['content']
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
                    FROM ensaiGPT.messages
                    WHERE id_chat = %s
                    ORDER BY date_sending ASC;
                """
                cursor.execute(query, (id_chat,))
                res = cursor.fetchall()

        messages = [
            Message(
                
                id_message=row['id_message'],
                id_chat=row['id_chat'],
                date_sending=row['date_sending'],
                role_author=row['role_author'],
                content=row['content']

            )
            for row in res
        ]

        return messages


"""
if __name__ == "__main__":

    print("=== TEST DE LA CLASSE MessageDAO ===")
    message_dao = MessageDAO()

    # Variables de test
    id_chat_test = 2
    role_author_test = "assistant"
    content_test = "Bonjour, ceci est un message de test."
    content_update = "Message mis à jour."

    #  - Création d’un message
    print("\n--- Création d’un message ---")
    new_message = message_dao.create_message(
        id_chat=id_chat_test,
        date_sending=datetime.now(),
        role_author=role_author_test,
        content=content_test
    )
    if new_message:
        print(f"Message inséré avec succès : id={new_message.id_message}, contenu='{new_message.content}'")
    else:
        print("Échec de création du message")

    #  - Récupération par ID
    print("\n--- Récupération par ID ---")
    if new_message:
        fetched = message_dao.get_message_by_id(new_message.id_message)
        print(f"Message récupéré : {fetched.content if fetched else 'Aucun message trouvé'}")

    # 3 - Récupération par chat
    print("\n--- Liste des messages du chat ---")
    messages = message_dao.get_messages_by_chat(id_chat_test)
    if messages:
        for m in messages:
            print(f"[{m.date_sending}] {m.role_author} : {m.content}")
    else:
        print("Aucun message trouvé pour ce chat")


    # 4️⃣ - Suppression du message
    print("\n--- Suppression du message ---")
    if new_message:
        deleted = message_dao.delete_message(new_message.id_message-1)
        print("Message supprimé avec succès" if deleted else "Échec de suppression")


    #  - Vérification après suppression
    print("\n--- Vérification après suppression ---")
    if new_message:
        message_check = message_dao.get_message_by_id(new_message.id_message-1)
        print("Message encore présent" if message_check else "Message bien supprimé")
"""