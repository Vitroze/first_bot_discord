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

    @app_commands.command(name="info", description="Affiche des informations sur le bot.")
    async def info(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Informations sur le bot", color=discord.Color.blue())
        embed.add_field(name="Nom du bot", value=f"<@{self.bot.user.id}>", inline=False)
        embed.add_field(name="ID du bot", value=self.bot.user.id, inline=False)
        embed.add_field(name="Version de discord.py", value=discord.__version__, inline=False)
        embed.add_field(name="Latence", value=f"{round(self.bot.latency * 1000)} ms", inline=False)
        embed.add_field(name="Nombre de serveurs", value=len(self.bot.guilds), inline=False)
        embed.add_field(name="Nombre d'utilisateurs", value=len(set(self.bot.get_all_members())), inline=False)
        embed.set_footer(text=f"Demandé par {interaction.user}", icon_url=interaction.user.avatar.url)

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Utils(bot))