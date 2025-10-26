from datetime import datetime


class Message:
    def __init__(self, id_message: int, id_chat: int, date_sending: datetime, role_author : str,
                 content: str):
        self.id_message = id_message
        self.id_chat = id_chat
        self.date_sending = date_sending
        self.role_author = role_author
        self.content = content
