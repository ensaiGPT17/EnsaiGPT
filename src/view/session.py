from datetime import datetime

from utils.singleton import Singleton
from model.user import User


class Session(metaclass=Singleton):
    """Stocke les données liées à une session.
    Cela permet par exemple de connaitre l'utilsiateur connecté à tout moment
    depuis n'importe quelle classe.
    Sans cela, il faudrait transmettre ce joueur entre les différentes vues.
    """

    def __init__(self):
        """Création de la session"""
        self.user = None
        self.connexion_date = None

    def connexion(self, user: User):
        """Enregistement des données en session"""
        self.user = user
        self.connexion_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def deconnexion(self):
        """Suppression des données de la session"""
        self.id_user = None
        self.connexion_date = None

    def afficher(self) -> str:
        """Afficher les informations de connexion"""
        res = "Actuellement en session :\n"
        res += "-------------------------\n"
        for att in list(self.__dict__.items()):
            res += f"{att[0]} : {att[1]}\n"

        return res