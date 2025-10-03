from abc import ABC, abstractmethod


class VueAbstraite(ABC):
    """Modèle de Vue"""

    def __init__(self, message=""):
        self.message = message

    def nettoyer_console(self):
        """Insérer des lignes vides pour simuler un nettoyage"""
        for _ in range(30):
            print("")

    def afficher(self) -> None:
        """Echappe un grand espace dans le terminal pour simuler
        le changement de page de l'application"""
        self.nettoyer_console()
        print(self.message)
        self.choisir_menu()
        print()

    @abstractmethod
    def choisir_menu(self):
        """Choix du menu suivant de l'utilisateur"""
        pass