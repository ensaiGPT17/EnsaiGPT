from abstract_view import AbstractView
from InquirerPy import inquirer
from user_service import UserService


class SignUpView(AbstractView):
    def __init__(self, message):
        super().__init__(message)

    def choisir_menu(self):
    """Vue d'inscription (saisie de pseudo et mdp)"""
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

        res_user_creation = UserService().create_user(username, )

        # Si le joueur a été trouvé à partir des ses identifiants de connexion
        if res_user_creation.code == 200 :
            message = f"Vous êtes connecté sous le pseudo {user.username}"
            Session().connexion(joueur)

            from userview.principal_menu_view import PrincipalMenuView

            return PrincipalMenuView(message)

        message = "Erreur inconnue"
        from view.home.home_view import HomeView

        return HomeView(message)
