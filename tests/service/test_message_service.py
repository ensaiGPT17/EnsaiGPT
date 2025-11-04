import pytest
from datetime import datetime
from service.message_service import MessageService
from service.response_service import ResponseService
from tests.test_dao.mocks import MessageDAOMock  


@pytest.fixture
def message_service():
    dao = MessageDAOMock()
    dao.clear_all() 
    return MessageService(dao)


def test_create_message_success(message_service):
    # GIVEN
    id_chat = 1
    date_sending = datetime.now()
    role_author = "user"
    content = "Bonjour, ceci est un test"

    # WHEN
    resp = message_service.create_message(id_chat, date_sending, role_author, content)

    # THEN
    assert resp.code == 201
    assert "Message créé avec succès" in resp.content
    # vérifier qu'on peut récupérer le message via le DAO
    messages = message_service.get_messages_by_chat(id_chat)
    assert len(messages) == 1
    assert messages[0].content == content


def test_get_message_by_id_found(message_service):
    # GIVEN
    msg = message_service.message_dao.create_message(1, datetime.now(), "user", "Test message")

    # WHEN
    fetched = message_service.get_message_by_id(msg.id_message)

    # THEN
    assert fetched is not None
    assert fetched.id_message == msg.id_message


def test_get_message_by_id_not_found(message_service):
    # WHEN
    fetched = message_service.get_message_by_id(999)

    # THEN
    assert fetched is None


def test_get_messages_by_chat(message_service):
    # GIVEN
    dao = message_service.message_dao
    dao.create_message(1, datetime.now(), "user", "Message 1")
    dao.create_message(1, datetime.now(), "assistant", "Message 2")
    dao.create_message(2, datetime.now(), "user", "Message 3")

    # WHEN
    messages_chat1 = message_service.get_messages_by_chat(1)
    messages_chat2 = message_service.get_messages_by_chat(2)

    # THEN
    assert len(messages_chat1) == 2
    assert len(messages_chat2) == 1


def test_delete_message_success(message_service):
    # GIVEN
    msg = message_service.message_dao.create_message(1, datetime.now(), "user", "Message à supprimer")

    # WHEN
    resp = message_service.delete_message(msg.id_message)

    # THEN
    assert resp.code == 200
    assert "supprimé avec succès" in resp.content
    assert message_service.get_message_by_id(msg.id_message) is None


def test_delete_message_not_found(message_service):
    # WHEN
    resp = message_service.delete_message(999)

    # THEN
    assert resp.code == 404
    assert "introuvable" in resp.content
