import pytest
from service.user_service import UserService
from tests.test_dao.mocks import UserDAOMock
from dao.user_dao import UserDAO
from utils.reset_database import ResetDatabase


@pytest.fixture
def user_service_mock():
    """
    Pour les tests unitaires.
    """
    dao = UserDAOMock()
    dao.clear_all()  # important
    return UserService(dao)


@pytest.fixture
def user_service_real():
    """
    Pour les tests d integration.
    """
    ResetDatabase().lancer()
    dao = UserDAO()
    return UserService(dao)


def test_get_user_by_username_not_found(user_service_mock):
    # GIVEN : aucun utilisateur créé

    # WHEN
    result = user_service_mock.get_user_by_username("Inconnu")

    # THEN
    assert result is None


def test_get_user_by_username_not_found_real(user_service_real):
    # GIVEN : aucun utilisateur créé

    # WHEN
    result = user_service_real.get_user_by_username("Inconnu")

    # THEN
    assert result is None


def test_create_user_success(user_service_mock):
    # GIVEN
    username = "Louis"
    password = "UnMotDePasseSecure*159"

    # WHEN
    result = user_service_mock.create_user(username, password)

    # THEN
    assert result.code == 201
    assert result.content == "Utilisateur créé avec succès"
    assert user_service_mock.get_user_by_username("Louis") is not None


def test_create_user_success_real(user_service_real):
    # GIVEN
    username = "Louis"
    password = "UnMotDePasseSecure*159"

    # WHEN
    result = user_service_real.create_user(username, password)

    # THEN
    assert result.code == 201
    assert result.content == "Utilisateur créé avec succès"
    assert user_service_real.get_user_by_username("Louis") is not None


def test_create_user_duplicate(user_service_mock):
    # GIVEN
    user_service_mock.create_user("Louis", "UnMotDePasseSecure*159")

    # WHEN
    result = user_service_mock.create_user("Louis", "UnAutreMotDePasseSecure*159")

    # THEN
    assert result.code == 409
    assert result.content == "Nom d'utilisateur déjà utilisé"


def test_create_user_duplicate_real(user_service_real):
    # GIVEN
    user_service_real.create_user("Louis", "UnMotDePasseSecure*159")

    # WHEN
    result = user_service_real.create_user("Louis", "UnAutreMotDePasseSecure*159")

    # THEN
    assert result.code == 409
    assert result.content == "Nom d'utilisateur déjà utilisé"


def test_create_user_not_secure_password(user_service_mock):
    # GIVEN : aucun utilisateur créé

    # WHEN
    result = user_service_mock.create_user("Louis", "mdp")

    # THEN
    assert result.code == 400
    assert result.content == "Mot de passe trop faible"
    assert user_service_mock.get_user_by_username("Louis") is None


def test_create_two_user_success(user_service_mock):
    # GIVEN
    user_service_mock.create_user("Louis", "UnMotDePasseSecure*159")

    # WHEN
    result = user_service_mock.create_user("louis", "UnMotDePasseSecure*159")

    # THEN
    assert result.code == 201
    assert result.content == "Utilisateur créé avec succès"
    first_user = user_service_mock.get_user_by_username("Louis")
    second_user = user_service_mock.get_user_by_username("louis")
    assert first_user.username == "Louis"
    assert second_user.username == "louis"


def test_authenticate_success(user_service_mock):
    # GIVEN
    user_service_mock.create_user("Louis", "UnMotDePasseSecure*159")

    # WHEN
    result = user_service_mock.authenticate("Louis", "UnMotDePasseSecure*159")

    # THEN
    assert result.code == 200
    assert result.content == "Authentification réussie"


def test_authenticate_failure(user_service_mock):
    # GIVEN
    user_service_mock.create_user("Louis", "UnMotDePasseSecure*159")

    # WHEN
    result1 = user_service_mock.authenticate("louis", "UnMotDePasseSecure*159")
    result2 = user_service_mock.authenticate("Louis", "mauvais_mdp")

    # THEN
    assert result1.code == 401
    assert result2.code == 401
    assert result1.content == "Nom d'utilisateur ou mot de passe incorrect"
    assert result2.content == "Nom d'utilisateur ou mot de passe incorrect"


def test_change_password_success(user_service_mock):
    # GIVEN
    user_service_mock.create_user("Louis", "UnMotDePasseSecure*159")
    created = user_service_mock.get_user_by_username("Louis")

    # WHEN
    result = user_service_mock.change_password(created.id_user,
                                               "UnMotDePasseSecure*159",
                                               "AutreMotDePasseSecure*159")
    result_auth = user_service_mock.authenticate("Louis", "AutreMotDePasseSecure*159")
    result_wrong_auth = user_service_mock.authenticate("Louis",
                                                       "UnMotDePasseSecure*159")

    # THEN
    assert result.code == 200
    assert result.content == "Mot de passe modifié avec succès"
    assert result_auth.code == 200
    assert result_wrong_auth.code == 401


