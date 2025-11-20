import os
import logging
import logging.config
import yaml


def initialiser_logs(nom: str):
    # Chemin absolu du fichier YAML à la racine du projet
    config_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "logging_config.yml"))

    if not os.path.exists(config_file):
        raise FileNotFoundError(f"Le fichier de configuration {config_file} est "
                                f"introuvable.")

    with open(config_file, encoding="utf-8") as stream:
        config = yaml.load(stream, Loader=yaml.FullLoader)

    # Crée le dossier logs à la racine du projet
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    logs_dir = os.path.join(project_root, "logs")
    os.makedirs(logs_dir, exist_ok=True)

    # Chemin absolu du fichier log
    log_file = os.path.join(logs_dir, "my_application.log")
    config["handlers"]["file"]["filename"] = log_file

    # Application de la config
    logging.config.dictConfig(config)

    logging.info("-" * 50)
    logging.info(f"Lancement {nom}")
    logging.info("-" * 50)
