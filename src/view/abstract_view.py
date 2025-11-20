from abc import ABC, abstractmethod


class AbstractView(ABC):
    """Modèle de Vue"""

    def __init__(self, message=""):
        self.message = message

    def nettoyer_console(self):
        """Insérer des lignes vides pour simuler un nettoyage"""
        for _ in range(30):
            print("")

    def afficher(self) -> None:
        """Affiche le message / en-tête. NE PAS appeler choisir_menu ici."""
        self.nettoyer_console()
        if self.message:
            print("\n" + "-" * 50 + f"\n{self.message}\n" + "-" * 50 + "\n")
        print()

    @abstractmethod
    def choisir_menu(self):
        """Choix du menu suivant de l'utilisateur"""
        raise NotImplementedError
