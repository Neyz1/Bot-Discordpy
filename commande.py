import time
import asyncio
from dotenv import load_dotenv
import os
from utils.loggers import log_message

import discord 
from discord.ext import commands, tasks # Pour les commandes et les tâches répétitives
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all()) # Le préfixe de commande est "!", donc les commandes seront déclenchées par des messages commençant par "!"

######################################################################################################

@bot.command(
        description='Test de la commande !test',
        help='Utilisez !test pour vérifier que le bot répond correctement.' ,
        hidden=False 
)  
async def test(a):   # actif quand !aide
    await a.send('Test réussi !') # Envoie "Test réussi !" dans le même canal où la commande a été utilisée, lorsque l'utilisateur tape "!test"
    await a.author.send('Test réussi !') # Envoie "Test réussi !" en message privé à l'utilisateur qui a utilisé la commande "!test"

######################################################################################################

@bot.command(
        description='Démarre un décompte de X secondes.',
        help='Utilisez !decompte <nombre_de_secondes> pour démarrer un décompte.',
        hidden=False
)
async def decompte(a, delai: int):
    await a.send(f'Le décompte de {delai} secondes commence !') # Envoie un message dans le même canal où la commande a été utilisée, indiquant que le décompte a commencé
    for i in range(delai, 0, -1): # commence à delai, puis delai-1, etc. jusqu'à 1
        await a.send(i)
        time.sleep(1) 
    await a.send('Le décompte est terminé !')

######################################################################################################

@bot.command(
        help="Affiche les informations de l'utilisateur qui a utilisé la commande." ,
)
async def userinfo(ctx):
    nom = ctx.author.name    
    id = ctx.author.id
    created = ctx.author.created_at
    joined = ctx.author.joined_at
    roles = ctx.author.roles
    await ctx.send(f'Votre nom d\'utilisateur est {nom} et votre ID est {id}. Vous avez rejoint le serveur le {joined} et votre compte a été créé le {created}. Vos rôles sont : {roles}')

######################################################################################################

@bot.command(
        help="Programme une alerte. " 
)
async def rappel(ctx, delai: int, *, message: str):
    await ctx.send(f'Alerte programmée dans {delai} secondes : {message}') 
    await asyncio.sleep(delai)  # pause non bloquante
    await ctx.send(f'Message programé : {message}')
    await ctx.author.send(f'Message programmé : {message}') 

######################################################################################################

@bot.command(
        help="Affiche l'avatar de l'utilisateur."
)
async def avatar(ctx, membre: discord.Member = None):
    membre =  membre or ctx.author  # Si aucun membre n'est spécifié, utilise l'auteur de la commande
    avatar_url = membre.avatar.url  # URL de l'avatar
    await ctx.send(f"Voici l'avatar de {membre.name} : {avatar_url}")

#######################################   LOGGER    ##############################################

@bot.event
async def on_message(content):
    log_message(f"[{content}")


######################################################################################################

@bot.command()
async def aaa(ctx):
    ping = round(bot.latency * 1000)  # latency en secondes → on convertit en ms
    a = bot
    await ctx.send(f"Pong 🏓 | {ping} ms")

######################################################################################################

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(DISCORD_TOKEN) 