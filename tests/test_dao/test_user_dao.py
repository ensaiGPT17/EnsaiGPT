import pytest
from dao.user_dao import UserDAO
from utils.reset_database import ResetDatabase
from model.user import User


@pytest.fixture
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


def test_insert_user(user_dao):
    """Test l'insertion d'un utilisateur"""
    new_user = User(id_user=1, username="alice", hashed_password="hashedpwd123")
    inserted_user = user_dao.insert(new_user)

    assert inserted_user is not None
    assert inserted_user.id_user is not None
    assert inserted_user.username == "alice"
    assert user_dao.username_exists("alice") is True


def test_get_user(user_dao):
    """Test la récupération d'un utilisateur par ID"""
    user = user_dao.insert(User(1, "alice", "pwd"))
    fetched = user_dao.get_user(user.id_user)

    assert fetched is not None
    assert fetched.id_user == user.id_user
    assert fetched.username == "alice"


def test_get_user_by_username(user_dao):
    """Test récupération par username"""
    user_dao.insert(User(1, "alice", "pwd"))
    user = user_dao.get_user_by_username("alice")
    assert user is not None
    assert user.username == "alice"


def test_update_user(user_dao):
    """Test la mise à jour d'un utilisateur"""
    user = user_dao.insert(User(1, "alice", "pwd"))
    updated_user = User(id_user=user.id_user, username="alice_new", hashed_password="newhash")

    result = user_dao.update(user.id_user, updated_user)
    assert result is not None

    fetched = user_dao.get_user(user.id_user)
    assert fetched.username == "alice_new"
    assert fetched.hashed_password == "newhash"


def test_delete_user(user_dao):
    """Test suppression d'un utilisateur"""
    user = user_dao.insert(User(1, "alice", "pwd"))
    deleted = user_dao.delete(user.id_user)

    assert deleted is True
    assert user_dao.get_user(user.id_user) is None
    assert user_dao.get_user_by_username("alice") is None


def test_get_all_users(user_dao):
    """Test récupération de tous les utilisateurs"""
    users = user_dao.get_all()
    assert isinstance(users, list)


def test_count_users(user_dao):
    """Test le comptage des utilisateurs"""
    count = user_dao.count_users()
    assert isinstance(count, int)


if __name__ == "__main__":
    pytest.main([__file__])