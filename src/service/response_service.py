class ResponseService:
    """
    Classe représentant une réponse renvoyée par le système.

    Attributs
    ---------
    code : int
        Code de statut indiquant le résultat de l'opération.
    content : str
        Message ou contenu associé à la réponse.
    """
    def __init__(self, code: int, content: str):
        """
        Constructeur de ResponseService.

        Paramètres
        ----------
        code : int
            Code de statut de la réponse (par exemple 200 pour un succès).
        content : str
            Contenu ou message inclus dans la réponse.
        """
        self.code = code
        self.content = content
