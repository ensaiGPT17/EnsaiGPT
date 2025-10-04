from model.chat import Chat
from dao.chat_dao import ChatDAO


class ChatService:
    def __init__(self, chat_dao: ChatDAO):
        self.chat_dao = chat_dao
