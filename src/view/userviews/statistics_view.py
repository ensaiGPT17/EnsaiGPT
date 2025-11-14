from view.abstract_view import AbstractView
from InquirerPy import inquirer
from view.session import Session
from service.chat_service import ChatService
from dao.chat_dao import ChatDAO
from datetime import datetime
from model.chat import Chat

class StatisticView(AbstractView):
    def __init__(self, message: str = ""):
        super().__init__(message)

    def choisir_menu(self):
        user = Session().user
        username = user.username
        chat_dao = ChatDAO()
        chat_service = ChatService(chat_dao)

        print("\n" + "-" * 50 + "\nAfficher les statistiques\n" + "-" * 50 + "\n")
        choix = inquirer.select(
            message=f"Que voulez-vous faire {username} ?",
            choices=[
                "Afficher le nombre de conversations",
                "Afficher le nombre de messages envoyés",
                "Retour"               
            ],
        ).execute()

        if choix == "Afficher le nombre de conversations":
            chats = chat_service.get_chats_by_id_user(user.id_user)
            nb_conv = len(chats) if chats is not None else 0
            print (f"Nombre de conversations: {nb_conv}")
            choix_action = inquirer.select(
                    message=f"Que voulez-vous?",
                    choices=["Retour"]
                ).execute()

            if choix_action == "Retour":
                return self 

        elif choix == "Afficher le nombre de messages envoyés":
            nb_messages = chat_service.counts_user_message(user.id_user)
            print(f"Nombre de messages échangés au total:{nb_messages}")
            choix_action = inquirer.select(
                    message=f"Que voulez-vous?",
                    choices=["Retour"]
                ).execute()

            if choix_action == "Retour":
                return self 

        elif choix == "Retour":
            from view.userviews.main_menu_view import MainMenuView
            return MainMenuView("Retour au menu principal")