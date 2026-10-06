import os

import discord
import random
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.all()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Commandes slash synchronisées : {len(synced)}")
    except Exception as e:
        print(e)

# src = open("/dcshim/discord.py", encoding="utf-8").read()
# mots = ["on_member_join", "member_join", "on_member", "dispatch"]
# for i, ligne in enumerate(src.splitlines(), 1):
#     if any(m in ligne for m in mots):
#         print(i, ":", ligne)

@bot.event
async def on_member_join(member):
    print(f"Test {member}")
    await member.send("Bienvenue à toi sur le serveur")

@bot.tree.command(name="ping", description="Réponse ?")
async def ping(interaction: discord.Interaction, text: str, number:int, boolean: bool = False) -> None:
    print(f"Texte : {text} ; {number} ; {boolean}")
    await interaction.response.send_message("Boom", delete_after=1.0)

@bot.tree.command(description="Envoie le même")
async def send_meme(interaction: discord.Interaction):
    await interaction.response.send_message("https://klipy.com/gifs/greetings-PSr")

listMeme = [
    "https://klipy.com/gifs/greetings-PSr",
    "https://klipy.com/gifs/wake-up-meme-1",
    "https://klipy.com/gifs/dexter-james-doakes-5",
    "https://klipy.com/gifs/disgrace-didier-drogba",
    "https://klipy.com/gifs/british-cop-screaming-sad-2",
    "https://cdn.discordapp.com/attachments/892144268083355679/1510572691432935505/Capture_decran_2026-05-30_001249.gif",
    "https://tenor.com/view/dexter-gif-4569783388286649357",
]

@bot.tree.command(description="Random meme, lol")
async def random_meme(interaction: discord.Interaction):
    await interaction.response.send_message(random.choice(listMeme))

print("Bot ready")

@bot.tree.command(description="Supprime les messages")
async def clear_commands(interaction: discord.Interaction, number: int):
    if number < 1 or number > 100:
        await interaction.response.send_message("Le nombre doit être compris entre 1 et 100.", ephemeral=True)
        return

    deleted = await interaction.channel.purge(limit=number)
    print(number)
    await interaction.response.send_message(f"{len(deleted)} messages supprimés.", ephemeral=True)

@bot.tree.command(name="test_choose", description="Choisis une option")
@app_commands.describe(choices="Pierre, feuille ou ciseaux")
@app_commands.choices(choices=[
    app_commands.Choice(name="Rock", value="rock"),
    app_commands.Choice(name="Paper", value="paper"),
    app_commands.Choice(name="Scissors", value="scissors"),
])
async def test_choose(interaction: discord.Interaction, choices: app_commands.Choice[str]):
    await interaction.response.send_message(f"Ton option : {choices.name} - {choices.value}")

bot.run(os.getenv("DISCORD_TOKEN"))
