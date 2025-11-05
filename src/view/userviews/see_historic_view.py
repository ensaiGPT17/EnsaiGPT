from view.abstract_view import AbstractView
from InquirerPy import inquirer
from view.session import Session
from service.chat_service import ChatService
from dao.chat_dao import ChatDAO
from model.chat import Chat
from datetime import datetime

class SeeHistoricView(AbstractView):
    def __init__(self, message: str = "", conv_list = conv_list):
        super().__init__(message)
        self.conv_list = conv_list

    def choisir_menu(self):
        user = Session().user
        username = user.username
        print("\n" + "-" * 50 + "\nHistorique de conversation\n" + "-" * 50 + "\n")

        # importation de la liste de conversation
        # conv_list = ChatService(ChatDAO()).
        max_tokens = 4000
        top_p = 0.5
        temperature = 0.5

        conv_list = [
            Chat(50, 2, "Conversation sur l'IA et les technologies", 
                datetime.now(), datetime.now(), max_tokens, top_p, temperature),
            Chat(50, 2, "Projet Machine Learning", 
                datetime.now(), datetime.now(), max_tokens, top_p, temperature),
            Chat(50, 2, "Discussion sur les statistiques", 
                datetime.now(), datetime.now(), max_tokens, top_p, temperature),
            Chat(50, 2, "Analyse de données et Visualisation", 
                datetime.now(), datetime.now(), max_tokens, top_p, temperature)
        ]
        # Largeur totale pour la ligne (par exemple, 40 caractères)
        total_width = 60

        # Formatage de la liste des conversations avec un compteur i et des underscores ajustés
        formated_conv_list = []
        for i, conv in enumerate(conv_list, start=1):
            # Formatage de la date en accédant correctement à l'objet datetime dans le tuple
            formatted_date = conv.last_date[0].strftime("%Y-%m-%d %H:%M:%S")

            # Calculer le nombre d'underscores nécessaires
            num_underscores = total_width - len(f"{i}- {conv.title[:40]}") - len(formatted_date)
            
            # Si le titre est trop long, on peut ajuster la longueur
            formatted_item = f"{i}- {conv.title[:20]}" + "_" * num_underscores + f"{formatted_date}"
            
            formated_conv_list.append(formatted_item)

        # Afficher la liste à l'utilisateur
        choix = inquirer.select(
            message="Sélectionne un titre et une date:",
            choices=formated_conv_list
        ).execute()

        print("Vous avez sélectionné:\n --->", choix)

        return self