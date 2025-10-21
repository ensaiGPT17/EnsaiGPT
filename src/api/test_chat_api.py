import os
from dotenv import load_dotenv
from chat_client import EnsaiGPTClient  # ton fichier client
from pprint import pprint

# Charge les variables d'environnement depuis le fichier .env
load_dotenv()  

# Maintenant ENSAI_GPT_HOST est disponible
client = EnsaiGPTClient()
client.add_system_message("Tu es un assistant utile.")
response = client.generate("Bonjour, peux-tu me donner une citation inspirante ?")
pprint(response)
