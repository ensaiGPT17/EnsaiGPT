from view.abstract_view import AbstractView
from InquirerPy import inquirer
from view.session import Session


class FirstMessageView(AbstractView):
    def __init__(
            self, message: str = "",
            max_tokens=512,
            top_p=1.0,
            temperature=0.7,
            system_message="Tu es un assistant utile."):
        """
        Constructeur de la classe FirstMessageView.

        Parameters
        ----------
        message : str
            Message optionnel à afficher lors de l'initialisation.
        max_tokens : int
            Nombre maximal de tokens générés pour la conversation.
        top_p : float
            Paramètre de nucleus sampling pour contrôler la diversité des réponses.
        temperature : float
            Paramètre de créativité des réponses.
        system_message : str
            Message système guidant le comportement de l'assistant.
        """

        super().__init__(message)
        self.conversation = []  # liste de tuples (role, message)
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.temperature = temperature
        self.system = system_message

    def afficher_conversation(self):
        """
        Affiche la conversation actuelle dans la console.

        Les messages de l'utilisateur et de l'assistant sont affichés
        avec des labels et séparés par des lignes.
        """
        print("\n" + "-" * 50)
        print("Discussion".center(50))

        print("-" * 50 + "\n")

        for role, msg in self.conversation:
            if role == "assistant":
                print("Assistant 🤖:")
            else:
                print("Vous 👤:")
            print(msg)
            print("-" * 50)

    def choisir_menu(self):
        """
        Affiche le menu interactif pour envoyer le premier message.

        L'utilisateur peut :
        - Envoyer un premier message et créer une nouvelle conversation
        - Retourner au menu précédent

        Returns
        -------
        AbstractView
            Vue suivante selon le choix de l'utilisateur.
        """
        user = Session().user
        username = user.username

        self.afficher_conversation()

        choix = inquirer.select(
            message=f"Que voulez-vous faire {username} ?",
            choices=[
                "Envoyer un premier message",
                "Retour"
            ],
        ).execute()

        if choix == "Envoyer un premier message":
            from service.chat_service import ChatService
            from dao.chat_dao import ChatDAO
            from service.message_service import MessageService
            from dao.message_dao import MessageDAO
            from view.userviews.discussion_view import DiscussionView

            message_user = inquirer.text(message="Votre message :").execute()
            self.conversation.append(("user", message_user))

            chat_service = ChatService(ChatDAO())
            message_service = MessageService(MessageDAO())

            new_chat = chat_service.create_chat(
                user_first_message_content=message_user,
                id_user=user.id_user,
                max_tokens=self.max_tokens,
                top_p=self.top_p,
                temperature=self.temperature,
                system_message=self.system
            )
            message_list_of_new_chat = message_service.get_messages_by_chat(
                new_chat.id_chat)

            message_list_of_new_chat = message_list_of_new_chat[1:]
            return DiscussionView(chat=new_chat, liste_message=message_list_of_new_chat)

        elif choix == "Retour":
            from view.userviews.start_conversation_view import StartConversationView
            return StartConversationView(
                f"Retour au menu démarrer une conversation, {username}.")
