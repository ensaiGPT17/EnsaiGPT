from model.message import Message
from dao.message_dao import MessageDAO
from service.response_service import ResponseService
from datetime import datetime
from typing import Optional, List
from utils.log_decorator import log


class MessageService:
    CREATION_ERROR = (500, "Erreur interne lors de la création du message")
    CREATION_SUCCESS = (201, "Message créé avec succès")
    DELETE_SUCCESS = (200, "Message supprimé avec succès")
    DELETE_NOT_FOUND = (404, "Message introuvable ou non supprimé")

    def __init__(self, message_dao: MessageDAO):
        """
        Constructeur du service MessageService.

        Paramètres
        ----------
        message_dao : MessageDAO
            DAO permettant l'interaction avec la base de données pour les messages.
        """
        self.message_dao = message_dao

    @log
    def get_message_by_id(self, id_message: int) -> Optional[Message]:
        """
        Récupère un message à partir de son identifiant.

        Paramètres
        ----------
        id_message : int
            Identifiant du message recherché.

        Retour
        ------
        Optional[Message]
            Le message correspondant ou None s'il n'existe pas.
        """
        return self.message_dao.get_message_by_id(id_message)

    @log
    def get_messages_by_chat(self, id_chat: int) -> Optional[List[Message]]:
        """
        Récupère et retourne la liste des messages d'un chat, triée par date d’envoi.

        Paramètres
        ----------
        id_chat : int
            Identifiant du chat dont on veut récupérer les messages.

        Retour
        ------
        Optional[List[Message]]
            Liste triée des messages, ou None si le chat n'existe pas.
        """
        messages = self.message_dao.get_messages_by_chat(id_chat)
        if messages is None:
            return None
        messages.sort(key=lambda m: m.date_sending)
        return messages

    @log
    def create_message(self, id_chat: int, date_sending: datetime, role_author: str, content: str):
        """
        Crée un nouveau message pour un chat donné.

        Paramètres
        ----------
        id_chat : int
            Identifiant du chat auquel appartient le message.
        date_sending : datetime
            Date d’envoi du message.
        role_author : str
            Rôle de l’auteur (ex: "user", "assistant", "tool").
        content : str
            Contenu textuel du message.

        Retour
        ------
        Tuple[ResponseService, Optional[Message]]
            - Un objet ResponseService indiquant succès ou échec.
            - Le message créé, ou None si la création échoue.
        """
        # appel messageDAO
        message = self.message_dao.insert(Message(-1, id_chat, date_sending, role_author, content))
        # si echec creation du message 
        if message is None:

            return ResponseService(*self.CREATION_ERROR), message
        # si reussite 
        return ResponseService(self.CREATION_SUCCESS[0], f"{self.CREATION_SUCCESS[1]} (id={message.id_message})"), message

    @log
    def delete_message(self, id_message: int) -> ResponseService:
        """
        Supprime un message à partir de son identifiant.

        Paramètres
        ----------
        id_message : int
            Identifiant du message à supprimer.

        Retour
        ------
        ResponseService
            Un objet indiquant le résultat de l’opération.
        """
        # Appel messageDAO 
        deleted = self.message_dao.delete(id_message)
        # si erreur 
        if not deleted:
            return ResponseService(*self.DELETE_NOT_FOUND)
        # si suppression reussie 
        return ResponseService(*self.DELETE_SUCCESS)

    @log
    def title_request(self):
        """
        Génère un message interne (role 'tool') demandant un titre pour la conversation.

        Retour
        ------
        Message
            Un message spécial utilisé pour solliciter un titre auprès du modèle.
        """
        prompt = "Donne un titre en moins de 10 mots à cette conversation."
        return Message(id_message=-1, id_chat=-1, date_sending=datetime.now(),
                       role_author="tool", content=prompt)
