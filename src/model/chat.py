from datetime import datetime
from typing import Optional


class Chat:
    def __init__(self, 
                id_chat,
                id_user,
                title,date_start,
                last_date,
                max_tokens,
                top_p,
                temperature
                ):
                self.id_chat = id_chat,
                self.id_user = id_user,
                self.title = title
                self.date_start = date_start,
                self.last_date = last_date,
                self.max_tokens = max_tokens,
                self.top_p = top_p,
                self.temperature = temperature

