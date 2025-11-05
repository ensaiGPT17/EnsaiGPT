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
        self.message_dao = message_dao

    @log
    def get_message_by_id(self, id_message: int) -> Optional[Message]:
        """recuperer un message par son id"""
        return self.message_dao.get_message_by_id(id_message)

    @log
    def get_messages_by_chat(self, id_chat: int) -> Optional[List[Message]]:
        """Retourne la liste triée des messages."""
        messages = self.message_dao.get_messages_by_chat(id_chat)
        if messages is None:
            return None
        messages.sort(key=lambda m: m.date_sending)
        return messages


    @log
    def create_message(self, id_chat: int, date_sending: datetime, role_author: str, content: str) -> ResponseService:
        """creer un nouveau message"""
        # appel messageDAO
        message = self.message_dao.insert(Message(-1, id_chat, date_sending, role_author, content))
        # si echec creation du message 
        if message is None:
            
            return ResponseService(*self.CREATION_ERROR)
        # si reussite 
        return ResponseService(self.CREATION_SUCCESS[0], f"{self.CREATION_SUCCESS[1]} (id={message.id_message})")

    @log
    def delete_message(self, id_message: int) -> ResponseService:
        """Supprime un message à partir de son ID."""
        # Appel messageDAO 
        deleted = self.message_dao.delete(id_message)
        # si erreur 
        if not deleted:
            return ResponseService(*self.DELETE_NOT_FOUND)
        # si suppression reussie 
        return ResponseService(*self.DELETE_SUCCESS)
