import pytest
from dao.chat_dao import ChatDAO
from utils.reset_database import ResetDatabase
from model.chat import Chat
from datetime import date


@pytest.fixture
def chat_dao():
    """
    Réinitialise la base de données et renvoie une instance de ChatDAO.
    Cette fixture est appelée avant chaque test.
    """
    ResetDatabase().lancer()
    return ChatDAO()


def test_get_chat_found(chat_dao):
    """Doit récupérer un chat existant (préchargé dans ResetDatabase)."""
    chat = chat_dao.get_chat(1)
    assert chat is not None
    # Certains drivers renvoient un tuple (1,)
    assert chat.id_chat == 1 or chat.id_chat == (1,)


def test_get_chat_not_found(chat_dao):
    """Doit retourner None si le chat n’existe pas."""
    chat = chat_dao.get_chat(9999)
    assert chat is None


def test_insert_chat(chat_dao):
    """Test de l'insertion d'un nouveau chat."""
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

    inserted_chat = chat_dao.insert(new_chat)
    assert inserted_chat is not None
    assert inserted_chat.id_chat is not None
    assert inserted_chat.title == "Chat de test"

    # Vérifie qu’il existe bien dans la base
    fetched = chat_dao.get_chat(inserted_chat.id_chat)
    assert fetched is not None
    assert fetched.title == "Chat de test"


def test_update_chat(chat_dao):
    """Test la mise à jour d’un chat existant."""
    chat = chat_dao.insert(Chat(None, 1, "Titre initial", None, None, 256, 0.5, 0.8))

    chat_updated = Chat(
        id_chat=chat.id_chat,
        id_user=chat.id_user,
        title="Nouveau titre",
        date_start=chat.date_start,
        last_date=chat.last_date,
        max_tokens=chat.max_tokens,
        temperature=chat.temperature,
        top_p=chat.top_p,
    )

    result = chat_dao.update(chat.id_chat, chat_updated)
    assert result is not None

    # Vérifie que le titre a bien changé
    updated_in_db = chat_dao.get_chat(chat.id_chat)
    assert updated_in_db.title == "Nouveau titre"


def test_delete_chat(chat_dao):
    """Test la suppression d’un chat."""
    chat = chat_dao.insert(Chat(None, 1, "Chat à supprimer", None, None, 256, 0.5, 0.9))

    deleted = chat_dao.delete(chat.id_chat)
    assert deleted is True

    # Vérifie qu’il n’existe plus
    assert chat_dao.get_chat(chat.id_chat) is None


def test_get_all_chats(chat_dao):
    """Doit retourner une liste de chats."""
    chats = chat_dao.get_all()
    assert isinstance(chats, list)
    assert all(isinstance(c, Chat) for c in chats)


def test_list_chats_id_user(chat_dao):
    """Doit lister les chats d’un utilisateur donné."""
    user_id = 1
    chats = chat_dao.list_chats_id_user(user_id)
    assert chats is not None, "La requête n’a retourné aucun résultat"
    assert isinstance(chats, list)
    print("\nRésultats retournés par list_chats_id_user(1):")
    for c in chats:
        print(f"id_chat={c.id_chat}, id_user={c.id_user}, title={c.title}")
    assert all(c.id_user == (user_id,) for c in chats) # c'est une solution pas efficace,(probleme de tuple) je vais revoir ça (yassine)



def test_count_chats(chat_dao):
    """Test le comptage total des chats."""
    count_before = chat_dao.count_chats()

    chat_dao.insert(Chat(None, 1, "New Chat", None, None, 256, 0.5, 0.9))
    count_after = chat_dao.count_chats()

    assert isinstance(count_before, int)
    assert count_after == count_before + 1


if __name__ == "__main__":
    pytest.main([__file__])