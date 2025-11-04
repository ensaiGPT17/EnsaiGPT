import pytest
from dao.user_dao import UserDAO
from utils.reset_database import ResetDatabase


@pytest.fixture(scope="module")
def user_dao():
    """Initialise la base et fournit une instance de UserDAO pour tous les tests"""
    ResetDatabase().lancer()
    return UserDAO()


def test_username_exists_true(user_dao):
    """Doit retourner True si l'utilisateur existe"""
    result = user_dao.username_exists("bruno")
    assert result is True


def test_username_exists_false(user_dao):
    """Doit retourner False si l'utilisateur n'existe pas"""
    result = user_dao.username_exists("user_inconnu")
    assert result is False


if __name__ == "__main__":
    pytest.main([__file__])