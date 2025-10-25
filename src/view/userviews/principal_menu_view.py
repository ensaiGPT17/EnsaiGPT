# view/userviews/principal_menu_view.py
from view.abstract_view import AbstractView
from InquirerPy import inquirer
from view.session import Session

class PrincipalMenuView(AbstractView):
    def __init__(self, message: str = ""):
        super().__init__(message)

    def choisir_menu(self):
        user = Session().user
        username = getattr(user, "username", "utilisateur")
        print("\n" + "-" * 50 + "\nAccueil\n" + "-" * 50 + "\n")
        choix = inquirer.select(
            message=f"Que voulez-vous faire {username} ?",
            choices=[
                "Démarrer une conversation",
                "Historique de conversation",
                "Se déconnecter",
                "Supprimer mon compte",
                "Afficher les statistiques"
            ],
        ).execute()

        if choix == "Démarrer une conversation":
            print("Fonctionnalité non implémentée")
            return self
        elif choix == "Historique de conversation":
            print("Fonctionnalité non implémentée")
            return self
        elif choix == "Se déconnecter":
            Session().user = None
            from view.home.home_view import HomeView
            return HomeView("Vous avez été déconnecté.")
        elif choix == "Supprimer mon compte":
            # exemple : déléguer au service utilisateur
            from service.user_service import UserService
            res = UserService().delete_account(user)
            status = res.code
            if status == 200:
                Session().user = None
                from view.home.home_view import HomeView
                return HomeView("Votre compte a été supprimé.")
            else:
                print("Impossible de supprimer le compte.")
                return self
