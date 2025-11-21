from abc import ABC, abstractmethod


class AbstractView(ABC):
    """
    Modèle abstrait représentant une vue de l'application.
    """

    def __init__(self, message=""):
        """
        Constructeur de la classe AbstractView.

        Parameters
        ----------
        message : str
            Message d'en-tête affiché lors du rendu de la vue.
        """
        self.message = message

    def nettoyer_console(self):
        """
        Insère des lignes vides dans la console afin de simuler un nettoyage visuel.
        """
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
