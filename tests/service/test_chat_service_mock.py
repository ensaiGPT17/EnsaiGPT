from unittest.mock import MagicMock
from datetime import datetime

from service.chat_service import ChatService
from dao.chat_dao import ChatDAO
from dao.message_dao import MessageDAO
from model.chat import Chat
from model.message import Message
from service.response_service import ResponseService

# Liste de chats fictifs
liste_chats = [
    Chat(id_chat=1, id_user=1, title="Chat1", date_start=datetime(2025,1,1,10,0), last_date=datetime(2025,1,1,10,0), max_tokens=512, top_p=1.0, temperature=0.7),
    Chat(id_chat=2, id_user=1, title="Chat2", date_start=datetime(2025,1,2,10,0), last_date=datetime(2025,1,2,10,0), max_tokens=512, top_p=1.0, temperature=0.7),
]

# =============================
# Tests unitaires ChatService
# =============================

def test_get_chat_found():
    """Chat trouvé"""
    # GIVEN
    ChatDAO.get_chat = MagicMock(return_value=liste_chats[0])
    service = ChatService(ChatDAO())

    # WHEN
    chat = service.get_chat(1)

    # THEN
    assert chat.id_chat == 1
    assert chat.title == "Chat1"

def test_get_chat_not_found():
    """Chat non trouvé"""
    # GIVEN
    ChatDAO.get_chat = MagicMock(return_value=None)
    service = ChatService(ChatDAO())

    # WHEN
    chat = service.get_chat(999)

    # THEN
    assert chat is None

def test_get_chats_by_id_user_sorted():
    """Récupération des chats triés par last_date"""
    # GIVEN
    ChatDAO.list_chats_id_user = MagicMock(return_value=liste_chats[::-1])  # ordre inversé
    service = ChatService(ChatDAO())

    # WHEN
    chats = service.get_chats_by_id_user(1)

    # THEN
    assert chats[0].id_chat == 2
    assert chats[1].id_chat == 1

def test_get_chats_by_id_user_none():
    """Pas de chats pour cet utilisateur"""
    # GIVEN
    ChatDAO.list_chats_id_user = MagicMock(return_value=None)
    service = ChatService(ChatDAO())

    # WHEN
    chats = service.get_chats_by_id_user(999)

    # THEN
    assert chats is None

def test_create_chat_success():
    """Création de chat réussie"""
    # GIVEN
    chat_inserted = Chat(id_chat=10, id_user=1, title="Nouvelle conversation",
                         date_start=datetime.now(), last_date=datetime.now(),
                         max_tokens=512, top_p=1.0, temperature=0.7)
    ChatDAO.insert = MagicMock(return_value=chat_inserted)
    ChatDAO.update = MagicMock(return_value=chat_inserted)
    
    MessageDAO.create_message = MagicMock(return_value=(None, Message(1,10,datetime.now(),"user","msg")))
    MessageDAO.get_messages_by_chat = MagicMock(return_value=[Message(1,10,datetime.now(),"user","msg")])
    
    client_mock = MagicMock()
    client_mock.generate = MagicMock(return_value="Assistant response")
    
    service = ChatService(ChatDAO())
    service.client = client_mock
    service.message_service = MagicMock()
    service.message_service.create_message = MagicMock(side_effect=[(None, Message(1,10,datetime.now(),"system","sys")),
                                                                   (None, Message(2,10,datetime.now(),"user","first")),
                                                                   (None, Message(3,10,datetime.now(),"assistant","resp"))])
    service.message_service.get_messages_by_chat = MagicMock(return_value=[Message(2,10,datetime.now(),"user","first")])
    service.get_chat = MagicMock(return_value=chat_inserted)
    service.request_title = MagicMock(return_value="Titre généré")

    # WHEN
    chat = service.create_chat("Bonjour", 1)

    # THEN
    assert chat.id_chat == 10
    assert chat.title == "Titre généré"

def test_send_message_appends_history():
    """Envoi d'un message et réception assistant"""
    # GIVEN
    chat = Chat(id_chat=1, id_user=1, title="Chat1",
                date_start=datetime.now(), last_date=datetime.now(),
                max_tokens=512, top_p=1.0, temperature=0.7)
    history = []

    service = ChatService(ChatDAO())
    service.message_service = MagicMock()
    service.message_service.create_message = MagicMock(side_effect=[
        (None, Message(1,1,datetime.now(),"user","msg")),
        (None, Message(2,1,datetime.now(),"assistant","resp"))
    ])
    service.client = MagicMock()
    service.client.generate = MagicMock(return_value="resp")
    service.chat_dao.update = MagicMock()

    # WHEN
    new_history = service.send_message(chat, history, "msg")

    # THEN
    assert len(new_history) == 2
    assert new_history[0].role_author == "user"
    assert new_history[1].role_author == "assistant"

def test_delete_chat_success():
    """Suppression de chat réussie"""
    # GIVEN
    ChatDAO.delete = MagicMock(return_value=True)
    service = ChatService(ChatDAO())

    # WHEN
    resp = service.delete_chat(1)

    # THEN
    assert resp.code == 200

def test_delete_chat_fail():
    """Échec suppression de chat"""
    # GIVEN
    ChatDAO.delete = MagicMock(return_value=False)
    service = ChatService(ChatDAO())

    # WHEN
    resp = service.delete_chat(999)

    # THEN
    assert resp.code == 500
