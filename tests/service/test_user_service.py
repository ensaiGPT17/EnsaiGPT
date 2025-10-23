import pytest
from service.user_service import UserService
from tests.dao.mocks import UserDAOMock


@pytest.fixture
def user_service():
    dao = UserDAOMock()
    dao.clear_all()  # important
    return UserService(dao)


def test_get_user_not_found(user_service):
    # GIVEN : aucun utilisateur créé

    # WHEN
    result = user_service.get_user(1)

    # THEN
    assert result is None


def test_get_user_by_username_not_found(user_service):
    # GIVEN : aucun utilisateur créé

    # WHEN
    result = user_service.get_user_by_username("Inconnu")

    # THEN
    assert result is None


def test_create_user_success(user_service):
    # GIVEN
    username = "Louis"
    password = "UnMotDePasseSecure*159"

    # WHEN
    result = user_service.create_user(username, password)

    # THEN
    assert result.code == 201
    assert result.content == "Utilisateur créé avec succès"
    assert user_service.get_user_by_username("Louis") is not None


def test_create_user_duplicate(user_service):
    # GIVEN
    user_service.create_user("Louis", "UnMotDePasseSecure*159")

    # WHEN
    result = user_service.create_user("Louis", "UnAutreMotDePasseSecure*159")

    # THEN
    assert result.code == 409
    assert result.content == "Nom d'utilisateur déjà utilisé"
    assert user_service.count_users() == 1


def test_create_user_not_secure_password(user_service):
    # GIVEN : aucun utilisateur créé

    # WHEN
    result = user_service.create_user("Louis", "mdp")

    # THEN
    assert result.code == 400
    assert result.content == "Mot de passe trop faible"
    assert user_service.get_user_by_username("Louis") is None
    assert user_service.count_users() == 0


def test_create_two_user_success(user_service):
    # GIVEN
    user_service.create_user("Louis", "UnMotDePasseSecure*159")

    # WHEN
    result = user_service.create_user("louis", "UnMotDePasseSecure*159")

    # THEN
    assert result.code == 201
    assert result.content == "Utilisateur créé avec succès"
    first_user = user_service.get_user_by_username("Louis")
    second_user = user_service.get_user_by_username("louis")
    assert first_user.username == "Louis"
    assert second_user.username == "louis"


def test_authenticate_success(user_service):
    # GIVEN
    user_service.create_user("Louis", "UnMotDePasseSecure*159")

    # WHEN
    result = user_service.authenticate("Louis", "UnMotDePasseSecure*159")

    # THEN
    assert result.code == 200
    assert result.content == "Authentification réussie"


def test_authenticate_failure(user_service):
    # GIVEN
    user_service.create_user("Louis", "UnMotDePasseSecure*159")

    # WHEN
    result1 = user_service.authenticate("louis", "UnMotDePasseSecure*159")
    result2 = user_service.authenticate("Louis", "mauvais_mdp")

    # THEN
    assert result1.code == 401
    assert result2.code == 401
    assert result1.content == "Nom d'utilisateur ou mot de passe incorrect"
    assert result2.content == "Nom d'utilisateur ou mot de passe incorrect"


def test_change_password_success(user_service):
    # GIVEN
    user_service.create_user("Louis", "UnMotDePasseSecure*159")

    # WHEN
    result = user_service.change_password("Louis", "UnMotDePasseSecure*159",
                                          "AutreMotDePasseSecure*159")
    result_auth = user_service.authenticate("Louis", "AutreMotDePasseSecure*159")
    result_wrong_auth = user_service.authenticate("Louis", "UnMotDePasseSecure*159")

    # THEN
    assert result.code == 200
    assert result.content == "Mot de passe modifié avec succès"
    assert result_auth.code == 200
    assert result_wrong_auth.code == 401


def test_change_password_failure(user_service):
    # GIVEN
    user_service.create_user("Louis", "UnMotDePasseSecure*159")

    # WHEN
    result_wrong_password = user_service.change_password("Louis", "mauvais_mdp",
                                                         "159*AutreMotDePasseSecure")
    result_weak_password = user_service.change_password("Louis",
                                                        "UnMotDePasseSecure*159", "mdp")
    result_user_not_found = user_service.change_password("Alice",
                                                         "UnMotDePasseSecure*159",
                                                         "159*AutreMotDePasseSecure")
    result_auth = user_service.authenticate("Louis", "UnMotDePasseSecure*159")
    result_wrong_auth = user_service.authenticate("Louis", "159*AutreMotDePasseSecure")

    # THEN
    assert result_wrong_password.code == 401
    assert result_weak_password.code == 400
    assert result_user_not_found.code == 404
    assert result_auth.code == 200
    assert result_wrong_auth.code == 401


def test_change_username_success(user_service):
    # GIVEN
    user_service.create_user("Louis", "UnMotDePasseSecure*159")

    # WHEN
    result = user_service.change_username("Louis", "Bob")
    result_auth = user_service.authenticate("Bob", "UnMotDePasseSecure*159")
    result_wrong_auth = user_service.authenticate("Louis", "UnMotDePasseSecure*159")

    # THEN
    assert result.code == 200
    assert result.content == "Nom d'utilisateur modifié avec succès"
    assert result_auth.code == 200
    assert result_wrong_auth.code == 401


def test_change_username_failure(user_service):
    # GIVEN
    user_service.create_user("Louis", "UnMotDePasseSecure*159")
    user_service.create_user("Alice", "A159*MotDePasseSecure")

    # WHEN
    result_duplicate = user_service.change_username("Louis", "Alice")
    result_user_not_found = user_service.change_username("Bob", "Bob2")
    result_auth = user_service.authenticate("Louis", "UnMotDePasseSecure*159")
    result_wrong_auth = user_service.authenticate("Bob2", "159*AutreMotDePasseSecure")

    # THEN
    assert result_duplicate.code == 409
    assert result_user_not_found.code == 404
    assert result_auth.code == 200
    assert result_wrong_auth.code == 401