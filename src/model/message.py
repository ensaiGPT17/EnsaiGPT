from datetime import datetime


class Message:
    """
    Classe représentant un message envoyé dans un chat.

    Attributs
    ---------
    id_message : int
        Identifiant unique du message.
    id_chat : int
        Identifiant du chat auquel appartient le message.
    date_sending : datetime
        Date et heure d'envoi du message.
    role_author : str
        Rôle de l'auteur du message (ex. : 'user', 'assistant').
    content : str
        Contenu textuel du message.
    """

    def __init__(self, id_message: int, id_chat: int, date_sending: datetime, role_author: str,
                 content: str):
        """
        Constructeur de la classe Message.

        Parameters
        ----------
        id_message : int
            Identifiant unique du message.
        id_chat : int
            Identifiant du chat auquel le message appartient.
        date_sending : datetime
            Date et heure d'envoi du message.
        role_author : str
            Rôle de l'auteur du message ('user', 'assistant', etc.).
        content : str
            Contenu textuel du message.
        """
        self.id_message = id_message
        self.id_chat = id_chat
        self.date_sending = date_sending
        self.role_author = role_author
        self.content = content
