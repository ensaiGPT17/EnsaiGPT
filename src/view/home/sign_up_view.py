from abstract_view import VueAbstraite
# from InquirerPy import inquirer


class SignUpView(VueAbstraite):
    def __init__(self, message):
        super().__init__(message)

    def choisir_menu(self):
        # Champ pour saisir l'identifiant
        username = inquirer.text(
            message="Nom d'utilisateur :"
        ).execute()

        # Champ pour saisir le mot de passe (masqué à l'écran)
        password = inquirer.secret(
            message="Mot de passe :"
        ).execute()
