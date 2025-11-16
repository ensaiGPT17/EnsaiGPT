import pytest
from unittest.mock import MagicMock, patch
from model.user import User
from service.user_service import UserService
from dao.user_dao import UserDAO


liste_user = [User(1, "alice", "hashed123")]

def test_get_user_ok():
    # given
    UserDAO.get_user = MagicMock(return_value=liste_user[0])
    # when
    res = UserService(UserDAO()).get_user(1)
    #then
    assert res == liste_user[0]

def test_get_user_not_found():

    # GIVEN
    UserDAO.get_user = MagicMock(return_value=None)

    # WHEN
    res = UserService(UserDAO()).get_user(99)

    # THEN
    assert res is None

def test_get_user_by_username_found():
    # given
    UserDAO.get_user = MagicMock(return_value=liste_user[0])
    # when
    res = UserService(UserDAO()).get_user("alice")
    #then
    assert res == liste_user[0]

def test_get_user_by_username_not_found():
    # GIVEN
    UserDAO.get_user = MagicMock(return_value=None)

    # WHEN
    res = UserService(UserDAO()).get_user_by_username("napoleon")

    # THEN
    assert res is None

def test_is_username_available_ok():

    # GIVEN
    UserDAO.username_exists = MagicMock(return_value=False)

    # WHEN
    res = UserService(UserDAO()).is_username_available("bob")

    # THEN
    assert res.code == 200

def test_is_username_available_non_dispo():

    # GIVEN
    UserDAO.username_exists = MagicMock(return_value=True)

    # WHEN
    res = UserService(UserDAO()).is_username_available("bob")

    # THEN
    assert res.code == 409

# ------------------------------
#       Tests create_user
# ------------------------------

def test_create_user_username_exists():
    """Création échoue car pseudo déjà pris"""

    # GIVEN
    UserDAO.username_exists = MagicMock(return_value=True)

    # WHEN
    res = UserService(UserDAO()).create_user("alice", "abcd")

    # THEN
    assert res.code == 409


def test_create_user_password_weak():
    """Création échoue car mot de passe trop faible"""

    # GIVEN
    UserDAO.username_exists = MagicMock(return_value=False)
    globals()["password_is_secure"] = lambda x: False

    # WHEN
    res = UserService(UserDAO()).create_user("alice", "abc")

    # THEN
    assert res.code == 400


def test_create_user_insert_error():
    """Erreur interne DAO lors de l'insertion"""

    # GIVEN
    UserDAO.username_exists = MagicMock(return_value=False)
    globals()["password_is_secure"] = lambda x: True
    UserDAO.insert = MagicMock(return_value=None)

    # WHEN
    res = UserService(UserDAO()).create_user("bob", "Abcd1234!")

    # THEN
    assert res.code == 500


def test_create_user_ok():
    """Création réussie"""

    # GIVEN
    UserDAO.username_exists = MagicMock(return_value=False)
    globals()["password_is_secure"] = lambda x: True
    UserDAO.insert = MagicMock(return_value=User(1, "alice", "hashedhh"))

    # WHEN
    res = UserService(UserDAO()).create_user("alice", "Abcd1234!")

    # THEN
    assert res.code == 201


# ------------------------------
#       Tests authenticate
# ------------------------------

def test_authenticate_username_not_found():
    """Nom d'utilisateur inconnu"""

    # GIVEN
    UserDAO.get_user_by_username = MagicMock(return_value=None)

    # WHEN
    res = UserService(UserDAO()).authenticate("alice", "aaa")

    # THEN
    assert res.code == 401


def test_authenticate_mdp_incorrect():
    """Mot de passe incorrect"""

    # GIVEN
    user = User(1, "alice", "hashed")
    UserDAO.get_user_by_username = MagicMock(return_value=user)

    with patch("service.user_service.check_password", return_value=False):
        # WHEN
        res = UserService(UserDAO()).authenticate("alice", "wrong")

    # THEN
    assert res.code == 401


def test_authenticate_ok():
    """Connexion OK"""

    # GIVEN
    user = User(1, "alice", "hashed")
    UserDAO.get_user_by_username = MagicMock(return_value=user)

    with patch("service.user_service.check_password", return_value=True):
        # WHEN
        res = UserService(UserDAO()).authenticate("alice", "correct")

    # THEN
    assert res.code == 200

# ------------------------------
#       Tests change_password
# ------------------------------

def test_change_password_too_weak():
    """Nouveau mot de passe trop faible"""

    # GIVEN
    with patch("service.user_service.password_is_secure", return_value=False):
        # WHEN
        res = UserService(UserDAO()).change_password(1, "old", "a")

    # THEN
    assert res.code == 400


def test_change_password_user_not_found():
    """Utilisateur inexistant"""

    # GIVEN
    with patch("service.user_service.password_is_secure", return_value=True):
        UserDAO.get_user = MagicMock(return_value=None)
        # WHEN
        res = UserService(UserDAO()).change_password(1, "old", "newpass")

    # THEN
    assert res.code == 404


