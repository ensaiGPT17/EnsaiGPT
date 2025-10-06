from model.message import Message
from dao.message_dao import MessageDAO
from response_service import ResponseService
from datetime import datetime
from typing import Optional


class MessageService:
    def __init__(self, message_dao: MessageDAO):
        self.message_dao = message_dao

    def créer_message(self, id_chat: int, role: str, content: str) -> Optional[Message]:
        pass

    def supprimer_message(self, id_message: int) -> bool:
        pass