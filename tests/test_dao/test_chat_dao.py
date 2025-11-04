import pytest
from dao.chat_dao import ChatDAO
from utils.reset_database import ResetDatabase
from model.chat import Chat
from datetime import date


@pytest.fixture(scope="module")
def chat_dao():
    """Réinitialise la base et fournit une instance de ChatDAO"""
    ResetDatabase().lancer()
    return ChatDAO()

def test_insert_chat(chat_dao):
    """Test l'insertion d'un nouveau chat"""
    pass

def test_get_chat(chat_dao):
    """Test la récupération d'un chat par son id"""
    pass

def test_update_chat(chat_dao):
    """Test la mise à jour d'un chat"""
    pass

def test_list_chats_id_user(chat_dao):
    """Test la récupération de tous les chats d'un utilisateur"""
    pass

def test_count_chats(chat_dao):
    """Test le comptage total des chats"""
    pass

def test_delete_chat(chat_dao):
    """Test la suppression d'un chat"""
    pass


if __name__ == "__main__":
    pytest.main([__file__])