import os
from dotenv import load_dotenv
from api.chat_client import EnsaiGPTClient  # ton fichier client
from pprint import pprint

# Charge les variables d'environnement depuis le fichier .env
load_dotenv()  


client = EnsaiGPTClient(default_max_tokens = 500)
client.add_system_message("Tu es un assistant utile.")
response = client.generate("Bonjour, peux-tu me donner une citation inspirante ?")
pprint(response)

# La reponse reellement envoyée
print("---- ------ La reponse reellement envoyée ---- --------")
rep = response['choices'][0]['message']['content']
print(rep)

# ENSAI_GPT_HOST = "https://ensai-gpt-109912438483.europe-west4.run.app"