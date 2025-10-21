import requests
import json
from pprint import pprint

# === Configuration ===
BASE_URL = "https://ensai-gpt-109912438483.europe-west4.run.app"
ENDPOINTS = ["/openapi.json", "/generate"]

def test_endpoint(endpoint, method="GET", payload=None):
    """Teste un endpoint spécifique et affiche le statut et le contenu."""
    url = BASE_URL + endpoint
    print(f"\n🔍 Test de l’endpoint : {url}")
    
    try:
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=payload, timeout=15)
        else:
            raise ValueError("Méthode HTTP non supportée.")
        
        print(f"✅ Statut HTTP : {response.status_code}")
        
        try:
            data = response.json()
            pprint(data if len(str(data)) < 1000 else str(data)[:1000] + "...")

            message = data['choices'][0]['message']
            print(message)
        except json.JSONDecodeError:
            print("ℹ️ Réponse brute :", response.text[:500])

        return response.status_code, response
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur de connexion : {e}")
        return None, None

def main():
    """ print("=== Test complet de l’API ensaiGPT (HTTPS) ===")

    # Vérifier l’endpoint /openapi.json
    print("\n--- Test du fichier OpenAPI ---")
    test_endpoint("/openapi.json") 
    """

    # Tester le endpoint /generate avec un message test
    print("\n--- Test du endpoint /generate ---")
    payload = {
        "history": [
            {"role": "system", "content": "Tu es un assistant utile."},
            {"role": "user", "content": "Bonjour, peux-tu me donner une citation inspirante pour tester la connexion API ?"}
        ],
        "temperature": 0.7,
        "top_p": 1.0,
        "max_tokens": 150
    }

    code, response = test_endpoint("/generate", method="POST", payload=payload)

    if code == 200:
        print("\n✅ ✅ Connexion réussie et réponse générée avec succès !")
    else:
        print("\n⚠️ Problème détecté lors du test de génération.")

if __name__ == "__main__":
    main()
