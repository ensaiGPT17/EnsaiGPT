import os
import logging
import dotenv

from utils.singleton import Singleton
from dao.db_connection import DBConnection
from utils.log_decorator import log


class ResetDatabase(metaclass=Singleton):
    """
    Réinitialisation de la base de données (mode normal ou mode test DAO)
    """

    @log
    def lancer(self, test_dao: bool = False):
        """Réinitialise le schéma de la base.
        Si test_dao=True : utilise le schéma dédié aux tests et pop_db_test.sql
        """
        if test_dao:
            print("Ré-initialisation de la base de données de TEST")
        else:
            print("Ré-initialisation de la base de données")
        # Charge le .env
        dotenv.load_dotenv(override=True)

        # Chemins absolus vers les fichiers SQL
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        init_db_path = os.path.join(BASE_DIR, "data", "init_db.sql")
        pop_db_path = os.path.join(BASE_DIR, "data", "pop_db.sql")
        init_db_test_path = os.path.join(BASE_DIR, "data", "init_db_test.sql")
        pop_db_test_path = os.path.join(BASE_DIR, "data", "pop_db_test.sql")

        # Choix du schéma et du fichier de peuplement
        if test_dao:
            init_path = init_db_test_path
            pop_path = pop_db_test_path
        else:
            init_path = init_db_path
            pop_path = pop_db_path

        # Vérification de l'existence des fichiers
        if not os.path.exists(init_path) or not os.path.exists(pop_path):
            raise FileNotFoundError(
                f"Le fichier SQL d'initialisation ou de peuplement est introuvable.\n"
                f"init_db: {init_path}\npop_db: {pop_path}"
            )

        # Lecture des fichiers SQL
        with open(init_path, encoding="utf-8") as f:
            init_db_sql = f.read()

        with open(pop_path, encoding="utf-8") as f:
            pop_db_sql = f.read()

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(init_db_sql)
                    cursor.execute(pop_db_sql)

        except Exception as e:
            logging.error(f"Erreur lors de la réinitialisation du schéma : {e}")
            raise

        logging.info(f"Schéma réinitialisé avec succès.")

        if test_dao:
            print("Ré-initialisation de la base de données de TEST - Terminée")
        else:
            print("Ré-initialisation de la base de données - Terminée")

        return True


if __name__ == "__main__":
    # Réinitialisation du schéma réel
    ResetDatabase().lancer(test_dao=False)
