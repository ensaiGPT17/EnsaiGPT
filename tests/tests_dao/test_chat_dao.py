import pytest
from datetime import datetime, date

from dao.chat_dao import ChatDAO
from utils.reset_database import ResetDatabase
from model.chat import Chat


# --------------------------------------------------------
# Initialisation du schéma de test
# --------------------------------------------------------
@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Réinitialise la base en mode test avant toute la session de tests"""
    ResetDatabase().lancer(test_dao=True)
    yield


# --------------------------------------------------------
# Fixture DAO
# --------------------------------------------------------
@pytest.fixture
def chat_dao():
    """Retourne une instance propre de UserDAO"""
    return ChatDAO(schema="ensaiGPTTEST")

# -----------------------------------------------------
# GET CHAT
# -----------------------------------------------------

def test_get_chat_found(chat_dao):
    """Doit trouver un chat existant."""
    chat = chat_dao.get_chat(1)

    assert chat is not None
    # Certains drivers renvoient (1,) → on tolère
    assert chat.id_chat == 1 or chat.id_chat == (1,)


def test_get_chat_not_found(chat_dao):
    """Retourne None si le chat n'existe pas."""
    assert chat_dao.get_chat(9999) is None


# -----------------------------------------------------
# INSERT
# -----------------------------------------------------

def test_insert_chat(chat_dao):
    """Test insertion d'un nouveau chat."""
    new_chat = Chat(
        id_chat=None,
        id_user=1,
        title="Chat de test",
        date_start=None,
        last_date=None,
        max_tokens=512,
        temperature=0.7,
        top_p=0.9,
    )

    inserted = chat_dao.insert(new_chat)

    assert inserted is not None
    assert inserted.id_chat is not None
    assert inserted.title == "Chat de test"

    fetched = chat_dao.get_chat(inserted.id_chat)
    assert fetched is not None
    assert fetched.title == "Chat de test"


# -----------------------------------------------------
# UPDATE
# -----------------------------------------------------

def test_update_chat(chat_dao):
    """Test mise à jour d'un chat."""
    chat = chat_dao.insert(Chat(None, 1, "Titre Initial", None, None, 256, 0.5, 0.8))

    updated = Chat(
        id_chat=chat.id_chat,
        id_user=chat.id_user,
        title="Nouveau Titre",
        date_start=chat.date_start,
        last_date=chat.last_date,
        max_tokens=chat.max_tokens,
        temperature=chat.temperature,
        top_p=chat.top_p,
    )

    result = chat_dao.update(chat.id_chat, updated)
    assert result is not None

    updated_in_db = chat_dao.get_chat(chat.id_chat)
    assert updated_in_db.title == "Nouveau Titre"


# -----------------------------------------------------
# DELETE
# -----------------------------------------------------

def test_delete_chat(chat_dao):
    """Supprime un chat."""
    chat = chat_dao.insert(Chat(None, 1, "Chat à supprimer", None, None, 256, 0.5, 0.9))

    deleted = chat_dao.delete(chat.id_chat)
    assert deleted is True

    assert chat_dao.get_chat(chat.id_chat) is None


# -----------------------------------------------------
# GET ALL
# -----------------------------------------------------

def test_get_all_chats(chat_dao):
    """Doit renvoyer une liste de chat."""
    chats = chat_dao.get_all()

    assert isinstance(chats, list)
    assert all(isinstance(c, Chat) for c in chats)


# -----------------------------------------------------
# LIST BY USER
# -----------------------------------------------------

def test_list_chats_id_user(chat_dao):
    """Liste les chats d'un utilisateur."""
    user_id = 1

    chats = chat_dao.list_chats_id_user(user_id)

    assert chats is not None
    assert isinstance(chats, list)
    assert all(c.id_user == user_id for c in chats)


# -----------------------------------------------------
# COUNT
# -----------------------------------------------------

def test_count_chats(chat_dao):
    """Comptage total des chats."""
    before = chat_dao.count_chats()

    chat_dao.insert(Chat(None, 1, "New Chat", None, None, 256, 0.5, 0.9))
    after = chat_dao.count_chats()

    assert isinstance(before, int)
    assert after == before + 1


# -----------------------------------------------------
# SEARCH BY TITLE
# -----------------------------------------------------

def test_search_by_title_found(chat_dao):
    """Recherche par mot clé dans les titres."""
    chat_dao.insert(Chat(None, 1, "Discussion GPT Test", datetime.now(), datetime.now(), 512, 0.7, 0.9))
    chat_dao.insert(Chat(None, 1, "Autre conversation", datetime.now(), datetime.now(), 256, 0.6, 0.8))
    chat_dao.insert(Chat(None, 1, "GPT Historique", datetime.now(), datetime.now(), 256, 0.6, 0.8))

    results = chat_dao.search_by_title(1, "gpt")

    assert results is not None
    assert isinstance(results, list)
    assert all(isinstance(c, Chat) for c in results)
    assert all("gpt" in c.title.lower() for c in results)
    assert len(results) >= 2


def test_search_by_title_not_found(chat_dao):
    """Aucun titre correspondant."""
    chat_dao.insert(Chat(None, 1, "Conversation classique", datetime.now(), datetime.now(), 512, 0.7, 0.9))

    results = chat_dao.search_by_title(1, "inexistant")

    assert results is None


# -----------------------------------------------------
# SEARCH BY DATE
# -----------------------------------------------------
from datetime import datetime
def test_search_by_date_found(chat_dao):
    """Recherche par date (simple)."""
    today = datetime.today()
    chat_dao.insert(Chat(None, 1, "Chat d’aujourd’hui", today, today, 512, 0.7, 0.9))

    results = chat_dao.search_by_date(1, today.date())
    d = date.today()

    results = chat_dao.search_by_date(1, d)

    assert results is not None
    assert isinstance(results, list)
    #assert len(results) == 1
    assert results[0].title == "Chat d’aujourd’hui"


def test_search_by_date_not_found(chat_dao):
    """Recherche par date -> aucun résultat."""
    chat_dao.insert(Chat(None, 1, "Chat ancien", datetime(2024, 10, 1), datetime(2024, 10, 1), 256, 0.5, 0.9))

    results = chat_dao.search_by_date(1, datetime(2025, 1, 1))

    assert results is None


# -----------------------------------------------------
# DELETE ALL CHATS
# -----------------------------------------------------

def test_delete_all_chats(chat_dao):
    """Supprimer toutes les conversations d'un utilisateur."""
    user_id = 1

    chat_dao.insert(Chat(None, user_id, "Chat 1", datetime.now(), datetime.now(), 256, 0.9, 0.5))
    chat_dao.insert(Chat(None, user_id, "Chat 2", datetime.now(), datetime.now(), 256, 0.8, 0.6))

    before = chat_dao.list_chats_id_user(user_id)
    assert before is not None
    assert len(before) >= 2

    result = chat_dao.delete_all_chats(user_id)
    assert result is True

    after = chat_dao.list_chats_id_user(user_id)
    assert after is None or len(after) == 0


if __name__ == "__main__":
    pytest.main([__file__])
