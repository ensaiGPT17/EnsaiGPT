class User:
    """
    Classe représentant un utilisateur de l'application.

    Attributs
    ---------
    id_user : int
        Identifiant unique de l'utilisateur.
    username : str
        Nom d'utilisateur choisi pour la connexion.
    hashed_password : str
        Mot de passe de l'utilisateur, déjà haché pour des raisons de sécurité.
    """

    def __init__(self, id_user: int, username: str, hashed_password: str):
        """
        Constructeur de la classe User.

        Parameters
        ----------
        id_user : int
            Identifiant unique attribué à l'utilisateur.
        username : str
            Nom d'utilisateur de connexion.
        hashed_password : str
            Mot de passe haché de l'utilisateur.
        """
        self.id_user = id_user
        self.username = username
        self.hashed_password = hashed_password
