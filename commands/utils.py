import discord
from discord import app_commands
from discord.ext import commands
from main import printMessage

printMessage("Utils", "Chargement de l'extension : utils")

class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Vérifie la latence du bot.")
    async def ping(self, interaction: discord.Interaction):
        latency = round(self.bot.latency * 1000)  # Convertit la latence en millisecondes
        await interaction.response.send_message(f"Pong! Latence : {latency} ms")

async def setup(bot):
    await bot.add_cog(Utils(bot))