import logging
from abc import ABC, abstractmethod


class AbstractView(ABC):
    """Modèle de Vue"""

    def __init__(self):
        logging.info(type(self).__name__)

    def clean_console(self):
        """Insérer des lignes vides pour simuler un nettoyage"""
        for _ in range(30):
            print("")

    def display(self, message: str = "") -> None:
        """Affiche le message après avoir nettoyé l'écran"""
        self.clean_console()
        if message:
            print(message)
            print()

    @abstractmethod
    def choose_menu(self):
        """Choix du menu suivant de l'utilisateur"""
        pass