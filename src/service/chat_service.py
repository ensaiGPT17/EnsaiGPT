from model.chat import Chat


class ChatService:
    def __init__(self, chat_dao: ChatDAO):
        self.chat_dao = chat_dao
