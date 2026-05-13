from email import message
import time
import asyncio
from dotenv import load_dotenv
import os
import random

##################################   Downloader   ##############################################
from utils.Downloader.lin import *
from utils.Downloader.win import *
from tools.downloader import download_video


###############################   Scrapper CreatorsArea   ########################################

from tools.scrapper_creatorsArea import main
from tools.MySQL import get_last_id, get_new_offers
import schedule
import time

###############################  Logger  ########################################
from utils.loggers import log_message

from discord import Guild, guild
import discord

from discord.ext import commands, tasks # Pour les commandes et les tâches répétitives

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all(), help_command=None) # Le préfixe de commande est "!", donc les commandes seront déclenchées par des messages commençant par "!"



######################################################################################################

@tasks.loop(seconds=60) # Exécute la fonction toutes les 60 secondes
async def scrape_loop():
    # Récupérer le dernier ID connu avant le scraping
    last_known_id = get_last_id()

    # Lancer le scraping
    await asyncio.to_thread(main)

    # Récupérer les nouvelles offres ajoutées
    nouvelles_offres = get_new_offers(last_known_id)

    if nouvelles_offres:
        channel = bot.get_channel(1500600178011537488)
        for offre in nouvelles_offres:
            # Les colonnes de la DB dans des variables
            offre_id = offre["id"]
            offre_url = offre["url"]
            offre_pricing = offre["pricing"]
            offre_username = offre["username"]
            offre_tags = offre["tags"]
            offre_posted_at = offre["posted_at"]

            # Création de l'embed
            embed = discord.Embed(
                title=f"📢 Nouvelle offre : {offre_username}",
                url=offre_url,
                description=f"Une nouvelle mission vient d'être postée sur Creators Area !",
                color=0x8C1D7B,
                timestamp=discord.utils.utcnow()
            )
            embed.add_field(name="💰 Budget", value=f"{offre_pricing}€" if offre_pricing else "Non précisé", inline=True)
            embed.add_field(name="🏷️ Tags", value=offre_tags or "—", inline=True)
            embed.add_field(name="📅 Publié le", value=str(offre_posted_at)[:10], inline=True)
            embed.set_footer(text=f"ID #{offre_id}")

            await channel.send(embed=embed)
        
        await channel.send(f"✅ **{len(nouvelles_offres)}** nouvelle(s) offre(s) détectée(s) et envoyée(s) !")
    else:
        print("[ScrapeLoop] Aucune nouvelle offre détectée.")

       

@bot.event
async def on_ready():
    channel = bot.get_channel(1500600178011537488)
    fichiers = os.listdir("images")
    nombre = random.randint(1, len(fichiers)) # Génère un nombre aléatoire entre 1 et le nombre de fichiers dans le dossier "images"
    await channel.send("Le bot est prêt ! @everyone")
    await channel.send(file=discord.File(f"images/{nombre}.jpg"))

    await scrape_loop.start() # Démarre la boucle de scraping
  



######################################################################################################


@bot.command(
        help="Purge le channel en supprimant tous les messages et en recréant le channel avec le même nom."
)
async def clear(ctx):
    channel = ctx.channel
    guild = ctx.guild

    channel_name = channel.name

    await channel.delete()
   
    new_channel = await guild.create_text_channel(channel_name)
   
    log_message(f"Channel #{channel_name} purgé par {ctx.author} (ID NEW CHANNEL: {new_channel.id})")

    id = new_channel.id  # Récupere l'ID du nouveau channel
    channel = bot.get_channel(id) # Récupère le channel à partir de son ID

    await channel.send(f"Le channel {channel_name} a été purgé ! @everyone")


######################################################################################################

@bot.command(
        description='Test de la commande !test',
        help='Utilisez !test pour vérifier que le bot répond correctement.' ,
        hidden=False
)  
async def test(a):   # actif quand !aide
    await a.send('Test réussi !') # Envoie "Test réussi !" dans le même canal où la commande a été utilisée, lorsque l'utilisateur tape "!test"
    await a.author.send('Test réussi !') # Envoie "Test réussi !" en message privé à l'utilisateur qui a utilisé la commande "!test"
    log_message(f"{a.author} a utilisé !test dans #{a.channel}")


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
async def on_message(message):
    log_message(f'Message reçu de {message.author} : {message.content}')
    await bot.process_commands(message)


######################################################################################################

@bot.command()
async def ping(ctx):
    ping = round(bot.latency * 1000)  # latency en secondes → on convertit en ms
    a = bot
    await ctx.send(f"Pong 🏓 | {ping} ms")

#######################################    TEST     ##############################################


@bot.command(
        help="Test de la commande !test_embed",
)
async def test_embed(bot):
    message = bot.message  

    embed = discord.Embed(
        title="Salut toi !",
        description=f"Message envoyé dans {message.channel.mention}.",
        color=0x00BFFF,
        timestamp=discord.utils.utcnow()
    )
    
    embed.add_field(
        name="Auteur",
        value=f"{message.author}",
        inline=False
    )
    
    embed.add_field(
        name="Channel",
        value=message.channel.mention,
        inline=False
    )
    
    embed.add_field(
        name="Content",
        value=message.content if message.content else "No content",
        inline=False
    )

    embed.set_thumbnail(url=message.author.display_avatar.url)

    await bot.send(embed=embed)

