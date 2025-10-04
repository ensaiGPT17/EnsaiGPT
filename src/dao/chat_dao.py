from typing import Optional
from model.chat import Chat
from datetime import datetime


class ChatDAO:
    def __init__(self):
        pass

    def get_chat(self, id_chat) -> Optional[Chat]:
        pass

    def insert(self, chat: Chat) -> Optional[Chat]:
        pass

    def delete(self, id_chat: int) -> bool:
        pass

    def update(self, id_chat: int, chat_updated: Chat) -> Optional[Chat]:
        pass

    def get_all(self):
        pass

    def get_max_id(self) -> int:
        pass

    def list_chat_user(self, id_user):
        pass

    def count_chats(self) -> int:
        pass

    def search_by_title(self, id_user: int ,search_title: str):
        pass

    def search_by_date(self, id_user: int, date: datetime):
        pass
