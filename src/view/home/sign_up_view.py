from dao.user_dao import UserDAO
from view.abstract_view import AbstractView
from InquirerPy import inquirer
from service.user_service import UserService
from view.home.home_view import HomeView


def is_valid_password(pw: str) -> bool:
    return (
        isinstance(pw, str)
        and len(pw) >= 6
        and any(c.isupper() for c in pw)
        and any(c.isdigit() for c in pw)
    )


class SignUpView(AbstractView):
    def __init__(self, message: str = ""):
        super().__init__(message)

    def choisir_menu(self):
        username = inquirer.text(message="Nom d'utilisateur :").execute()
        password = inquirer.secret(message="Mot de passe :").execute()
        password_confirm = inquirer.secret(message="Confirmez le mot de passe "
                                                   ":").execute()

        if password != password_confirm:
            return HomeView(f"Erreur : Les mots de passe ne correspondent pas.")

        user_dao = UserDAO()
        user_service = UserService(user_dao)

        res = user_service.create_user(username, password)
        status = res.code

        if status == 201:
            # utilisateur crée avec succes
            return HomeView(f"{res.content}\nVous pouvez vous connecter à présent!")
        elif status == 409:
            return HomeView(f"Erreur: {res.content}\nLe pseudo {username} est déjà "
                            f"utilisé.")
        elif status == 400:
            return HomeView(f"Erreur: {res.content}") 
        else:
            # erreur interne, status = 500
            return HomeView(f"{res.content}")
