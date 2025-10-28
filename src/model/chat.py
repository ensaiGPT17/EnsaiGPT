from datetime import datetime
from typing import Optional


class Chat:
    def __init__(self,
                 id_chat: Optional[int],
                 id_user: int,
                 title: str,
                 created_at: Optional[datetime] = None,
                 updated_at: Optional[datetime] = None):
        self.id_chat = id_chat
        self.id_user = id_user
        self.title = title
        self.created_at = created_at
        self.updated_at = updated_at
