from view.abstract_view import AbstractView
from service.user_service import UserService
from InquirerPy import inquirer
from model.user import User


# view/home/sign_up_view.py
from view.abstract_view import AbstractView
from InquirerPy import inquirer
from service.user_service import UserService
from view.home.home_view import HomeView

def is_valid_password(pw: str) -> bool:
    return (
        isinstance(pw, str)
        and len(pw) >= 6
        and any(c.isupper() for c in pw)
        and any(c.isdigit() for c in pw)
    )

class SignUpView(AbstractView):
    def __init__(self, message: str = ""):
        super().__init__(message)

    def choisir_menu(self):
        print("\n" + "-" * 50 + "\nInscrivez vous\n" + "-" * 50 + "\n")
        username = inquirer.text(message="Nom d'utilisateur :").execute()

        res = UserService().is_username_available(username)
        status = res.code
        status = 1
        if status != 200:
            return HomeView(f"Le pseudo {username} est déjà utilisé.")

        # Saisie du mot de passe avec validation manuelle
        while True:
            password = inquirer.secret(
                message="Mot de passe :",
                validate=PasswordValidator(
                    length=6,
                    cap=True,
                    number=True,
                    message="Au moins 12 caractères, incluant une majuscule et un chiffre",
                ),
            ).execute()
            if is_valid_password(password):
                break
            print("Mot de passe invalide — au moins 12 caractères, une majuscule et un chiffre.")

        res_user_creation = UserService().create_user(username, password)
        status = res_user_creation.code
        status = 200
        if status == 200:
            message = f"Votre compte {username} a été créé. Vous pouvez maintenant vous connecter."
        else:
            message = "Erreur inconnue lors de la création du compte."

        return HomeView(message)