def test_change_password_failure(user_service_mock):
    # GIVEN
    user_service_mock.create_user("Louis", "UnMotDePasseSecure*159")
    created = user_service_mock.get_user_by_username("Louis")

    # WHEN
    result_wrong_password = user_service_mock.change_password(created.id_user,
                                                              "mauvais_mdp",
                                                              "159*AutreMotDePasseSecure")
    result_weak_password = user_service_mock.change_password(created.id_user,
                                                             "UnMotDePasseSecure*159",
                                                             "mdp")
    result_auth = user_service_mock.authenticate("Louis", "UnMotDePasseSecure*159")
    result_wrong_auth = user_service_mock.authenticate("Louis",
                                                       "159*AutreMotDePasseSecure")

    # THEN
    assert result_wrong_password.code == 401
    assert result_weak_password.code == 400
    assert result_auth.code == 200
    assert result_wrong_auth.code == 401


def test_change_password_failure_real(user_service_real):
    # GIVEN
    user_service_real.create_user("Louis", "UnMotDePasseSecure*159")
    created = user_service_real.get_user_by_username("Louis")

    # WHEN
    result_wrong_password = user_service_real.change_password(created.id_user,
                                                              "mauvais_mdp",
                                                              "159*AutreMotDePasseSecure")
    result_weak_password = user_service_real.change_password(created.id_user,
                                                             "UnMotDePasseSecure*159",
                                                             "mdp")
    result_auth = user_service_real.authenticate("Louis", "UnMotDePasseSecure*159")
    result_wrong_auth = user_service_real.authenticate("Louis",
                                                       "159*AutreMotDePasseSecure")

    # THEN
    assert result_wrong_password.code == 401
    assert result_weak_password.code == 400
    assert result_auth.code == 200
    assert result_wrong_auth.code == 401


def test_change_username_success(user_service_mock):
    # GIVEN
    user_service_mock.create_user("Louis", "UnMotDePasseSecure*159")
    created = user_service_mock.get_user_by_username("Louis")

    # WHEN
    result = user_service_mock.change_username(created.id_user, "Bob")
    result_auth = user_service_mock.authenticate("Bob", "UnMotDePasseSecure*159")
    result_wrong_auth = user_service_mock.authenticate("Louis",
                                                       "UnMotDePasseSecure*159")

    # THEN
    assert result.code == 200
    assert result.content == "Nom d'utilisateur modifié avec succès"
    assert result_auth.code == 200
    assert result_wrong_auth.code == 401


def test_change_username_failure(user_service_mock):
    # GIVEN
    result_user_not_found = user_service_mock.change_username(1, "Bob2")
    user_service_mock.create_user("Louis", "UnMotDePasseSecure*159")
    user_service_mock.create_user("Alice", "A159*MotDePasseSecure")
    created = user_service_mock.get_user_by_username("Louis")

    # WHEN
    result_duplicate = user_service_mock.change_username(created.id_user, "Alice")
    result_auth = user_service_mock.authenticate("Louis", "UnMotDePasseSecure*159")
    result_wrong_auth = user_service_mock.authenticate("Bob2",
                                                       "159*AutreMotDePasseSecure")

    # THEN
    assert result_duplicate.code == 409
    assert result_user_not_found.code == 404
    assert result_auth.code == 200
    assert result_wrong_auth.code == 401


def test_delete_user_success(user_service_mock):
    # GIVEN
    user_service_mock.create_user("Louis", "UnMotDePasseSecure*159")
    user_service_mock.create_user("Alice", "A159*MotDePasseSecure")
    created_f = user_service_mock.get_user_by_username("Louis")

    # WHEN
    delete = user_service_mock.delete_user(created_f.id_user, "UnMotDePasseSecure*159")

    # THEN
    assert user_service_mock.get_user_by_username("Louis") is None
    assert user_service_mock.get_user_by_username("Alice") is not None
    assert delete.code == 200


def test_delete_user_failure(user_service_mock):
    # GIVEN
    user_service_mock.create_user("Louis", "UnMotDePasseSecure*159")
    created = user_service_mock.get_user_by_username("Louis")

    # WHEN
    wrong_password = user_service_mock.delete_user(created.id_user,
                                                   "unMotDePasseSecure*159")

    # THEN
    assert wrong_password.code == 401


def test_delete_user_failure_real(user_service_real):
    # GIVEN
    user_service_real.create_user("Louis", "UnMotDePasseSecure*159")
    created = user_service_real.get_user_by_username("Louis")

    # WHEN
    wrong_password = user_service_real.delete_user(created.id_user,
                                                   "unMotDePasseSecure*159")

    # THEN
    assert wrong_password.code == 401
