from view.abstract_view import AbstractView
from InquirerPy import inquirer
from view.session import Session

class HistoricConversationView(AbstractView):
    def __init__(self, message: str = ""):
        super().__init__(message)

    def choisir_menu(self):
        user = Session().user
        username = user.username
        print("\n" + "-" * 50 + "\nHistorique de conversation\n" + "-" * 50 + "\n")
        choix = inquirer.select(
            message=f"Que voulez-vous faire {username} ?",
            choices=[
                "Voir l'historique",
                "Rechercher une conversation",
                "Retour"               
            ],
        ).execute()

        if choix == "Voir l'historique":
            from view.userviews.see_historic_view import SeeHistoricView
            return SeeHistoricView("Voir l'historique")
        elif choix == "Rechercher une conversation":
            from view.userviews.search_conversation_view import SearchConversationView
            return SearchConversationView("Rechercher une conversation")
        elif choix == "Retour":
            from view.userviews.main_menu_view import MainMenuView
            return MainMenuView("Menu Principal")