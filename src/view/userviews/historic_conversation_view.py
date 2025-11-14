from view.abstract_view import AbstractView
from InquirerPy import inquirer
from view.session import Session
from model.chat import Chat
from datetime import datetime
from service.chat_service import ChatService
from dao.chat_dao import ChatDAO

class HistoricConversationView(AbstractView):
    def __init__(self, message: str = ""):
        super().__init__(message)

    def choisir_menu(self):
        user = Session().user
        username = user.username
        chat_dao = ChatDAO()
        chat_service = ChatService(chat_dao)

        print("\n" + "-" * 50 + "\nHistorique de conversation\n" + "-" * 50 + "\n")
        choix = inquirer.select(
            message=f"Que voulez-vous faire {username} ?",
            choices=[
                "Voir l'historique",
                "Rechercher une conversation",
                "Supprimer toutes conversations",
                "Retour"               
            ],
        ).execute()

        if choix == "Voir l'historique":
            from view.userviews.list_conversation_view import ListConversationView
            res = chat_service.get_chats_by_id_user(user.id_user)

            return ListConversationView(message="Voir l'historique", conv_list=res, last_view=0)
        elif choix == "Rechercher une conversation":
            from view.userviews.search_conversation_view import SearchConversationView
            return SearchConversationView("Rechercher une conversation")
        elif choix == "Supprimer toutes conversations":
            res = chat_service.delete_all_chats(user.id_user)
            if res.code == 200:
                message = "Succès"
                from view.userviews.main_menu_view import MainMenuView
                return MainMenuView(message=message + "\n" + res.content)
            else:
                message = "Erreur interne"
                from view.userviews.main_menu_view import MainMenuView
                return MainMenuView(message=message + "\n" + res.content)
            
        elif choix == "Retour":
            from view.userviews.main_menu_view import MainMenuView
            return MainMenuView("Menu Principal")