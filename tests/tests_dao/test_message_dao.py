import pytest
from datetime import datetime

from dao.message_dao import MessageDAO
from model.message import Message
from utils.reset_database import ResetDatabase


# --------------------------------------------------------
# Initialisation du schéma de test (comme le projet modèle)
# --------------------------------------------------------
@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Réinitialise la base en mode test DAO avant TOUTE la session"""
    ResetDatabase().lancer(test_dao=True)
    yield


# --------------------------------------------------------
# Fixture DAO
# --------------------------------------------------------
@pytest.fixture
def message_dao():
    """Retourne une instance propre de MessageDAO"""
    return MessageDAO(schema="ensaiGPTTEST")


# --------------------------------------------------------
# Tests d'insertion
# --------------------------------------------------------
def test_insert_message(message_dao):
    """Test l'insertion d'un message"""
    msg = Message(
        id_message=0,
        id_chat=1,
        date_sending=datetime.now(),
        role_author="user",
        content="Bonjour, ceci est un message de test"
    )

    inserted = message_dao.insert(msg)

    assert inserted is not None
    assert inserted.id_message is not None
    assert inserted.content == msg.content
    assert inserted.role_author == "user"


def test_delete_message(message_dao):
    """Test la suppression d'un message"""
    msg = Message(
        0, 1, datetime.now(), "assistant", "Message à supprimer"
    )
    inserted = message_dao.insert(msg)

    deleted = message_dao.delete(inserted.id_message)

    assert deleted is True


# --------------------------------------------------------
# Tests de récupération
# --------------------------------------------------------
def test_get_message_by_id(message_dao):
    """Test récupération par id"""
    msg = Message(
        0, 1, datetime.now(), "user", "Message pour get_by_id"
    )
    inserted = message_dao.insert(msg)

    fetched = message_dao.get_message_by_id(inserted.id_message)

    assert fetched is not None
    assert fetched.id_message == inserted.id_message
    assert fetched.content == "Message pour get_by_id"


def test_get_message_by_id_not_found(message_dao):
    """Retourne None si l'id n'existe pas"""
    fetched = message_dao.get_message_by_id(999999)
    assert fetched is None


def test_get_messages_by_chat(message_dao):
    """Récupère tous les messages d’un chat dans l’ordre chronologique"""

    chat_id = 1

    msg1 = Message(
        0, chat_id, datetime(2025, 1, 1, 10, 0),
        "user", "Message 1"
    )
    msg2 = Message(
        0, chat_id, datetime(2025, 1, 1, 10, 5),
        "assistant", "Message 2"
    )

    inserted1 = message_dao.insert(msg1)
    inserted2 = message_dao.insert(msg2)

    messages = message_dao.get_messages_by_chat(chat_id)

    assert isinstance(messages, list)
    assert len(messages) >= 2

    # Vérif contenu
    assert messages[0].content == "Message 1"
    assert messages[1].content == "Message 2"

    # Vérif ordre
    assert messages[0].date_sending <= messages[1].date_sending


if __name__ == "__main__":
    pytest.main([__file__])