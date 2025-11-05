from view.abstract_view import AbstractView
from InquirerPy import inquirer
from view.session import Session

class HistoricConversationView(AbstractView):
    def __init__(self, message: str = ""):
        super().__init__(message)

    def choisir_menu(self):
        user = Session().user
        username = user.username
        print("\n" + "-" * 50 + "\nDémarrer une conversation\n" + "-" * 50 + "\n")
        choix = inquirer.select(
            message=f"Que voulez-vous faire {username} ?",
            choices=[
                "Continuer",
                "Configurer les paramètres",
                "Retour"               
            ],
        ).execute()

        if choix == "Continuer":
            from view.userviews.discussion_view import DiscussionView
            return DiscussionView("Discussion")
        elif choix == "Configurer les paramètres":
            from view.userviews.change_params_view import ChangeConvParamsView
            return ChangeConvParamsView("Configurer les paramètres")
        elif choix == "Retour":
            from view.userviews.main_menu_view import MainMenuView
            return MainMenuView("Menu Principal")