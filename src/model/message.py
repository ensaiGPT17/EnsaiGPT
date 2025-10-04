from datetime import datetime


class Message:
    def __init__(self, id_message: int, id_chat: int, date: datetime, role,
                 content: str):
        self.id_message = id_message
        self.id_chat = id_chat
        self.date = date
        self.role = role
        self.content = content
