import pytest
from unittest.mock import MagicMock
from datetime import datetime
from model.chat import Chat
from model.message import Message
from model.user import User
from service.chat_service import ChatService
from service.response_service import ResponseService


# -----------------------------
# FIXTURE CHAT SERVICE MOCK
# -----------------------------
@pytest.fixture
def chat_service_mock():
    dao = MagicMock()
    dao.get_chat = MagicMock()
    dao.insert = MagicMock()
    dao.update = MagicMock()
    dao.delete = MagicMock()
    dao.list_chats_id_user = MagicMock()
    dao.delete_all_chats = MagicMock()
    dao.search_by_date = MagicMock()

    service = ChatService(chat_dao=dao)

    # MessageService mocké
    service.message_service = MagicMock()
    service.message_service.create_message.return_value = (
        ResponseService(201, "Message créé avec succès"),
        Message(1, 1, datetime.now(), "user", "test")
    )
    service.message_service.get_messages_by_chat.return_value = []
    service.message_service.title_request.return_value = "Titre de test"

    # Client EnsaiGPT mocké
    service.client.generate = MagicMock(return_value="Titre simulé")

    return service


# -----------------------------
# TEST CREATION DE CHAT
# -----------------------------
def test_create_chat_success(chat_service_mock):
    # GIVEN : message initial et user
    first_msg = "Bonjour, test"
    id_user = 1

    # Mock insert pour renvoyer un Chat avec id_chat simulé
    inserted_chat = Chat(
        id_chat=1, id_user=id_user, title="Nouvelle conversation",
        date_start=datetime.now(), last_date=datetime.now(),
        max_tokens=512, top_p=1.0, temperature=0.7
    )
    chat_service_mock.chat_dao.insert.return_value = inserted_chat

    # Mock update pour renvoyer le chat final (même id)
    chat_service_mock.chat_dao.update.return_value = inserted_chat

    # Mock request_title pour éviter l'appel réel
    chat_service_mock.request_title = MagicMock(return_value="Titre simulé")

    # WHEN : création du chat
    chat = chat_service_mock.create_chat(first_msg, id_user)

    # THEN : vérifications
    assert chat.id_chat == 1
    assert chat.title == "Titre simulé"
    chat_service_mock.chat_dao.insert.assert_called_once()
    chat_service_mock.chat_dao.update.assert_called_once()
    # Vérifie que 3 messages ont été créés : system, user, assistant
    assert chat_service_mock.message_service.create_message.call_count == 3 

# -----------------------------
# TEST SUPPRESSION DE CHAT
# -----------------------------
def test_delete_chat_success(chat_service_mock):
    # GIVEN : un chat à supprimer
    chat_service_mock.chat_dao.delete.return_value = True
    id_chat = 1

    # WHEN : suppression
    response = chat_service_mock.delete_chat(id_chat)

    # THEN : vérification
    assert response.code == 200
    assert "supression conversation reussie" in response.content
    chat_service_mock.chat_dao.delete.assert_called_once_with(id_chat)

def test_delete_chat_failure(chat_service_mock):
    # GIVEN : chat inexistant ou échec suppression
    chat_service_mock.chat_dao.delete.return_value = False
    id_chat = 999

    # WHEN : suppression
    response = chat_service_mock.delete_chat(id_chat)

    # THEN : vérification
    assert response.code == 500
    assert "echec suppression conversation" in response.content
    chat_service_mock.chat_dao.delete.assert_called_once_with(id_chat)


# -----------------------------
# TESTS GET_CHATS_BY_ID_USER
# -----------------------------
def test_get_chats_by_id_user(chat_service_mock):
    user_id = 1
    chat1 = Chat(1, user_id, "Chat1", datetime(2025,1,1), datetime(2025,1,2), 512, 1.0, 0.7)
    chat2 = Chat(2, user_id, "Chat2", datetime(2025,1,3), datetime(2025,1,4), 512, 1.0, 0.7)
    chat_service_mock.chat_dao.list_chats_id_user.return_value = [chat1, chat2]

    chats = chat_service_mock.get_chats_by_id_user(user_id)
    assert chats[0].id_chat == 2  # Trié par last_date décroissant
    assert chats[1].id_chat == 1
    chat_service_mock.chat_dao.list_chats_id_user.assert_called_once_with(user_id)

