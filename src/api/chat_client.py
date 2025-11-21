import os
import requests
from typing import List
from model.message import Message
from model.chat import Chat
import dotenv

dotenv.load_dotenv(override=True)


class EnsaiGPTClient:
    # Récupère l'URL de base de l'API depuis l'environnement
    host = os.environ.get("ENSAI_GPT_HOST")
    if not host:
        raise ValueError("L'URL de base de l'API doit être définie via 'host' ou "
                         "'ENSAI_GPT_HOST'.")

    def __init__(self, base_url: str = host):
        """
        Constructeur de la classe EnsaiGPTClient.

        Parameters
        ----------
        base_url : str
            URL de base de l’API EnsaiGPT utilisée pour envoyer les requêtes.
        """
        self.base_url = base_url.rstrip("/")  # Enlève le slash final si présent

    def generate(self, chat: Chat, history: List[Message]) -> str:
        """
        Envoie un message utilisateur au modèle et retourne la réponse générée.

        Parameters
        ----------
        chat : Chat
            Objet contenant les paramètres de génération (temperature, top_p, max_tokens).
        history : List[Message]
            Liste des messages précédents de la conversation, utilisés comme contexte.

        Returns
        -------
        str
            Contenu textuel de la réponse générée par le modèle.
        """

        # Vérification des types avant de créer le payload
        assert isinstance(chat.top_p, (int, float)), "top_p doit être un float ou int"
        assert isinstance(chat.temperature, (int, float)), "temperature doit être un " \
                                                           "float ou int"
        assert isinstance(chat.max_tokens, int), "max_tokens doit être un int"

        # Construire le payload
        payload = {
            "history": [{"role": message.role_author, "content": message.content} for
                        message in history],
            "temperature": float(chat.temperature),  # S'assurer que c'est un float
            "top_p": float(chat.top_p),              # S'assurer que c'est un float
            "max_tokens": int(chat.max_tokens),      # S'assurer que c'est un int
        }
        
        try:
            response = requests.post(f"{self.base_url}/generate", json=payload,
                                     timeout=15)
            response.raise_for_status()  # Vérifie si la réponse est correcte
            answer = response.json()  # Récupère la réponse JSON

            assistant_answer_message = answer["choices"][0]["message"]["content"]
            return assistant_answer_message

        except requests.RequestException as e:
            # Affiche les détails de la réponse de l'API pour mieux comprendre l'erreur
            if e.response is not None:
                print(f"Erreur détaillée: {e.response.text}")  # réponse du serveur
            raise RuntimeError(f"Erreur lors de l'appel à l'API ensaiGPT: {e}. URL:"
                               f" {self.base_url}/generate")
