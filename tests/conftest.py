import pytest
from dao.user_dao import UserDAO
from dao.chat_dao import ChatDAO
from dao.message_dao import MessageDAO

@pytest.fixture(autouse=True)
def reset_singleton():
    # Réinitialise tous les singletons DAO avant chaque test
    UserDAO._instances = {}
    ChatDAO._instances = {}
    MessageDAO._instances = {}
