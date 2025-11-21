from view.abstract_view import AbstractView
from InquirerPy import inquirer
from view.session import Session
from service.chat_service import ChatService
from dao.chat_dao import ChatDAO


class StatisticView(AbstractView):
    def __init__(self, message: str = ""):
        """
        Constructeur de la classe StatisticView.

        Parameters
        ----------
        message : str
            Message optionnel à afficher lors de l'initialisation.
        """
        super().__init__(message)

    def choisir_menu(self):
        """
        Affiche les statistiques de l'utilisateur et propose de revenir
        au menu principal.

        Returns
        -------
        AbstractView
            Vue suivante selon le choix de l'utilisateur (ici le menu principal).
        """
        user = Session().user
        chat_dao = ChatDAO()
        chat_service = ChatService(chat_dao)

        stats = chat_service.get_user_statistics(user.id_user)

        print("Statistiques :\n")
        print(f"Nombre de conversations      : {stats['nb_conversations']}")
        print(f"Nombre total de messages     : {stats['nb_messages']}")
        print(f"Moyenne de messages par chat : {stats['avg_messages_per_chat']}")
        print(f"Date de la première conversation : {stats['first_chat_date']}")
        print(f"Date de la dernière conversation  : {stats['last_chat_date']}")

        choix_action = inquirer.select(
            message="",
            choices=["Retour"],
            qmark=""
        ).execute()

        if choix_action == "Retour":
            from view.userviews.main_menu_view import MainMenuView
            return MainMenuView("Menu principal")
