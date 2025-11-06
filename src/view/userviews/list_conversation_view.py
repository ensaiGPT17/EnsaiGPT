from view.abstract_view import AbstractView
from InquirerPy import inquirer
from view.session import Session
from service.chat_service import ChatService
from dao.chat_dao import ChatDAO
from model.chat import Chat
from datetime import datetime
from service.message_service import MessageService
from dao.message_dao import MessageDAO

class ListConversationView(AbstractView):
    def __init__(self, message: str = "", conv_list=None, last_view = 0):
        super().__init__(message)
        self.conv_list = conv_list if conv_list is not None else []
        self.last_view = last_view

    def choisir_menu(self):
        user = Session().user
        username = user.username
        print("\n" + "-" * 50 + "\nHistorique de conversation\n" + "-" * 50 + "\n")

        # Formatage de la liste des conversations avec un compteur i et des underscores ajustés

        total_width = 80
        formated_conv_list = []
        for i, conv in enumerate(self.conv_list, start=1):
            # Assurer que la date soit un objet datetime
            if isinstance(conv.last_date, tuple):  # Si c'est un tuple
                formatted_date = conv.last_date[0].strftime("%Y-%m-%d %H:%M:%S")
            else:
                formatted_date = conv.last_date.strftime("%Y-%m-%d %H:%M:%S")
            
            # Calculer le nombre d'underscores nécessaires pour aligner la date
            num_underscores = total_width - len(f"{i}- {conv.title[:40]}") - len(formatted_date)
            
            # Si le titre est trop long, le tronquer à 40 caractères (ou toute autre valeur que tu préfères)
            formatted_item = f"{i}- {conv.title[:40]}" + "_" * num_underscores + f"{formatted_date}"
            
            formated_conv_list.append(formatted_item)
        formated_conv_list.append("Retour")

        # Afficher la liste à l'utilisateur et lui permettre de choisir une conversation
        choix = inquirer.select(
            message="Sélectionne un titre et une date:",
            choices=formated_conv_list
        ).execute()

        if choix == "Retour":
            if self.last_view == 0:
                from view.userviews.historic_conversation_view import HistoricConversationView
                return HistoricConversationView("Retour au menu historique")
            else:
                from view.userviews.search_conversation_view import SearchConversationView
                return SearchConversationView("Retour au menu de recherche")
        else: 
            message_dao = MessageDAO()
            message_service = MessageService(message_dao)
            # si on selectionne une conversation : afficher la conv et pouvoir la reprendre
            # Récupérer l'index de la conversation sélectionnée
            selected_conv_index = formated_conv_list.index(choix)
            selected_conv = self.conv_list[selected_conv_index]  # Récupérer l'objet Chat complet
            
            choix_action = inquirer.select(
                message=f"Que voulez-vous faire avec la conversation '{selected_conv.title}' ?",
                choices=["Reprendre la discussion", "Supprimer la conversation"]
            ).execute()

            if choix_action=="Reprendre la discussion":
                # Récupérer l'ID du chat
                chat_id = selected_conv.id_chat 
                # on recupere la liste des messages deja envoyes 
                messages_envoyes = message_service.get_messages_by_chat(id_chat=chat_id)
                from view.userviews.discussion_view import DiscussionView
                return DiscussionView(selected_conv, messages_envoyes)

            else : 
                chat_dao = ChatDAO()
                chat_service = ChatService(chat_dao)
                chat_id = selected_conv.id_chat 
                res = chat_service.delete_chat(chat_id)
                if res.code == 200 : 
                    from view.userviews.main_menu_view import MainMenuView
                    message = f"{res.content}"
                    return MainMenuView(message)
                else:
                    from view.userviews.historic_conversation_view import HistoricConversationView
                    message = f"{res.content}"
                    return HistoricConversationView(message)

        # Afficher la conversation sélectionnée
        print("Vous avez sélectionné:\n --->", choix)

        # Retourner à la vue actuelle pour éventuellement effectuer d'autres actions
        return self
