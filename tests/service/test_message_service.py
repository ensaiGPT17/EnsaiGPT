import pytest
from utils.reset_database import ResetDatabase
from dao.message_dao import MessageDAO
from service.message_service import MessageService
from service.response_service import ResponseService


@pytest.fixture(scope="module")
def message_service():
    """Réinitialise la base et fournit une instance de MessageService"""
    ResetDatabase().lancer()
    message_dao = MessageDAO()
    return MessageService(message_dao)


def  test_créer_message(self, id_chat: int, role: str, content: str):
        pass


if __name__ == "__main__":
    pytest.main([__file__])