from src.controller.user_controller import UserController
from src.service.user_service import UserService
from src.dao.user_dao import UserDAO
from src.view.abstract_view import AbstractView
from tests.dao.mocks import UserDAOMock
from src.view.home_view import HomeView


class Run(AbstractView):
    def __init__(self):
        super().__init__()
        self.user_dao = UserDAOMock()  #à remplacer par ligne suivante pour vraie DAO
        # self.user_dao = UserDAO()
        self.user_service = UserService(self.user_dao)
        self.user_controller = UserController(self.user_service)

    def start(self):
        while True:
            print("Bienvenue dans l'appli !")
            choice = self.choose_menu()

            if choice == "1":
                self.handle_login()
            elif choice == "2":
                self.handle_register()
            elif choice == "3":
                self.display("Au revoir!")
                break
            else:
                self.display("Choix invalide!")

    def choose_menu(self):
        print("1 - Se connecter")
        print("2 - S'enregistrer")
        print("3 - Sortir")
        return input("Choisissez une option: ")

    def handle_login(self):
        username = input("Nom d'utilisateur: ")
        password = input("Mot de passe: ")
        if self.user_controller.login(username, password):
            self.display(f"Connexion réussie, bienvenue {username} !")
            home = HomeView(username)
            home.start()
        else:
            self.display("Nom d'utilisateur ou mot de passe incorrect.")

    def handle_register(self):
        username = input("Nom d'utilisateur: ")
        password = input("Mot de passe: ")
        if self.user_controller.register(username, password):
            self.display(f"Utilisateur {username} créé avec succès !")
        else:
            print("Erreur")
