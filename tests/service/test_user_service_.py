import pytest
from utils.reset_database import ResetDatabase
from dao.user_dao import UserDAO
from service.user_service import UserService
from service.response_service import ResponseService


@pytest.fixture(scope="module")
def user_service():
    """Réinitialise la base et fournit une instance de UserService"""
    ResetDatabase().lancer()
    user_dao = UserDAO()
    return UserService(user_dao)


def test_is_username_available(user_service):
    """Test la disponibilité d'un nom d'utilisateur"""
    # username = "bruno", existe dans la base de donnée pop_db_test.sql
    resp_existing = user_service.is_username_available("bruno")
    assert resp_existing.code == 409

    resp_new = user_service.is_username_available("nouvel_user")
    assert resp_new.code == 200


def test_is_password_secure(user_service):
    """Test la vérification de la sécurité du mot de passe"""
    pass

def test_create_user(user_service):
    """Test la création d'un utilisateur"""
    pass

def test_authenticate(user_service):
    """Test l'authentification"""
    pass

def test_change_password(user_service):
    """Test le changement de mot de passe"""
    pass

def test_change_username(user_service):
    """Test le changement de nom d'utilisateur"""
    pass


if __name__ == "__main__":
    pytest.main([__file__])