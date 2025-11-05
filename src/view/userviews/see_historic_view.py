from view.abstract_view import AbstractView
from InquirerPy import inquirer
from view.session import Session
from service.chat_service import ChatService
from dao.chat_dao import ChatDAO

class SeeHistoricView(AbstractView):
    def __init__(self, message: str = ""):
        super().__init__(message)

    def choisir_menu(self):
        user = Session().user
        username = user.username
        print("\n" + "-" * 50 + "\nHistorique de conversation\n" + "-" * 50 + "\n")

        # importation de la liste de conversation
        # conv_list = ChatService(ChatDAO()).
        conv_list = ...
        # Largeur totale pour la ligne (par exemple, 40 caractères)
        total_width = 40

        # Formatage de la liste des conversations avec un compteur i et des underscores ajustés
        formated_conv_list = []
        for i, conv in enumerate(conv_list, start=1):
            # Formatage du titre et ajout des underscores jusqu'à la largeur totale
            formatted_item = f"{i}- {conv.title[:20]}" + "_"*(total_width - len(conv.title[:20])) + f"{conv.last_date}"
            formated_conv_list.append(formatted_item)

        # Afficher la liste à l'utilisateur
        choix = inquirer.select(
            message="Sélectionne un titre et une date:",
            choices=formated_conv_list
        ).execute()

        print("Vous avez sélectionné:\n --->", choix)

        return self