from view.abstract_view import AbstractView
from InquirerPy import inquirer
from view.session import Session
from service.chat_service import ChatService
from dao.chat_dao import ChatDAO
from datetime import datetime
from model.chat import Chat

class SearchConversationView(AbstractView):
    def __init__(self, message: str = ""):
        super().__init__(message)

    def choisir_menu(self):
        user = Session().user
        username = user.username
        chat_dao = ChatDAO()
        chat_service = ChatService(chat_dao)

        print("\n" + "-" * 50 + "\nRechercher une conversation\n" + "-" * 50 + "\n")
        choix = inquirer.select(
            message=f"Que voulez-vous faire {username} ?",
            choices=[
                "Rechercher une conversation par mot-clé dans le titre",
                "Rechercher une conversation par date",
                "Retour"               
            ],
        ).execute()

        if choix == "Rechercher une conversation par mot-clé dans le titre":
            # demande du mot clé à l'utilisateur
            mot_cle = inquirer.text("Rentrez un mot-clé pour la recherche: ").execute()
            # appel a la fonction dans chat service qui renvoie une liste de conversations
            res = chat_service.search_chat_by_title(user.id_user, mot_cle)
            
            # si liste vide, aucune conversation trouvée 
            if res == [] : 
                from view.userviews.list_conversation_view import ListConversationView
                return ListConversationView(message="Aucune conversation trouvée", conv_list=res, last_view=1)

            # on bascule dans la vue liste conversations 
            from view.userviews.list_conversation_view import ListConversationView
            return ListConversationView(message="Voir l'historique de conversation", conv_list=res, last_view=1) 
            

        elif choix == "Rechercher une conversation par date":
            # demande de la date à l'utilisateur
            date = inquirer.text("Rentrez une date pour la recherche (YYYY-MM-DD): ").execute()
            # appel a la fonction dans chat service qui renvoie une liste de conversations
            res = chat_service.search_chat_by_date(user.id_user, date)

            if res == [] : 
                from view.userviews.list_conversation_view import ListConversationView
                return ListConversationView(message="Aucune conversation trouvée", conv_list=res, last_view=1)
            
            # on bascule vers la vue liste conversations
            from view.userviews.list_conversation_view import ListConversationView
            return ListConversationView(message="Voir l'historique de conversation", conv_list=res, last_view=1)
            
        elif choix == "Retour":
            from view.userviews.historic_conversation_view import HistoricConversationView
            return HistoricConversationView("Historique de conversation")