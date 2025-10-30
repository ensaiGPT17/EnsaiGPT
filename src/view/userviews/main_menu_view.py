# view/userviews/principal_menu_view.py
from view.abstract_view import AbstractView
from InquirerPy import inquirer
from view.session import Session

class MainMenuView(AbstractView):
    def __init__(self, message: str = ""):
        super().__init__(message)

    def choisir_menu(self):
        user = Session().user
        username = user.username
        print("\n" + "-" * 50 + "\nMenu Principal\n" + "-" * 50 + "\n")
        choix = inquirer.select(
            message=f"Que voulez-vous faire {username} ?",
            choices=[
                "Démarrer une conversation",
                "Historique de conversation",
                "Afficher les statistiques",
                "Modifier mes identifiants",
                "Se déconnecter",
                "Supprimer mon compte"              
            ],
        ).execute()

        if choix == "Démarrer une conversation":
            print("Fonctionnalité non implémentée")
            from view.userviews.start_conversation_view import StartConversationView
            return StartConversationView("Démarrer une conversation")

            return self
        elif choix == "Historique de conversation":
            print("Fonctionnalité non implémentée")
            return self
        elif choix == "Se déconnecter":
            # Confirmation avant la déconnexion
            confirm = inquirer.confirm(
                message="Êtes-vous sûr de vouloir vous déconnecter ?",
                default=False,
            ).execute()

            if confirm:
                Session().deconnexion()
                from view.home.home_view import HomeView
                return HomeView("Vous avez été déconnecté.")
            else:
                print("\nDéconnexion annulée.\n")
                return self

        elif choix == "Supprimer mon compte":
            # exemple : déléguer au service utilisateur
            from service.user_service import UserService
            from dao.user_dao import UserDAO
            confirm = inquirer.confirm(
                message="Êtes-vous sûr de vouloir supprimer votre compte ?",
                default=False,
            ).execute()

            if confirm:
                user_dao = UserDAO()
                user_service = UserService(user_dao)
                #user = Session().user
                password = inquirer.secret(message="Rentrer votre mot de passe :").execute()
                res = user_service.delete_user(user.id_user, password)
                status = res.code

                if status == 500:
                    message = f"Echec!\n{res.content}"
                elif status == 200:
                    # status == 200, succes
                    Session().deconnexion()
                    message = f"{res.content}\nSuppression de compte réussi"

                    from view.home.home_view import HomeView
                    return HomeView(message)
                elif status == 400 or status == 404:
                    from view.userviews.main_menu_view import MainMenuView
                    return MainMenuView("Mot de passe erroné!\n Retour au Menu Princiapl")
            else:
                from view.userviews.main_menu_view import MainMenuView
                return MainMenuView("Retour au Menu Princiapl")

        elif choix == "Modifier mes identifiants":
            from view.userviews.change_credentials_view import ChangeCredentialsView
            return ChangeCredentialsView("Modifier mes identifiants")
        elif choix == "Afficher les statistiques":
            print("Fonctionnalitée non implémentée")
            return self

