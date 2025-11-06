from datetime import datetime
from typing import Optional

class Chat:
    def __init__(self, 
                id_chat: int,
                id_user: int,
                title: str,
                date_start: datetime,
                last_date: datetime,
                max_tokens: int,
                top_p: float,
                temperature: float):
        self.id_chat = id_chat
        self.id_user = id_user
        self.title = title
        self.date_start = date_start
        self.last_date = last_date
        self.max_tokens = max_tokens  # Assurez-vous qu'il s'agit d'un entier simple, pas un tuple.
        self.top_p = top_p  # Assurez-vous qu'il s'agit d'un float simple, pas un tuple.
        self.temperature = temperature
