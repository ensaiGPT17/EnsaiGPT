from view.abstract_view import AbstractView
from InquirerPy import inquirer
from view.session import Session

class ChangeConvParamsView(AbstractView):
    """
    Vue permettant de changer les paramètres d'une conversation LLM :
    max_tokens, top_p, temperature.
    
    Cette vue permet à l'utilisateur de personnaliser les paramètres de la conversation avec un modèle de langage.
    """
    def __init__(self, message: str = "", max_tokens: int = 4096,
                 top_p: float = 1.0, temperature: float = 0.7):
        """
        Constructeur pour initialiser les paramètres de la conversation.

        :param message: Message optionnel à afficher lors de l'initialisation.
        :param max_tokens: Nombre maximum de tokens générés, par défaut 4096.
        :param top_p: Paramètre de nucleus sampling, par défaut 1.0.
        :param temperature: Température de génération de texte, par défaut 0.7.
        """
        super().__init__(message)

        # Initialisation des paramètres de la conversation
        self.max_tokens = max_tokens  # Valeur par défaut : 4096
        self.top_p = top_p  # Valeur par défaut : 1.0
        self.temperature = temperature  # Valeur par défaut : 0.7

    def choisir_menu(self):
        """
        Affiche un menu interactif permettant à l'utilisateur de changer les paramètres de la conversation
        :max_tokens, top_p et temperature. Les nouveaux paramètres sont ensuite affichés et confirmés.
        """
        # Affichage d'un message d'introduction pour l'utilisateur
        print("\n" + "-"*50 + "\nModifier les paramètres de la conversation\n" + "-"*50 + "\n")
        
        # Affichage des messages explicatifs avant de demander les valeurs
        print("Modifiez les paramètres de la conversation :")
        print("-" * 50)

        # Modification du paramètre max_tokens
        print("\n>>> Nombre maximum de tokens générés :")
        print("Cela détermine la longueur maximale de la réponse générée.")
        self.max_tokens = inquirer.number(
            message=f"[Actuel : {self.max_tokens}] - Entrez un nouveau nombre de tokens (min 1) :",
            default=self.max_tokens,
            min_allowed=1
        ).execute()

        # Modification du paramètre top_p
        print("\n>>> Diversité des réponses : Top P (0.0 à 1.0)")
        print("Contrôlez la diversité des mots générés. Une valeur plus basse signifie plus de diversité.")
        self.top_p = inquirer.number(
            message=f"[Actuel : {self.top_p}] - Entrez la valeur de Top P (min 0.0, max 1.0) :",
            default=self.top_p,
            min_allowed=0.0,
            max_allowed=1.0,
            float_allowed=True
        ).execute()

        # Modification du paramètre temperature
        print("\n>>> Créativité des réponses : Temperature (0.0 à 1.0)")
        print("Une température plus élevée rend les réponses plus créatives et variées.")
        self.temperature = inquirer.number(
            message=f"[Actuel : {self.temperature}] - Entrez la valeur de Temperature (min 0.0, max 1.0) :",
            default=self.temperature,
            min_allowed=0.0,
            max_allowed=1.0,
            float_allowed=True
        ).execute()

        # Confirmation des modifications
        print("\nParamètres mis à jour avec succès :")
        print(f"max_tokens = {self.max_tokens}, top_p = {self.top_p}, temperature = {self.temperature}\n")

        # Retour au menu principal
        from view.userviews.discussion_view import DiscussionView
        return DiscussionView(f"Paramètres de la conversation mis à jour\n")

