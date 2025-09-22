import pytest
from src.service.user_service import UserService
from tests.dao.mocks import UserDAOMock


@pytest.fixture
def user_service():
    return UserService(UserDAOMock())


def test_get_user_info_not_found(user_service):
    # GIVEN : rien

    # WHEN
    result = user_service.get_user_info(1)

    # THEN
    assert result is None


def test_get_user_info_by_username_not_found(user_service):
    # GIVEN : rien

    # WHEN
    result = user_service.get_user_info_by_username("Inconnu")

    # THEN
    assert result is None


def test_create_user_success(user_service):
    # GIVEN
    username = "Louis"
    password = "UnMotDePasseSecure*159"

    # WHEN
    result = user_service.create_user(username, password)

    # THEN
    assert result is True
    assert user_service.get_user_info_by_username("Louis")["username"] == "Louis"


def test_create_user_duplicate(user_service):
    # GIVEN
    user_service.create_user("Louis", "UnMotDePasseSecure*159")

    # WHEN
    result = user_service.create_user("Louis", "UnAutreMotDePasseSecure*159")

    # THEN
    assert result is False
    user_info = user_service.get_user_info_by_username("Louis")
    assert user_info is not None
    assert user_service.count_users() == 1


def test_create_two_user_success(user_service):
    # GIVEN
    user_service.create_user("Louis", "UnMotDePasseSecure*159")

    # WHEN
    result = user_service.create_user("louis", "UnMotDePasseSecure*159")

    # THEN
    assert result is True
    first_user_info = user_service.get_user_info_by_username("Louis")
    second_user_info = user_service.get_user_info_by_username("louis")
    assert first_user_info["username"] == "Louis"
    assert second_user_info["username"] == "louis"


def test_authenticate_success(user_service):
    # GIVEN
    user_service.create_user("Louis", "UnMotDePasseSecure*159")

    # WHEN
    result = user_service.authenticate("Louis", "UnMotDePasseSecure*159")

    # THEN
    assert result is True


def test_authenticate_failure(user_service):
    # GIVEN
    user_service.create_user("Louis", "UnMotDePasseSecure*159")

    # WHEN
    result1 = user_service.authenticate("louis", "UnMotDePasseSecure*159")  #lowercase
    result2 = user_service.authenticate("Louis", "mauvais_mdp")

    # THEN
    assert result1 is False
    assert result2 is False
