from view.abstract_view import AbstractView
from InquirerPy import inquirer
from service.user_service import UserService
from dao.user_dao import UserDAO
from view.session import Session
from view.home.home_view import HomeView


class SignInView(AbstractView):
    def __init__(self, message: str = ""):
        """
        Constructeur de la classe SignInView.

        Parameters
        ----------
        message : str, optional
            Message à afficher en en-tête de la vue.
        """
        super().__init__(message)

    def choisir_menu(self):
        """
        Gère le processus de connexion de l'utilisateur.

        Demande le nom d'utilisateur et le mot de passe,
        authentifie l'utilisateur via UserService,
        puis ouvre une Session en cas de succès.

        Returns
        -------
        AbstractView
            - MainMenuView si la connexion réussit,
            - HomeView si l'authentification échoue.
        """
        username = inquirer.text(message="Nom d'utilisateur :").execute()
        password = inquirer.secret(message="Mot de passe :").execute()

        user_dao = UserDAO()
        user_service = UserService(user_dao)

        res = user_service.authenticate(username, password)
        status = res.code

        if status == 200:
            # récupérer le user
            connected_user = user_service.get_user_by_username(username)

            # ouvir la session
            Session().connexion(user=connected_user)

            message = f"{res.content}\nVous êtes connecté sous le pseudo" \
                      f" {connected_user.username}"

            from view.userviews.main_menu_view import MainMenuView
            return MainMenuView(message)
        else:
            # status = 401
            # sinon, nom d'user ou mdp incorrect
            return HomeView(f"Erreur de connexion!\n{res.content}")
