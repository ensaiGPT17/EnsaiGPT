import pytest
from unittest.mock import MagicMock
from datetime import datetime
from model.message import Message
from service.message_service import MessageService
from service.response_service import ResponseService

@pytest.fixture
def message_service_mock():
    """
    Service MessageService avec DAO mocké pour tests unitaires.
    Toutes les méthodes DAO sont remplacées par des MagicMock().
    """
    dao = MagicMock()
    dao.insert = MagicMock()              # insert message
    dao.delete = MagicMock()              # delete message
    dao.get_message_by_id = MagicMock()   # get by id
    dao.get_messages_by_chat = MagicMock()# get messages by chat
    return MessageService(dao)

# -----------------------------
# CREATE MESSAGE
# -----------------------------
def test_create_message_success(message_service_mock):
    # GIVEN : message valide
    id_chat = 1
    date_sending = datetime.now()
    role_author = "user"
    content = "Bonjour, test MagicMock"
    
    # setup du mock : insert retourne un Message avec id_message simulé
    message_service_mock.message_dao.insert.return_value = Message(1, id_chat, date_sending, role_author, content)

    # WHEN : création du message
    resp, msg = message_service_mock.create_message(id_chat, date_sending, role_author, content)

    # THEN : vérification réponse
    assert resp.code == 201
    assert "Message créé avec succès" in resp.content
    assert msg.id_message == 1
    message_service_mock.message_dao.insert.assert_called_once()  # vérifie appel DAO

def test_create_message_failure(message_service_mock):
    # GIVEN : insert retourne None (échec DAO)
    message_service_mock.message_dao.insert.return_value = None

    # WHEN
    resp, msg = message_service_mock.create_message(1, datetime.now(), "user", "Fail message")

    # THEN
    assert resp.code == 500
    assert "Erreur interne" in resp.content
    assert msg is None

# -----------------------------
# DELETE MESSAGE
# -----------------------------
def test_delete_message_success(message_service_mock):
    # GIVEN : delete retourne True
    message_service_mock.message_dao.delete.return_value = True

    # WHEN
    resp = message_service_mock.delete_message(1)

    # THEN
    assert resp.code == 200
    assert "supprimé avec succès" in resp.content
    message_service_mock.message_dao.delete.assert_called_once_with(1)

def test_delete_message_not_found(message_service_mock):
    # GIVEN : delete retourne False
    message_service_mock.message_dao.delete.return_value = False

    # WHEN
    resp = message_service_mock.delete_message(999)

    # THEN
    assert resp.code == 404
    assert "introuvable" in resp.content

# -----------------------------
# GET MESSAGE BY ID
# -----------------------------
def test_get_message_by_id_found(message_service_mock):
    # GIVEN : DAO retourne un message
    message = Message(1, 1, datetime.now(), "user", "Test")
    message_service_mock.message_dao.get_message_by_id.return_value = message

    # WHEN
    fetched = message_service_mock.get_message_by_id(1)

    # THEN
    assert fetched is message

def test_get_message_by_id_not_found(message_service_mock):
    # GIVEN : DAO retourne None
    message_service_mock.message_dao.get_message_by_id.return_value = None

    # WHEN
    fetched = message_service_mock.get_message_by_id(999)

    # THEN
    assert fetched is None

# -----------------------------
# GET MESSAGES BY CHAT
# -----------------------------
def test_get_messages_by_chat_sorted(message_service_mock):
    # GIVEN : messages non triés
    msg1 = Message(1, 1, datetime(2025,1,1,12,0), "user", "A")
    msg2 = Message(2, 1, datetime(2025,1,1,11,0), "assistant", "B")
    message_service_mock.message_dao.get_messages_by_chat.return_value = [msg1, msg2]

    # WHEN
    messages = message_service_mock.get_messages_by_chat(1)

    # THEN : doivent être triés par date_sending
    assert messages[0] == msg2
    assert messages[1] == msg1


if __name__ == "__main__":
    pytest.main([__file__])
