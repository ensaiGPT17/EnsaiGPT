import os
import requests
from typing import List, Dict, Optional

"""
Une bonne partie des methodes developpée ici vont disparaitre une fois le
SERVICE de la CONVERSATION plus complete.

Nous verrons par la suite comment nous allons les reorganiser dans CONV SERVICE.

C'est le cas de : 

    - add_assisatnt_message: ajouter un message de l'assistant,
    - add_user_message: ajouter un message du user, 

    - add_system_message: donne la phrase de base servant de guide à l'assistant
                            dans les reponses generées.

    - reset_history: vide la lsite des message echangé à envoyer à l'API
                    en plus du dernier message

    - Les parametres de l'assis. seront envoyés par CONV SERV, ce serait mieux.
    et ce sera CONV SER qui fera appel à l'API, notamment la classe
    EnsaiGPTClient de #chat_client.py
"""

class EnsaiGPTClient:

    def __init__(self, payload):
        self.payload = payload
    
    def generate(self) -> str:
        """
        Envoie un message utilisateur au modèle et retourne la réponse générée
        """


        try:
            response = requests.post(f"{self.base_url}/generate", json=self.payload, timeout=15)
            response.raise_for_status()
            answer = response.json()
            assistant_answer_message = answer["choices"][0]["message"]["content"]
            assistant_answer_message = {"role": "assistant", "content": assistant_answer_message}
            return assistant_answer_message
        except requests.RequestException as e:
            raise RuntimeError(f"Erreur lors de l'appel à l'API ensaiGPT: {e}")



class EnsaiGPTClient_:
    """
    Client pour interagir avec l'API ensaiGPT.
    
    Expose des méthodes pour envoyer des messages et récupérer les réponses du modèle.
    Gère l'historique des conversations pour les interactions multi-tours.
    """

    def __init__(
        self,
        host: Optional[str] = None,
        default_temperature: float = 0.7,
        default_top_p: float = 1.0,
        default_max_tokens: int = 512,
    ):
        """
        Args:
            host (str, optional): URL de base de l'API. Si None, lit la variable d'environnement 'ENSAI_GPT_HOST'.
            default_temperature (float): créativité par défaut
            default_top_p (float): filtrage nucleus sampling par défaut
            default_max_tokens (int): nombre max de tokens générés par défaut
        """
        self.host = host or os.environ.get("ENSAI_GPT_HOST")
        if not self.host:
            raise ValueError("L'URL de base de l'API doit être définie via 'host' ou 'ENSAI_GPT_HOST'.")

        self.base_url = self.host.rstrip("/")
        self.default_temperature = default_temperature
        self.default_top_p = default_top_p
        self.default_max_tokens = default_max_tokens

        # Historique de la conversation, qui sera dans CONV SERV
        self.history: List[Dict[str, str]] = []

    def add_system_message(self, content: str):
        """Ajoute un message system (instruction globale) à l'historique."""
        self.history.append({"role": "system", "content": content})

    def add_user_message(self, content: str):
        """Ajoute un message utilisateur à l'historique."""
        self.history.append({"role": "user", "content": content})

    def add_assistant_message(self, content: str):
        """Ajoute un message assistant à l'historique."""
        self.history.append({"role": "assistant", "content": content})

    def reset_history(self):
        """Réinitialise l'historique de la conversation."""
        self.history.clear()

    def generate(
        self,
        user_message: str,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        max_tokens: Optional[int] = None,
        stop: Optional[List[str]] = None,
    ) -> str:
        """
        Envoie un message utilisateur au modèle et retourne la réponse générée.

        Args:
            user_message (str): message utilisateur
            temperature (float, optional): créativité
            top_p (float, optional): filtrage nucleus
            max_tokens (int, optional): limite de tokens
            stop (List[str], optional): séquences d'arrêt

        Returns:
            str: réponse générée par le modèle
        """
        self.add_user_message(user_message)

        payload = {
            "history": self.history,
            "temperature": temperature if temperature is not None else self.default_temperature,
            "top_p": top_p if top_p is not None else self.default_top_p,
            "max_tokens": max_tokens if max_tokens is not None else self.default_max_tokens,
            "stop": stop,
        }

        try:
            response = requests.post(f"{self.base_url}/generate", json=payload, timeout=15)
            response.raise_for_status()
            answer = response.json()
            assistant_answer_message = answer["choices"][0]["message"]["content"]
            self.add_assistant_message(assistant_answer_message)
            return answer
        except requests.RequestException as e:
            raise RuntimeError(f"Erreur lors de l'appel à l'API ensaiGPT: {e}")

