import pytest
from unittest.mock import MagicMock

from model.user import User
from dao.user_dao import UserDAO
from service.user_service import UserService
from service.password_service import hash_password


@pytest.fixture
def user_service_mock():
    """Service avec DAO mocké pour tests unitaires."""
    dao = UserDAO()
    # Mock des méthodes BDD
    dao.get_user = MagicMock()              # get user
    dao.get_user_by_username = MagicMock()  # get user by username
    dao.insert = MagicMock()                # insert user
    dao.update = MagicMock()                # update user
    dao.delete = MagicMock()                # delete user
    dao.username_exists = MagicMock()       # check username
    dao.count_users = MagicMock()           # count users
    return UserService(dao)                 # return service


def test_create_user_success(user_service_mock):
    # GIVEN : utilisateur non existant et mot de passe fort
    username = "Louis"
    password = "MotDePasse*123"
    user_service_mock.user_dao.username_exists.return_value = False
    user_service_mock.user_dao.insert.return_value = User(1, username, hash_password(password))

    # WHEN : création de l'utilisateur
    res = user_service_mock.create_user(username, password)

    # THEN : succès création
    assert res.code == 201
    assert res.content == "Utilisateur créé avec succès"
    user_service_mock.user_dao.insert.assert_called_once()  # vérifie insertion


def test_create_user_duplicate(user_service_mock):
    # GIVEN : utilisateur déjà existant
    username = "Louis"
    password = "MotDePasse*123"
    user_service_mock.user_dao.username_exists.return_value = True

    # WHEN : tentative de création
    res = user_service_mock.create_user(username, password)

    # THEN : erreur doublon
    assert res.code == 409
    assert res.content == "Nom d'utilisateur déjà utilisé"


def test_create_user_weak_password(user_service_mock):
    # GIVEN : mot de passe trop faible
    username = "Louis"
    password = "mdp"
    user_service_mock.user_dao.username_exists.return_value = False

    # WHEN : tentative de création
    res = user_service_mock.create_user(username, password)

    # THEN : erreur mot de passe faible
    assert res.code == 400
    assert res.content == "Mot de passe trop faible"


def test_authenticate_success(user_service_mock):
    # GIVEN : utilisateur existant et mot de passe correct
    username = "Louis"
    password = "MotDePasse*123"
    hashed = hash_password(password)
    user_service_mock.user_dao.get_user_by_username.return_value = User(1, username, hashed)

    # WHEN : authentification
    res = user_service_mock.authenticate(username, password)

    # THEN : succès
    assert res.code == 200
    assert res.content == "Authentification réussie"


def test_authenticate_failure_wrong_password(user_service_mock):
    # GIVEN : utilisateur existant mais mauvais mot de passe
    username = "Louis"
    password = "MotDePasse*123"
    user_service_mock.user_dao.get_user_by_username.return_value = User(1, username, hash_password("AutreMotDePasse"))

    # WHEN : authentification
    res = user_service_mock.authenticate(username, password)

    # THEN : échec
    assert res.code == 401
    assert res.content == "Nom d'utilisateur ou mot de passe incorrect"


def test_authenticate_failure_user_not_found(user_service_mock):
    # GIVEN : utilisateur inexistant
    user_service_mock.user_dao.get_user_by_username.return_value = None

    # WHEN : authentification
    res = user_service_mock.authenticate("Inconnu", "mdp")

    # THEN : échec
    assert res.code == 401
    assert res.content == "Nom d'utilisateur ou mot de passe incorrect"


def test_change_password_success(user_service_mock):
    # GIVEN : utilisateur existant et ancien mot de passe correct
    old_password = "Ancien*123"
    new_password = "Nouveau*123"
    user = User(1, "Louis", hash_password(old_password))
    user_service_mock.user_dao.get_user.return_value = user
    user_service_mock.user_dao.update.return_value = user

    # WHEN : changement de mot de passe
    res = user_service_mock.change_password(user.id_user, old_password, new_password)

    # THEN : succès
    assert res.code == 200
    assert res.content == "Mot de passe modifié avec succès"


def test_change_password_failure_weak(user_service_mock):
    # GIVEN : utilisateur existant et nouveau mot de passe trop faible
    user = User(1, "Louis", hash_password("Ancien*123"))
    user_service_mock.user_dao.get_user.return_value = user

    # WHEN : changement mot de passe
    res = user_service_mock.change_password(user.id_user, "Ancien*123", "mdp")

    # THEN : échec
    assert res.code == 400
    assert res.content == "Mot de passe trop faible"


def test_change_password_failure_wrong_old(user_service_mock):
    # GIVEN : utilisateur existant mais mauvais ancien mot de passe
    user = User(1, "Louis", hash_password("Ancien*123"))
    user_service_mock.user_dao.get_user.return_value = user

    # WHEN : changement mot de passe
    res = user_service_mock.change_password(user.id_user, "Mauvais*123", "Nouveau*123")

    # THEN : échec
    assert res.code == 401
    assert res.content == "Nom d'utilisateur ou mot de passe incorrect"


def test_delete_user_success(user_service_mock):
    # GIVEN : utilisateur existant et mot de passe correct
    user = User(1, "Louis", hash_password("MotDePasse*123"))
    user_service_mock.user_dao.get_user.return_value = user
    user_service_mock.user_dao.delete.return_value = True

    # WHEN : suppression utilisateur
    res = user_service_mock.delete_user(user.id_user, "MotDePasse*123")

    # THEN : succès
    assert res.code == 200
    assert res.content == "Utilisateur supprimé avec succès"


def test_delete_user_failure_wrong_password(user_service_mock):
    # GIVEN : utilisateur existant et mauvais mot de passe
    user = User(1, "Louis", hash_password("MotDePasse*123"))
    user_service_mock.user_dao.get_user.return_value = user

    # WHEN : suppression
    res = user_service_mock.delete_user(user.id_user, "Mauvais*123")

    # THEN : échec
    assert res.code == 401
    assert res.content == "Nom d'utilisateur ou mot de passe incorrect"


def test_is_username_available(user_service_mock):
    # GIVEN : test disponibilité username
    user_service_mock.user_dao.username_exists.return_value = False

    # WHEN : vérification
    res = user_service_mock.is_username_available("Louis")
    # THEN : disponible
    assert res.code == 200
    assert res.content == "Nom d'utilisateur disponible"

    # GIVEN : username existant
    user_service_mock.user_dao.username_exists.return_value = True
    # WHEN : vérification
    res = user_service_mock.is_username_available("Louis")
    # THEN : indisponible
    assert res.code == 409
    assert res.content == "Nom d'utilisateur déjà utilisé"


def test_count_users(user_service_mock):
    # GIVEN : DAO retourne nombre utilisateurs
    user_service_mock.user_dao.count_users.return_value = 5
    # WHEN : appel count_users
    assert user_service_mock.count_users() == 5  # THEN : résultat correct


if __name__ == "__main__":
    pytest.main([__file__])
