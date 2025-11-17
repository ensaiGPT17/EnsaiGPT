import pytest
from datetime import datetime
from utils.reset_database import ResetDatabase
from dao.chat_dao import ChatDAO
from service.chat_service import ChatService
from service.response_service import ResponseService
from model.chat import Chat
from unittest.mock import patch

@pytest.fixture
def chat_service():
    """Réinitialise la base et fournit une instance de ChatService"""
    ResetDatabase().lancer()
    return ChatService(ChatDAO())

# ----------------------
# Tests CRUD de ChatService
# ----------------------

def test_create_chat(chat_service):
    """Test de la création d'un chat"""
    chat = chat_service.create_chat("Bonjour", 1)
    assert chat is not None
    assert chat.id_chat is not None
    assert chat.title != ""


def test_get_chat_found(chat_service):
    """Récupération d'un chat existant"""
    chat = chat_service.create_chat("Salut", 1)
    fetched = chat_service.get_chat(chat.id_chat)
    assert fetched is not None
    assert fetched.id_chat == chat.id_chat


def test_get_chat_not_found(chat_service):
    """Récupération d'un chat inexistant"""
    fetched = chat_service.get_chat(9999)
    assert fetched is None


def test_get_chats_by_id_user(chat_service):
    """Récupération de tous les chats d'un utilisateur"""
    user_id = 1
    chat_service.create_chat("Chat A", user_id)
    chat_service.create_chat("Chat B", user_id)
    chats = chat_service.get_chats_by_id_user(user_id)
    assert chats is not None
    assert len(chats) >= 2
    assert all(c.id_user == user_id for c in chats)


def test_delete_chat(chat_service):
    """Suppression d'un chat"""
    chat = chat_service.create_chat("Chat à supprimer", 1)
    response = chat_service.delete_chat(chat.id_chat)
    assert response.code == 200
    assert chat_service.get_chat(chat.id_chat) is None


# ----------------------
# Test delete_all_chats
# ----------------------

def test_delete_all_chats(chat_service):
    """Suppression de tous les chats d'un utilisateur"""
    user_id = 1
    chat_service.create_chat("Chat 1", user_id)
    chat_service.create_chat("Chat 2", user_id)

    # Vérifie qu'il y a bien des chats avant suppression
    chats_before = chat_service.get_chats_by_id_user(user_id)
    assert chats_before is not None
    assert len(chats_before) >= 2

    # Suppression
    response: ResponseService = chat_service.delete_all_chats(user_id)
    assert response.code == 200
    assert "Suppression de liste de conversations réussie" in response.content
    chats_after = chat_service.get_chats_by_id_user(user_id)
    assert chats_after is None or len(chats_after) == 0


# ----------------------
# Tests recherche
# ----------------------
def test_search_chat_by_title_found(chat_service):
    user_id = 1
    # On force le titre généré pour qu'il soit prévisible
    with patch.object(chat_service.client, 'generate', return_value="GPT Test"):
        chat_service.create_chat("GPT Test", user_id)
        chat_service.create_chat("Conversation normale", user_id)

    results = chat_service.search_chat_by_title(user_id, "gpt")
    assert results is not None
    assert len(results) >= 1
    assert any("GPT" in chat.title for chat in results)

def test_search_chat_by_title_not_found(chat_service):
    """Recherche par titre inexistante"""
    user_id = 1
    chat_service.create_chat("Chat classique", user_id)
    results = chat_service.search_chat_by_title(user_id, "inexistant")
    assert results == []


def test_search_chat_by_date_found(chat_service):
    """Recherche par date existante"""
    user_id = 1
    today = datetime.today().strftime("%Y-%m-%d")
    chat_service.create_chat("Chat d'aujourd'hui", user_id)
    results = chat_service.search_chat_by_date(user_id, today)
    assert results is not None
    assert len(results) >= 1


def test_search_chat_by_date_not_found(chat_service):
    """Recherche par date inexistante"""
    user_id = 1
    results = chat_service.search_chat_by_date(user_id, "2000-01-01")
    assert results == []

if __name__ == "__main__":
    pytest.main([__file__])