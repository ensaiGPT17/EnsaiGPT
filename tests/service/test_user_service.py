import pytest
from src.service.user_service import UserService
from tests.dao.mocks import UserDAOMock


@pytest.fixture
def user_service():
    return UserService(UserDAOMock())


def test_create_user_success(user_service):
    # GIVEN
    username = "Louis"
    password = "UnMotDePasseSecure*159"

    # WHEN
    result = user_service.create_user(username, password)

    # THEN
    assert result is True


def test_get_user_info_success(user_service):
    # GIVEN
    user_service.create_user("alice", "Mot*De*Passe*Alice123")

    # WHEN
    user = user_service.get_user_info(1)

    # THEN
    assert user["id_user"] == 1
    assert user["username"] == "alice"


def test_create_user_duplicate(user_service):
    # GIVEN
    user_service.create_user("Louis", "UnMotDePasseSecure*159")

    # WHEN
    result = user_service.create_user("Louis", "UnAutreMotDePasseSecure*159")

    # THEN
    assert result is False
    user_info = user_service.get_user_info(1)
    assert user_info["id_user"] == 1
    assert user_info["username"] == "Louis"
    assert user_service.user_dao.count_users() == 1


def test_create_two_user_success(user_service):
    # GIVEN
    user_service.create_user("Louis", "UnMotDePasseSecure*159")

    # WHEN
    result = user_service.create_user("louis", "UnMotDePasseSecure*159")

    # THEN
    assert result is True
    first_user_info = user_service.get_user_info(1)
    second_user_info = user_service.get_user_info(2)
    assert first_user_info["username"] == "Louis"
    assert first_user_info["id_user"] == 1
    assert second_user_info["username"] == "louis"
    assert second_user_info["id_user"] == 2


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
    result1 = user_service.authenticate("louis", "UnMotDePasseSecure*159")
    result2 = user_service.authenticate("Louis", "mauvais_mdp")

    # THEN
    assert result1 is False
    assert result2 is False
