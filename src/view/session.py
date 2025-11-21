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
        """
        Constructeur de la classe Session.

        Initialise une session vide, sans utilisateur connecté.
        
        Parameters
        ----------
        Aucun
        """
        self.user = None
        self.connexion_date = None

    def connexion(self, user: User):
        """
        Enregistre les informations d'un utilisateur lors de sa connexion.

        Parameters
        ----------
        user : User
            L'utilisateur qui vient de se connecter.
        """
        self.user = user
        self.connexion_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def deconnexion(self):
        """
        Supprime les informations de l'utilisateur lors de sa déconnexion.

        Réinitialise complètement la session.
        """
        self.id_user = None
        self.connexion_date = None

    def afficher(self) -> str:
        """
        Renvoie une représentation textuelle des informations de session.

        Returns
        -------
        str
            Informations détaillées concernant l'utilisateur connecté
            et la date de connexion.
        """
        res = "Actuellement en session :\n"
        res += "-------------------------\n"
        for att in list(self.__dict__.items()):
            res += f"{att[0]} : {att[1]}\n"

        return res