# view/userviews/discussion_view.py
from view.abstract_view import AbstractView
from InquirerPy import inquirer
from view.session import Session

class FirstMessageView(AbstractView):
    def __init__(self, message: str = ""):
        super().__init__(message)
        self.conversation = []  # liste de tuples (role, message)

    def afficher_conversation(self):
        print("\n" + "-"*50)
        print("Discussion".center(50))
        
        print("-"*50 + "\n")

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

            new_chat = chat_service.create_chat(message_user, user.id_user)
            message_list_of_new_chat = message_service.get_messages_by_chat(new_chat.id)
            
            message_list_of_new_chat = message_list_of_new_chat[1:]
            return DiscussionView(chat=new_chat, liste_message=message_list_of_new_chat, firt_time=1)
            
        elif choix == "Retour":
            from view.userviews.start_conversation_view import StartConversationView
            return StartConversationView(f"Retour au menu demarrer une conversation, {username}.")