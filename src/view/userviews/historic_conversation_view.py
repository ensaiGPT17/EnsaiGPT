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
                "Retour"               
            ],
        ).execute()

        if choix == "Voir l'historique":
            from view.userviews.list_conversation_view import ListConversationView
            res = chat_service.get_chats_by_id_user(user.id_user)
            
            """max_tokens = 4000
            top_p = 0.5
            temperature = 0.5

            res = [
            Chat(50, 2, "Conversation sur l'IA et les technologies", 
                datetime.now(), datetime.now(), max_tokens, top_p, temperature),
            Chat(50, 2, "Projet Machine Learning", 
                datetime.now(), datetime.now(), max_tokens, top_p, temperature),
            Chat(50, 2, "Discussion sur les statistiques", 
                datetime.now(), datetime.now(), max_tokens, top_p, temperature),
            Chat(50, 2, "Analyse de données et Visualisation", 
                datetime.now(), datetime.now(), max_tokens, top_p, temperature)
            ] """

            return ListConversationView(message="Voir l'historique", conv_list=res, last_view=0)
        elif choix == "Rechercher une conversation":
            from view.userviews.search_conversation_view import SearchConversationView
            return SearchConversationView("Rechercher une conversation")
        elif choix == "Retour":
            from view.userviews.main_menu_view import MainMenuView
            return MainMenuView("Menu Principal")