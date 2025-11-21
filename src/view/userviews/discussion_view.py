from view.abstract_view import AbstractView
from InquirerPy import inquirer
from view.session import Session
from model.message import Message
from model.chat import Chat


class DiscussionView(AbstractView):
    def __init__(self, chat: Chat, liste_message: list[Message]):
        """
        Constructeur de la classe DiscussionView.

        Parameters
        ----------
        chat : Chat
            Objet Chat contenant les informations de la conversation.
        liste_message : list[Message]
            Liste des messages échangés dans la conversation.
        """
        super().__init__('')
        self.conversation = [
            (message.role_author, message.content) for message in liste_message
        ]  # Liste de tuples (role, message)
        self.chat = chat
        self.liste_messages = liste_message

    def afficher_conversation(self):
        """
        Affiche la conversation complète dans la console.

        Les messages de l'assistant et de l'utilisateur sont affichés avec un label
        et séparés par des lignes.
        """
        print("\n" + "-"*50)
        print(f"Titre: {self.chat.title}".center(50))
        print("-"*50 + "\n")

        # Affichage de la conversation
        for role, msg in self.conversation:
            if role == "assistant":
                print("Assistant 🤖:")
                print(msg)
            elif role == "user":
                print("Vous 👤:")
                print(msg)
            print("-"*50)

    def choisir_menu(self):
        """
        Affiche le menu interactif de la discussion.

        L'utilisateur peut :
        - Envoyer un message et recevoir la réponse du modèle
        - Quitter la discussion et retourner au menu principal

        Returns
        -------
        AbstractView
            Vue suivante selon le choix de l'utilisateur.
        """
        user = Session().user
        username = user.username

        while True:
            self.afficher_conversation()

            choix = inquirer.select(
                message=f"Que voulez-vous faire {username} ?",
                choices=[
                    "Envoyer un message",
                    "Quitter la discussion"
                ],
            ).execute()

            if choix == "Envoyer un message":
                from service.chat_service import ChatService
                from dao.chat_dao import ChatDAO

                message_user = inquirer.text(message="Votre message :").execute()
                self.conversation.append(("user", message_user))

                chat_service = ChatService(ChatDAO())

                message_list = chat_service.send_message(
                    chat=self.chat,
                    history=self.liste_messages,
                    content=message_user
                )
                return DiscussionView(chat=self.chat, liste_message=message_list)

            elif choix == "Quitter la discussion":
                from view.userviews.main_menu_view import MainMenuView
                return MainMenuView("Retour au menu principal")
