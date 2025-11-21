from view.abstract_view import AbstractView
from InquirerPy import inquirer
from view.session import Session


class StartConversationView(AbstractView):
    def __init__(self, message: str = "Démarrer une conversation"):
        """
        Constructeur de la classe StartConversationView.

        Parameters
        ----------
        message : str
            Message optionnel à afficher lors de l'initialisation.
        """
        super().__init__(message)

    def choisir_menu(self):
        """
        Affiche le menu de démarrage de conversation et exécute l'action
        choisie par l'utilisateur.

        Returns
        -------
        AbstractView
            Vue suivante selon le choix de l'utilisateur.
        """
        user = Session().user
        username = user.username
        choix = inquirer.select(
            message=f"Que voulez-vous faire {username} ?",
            choices=[
                "Continuer",
                "Configurer les paramètres",
                "Retour"               
            ],
        ).execute()

        if choix == "Continuer":
            from view.userviews.first_message_view import FirstMessageView
            return FirstMessageView("Votre premier message")
        elif choix == "Configurer les paramètres":
            from view.userviews.change_params_view import ChangeConvParamsView
            return ChangeConvParamsView("Configurer les paramètres")
        elif choix == "Retour":
            from view.userviews.main_menu_view import MainMenuView
            return MainMenuView("Menu Principal")
