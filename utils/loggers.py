import logging
import os
from datetime import datetime

# Configuration du logger
logging.basicConfig(
    filename='logs.txt',  # Fichier de logs
    level=logging.DEBUG,   # Niveau de log
    format='%(asctime)s - %(levelname)s - %(message)s',  # Format
    encoding='utf-8'
)

# Logger principal
logger = logging.getLogger('main')
logger.info("Démarrage de l'application")

# Fonction pratique pour loguer un message personnalisé
def log_message(content: str):
    formatted = f"{content}"
    print(formatted)  # Affiche aussi dans la console
    logger.info(formatted)
    logger = logging.getLogger(__name__)
    logger.info(content)         # écrit aussi dans logs.txt



print("Logger configuré avec succès")