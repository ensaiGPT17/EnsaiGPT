from view.abstract_view import AbstractView
from InquirerPy import inquirer
from view.session import Session

class ChangeConvParamsView(AbstractView):
    """
    Vue permettant de changer les paramètres d'une conversation LLM :
    max_tokens, top_p, temperature.
    """
    def __init__(self, message: str = "", max_tokens: int = 4096,
                 top_p: float = 1.0, temperature: float = 0.7):
        super().__init__(message)

        self.max_tokens = max_tokens
        self.top_p = top_p
        self.temperature = temperature

    def choisir_menu(self):
        print("\n" + "-"*50 + "\nModifier les paramètres de la conversation\n" + "-"*50 + "\n")

        # max_tokens
        self.max_tokens = inquirer.number(
            message=f"Nombre maximum de tokens [{self.max_tokens}] :",
            default=self.max_tokens,
            min_allowed=1
        ).execute()

        # top_p
        self.top_p = inquirer.number(
            message=f"Top P (0.0 à 1.0) [{self.top_p}] :",
            default=self.top_p,
            min_allowed=0.0,
            max_allowed=1.0,
            float_allowed=True
        ).execute()

        # temperature
        self.temperature = inquirer.number(
            message=f"Temperature (0.0 à 1.0) [{self.temperature}] :",
            default=self.temperature,
            min_allowed=0.0,
            max_allowed=1.0,
            float_allowed=True
        ).execute()

        print("\nParamètres mis à jour avec succès :")
        print(f"max_tokens = {self.max_tokens}, top_p = {self.top_p}, temperature = {self.temperature}\n")

        # Retour au menu principal
        from view.userviews.principal_menu_view import MainMenuView
        return MainMenuView(f"Paramètres de la conversation mis à jour pour {Session().user.username}.")