def test_change_password_wrong_old_password():
    """Ancien mot de passe incorrect"""

    # GIVEN
    user = User(1, "alice", "hashed")
    with patch("service.user_service.password_is_secure", return_value=True):
        UserDAO.get_user = MagicMock(return_value=user)
        with patch("service.user_service.check_password", return_value=False):
            # WHEN
            res = UserService(UserDAO()).change_password(1, "old", "newpass")

    # THEN
    assert res.code == 401


def test_change_password_update_error():
    """Erreur DAO lors de la mise à jour"""

    # GIVEN
    user = User(1, "alice", "hashed")
    with patch("service.user_service.password_is_secure", return_value=True):
        UserDAO.get_user = MagicMock(return_value=user)
        with patch("service.user_service.check_password", return_value=True):
            UserDAO.update = MagicMock(return_value=None)
            # WHEN
            res = UserService(UserDAO()).change_password(1, "old", "newpass")

    # THEN
    assert res.code == 500


def test_change_password_ok():
    """Changement de mot de passe réussi"""

    # GIVEN
    user = User(1, "alice", "oldhashed")
    with patch("service.user_service.password_is_secure", return_value=True):
        UserDAO.get_user = MagicMock(return_value=user)
        with patch("service.user_service.check_password", return_value=True):
            UserDAO.update = MagicMock(return_value=True)
            # WHEN
            res = UserService(UserDAO()).change_password(1, "old", "newpass")

    # THEN
    assert res.code == 200

# ------------------------------
#       Tests change_username
# ------------------------------

def test_change_username_user_not_found():
    """Utilisateur inexistant"""

    # GIVEN
    UserDAO.get_user = MagicMock(return_value=None)

    # WHEN
    res = UserService(UserDAO()).change_username(1, "newname")

    # THEN
    assert res.code == 404


def test_change_username_already_exists():
    """Nouveau pseudo déjà utilisé"""

    # GIVEN
    UserDAO.get_user = MagicMock(return_value=User(1, "bob", "hashed"))
    UserDAO.username_exists = MagicMock(return_value=True)

    # WHEN
    res = UserService(UserDAO()).change_username(1, "alice")

    # THEN
    assert res.code == 409


def test_change_username_update_error():
    """Erreur DAO lors de la mise à jour"""

    # GIVEN
    user = User(1, "bob", "hashed")
    UserDAO.get_user = MagicMock(return_value=user)
    UserDAO.username_exists = MagicMock(return_value=False)
    UserDAO.update = MagicMock(return_value=None)

    # WHEN
    res = UserService(UserDAO()).change_username(1, "alice")

    # THEN
    assert res.code == 500


def test_change_username_ok():
    """Changement de pseudo OK"""

    # GIVEN
    user = User(1, "bob", "hashed")
    UserDAO.get_user = MagicMock(return_value=user)
    UserDAO.username_exists = MagicMock(return_value=False)
    UserDAO.update = MagicMock(return_value=True)

    # WHEN
    res = UserService(UserDAO()).change_username(1, "alice")

    # THEN
    assert res.code == 200


# ------------------------------
#       Tests delete_user
# ------------------------------

def test_delete_user_not_found():
    """Utilisateur introuvable"""

    # GIVEN
    UserDAO.get_user = MagicMock(return_value=None)

    # WHEN
    res = UserService(UserDAO()).delete_user(1, "pass")

    # THEN
    assert res.code == 404


def test_delete_user_wrong_password():
    """Mot de passe incorrect"""

    # GIVEN
    user = User(1, "bob", "hashed")
    UserDAO.get_user = MagicMock(return_value=user)
    with patch("service.user_service.check_password", return_value=False):
        # WHEN
        res = UserService(UserDAO()).delete_user(1, "wrong")

    # THEN
    assert res.code == 401


def test_delete_user_dao_error():
    """Erreur DAO lors de la suppression"""

    # GIVEN
    user = User(1, "bob", "hashed")
    UserDAO.get_user = MagicMock(return_value=user)
    with patch("service.user_service.check_password", return_value=True):
        UserDAO.delete = MagicMock(return_value=False)
        # WHEN
        res = UserService(UserDAO()).delete_user(1, "correct")

    # THEN
    assert res.code == 500


def test_delete_user_ok():
    """Suppression OK"""

    # GIVEN
    user = User(1, "bob", "hashed")
    UserDAO.get_user = MagicMock(return_value=user)
    with patch("service.user_service.check_password", return_value=True):
        UserDAO.delete = MagicMock(return_value=True)
        # WHEN
        res = UserService(UserDAO()).delete_user(1, "correct")

    # THEN
    assert res.code == 200


# ------------------------------
#       Tests count_users
# ------------------------------

def test_count_users():
    """Compter les utilisateurs"""

    # GIVEN
    UserDAO.count_users = MagicMock(return_value=42)

    # WHEN
    res = UserService(UserDAO()).count_users()

    # THEN
    assert res == 42