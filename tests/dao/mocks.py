from typing import Optional, List
from model.user import User
from dao.user_dao import UserDAO
from model.message import Message
from dao.message_dao import MessageDAO
from datetime import datetime


class UserDAOMock(UserDAO):
    def __init__(self):
        super().__init__()
        self.users: list[User] = []  #simule la base SQL des utilisateurs

    def clear_all(self):
        self.users.clear()

    def get_user(self, id_user) -> Optional[User]:
        for user in self.users:
            if user.id_user == id_user:
                return user
        return None

    def get_user_by_username(self, username) -> Optional[User]:
        """Permet d'avoir l'utilisateur grâce à son nom d'utilisateur"""
        for user in self.users:
            if user.username == username:
                return user
        return None

    def insert(self, user: User) -> Optional[User]:
        new_id = self.get_max_id() + 1
        user.id_user = new_id
        self.users.append(user)
        return user

    def delete(self, id_user: int) -> bool:
        """Supprime un utilisateur de la bdd."""
        for i in range(len(self.users)):
            if self.users[i].id_user == id_user:
                del self.users[i]
                return True
        return False

    def update(self, id_user: int, user_updated: User) -> Optional[User]:
        """Modifie un utilisateur de la bdd."""
        for i in range(len(self.users)):
            if self.users[i].id_user == id_user:
                user_updated.id_user = id_user
                self.users[i] = user_updated
                return user_updated
        return None

    def get_all(self):
        """Renvoie la liste des utilisateurs."""
        return self.users

    def username_exists(self, username: str) -> bool:
        """Permet de savoir si un certain nom d'utilisateur existe dans la base."""
        for user in self.users:
            if username == user.username:
                return True
        return False

    def get_max_id(self) -> int:
        """
        Donne le plus grand id associé à un utilisateur.
        Retourne 0 si aucun utilisateur n'existe.
        """
        if len(self.users) == 0:
            return 0
        return max(user.id_user for user in self.users)

    def count_users(self) -> int:
        """Renvoie le nombre d'utilisateurs dans la base de données."""
        return len(self.users)


class MessageDAOMock(MessageDAO):
    def __init__(self):
        super().__init__()
        self.messages: List[Message] = []  # simule la table messages

    def clear_all(self):
        self.messages.clear()

    def get_message_by_id(self, id_message: int) -> Optional[Message]:
        for msg in self.messages:
            if msg.id_message == id_message:
                return msg
        return None

    def get_messages_by_chat(self, id_chat: int) -> List[Message]:
        return [msg for msg in self.messages if msg.id_chat == id_chat]

    def create_message(self, id_chat: int, date_sending: datetime, role_author: str, content: str) -> Optional[Message]:
        new_id = self.get_max_id() + 1
        msg = Message(new_id, id_chat, date_sending, role_author, content)
        self.messages.append(msg)
        return msg

    def delete_message(self, id_message: int) -> bool:
        for i, msg in enumerate(self.messages):
            if msg.id_message == id_message:
                del self.messages[i]
                return True
        return False

    def get_max_id(self) -> int:
        if not self.messages:
            return 0
        return max(msg.id_message for msg in self.messages)