# view/userviews/principal_menu_view.py
from view.abstract_view import AbstractView
from InquirerPy import inquirer
from view.session import Session
from service.chat_service import ChatService
from dao.chat_dao import ChatDAO

class MainMenuView(AbstractView):
    def __init__(self, message: str = ""):
        super().__init__(message)

    def choisir_menu(self):
        user = Session().user
        username = user.username
        chat_dao = ChatDAO()
        chat_service = ChatService(chat_dao)

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
            from view.userviews.start_conversation_view import StartConversationView
            return StartConversationView("Démarrer une conversation")
        elif choix == "Historique de conversation":
            from view.userviews.historic_conversation_view import HistoricConversationView
            return HistoricConversationView("Historique de conversation")
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
                elif status == 401 or status == 404:
                    return MainMenuView("Mot de passe erroné!\n Retour au Menu Princiapl")
            else:
                return MainMenuView("Retour au Menu Princiapl")

        elif choix == "Modifier mes identifiants":
            from view.userviews.change_credentials_view import ChangeCredentialsView
            return ChangeCredentialsView("Modifier mes identifiants")
        elif choix == "Afficher les statistiques":
            from view.userviews.statistics_view import StatisticView
            return StatisticView("Affichage des statistiques")
            
            