#############################################################################




@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="📖 Aide du bot",
        description="Voici les commandes disponibles",
        color=0x3498db
    )

    embed.add_field(name="🧨 !clear", value="Reset un salon", inline=False) # Ajoute une ligne
    embed.add_field(name="📩 !sendmsg", value="Envoyer un message", inline=False)
    embed.add_field(name="🧠 !info", value="Infos serveur", inline=False)

    embed.set_footer(text=f"Demandé par {ctx.author}")

    await ctx.send(embed=embed)


#################################    Embed OFFRE    ##############################################


@bot.command(
        help="Affiche une offre d'emploi au format embed."
)
async def offre(ctx):
    embed = discord.Embed(
        title="Offre d'emploi : Développeur Python",
        description="Nous recherchons un développeur Python expérimenté pour rejoindre notre équipe dynamique.",
        color=0x8C1D7B,
        timestamp=discord.utils.utcnow()
    )

    embed.add_field(name="Entreprise", value="Tech Innovators Inc.", inline=False)
    embed.add_field(name="Lieu", value="Remote (France)", inline=False)
    embed.add_field(name="Budget", value="3000€ - 5000€ / mois", inline=False)
    embed.add_field(name="Tags", value="Python, Django, Remote", inline=False)

    embed.set_thumbnail(url="https://example.com/company_logo.png")

    await ctx.send(embed=embed)





#################################    DOWNLOADER    ##############################################
#  IDEES : 
#  1.Faire plusieurs boutons pour choisir la catégorie (chill, normal, salle)
#  2. Mettre la date comme sous dossier
#  3. Mettre progress bar (ex: "Téléchargement en cours : 50%") et mettre à jour le message à chaque étape du téléchargement
#  
#  ATTENTION: Bien mettre ytdlp 
#




class Extension(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

              
    @discord.ui.button(label="MP3", style=discord.ButtonStyle.green)
    async def button1(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer() 
        self.value = "MP3"

        self.stop()

    @discord.ui.button(label="MP4", style=discord.ButtonStyle.blurple)
    async def button2(self, interaction, button):
        await interaction.response.defer() 
        self.value = "MP4"
        self.stop()

    @discord.ui.button(label="Annuler", style=discord.ButtonStyle.danger)
    async def red(self, interaction, button):
        await interaction.response.defer() 
        self.value = False
        self.stop() # attends une interaction, puis stop la view (plus de boutons cliquables)


    
class playlist(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @discord.ui.button(label="Chill", style=discord.ButtonStyle.green)
    async def button1(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer() 
        self.value = "Chill"
        self.stop()

    @discord.ui.button(label="Normal", style=discord.ButtonStyle.blurple)
    async def button2(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer() 
        self.value = "Normal"
        self.stop()

    @discord.ui.button(label="Salle", style=discord.ButtonStyle.danger)
    async def button3(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer() 
        self.value = "Salle"
        self.stop()

    @discord.ui.button(label="Nope", style=discord.ButtonStyle.grey)
    async def button4(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer() 
        self.value = "Nope"
        self.stop()



@bot.command(
        help="Télécharge une vidéo YouTube en MP3 et l'envoie dans le channel."
)
async def download(ctx, url: str):
    embed = discord.Embed(
    title="Que souhaite-tu faire aujourd'hui ?",
    color=0x66D7FF,
    timestamp=discord.utils.utcnow()
    )
    embed.add_field(name="Playlist", value="Choisi dans quelle playlist l'entité sera enregistrée", inline=True)
    embed.add_field(name="Extension", value="Choisi l'extension de l'entité à télécharger", inline=True)

    nombre = random.randint(1, 1000)


    view = playlist()


    a = await ctx.send(embed=embed, view=view)
    await view.wait() # attend que l'utilisateur clique sur un bouton


    if view.value == "Chill":
        playlist_name = "Chill"
    elif view.value == "Normal":
        playlist_name = "Normal"
    elif view.value == "Salle":
        playlist_name = "Salle"
    else:
        playlist_name = "Nope"
   
    view = Extension()
    await a.edit(view=view)
    await view.wait()


    if view.value == "MP3":
        await ctx.send("La version MP3 est en cours de téléchargement", view=None)
        ext = "-x --audio-format mp3 --audio-quality 0"             
        process = download_video(url, ext, playlist_name) 
        
        
        await asyncio.to_thread(process.wait)
  
    elif view.value == "MP4":
        await ctx.send("La version MP4 est en cours de téléchargement", view=None)
        ext = '-f "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]" --merge-output-format mp4'  # Transforme la vidéo en mp4 avec la meilleur qualité dispo       
        process = download_video(url, ext, playlist_name) 

        await asyncio.to_thread(process.wait)

    elif view.value is False:
        await ctx.send("Annulation du téléchargement")
    
    await ctx.send(content="✅ Terminé")



###############################################################################


load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(DISCORD_TOKEN) 
print("Bot démarré avec succès")