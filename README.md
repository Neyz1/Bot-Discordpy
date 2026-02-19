# Bot Discord 

> **⚠️ IMPORTANT**  
> Ne jamais commiter votre token de bot dans des dépôts publics. Conservez‑le dans une variable d’environnement ou un fichier `.env` ignoré par Git.

---

## Table des matières

1. [Vue d’ensemble](#vue-densemble)
2. [Fonctionnalités](#fonctionnalites)
3. [Prérequis](#prerequis)
4. [Installation](#installation)
5. [Configuration](#configuration)
6. [Commandes](#commandes)
7. [Exécution du bot](#execution-du-bot)
8. [Développement & contribution](#developpement--contribution)
9. [Licence](#licence)

---

## Vue d’ensemble

Ce projet est un bot Discord écrit en Python avec **discord.py v2.x**.  
Il illustre :

- La prise en charge de commandes simples
- Les délais asynchrones (`asyncio.sleep`)
- Des utilitaires utilisateurs/membres (rôles, avatar, etc.)
- Un rappel simple via `tasks.loop`
- Le logging vers la console et optionnellement un canal Discord

N’hésitez pas à forker, ajuster ou étendre ce bot pour votre serveur !

---

## Fonctionnalités

| Fonction | Description |
|---------|-------------|
| **Commande de test** (`!test`) | Envoie un message de test dans le salon actuel et en DM. |
| **Compte à rebours** (`!decompte <seconds>`) | Compte les secondes données jusqu’à 0, une seconde par tick. |
| **Infos utilisateur** (`!userinfo`) | Affiche l’ID, le nom, le discriminant, le lien de l’avatar et les rôles de l’utilisateur. |
| **Rappel** (`!rappel <time> <message>`) | Envoie un rappel après la durée spécifiée (ex : `5m`, `2h`). |
| **Avatar** (`!avatar [@user]`) | Montre l’avatar du membre mentionné ou de celui qui a lancé la commande. |
| **Ping** (`!aaa`) | Renvoie la latence du bot en ms et le nombre de serveurs. |

---

## Prérequis

- Python 3.10+  
- Compte Discord & token de bot (créé via <https://discord.com/developers/applications>)

---

## Installation

```bash
# Cloner le dépôt
git clone https://github.com/votre-nom/anythingbot.git
cd anythingbot

# Créer un environnement virtuel (optionnel mais recommandé)
python -m venv .venv
source .venv/bin/activate  # Sous Windows : .venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt
