import pytest
from datetime import datetime
from service.message_service import MessageService
from service.response_service import ResponseService
from tests.test_dao.mocks import MessageDAOMock
from utils.reset_database import ResetDatabase
from dao.message_dao import MessageDAO

#  /!\ les tests ne sont pas censés utiliser les méthodes de la dao  /!\

@pytest.fixture
def message_service_mock():
    """
    Pour les tests unitaires.
    """
    dao = MessageDAOMock()
    dao.clear_all() 
    return MessageService(dao)


@pytest.fixture
def user_service_real():
    """
    Pour les tests d integration.
    """
    ResetDatabase().lancer()
    dao = MessageDAO()
    return MessageService(dao)


def test_create_message_success(message_service_mock):
    # GIVEN
    id_chat = 1
    date_sending = datetime.now()
    role_author = "user"
    content = "Bonjour, ceci est un test"

    # WHEN
    resp, message = message_service_mock.create_message(id_chat, date_sending, role_author, content)
    print(f"Response code: {resp.code}")
    print(f"Response content: {resp.content}")
    # THEN
    assert resp.code == 201
    assert "Message créé avec succès" in resp.content
    # vérifier qu'on peut récupérer le message via le DAO
    messages = message_service_mock.get_messages_by_chat(id_chat)
    print(f"Messages for chat {id_chat}: {messages}")
    assert len(messages) == 1
    assert messages[0].content == content


def test_get_message_by_id_found(message_service_mock):
    # GIVEN
    msg = message_service_mock.message_dao.create_message(1, datetime.now(), "user", "Test message")

    # WHEN
    fetched = message_service_mock.get_message_by_id(msg.id_message)

    # THEN
    assert fetched is not None
    assert fetched.id_message == msg.id_message


def test_get_message_by_id_not_found(message_service_mock):
    # WHEN
    fetched = message_service_mock.get_message_by_id(999)

    # THEN
    assert fetched is None


def test_get_messages_by_chat(message_service_mock):
    # GIVEN
    #  /!\ test mal conçu /!\
    dao = message_service_mock.message_dao
    dao.create_message(1, datetime.now(), "user", "Message 1")
    dao.create_message(1, datetime.now(), "assistant", "Message 2")
    dao.create_message(2, datetime.now(), "user", "Message 3")

    # WHEN
    messages_chat1 = message_service_mock.get_messages_by_chat(1)
    messages_chat2 = message_service_mock.get_messages_by_chat(2)

    # THEN
    assert len(messages_chat1) == 2
    assert len(messages_chat2) == 1


def test_delete_message_success(message_service_mock):
    # GIVEN
    msg = message_service_mock.message_dao.create_message(1, datetime.now(), "user", "Message à supprimer")

    # WHEN
    resp = message_service_mock.delete_message(msg.id_message)

    # THEN
    assert resp.code == 200
    assert "supprimé avec succès" in resp.content
    assert message_service_mock.get_message_by_id(msg.id_message) is None


def test_delete_message_not_found(message_service_mock):
    # WHEN
    resp = message_service_mock.delete_message(999)

    # THEN
    assert resp.code == 404
    assert "introuvable" in resp.content
