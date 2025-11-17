import logging
import dotenv
import os

from utils.log_init import initialiser_logs
from view.home.home_view import HomeView
from utils.reset_database import ResetDatabase

if __name__ == "__main__":
    # Charger les variables d'environnement
    dotenv.load_dotenv(override=True)

    initialiser_logs("Application")

    INIT_DIR = os.path.join("data")
    if not os.path.exists(INIT_DIR):
        os.makedirs(INIT_DIR)  # créer le dossier data s'il n'existe pas

    INIT_FILE = os.path.join(INIT_DIR, ".db_initialized")
    if not os.path.exists(INIT_FILE):
        print("Initialisation de la base...")
        ResetDatabase().lancer(test_dao=False)
        open(INIT_FILE, "w").close()  # créer le fichier .db_initialized


    if not os.path.exists(INIT_FILE):
        print("Initialisation de la base...")

        # Initialiser le schéma principal
        ResetDatabase().lancer(test_dao=False)

        # Facultatif : initialiser un schéma test séparé
        # ResetDatabase().lancer(test_dao=True)

        open(INIT_FILE, "w").close()  # créer le fichier .db_initialized

    current_view = HomeView("Bienvenue")
    nb_erreurs = 0

    while current_view:
        if nb_erreurs > 5:
            print("Le programme recense trop d'erreurs et va s'arrêter")
            break
        try:
            # Affichage du menu
            current_view.afficher()

            # Affichage des choix possibles
            current_view = current_view.choisir_menu()
        except Exception as e:
            logging.error(f"{type(e).__name__} : {e}", exc_info=True)
            print(f"ERREUR : {type(e).__name__} - {e}")
            nb_erreurs += 1
            current_view = HomeView(
                "Une erreur est survenue, retour au menu principal.\n"
                "Consultez les logs pour plus d'informations."
            )

    # Fin de l'application
    print("----------------------------------")
    print("Au revoir")
    logging.info("Fin de l'application")
