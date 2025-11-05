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
            # appel a la fonction dans chat service : 
            #res = chat_service.search_chat_by_title(mot_cle)
            max_tokens = 4000
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
            ]   
            # si pas d'erreur : la fonction doit renvoyer liste des conversations correspondantes
            # on bascule dans la vue voir historique 

            from view.userviews.list_conversation_view import ListConversationView
            return ListConversationView(message="Voir l'historique de conversation", conv_list=res, last_view=1)
            
            # si erreur : a faire 


            print("fonctionnalité non implémentée")
            return self

        elif choix == "Rechercher une conversation par date":
            # demande de la date à l'utilisateur et convertir en datetime 
            date = inquirer.text("Rentrez une date pour la recherche (YYYY-MM-DD): ").execute()
            date_convertie = datetime.strptime(date, "%Y-%m-%d")
            # appel a la fonction dans chat service 
            res = chat_service.search_chat_by_date(date_convertie)

            # si pas d'erreur : la fonction doit renvoyer liste des conv 
    
            


            # si erreur : 

            print("fonctionnalité non implémentée")
            return self
        elif choix == "Retour":
            from view.userviews.historic_conversation_view import HistoricConversationView
            return HistoricConversationView("Historique de conversation")