from view.abstract_view import AbstractView
from InquirerPy import inquirer
from service.user_service import UserService
from dao.user_dao import UserDAO
from view.session import Session
from view.home.home_view import HomeView
from model.user import User

class SignInView(AbstractView):
    def __init__(self, message: str = ""):
        super().__init__(message)

    def choisir_menu(self):
        print("\n" + "-" * 50 + f"\nConnectez vous\n" + "-" * 50 + "\n")
        username = inquirer.text(message="Nom d'utilisateur :").execute()
        password = inquirer.secret(message="Mot de passe :").execute()

        user_dao = UserDAO()
        user_service = UserService(user_dao)

        res = user_service.authenticate(username, password)
        status = res.code
        print(status)

        if status == 200:
            # récupérer l'objet user renvoyé si présent
            user = user_service.get_user_by_username(username)
            Session().user = user
            message = f"Vous êtes connecté sous le pseudo {user.username}"
            # import local pour éviter cycles
            from view.userviews.principal_menu_view import PrincipalMenuView
            return PrincipalMenuView(message)

        # sinon, nom d'user ou mdp incorrect
        return HomeView(f"Erreur de connexion {res.content}")