# -----------------------------
# TEST REQUEST_TITLE
# -----------------------------
def test_request_title(chat_service_mock):
    chat_id = 1
    chat_service_mock.get_chat = MagicMock(return_value=Chat(chat_id, 1, "Old title",
                                                             datetime.now(), datetime.now(), 512,1.0,0.7))
    title = chat_service_mock.request_title(chat_id)
    assert title == "Titre simulé"
    chat_service_mock.client.generate.assert_called_once()

# -----------------------------
# TEST SEND_MESSAGE
# -----------------------------
def test_send_message(chat_service_mock):
    chat = Chat(1, 1, "Chat test", datetime.now(), datetime.now(), 512,1.0,0.7)
    history = []

    updated_history = chat_service_mock.send_message(chat, history, "Bonjour")
    # 2 messages créés : user + assistant
    assert len(updated_history) == 2
    chat_service_mock.message_service.create_message.assert_called()
    chat_service_mock.chat_dao.update.assert_called_once()

# -----------------------------
# TEST SEARCH_CHAT_BY_TITLE
# -----------------------------
def test_search_chat_by_title(chat_service_mock):
    user_id = 1
    chat1 = Chat(1, user_id, "Hello World", datetime.now(), datetime.now(), 512,1.0,0.7)
    chat2 = Chat(2, user_id, "Test Chat", datetime.now(), datetime.now(), 512,1.0,0.7)
    chat_service_mock.chat_dao.list_chats_id_user.return_value = [chat1, chat2]

    results = chat_service_mock.search_chat_by_title(user_id, "Hello")
    assert results[0].id_chat == 1

# -----------------------------
# TEST SEARCH_CHAT_BY_DATE
# -----------------------------
def test_search_chat_by_date(chat_service_mock):
    user_id = 1
    search_date = "2025-01-01"
    chat1 = Chat(1, user_id, "Chat1", datetime(2025,1,1), datetime(2025,1,1), 512,1.0,0.7)
    chat_service_mock.chat_dao.search_by_date.return_value = [chat1]

    results = chat_service_mock.search_chat_by_date(user_id, search_date)
    assert len(results) == 1
    assert results[0].id_chat == 1

# -----------------------------
# TEST DELETE_ALL_CHATS
# -----------------------------
def test_delete_all_chats_success(chat_service_mock):
    chat_service_mock.chat_dao.delete_all_chats.return_value = True
    response = chat_service_mock.delete_all_chats(1)
    assert response.code == 200

def test_delete_all_chats_failure(chat_service_mock):
    chat_service_mock.chat_dao.delete_all_chats.return_value = False
    response = chat_service_mock.delete_all_chats(1)
    assert response.code == 500

# -----------------------------
# TEST GET_USER_STATISTICS
# -----------------------------
def test_get_user_statistics(chat_service_mock):
    user_id = 1
    chat1 = Chat(1, user_id, "Chat1", datetime(2025,1,1), datetime(2025,1,2), 512,1.0,0.7)
    chat2 = Chat(2, user_id, "Chat2", datetime(2025,1,3), datetime(2025,1,4), 512,1.0,0.7)
    chat_service_mock.get_chats_by_id_user = MagicMock(return_value=[chat1, chat2])
    chat_service_mock.counts_user_message = MagicMock(return_value=4)

    stats = chat_service_mock.get_user_statistics(user_id)
    assert stats["nb_conversations"] == 2
    assert stats["nb_messages"] == 3
    assert stats["avg_messages_per_chat"] == 1.5

if __name__ == "__main__":
    pytest.main([__file__])