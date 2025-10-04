from view.abstract_view import AbstractView
from InquirerPy import inquirer
from view.session import Session
from service.user_service import UserService
from model.user import User


class SignInView(AbstractView):
    def __init__(self, message):
        super().__init__(message)

    
    def choisir_menu(self):
        """Vue de Connexion (saisie de pseudo et mdp)"""

        print("\n" + "-" * 50 + f"\nConnectez vous\n" + "-" * 50 + "\n")
        username = inquirer.text(message="Nom d'utilisateur :").execute()
        password = inquirer.secret(message="Mot de passe :").execute()


        res_user_auth = UserService().authenticate(username, password)

        # Si le joueur a été trouvé à partir des ses identifiants de connexion
        if res_user_auth.code == 200:
            message = f"Vous êtes connecté sous le pseudo {joueur.pseudo}"
            
            from view.menu_joueur_vue import MenuJoueurVue

            return MenuJoueurVue(message)

        message = "Erreur de connexion (pseudo ou mot de passe invalide)"
        from view.accueil.accueil_vue import AccueilVue

        return AccueilVue(message)