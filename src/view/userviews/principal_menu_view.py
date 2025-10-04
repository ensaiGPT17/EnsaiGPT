from abstract_view import AbstractView
from view.session import Session

class PrincipalMenuView(AbstractView):
    def __init__(self, message):
            super().__init__(message)

    def choisir_menu(self):

        """Menu de l'utilisateur

        Return
        ------
        view
            Retourne la vue choisie par l'utilisateur dans le terminal
        """

        print("\n" + "-" * 50 + "\nAccueil\n" + "-" * 50 + "\n")
        choix = inquirer.select(
            message=f"Que voulez-vous faire {Session().user.username}\n",
            choices=[
                "Démarrer une conversation", 
                "Historique de conversation", 
                "Se déconnecter", 
                "Supprimer mon compte"
                ],
        ).execute()

        match choix:
            case "Démarrer une conversation":
                # from view.home.sign_in_view import SignInView
                # return SignInView("Connexion à l'application")
                pass
            case "Historique de conversation":
                pass
            case "Se déconnecter":
                pass
            case "Supprimer mon compte"
                pass