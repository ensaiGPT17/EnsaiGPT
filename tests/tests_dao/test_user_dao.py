import pytest

from dao.user_dao import UserDAO
from model.user import User
from utils.reset_database import ResetDatabase


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
def user_dao():
    """Retourne une instance propre de UserDAO"""
    return UserDAO()


# --------------------------------------------------------
# Tests
# --------------------------------------------------------
def test_username_exists_true(user_dao):
    """Retourne True si l'utilisateur existe"""
    # On s'appuie sur les données du pop_db_test.sql
    assert user_dao.username_exists("bruno") is True


def test_username_exists_false(user_dao):
    """Retourne False si l'utilisateur n'existe pas"""
    assert user_dao.username_exists("user_inconnu") is False


def test_insert_user(user_dao):
    """Insertion d’un utilisateur"""
    new_user = User(
        id_user=None,
        username="alice",
        hashed_password="hashedpwd123"
    )

    inserted_user = user_dao.insert(new_user)

    assert inserted_user is not None
    assert inserted_user.id_user is not None
    assert inserted_user.username == "alice"
    assert user_dao.username_exists("alice") is True


def test_get_user(user_dao):
    """Récupération par ID"""
    user = user_dao.insert(User(None, "bob", "pwd"))
    fetched = user_dao.get_user(user.id_user)

    assert fetched is not None
    assert fetched.id_user == user.id_user
    assert fetched.username == "bob"


def test_get_user_by_username(user_dao):
    """Récupération par username"""
    user_dao.insert(User(None, "charlie", "xyz"))
    user = user_dao.get_user_by_username("charlie")

    assert user is not None
    assert user.username == "charlie"


def test_update_user(user_dao):
    """Mise à jour utilisateur"""
    user = user_dao.insert(User(None, "denis", "pwd"))
    updated_user = User(
        id_user=user.id_user,
        username="denis_new",
        hashed_password="newhash"
    )

    result = user_dao.update(user.id_user, updated_user)
    assert result is not None

    fetched = user_dao.get_user(user.id_user)
    assert fetched.username == "denis_new"
    assert fetched.hashed_password == "newhash"


def test_delete_user(user_dao):
    """Suppression utilisateur"""
    user = user_dao.insert(User(None, "edgar", "pwd"))
    deleted = user_dao.delete(user.id_user)

    assert deleted is True
    assert user_dao.get_user(user.id_user) is None
    assert user_dao.get_user_by_username("edgar") is None


def test_get_all_users(user_dao):
    """Liste tous les utilisateurs"""
    users = user_dao.get_all()

    assert isinstance(users, list)
    for u in users:
        assert isinstance(u, User)


def test_count_users(user_dao):
    """Compter les utilisateurs"""
    count = user_dao.count_users()
    assert isinstance(count, int)
    assert count >= 0


if __name__ == "__main__":
    pytest.main([__file__])
