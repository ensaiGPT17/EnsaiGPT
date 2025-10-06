from typing import Optional, List
from datetime import datetime
from model.message import Message
from dao.db_connection import DBConnection
from utils.singleton import Singleton


class MessageDAO(metaclass=Singleton):
    def __init__(self):
        pass

    def créer_message(self, id_chat: int, role: str, content: str) -> Optional[Message]:
        pass

    def supprimer_message(self, id_message: int) -> bool:
        pass