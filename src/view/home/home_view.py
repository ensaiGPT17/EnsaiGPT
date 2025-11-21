from view.abstract_view import AbstractView
from InquirerPy import inquirer


class HomeView(AbstractView):
    def __init__(self, message):
        """
        Constructeur de la classe HomeView.

        Parameters
        ----------
        message : str
            Message affiché en en-tête lors de l'affichage de la vue.
        """
        super().__init__(message)

    def choisir_menu(self):

        """Choix du menu suivant

        Return
        ------
        view
            Retourne la vue choisie par l'utilisateur dans le terminal
        """

        choix = inquirer.select(
            message="Que voulez-vous faire?",
            choices=["Se connecter", "Créer un compte", "Quitter"],
        ).execute()

        match choix:
            case "Se connecter":
                from view.home.sign_in_view import SignInView
                return SignInView("Connexion à l'application.")
            case "Créer un compte":
                from view.home.sign_up_view import SignUpView
                return SignUpView("Création de compte.")
            case "Quitter":
                pass
