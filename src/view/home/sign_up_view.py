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
        """
        Constructeur de la classe SignUpView.

        Parameters
        ----------
        message : str, optional
            Message affiché en en-tête lors de l'affichage de la vue.
        """
        super().__init__(message)

    def choisir_menu(self):
        """
        Gère le processus d'inscription d'un nouvel utilisateur.

        Demande le nom d'utilisateur ainsi que deux saisies du mot de passe,
        vérifie leur correspondance puis tente de créer le nouvel utilisateur
        via le UserService.

        Returns
        -------
        AbstractView
            - HomeView avec un message de succès si l’inscription réussit,
            - HomeView avec un message d’erreur si un problème survient
              (pseudo déjà pris, mot de passe insuffisant ou erreur interne).
        """
        username = inquirer.text(message="Nom d'utilisateur :").execute()
        print("Le mot de passe doit contenir au moins 8 caractères, ainsi qu'une "
              "majuscule, une miniscule, un chiffre et un caractère spécial.")
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
