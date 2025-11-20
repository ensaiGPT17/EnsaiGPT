from datetime import datetime
from typing import Optional


class Chat:
    """
    Classe représentant un chat créé par un utilisateur.

    Attributs
    ---------
    id_chat : int
        Identifiant unique du chat.
    id_user : int
        Identifiant de l'utilisateur propriétaire du chat.
    title : str
        Titre du chat.
    date_start : datetime
        Date et heure de création du chat.
    last_date : datetime
        Date et heure de la dernière activité dans le chat.
    max_tokens : int
        Nombre maximal de tokens autorisés pour les réponses générées.
    top_p : float
        Paramètre de filtrage nucleus sampling (0 à 1).
    temperature : float
        Paramètre influençant la créativité/variabilité des réponses (0 à 2).
    """
    def __init__(self,
                id_chat: int,
                id_user: int,
                title: str,
                date_start: datetime,
                last_date: datetime,
                max_tokens: int,
                top_p: float,
                temperature: float):
        """
        Constructeur de la classe Chat.

        Parameters
        ----------
        id_chat : int
            Identifiant unique du chat.
        id_user : int
            Identifiant de l'utilisateur propriétaire du chat.
        title : str
            Titre défini pour le chat.
        date_start : datetime
            Date et heure de création du chat.
        last_date : datetime
            Dernière date/heure de mise à jour du chat.
        max_tokens : int
            Limite maximale de tokens pour les réponses générées.
        top_p : float
            ??????????????????????????????
        temperature : float
            ????????????????????????????????
        """
        self.id_chat = id_chat
        self.id_user = id_user
        self.title = title
        self.date_start = date_start
        self.last_date = last_date
        self.max_tokens = max_tokens  # Assurez-vous qu'il s'agit d'un entier simple, pas un tuple.
        self.top_p = top_p  # Assurez-vous qu'il s'agit d'un float simple, pas un tuple.
        self.temperature = temperature
