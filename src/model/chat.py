from datetime import datetime


class Chat:
    def __init__(self, id_chat, id_user: int, title: str, max_tokens: int,
                 top_p: float, temperature: float, start_date: datetime,
                 last_date: datetime):
        self.id_conv = id_chat
        self.id_user = id_user
        self.title = title
        self.start_date = start_date
        self.last_date = last_date

        # Yassine, c'est Bruno, (je n'ai pas fait le travail à ta place
        # ce fichier existe depuis plus d'une semaine avant la repartition des taches)

        # TU PEUX ME POSER DES QUESTIONS SI CE N'EST PAS CLAIR
        
        # ICi on garde une trace de la liste de messages echangé entre
        # l'assistant et le user
        self.history: List[Dict[str, str]] = []

        # il s'agit d'une liste de dic, chaque dictionnaire 
        # est ceomme ceci: {'role': "assisant/user", 
        #                           "content": "contenu du message recu/envoyé"}

        self.max_tokens = max_tokens
        self.top_p = top_p
        self.temperature = temperature
