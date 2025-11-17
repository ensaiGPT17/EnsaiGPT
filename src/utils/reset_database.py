import os
import logging
from unittest import mock
import dotenv

from utils.singleton import Singleton
from dao.db_connection import DBConnection
from utils.log_decorator import log


class ResetDatabase(metaclass=Singleton):
    """
    Réinitialisation de la base de données (mode normal ou mode test DAO)
    """

    @log
    def lancer(self, test_dao=False):
        """Réinitialise le schéma de la base.
        Si test_dao=True : utilise le schéma projet_test_dao et pop_db_test.sql
        """

        if test_dao:
            # On force le schéma dédié aux tests DAO
            mock.patch.dict(os.environ, {"POSTGRES_SCHEMA": "projet_test_dao"}).start()
            pop_data_path = "./data/pop_db_test.sql"
        else:
            pop_data_path = "./data/pop_db.sql"

        # Charge le .env pour récupérer POSTGRES_SCHEMA
        dotenv.load_dotenv()
        schema = os.environ["POSTGRES_SCHEMA"]

        # Scripts SQL
        with open("./data/init_db.sql", encoding="utf-8") as f:
            init_db_sql = f.read()

        with open(pop_data_path, encoding="utf-8") as f:
            pop_db_sql = f.read()

        # Recréation du schéma
        recreate_schema = f"""
            DROP SCHEMA IF EXISTS {schema} CASCADE;
            CREATE SCHEMA {schema};
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(recreate_schema)
                    cursor.execute(init_db_sql)
                    cursor.execute(pop_db_sql)

        except Exception as e:
            logging.error(e)
            raise

        return True


if __name__ == "__main__":
    ResetDatabase().lancer()
    ResetDatabase().lancer(test_dao=True)
