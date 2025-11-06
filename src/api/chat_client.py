import os
import requests
from typing import List, Dict
from model.message import Message
from model.chat import Chat
import dotenv
import json

# Charger les variables d'environnement au début
dotenv.load_dotenv(override=True)

class EnsaiGPTClient:
    # Récupère l'URL de base de l'API depuis l'environnement
    host = os.environ.get("ENSAI_GPT_HOST")
    if not host:
        raise ValueError("L'URL de base de l'API doit être définie via 'host' ou 'ENSAI_GPT_HOST'.")

    def __init__(self, base_url: str = host):
        self.base_url = base_url.rstrip("/")  # Enlève le slash final si présent

    def generate(self, chat: Chat, history: List[Message]) -> str:
        """
        Envoie un message utilisateur au modèle et retourne la réponse générée.
        """

        # Vérification des types avant de créer le payload
        assert isinstance(chat.top_p, (int, float)), "top_p doit être un float ou int"
        assert isinstance(chat.temperature, (int, float)), "temperature doit être un float ou int"
        assert isinstance(chat.max_tokens, int), "max_tokens doit être un int"

        # Construire le payload
        payload = {
            "history": [{"role": message.role_author, "content": message.content} for message in history],
            "temperature": float(chat.temperature),  # S'assurer que c'est un float
            "top_p": float(chat.top_p),              # S'assurer que c'est un float
            "max_tokens": int(chat.max_tokens),      # S'assurer que c'est un int
        }

        # Vérification de la sérialisation du payload
        try:
            json_payload = json.dumps(payload)  # Essayer de sérialiser manuellement
            print(f"Payload JSON: {json_payload}")
        except TypeError as e:
            print(f"Erreur de sérialisation: {e}")

        try:
            response = requests.post(f"{self.base_url}/generate", json=payload, timeout=15)
            response.raise_for_status()  # Vérifie si la réponse est correcte
            answer = response.json()  # Récupère la réponse JSON

            assistant_answer_message = answer["choices"][0]["message"]["content"]
            return assistant_answer_message

        except requests.RequestException as e:
            # Affiche les détails de la réponse de l'API pour mieux comprendre l'erreur
            if e.response is not None:
                print(f"Erreur détaillée: {e.response.text}")  # Affiche la réponse du serveur
            raise RuntimeError(f"Erreur lors de l'appel à l'API ensaiGPT: {e}. URL: {self.base_url}/generate")


"""
# Main pour tester le client
from datetime import datetime

if __name__ == "__main__":
    # Créer une instance de Chat avec des valeurs fictives
    chat = Chat(
        id_chat=1,
        id_user=1,
        title="Test Chat",
        date_start=datetime.now(),
        last_date=datetime.now(),
        max_tokens=150,
        top_p=0.9,
        temperature=0.7
    )

    # Créer une liste de messages simulés
    history = [
        Message(id_message=1, id_chat=1, date_sending=datetime.now(), role_author="user", content="Bonjour, comment ça va ?"),
        Message(id_message=2, id_chat=1, date_sending=datetime.now(), role_author="assistant", content="Bonjour ! Je vais bien, merci. Et vous ?"),
        Message(id_message=3, id_chat=1, date_sending=datetime.now(), role_author="user", content="Je vais bien aussi, merci.")
    ]

    # Instancier le client EnsaiGPT
    client = EnsaiGPTClient()

    # Appeler la méthode generate pour obtenir une réponse de l'assistant
    try:
        assistant_response = client.generate(chat, history)
        print(f"Réponse de l'assistant: {assistant_response}")
    except Exception as e:
        print(f"Erreur: {e}")
"""