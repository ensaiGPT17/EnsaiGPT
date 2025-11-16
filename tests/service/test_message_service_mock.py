from unittest.mock import MagicMock
from datetime import datetime

from service.message_service import MessageService
from dao.message_dao import MessageDAO
from model.message import Message
from service.response_service import ResponseService

# Liste de messages fictifs pour les tests
liste_messages = [
    Message(id_message=1, id_chat=1, date_sending=datetime(2025, 1, 1, 10, 0), role_author="user", content="Salut"),
    Message(id_message=2, id_chat=1, date_sending=datetime(2025, 1, 1, 10, 1), role_author="bot", content="Hello"),
    Message(id_message=3, id_chat=1, date_sending=datetime(2025, 1, 1, 10, 2), role_author="user", content="Comment ça va ?"),
]


def test_get_message_by_id_found():
    """Message trouvé"""
    # GIVEN
    MessageDAO.get_message_by_id = MagicMock(return_value=liste_messages[0])
    service = MessageService(MessageDAO())

    # WHEN
    msg = service.get_message_by_id(1)

    # THEN
    assert msg.id_message == 1
    assert msg.content == "Salut"

def test_get_message_by_id_not_found():
    """Message non trouvé"""
    # GIVEN
    MessageDAO.get_message_by_id = MagicMock(return_value=None)
    service = MessageService(MessageDAO())

    # WHEN
    msg = service.get_message_by_id(999)

    # THEN
    assert msg is None

def test_get_messages_by_chat_sorted():
    """Récupération des messages triés par date"""
    # GIVEN
    # on donne une liste dans le désordre
    messages_unsorted = [liste_messages[2], liste_messages[0], liste_messages[1]]
    MessageDAO.get_messages_by_chat = MagicMock(return_value=messages_unsorted)
    service = MessageService(MessageDAO())

    # WHEN
    msgs = service.get_messages_by_chat(1)

    # THEN
    assert msgs[0].id_message == 1
    assert msgs[1].id_message == 2
    assert msgs[2].id_message == 3

def test_get_messages_by_chat_none():
    """Pas de messages pour ce chat"""
    # GIVEN
    MessageDAO.get_messages_by_chat = MagicMock(return_value=None)
    service = MessageService(MessageDAO())

    # WHEN
    msgs = service.get_messages_by_chat(999)

    # THEN
    assert msgs is None

def test_create_message_success():
    """Création réussie"""
    # GIVEN
    new_msg = Message(-1, 1, datetime.now(), "user", "Nouveau message")
    MessageDAO.insert = MagicMock(return_value=Message(10, 1, new_msg.date_sending, "user", "Nouveau message"))
    service = MessageService(MessageDAO())

    # WHEN
    resp, msg = service.create_message(1, new_msg.date_sending, "user", "Nouveau message")

    # THEN
    assert isinstance(resp, ResponseService)
    assert resp.code == 201
    assert msg.id_message == 10

def test_create_message_fail():
    """Échec de création"""
    # GIVEN
    MessageDAO.insert = MagicMock(return_value=None)
    service = MessageService(MessageDAO())

    # WHEN
    resp, msg = service.create_message(1, datetime.now(), "user", "Message impossible")

    # THEN
    assert resp.code == 500
    assert msg is None

def test_delete_message_success():
    """Suppression réussie"""
    # GIVEN
    MessageDAO.delete = MagicMock(return_value=True)
    service = MessageService(MessageDAO())

    # WHEN
    resp = service.delete_message(1)

    # THEN
    assert resp.code == 200

def test_delete_message_fail():
    """Échec de suppression"""
    # GIVEN
    MessageDAO.delete = MagicMock(return_value=False)
    service = MessageService(MessageDAO())

    # WHEN
    resp = service.delete_message(999)

    # THEN
    assert resp.code == 404

def test_title_request_returns_message():
    """Vérifie que title_request retourne un Message"""
    # GIVEN
    service = MessageService(MessageDAO())

    # WHEN
    msg = service.title_request()

    # THEN
    assert isinstance(msg, Message)
    assert msg.role_author == "tool"
    assert "titre" in msg.content.lower()
