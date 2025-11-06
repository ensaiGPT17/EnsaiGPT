from view.abstract_view import AbstractView
from InquirerPy import inquirer
from view.session import Session
from model.message import Message
from model.chat import Chat

class DiscussionView(AbstractView):
    def __init__(self, chat: Chat, liste_message: list[Message], first_time=1):
        super().__init__(chat)  # Remplacer 'message' par 'chat' si nécessaire
        self.conversation = [
            (message.role_author, message.content) for message in liste_message
        ]  # Liste de tuples (role, message)
        self.chat = chat
        self.liste_messages = liste_message

    def afficher_conversation(self):
        print("\n" + "-"*50)
        print(f"Titre: {self.chat.title}".center(50))
        print("-"*50 + "\n")

        # Affichage de la conversation
        for role, msg in self.conversation:
            if role == "assistant":
                print("Assistant 🤖:")
            else:
                print("Vous 👤:")
            print(msg)
            print("-"*50)

    def choisir_menu(self):
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
                """
                message_user = inquirer.text(message="Votre message :").execute()
                self.conversation.append(("user", message_user))

                # Simulation de réponse de l’assistant (placeholder)
                message_assistant = f"Réponse à : '{message_user}'"  # À remplacer par un vrai modèle si besoin
                self.conversation.append(("assistant", message_assistant))
                """
                
                from service.chat_service import ChatService
                from dao.chat_dao import ChatDAO
                from service.message_service import MessageService
                from dao.message_dao import MessageDAO
                from view.userviews.discussion_view import DiscussionView

                message_user = inquirer.text(message="Votre message :").execute()
                self.conversation.append(("user", message_user))

                chat_service = ChatService(ChatDAO())
                message_service = MessageService(MessageDAO())

                #new_chat = chat_service.create_chat(message_user, user.id_user)

                message_list = chat_service.send_message(
                    chat=self.chat,
                    history=self.liste_messages,
                    content=message_user
                )
                
                message_list = message_list[1:]
                return DiscussionView(chat=self.chat, liste_message=message_list, first_time=1)


            elif choix == "Quitter la discussion":
                from view.userviews.main_menu_view import MainMenuView
                return MainMenuView(f"Retour au menu principal, {username}.")
