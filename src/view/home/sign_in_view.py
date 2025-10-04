from abstract_view import AbstractView
from InquirerPy import inquirer
from src.view.session import Session
from src.service.user_service import UserService


class SignInView(AbstractView):
    def __init__(self, message):
        super().__init__(message)

    """Vue de Connexion (saisie de pseudo et mdp)"""
    def choisir_menu(self):
        username = inquirer.text(message="Nom d'utilisateur :").execute()
        res_username_valide = UserService().is_username_available(username)
        if res_username_valide.code == 200:
            from home.home_view import HomeView
            return HomeView(f"Le pseudo {pseudo} est déjà utilisé.")

        mdp = inquirer.secret(
            message="Mot de passe :",
            validate=PasswordValidator(
                length=12,
                cap=True,
                number=True,
                message="Au moins 12 caractères, incluant une majuscule et un chiffre",
            ),
        ).execute()


        res_username_valide = UserService().create_user(username, )

        # Si le joueur a été trouvé à partir des ses identifiants de connexion
        if res_username_valide.code == 200 :
            message = f"Vous êtes connecté sous le pseudo {user.username}"
            Session().connexion(joueur)

            from userview.principal_menu_view import PrincipalMenuView

            return PrincipalMenuView(message)

        message = "Erreur inconnue"
        from view.home.home_view import HomeView

        return HomeView(message)
