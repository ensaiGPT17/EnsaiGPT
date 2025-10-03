from abstract_view import VueAbstraite
from InquirerPy import inquirer


class VueAcceuil(VueAbstraite):
    def __init__(self, message):
        super().__init__(message)

    def choisir_menu(self):

        """Choix du menu suivant

        Return
        ------
        view
            Retourne la vue choisie par l'utilisateur dans le terminal
        """

        print("\n" + "-" * 50 + "\nAccueil\n" + "-" * 50 + "\n")
        choix = inquirer.select(
            message="Que voulez-vous faire?",
            choices=["Se connecter", "Creer un compte", "Quitter"],
        ).execute()

        match choix:
            case "Se connecter":
                from view.accueil.connexion_view import VueConnexion
                return VueConnexion("Connexion à l'application")
            case "Creer un compte":
                from view.accueil.inscription_view import VueInscription
                return VueInscription("Création de compte joueur")
            case "Quitter":
                print("Vous avez cliqué sur: [Quitter]")