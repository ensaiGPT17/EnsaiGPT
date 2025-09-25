from src.view.abstract_view import AbstractView


class HomeView(AbstractView):
    def __init__(self, username):
        super().__init__()
        self.username = username

    def start(self):
        while True:
            print(f"Bienvenue sur votre tableau de bord, {self.username} !")
            choice = self.choose_menu()

            if choice == "1":
                self.display("Déconnexion...")
                break
            else:
                self.display("Choix invalide !")

    def choose_menu(self):
        print("1 - Quitter")
        return input("Choisissez une option: ")
