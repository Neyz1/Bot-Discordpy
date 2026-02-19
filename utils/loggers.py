import logging
import os
from datetime import datetime

def connexion():
    print("Connexion à la base de données...")

    # Chemin absolu vers le fichier log, au même niveau que ce script
    log_path = os.path.join(os.path.dirname(__file__), "logs.txt")

    # Crée le répertoire s’il n’existe pas (ici inutile car on écrit dans le même dossier)
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    logging.basicConfig(
        filename=log_path,
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
        encoding="utf-8"
    )

# Logger principal
logger = logging.getLogger('main')
logger.info("Démarrage de l'application")

# Fonction pratique pour loguer un message personnalisé
def log_message(ctx: str):
    #formatted = f"{content}"
    #print(formatted)  # Affiche aussi dans la console
   # logger.info(formatted)
  #  logger = logging.getLogger(__name__)
 #   logger.info(content)         # écrit aussi dans logs.txt
    # 1️⃣ Affichage en temps réel (console)
    print(ctx)

    # 2️⃣ Enregistrement dans le fichier
    logger(ctx)          # ← **c’est ce qui manquait**



print("Logger configuré avec succès")