import discord
import random
from discord import app_commands
from discord.ext import commands
from main import printMessage

printMessage("Fun", "Chargement de l'extension : fun")

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.listMeme = [
            "https://klipy.com/gifs/greetings-PSr",
            "https://klipy.com/gifs/wake-up-meme-1",
            "https://klipy.com/gifs/dexter-james-doakes-5",
            "https://klipy.com/gifs/disgrace-didier-drogba",
            "https://klipy.com/gifs/british-cop-screaming-sad-2",
            "https://cdn.discordapp.com/attachments/892144268083355679/1510572691432935505/Capture_decran_2026-05-30_001249.gif",
            "https://tenor.com/view/dexter-gif-4569783388286649357",
        ]

    @app_commands.command(description="Envoie le même")
    async def send_meme(self, interaction: discord.Interaction):
        await interaction.response.send_message("https://klipy.com/gifs/greetings-PSr")


    @app_commands.command(description="Random meme, lol")
    async def random_meme(self, interaction: discord.Interaction):
        await interaction.response.send_message(random.choice(self.listMeme))

    @app_commands.command(name="pierre_feuille_ciseaux", description="Choisis une option")
    @app_commands.describe(choices="Pierre, feuille ou ciseaux")
    @app_commands.choices(choices=[
        app_commands.Choice(name="Rock", value="rock"),
        app_commands.Choice(name="Paper", value="paper"),
        app_commands.Choice(name="Scissors", value="scissors"),
    ])
    async def test_choose(self, interaction: discord.Interaction, choices: app_commands.Choice[str]):
        await interaction.response.send_message(f"Ton option : {choices.name} - {choices.value}")

    @app_commands.command(description="Choisi un nombre aléatoire")
    async def roll(self, interaction: discord.Interaction, sides: int = 6):
        if sides < 1:
            await interaction.response.send_message(f"Le nombre doit être supérieur à 1. Votre nombre : {sides}")
            return

        result = random.randint(1, sides)
        await interaction.response.send_message(f"Vous avez lancé un dé à {sides} faces et obtenu : {result}")

async def setup(bot):
    await bot.add_cog(Fun(bot))