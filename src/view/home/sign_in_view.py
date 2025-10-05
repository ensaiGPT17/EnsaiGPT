from view.abstract_view import AbstractView
from InquirerPy import inquirer
from service.user_service import UserService
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

        res = UserService().authenticate(username, password)
        status = res.code
        status == 200
        if status == 200:
            # récupérer l'objet user renvoyé si présent
            user = getattr(res, "user", None)
            if user is None:
                user = User(username=username)
            Session().user = user
            message = f"Vous êtes connecté sous le pseudo {user.username}"
            # import local pour éviter cycles
            from view.userviews.principal_menu_view import PrincipalMenuView
            return PrincipalMenuView(message)

        return HomeView("Erreur de connexion (pseudo ou mot de passe invalide)")
