# view/userviews/discussion_view.py
from view.abstract_view import AbstractView
from InquirerPy import inquirer
from view.session import Session

class DiscussionView(AbstractView):
    def __init__(self, message: str = "", conv_title = "" , firt_time = 0):
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
                message_user = inquirer.text(message="Votre message :").execute()
                self.conversation.append(("user", message_user))

                # Simulation de réponse de l’assistant (placeholder)
                message_assistant = f"Réponse à : '{message_user}'"
                self.conversation.append(("assistant", message_assistant))

            elif choix == "Quitter la discussion":
                from view.userviews.main_menu_view import MainMenuView
                return MainMenuView(f"Retour au menu principal, {username}.")