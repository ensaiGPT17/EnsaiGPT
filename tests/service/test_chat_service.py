import pytest
from utils.reset_database import ResetDatabase
from dao.chat_dao import ChatDAO
from service.chat_service import ChatService
from service.response_service import ResponseService
from typing import Optional
from model.chat import Chat

@pytest.fixture(scope="module")
def chat_service():
    """Réinitialise la base et fournit une instance de ChatService"""
    ResetDatabase().lancer()
    chat_dao = ChatDAO()
    return ChatService(chat_dao)

def get_chat(self, id_chat) -> Optional[Chat]:
    pass


if __name__ == "__main__":
    pytest.main([__file__])