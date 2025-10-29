from view.abstract_view import AbstractView
from InquirerPy import inquirer
from view.session import Session
from dao.user_dao import UserDAO
from service.user_service import UserService


class ChangeCredentialsView(AbstractView):
    def __init__(self, message: str = ""):
        super().__init__(message)

    def choisir_menu(self):
        user = Session().user
        username = user.username
        user_dao = UserDAO()
        user_service = UserService(user_dao)

        print("\n" + "-" * 50 + "\nModifier mes identifiants\n" + "-" * 50 + "\n")
        choix = inquirer.select(
            message=f"Que voulez-vous faire {username} ?",
            choices=[
                "Changer nom d'utilisateur",
                "Changer mon mot de passe",
                "Retour"               
            ],
        ).execute()

        if choix == "Changer nom d'utilisateur":
            # demader mdp
            password = inquirer.secret(message="Rentrer votre mot de passe :").execute()
            res = user_service.authenticate(username, password)

            if res.code == 200:
                # user confirmé, il peut changer le USERNAME
                print("Fonctionnalité non implémentée")
                return self
            else:
                from view.userviews.main_menu_view import MainMenuView
                return MainMenuView("Mot de passe erronné! Retour au Menu Principal")

        elif choix == "Changer mon mot de passe":
            # demader mdp
            password = inquirer.secret(message="Rentrer votre mot de passe actuel:").execute()
            res = user_service.authenticate(username, password)

            if res.code == 200:
                # user confirmé, il peut changer le MOT DE PASSE
                print("Fonctionnalité non implémentée")
                return self
            else:
                from view.userviews.main_menu_view import MainMenuView
                return MainMenuView("Mot de passe erronné! Retour au Menu Principal")
        elif choix == "Retour":
            from view.userviews.main_menu_view import MainMenuView
            return MainMenuView("Menu Principal")