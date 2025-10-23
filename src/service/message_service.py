from model.message import Message
from dao.message_dao import MessageDAO
from service.response_service import ResponseService
from datetime import datetime
from typing import Optional


class MessageService:
    def __init__(self, message_dao: MessageDAO):
        self.message_dao = message_dao

    def create_message(self, id_chat: int, role: str, content: str) -> Optional[Message]:
        pass

    def delete_message(self, id_message: int) -> bool:
        pass
