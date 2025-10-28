import os
import logging
import logging.config
import yaml


def initialiser_logs(nom: str, config_file: str = "../logging_config.yml"):
    """
    Initialiser les logs à partir du fichier de configuration YAML.
    Args:
        nom (str): Nom du programme ou module pour le log.
        config_file (str): Chemin du fichier de configuration YAML.
    """
    # Création du dossier logs à la racine si non existant
    os.makedirs("logs", exist_ok=True)

    # Vérification de l'existence du fichier de config
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"Le fichier de configuration {config_file} est introuvable.")

    # Lecture du fichier YAML de configuration
    with open(config_file, encoding="utf-8") as stream:
        config = yaml.load(stream, Loader=yaml.FullLoader)

    logging.config.dictConfig(config)

    logging.info("-" * 50)
    logging.info(f"Lancement {nom}")
    logging.info("-" * 50)
