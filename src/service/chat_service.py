from model.chat import Chat
from dao.chat_dao import ChatDAO
from service.response_service import ResponseService
from datetime import datetime
from typing import Optional


class ChatService:
    def __init__(self, chat_dao: ChatDAO):
        self.chat_dao = chat_dao

    def get_chat(self, id_chat) -> Optional[Chat]:
        pass

    def get_chats_by_id_user(self, id_user):
        pass

    def create_chat(self, id_user: int, max_tokens: int, top_p: float,
                    temperature: float) -> ResponseService:
        pass

    def request_title(self, id_chat) -> ResponseService:
        pass

    def update_parameters_chat(self, id_chat, context: str, max_tokens: int,
                               top_p: float, temperature: float) -> ResponseService:
        pass

    def update_chat(self, id_chat, updated_chat: Chat) -> ResponseService:
        pass

    def delete_chat(self, id_chat) -> ResponseService:
        pass

    def search_chat_by_tile(self, search: str):
        pass

    def search_chat_by_date(self, search: datetime):
        pass
