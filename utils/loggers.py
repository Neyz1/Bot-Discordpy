import logging
import os

def connexion():
    log_path = os.path.join(os.path.dirname(__file__), "logs.txt")

    logging.basicConfig(
        filename=log_path,
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
        encoding="utf-8"
    )

connexion()

# Logger principal
logger = logging.getLogger("main")
logger.info("Démarrage de l'application")

def log_message(message: str):
    print(message)           # Affichage console
    logger.info(message)     # Écriture dans logs.txt

print("Logger configuré avec succès")