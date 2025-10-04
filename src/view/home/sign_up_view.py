from view.abstract_view import AbstractView
from service.user_service import UserService
from InquirerPy import inquirer
from model.user import User

class SignUpView(AbstractView):
    def __init__(self, message):
        super().__init__(message)

    def choisir_menu(self):
        """Vue d'inscription (saisie de pseudo et mdp)"""

        print("\n" + "-" * 50 + "\nAccueil\n" + "-" * 50 + "\n")
        username = inquirer.text(message="Nom d'utilisateur :").execute()

        res_username_valide = UserService().is_username_available(username)
        if res_username_valide.code == 200:
            from home.home_view import HomeView
            return HomeView(f"Le pseudo {pseudo} est déjà utilisé.")

        password = inquirer.secret(
            message="Mot de passe :",
            validate=PasswordValidator(
                length=12,
                cap=True,
                number=True,
                message="Au moins 12 caractères, incluant une majuscule et un chiffre",
            ),
        ).execute()

        res_user_creation = UserService().create_user(username, password)

        if res_user_creation.code == 200 :
            message = (
                f"Votre compte {user.username} a été créé. Vous pouvez maintenant vous connecter."
            )
        else:
            message = "Erreur inconnue"

        from view.home import HomeView

        return HomeView(message)
