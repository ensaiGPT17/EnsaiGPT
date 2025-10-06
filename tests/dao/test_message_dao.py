import pytest
from dao.message_dao import MessageDAO
from utils.reset_database import ResetDatabase

@pytest.fixture(scope="module")
def message_dao():
    """Réinitialise la base et fournit une instance de MessageDAO"""
    ResetDatabase().lancer()
    return MessageDAO()


def test_créer_message(message_dao):
    """Test la création d'un message"""
    pass

def test_supprimer_message(message_dao):
    """Test la suppression d'un message"""
    # Créer un message à supprimer, je pense
    pass

if __name__ == "__main__":
    pytest.main([__file__])