import logging
import dotenv

from utils.log_init import initialiser_logs
from view.home.home_view import HomeView

if __name__ == "__main__":
    # On charge les variables d'envionnement
    dotenv.load_dotenv(override=True)

    initialiser_logs("Application")

    current_view = HomeView("Bienvenue")
    nb_erreurs = 0

    while current_view:
        if nb_erreurs > 2:
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

    # Lorsque l on quitte l application
    print("----------------------------------")
    print("Au revoir")

    logging.info("Fin de l'application")