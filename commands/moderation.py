from pyexpat.errors import messages

import discord
from discord import app_commands
from discord.ext import commands
from main import printMessage

printMessage("Moderation", "Chargement de l'extension : moderation")

@app_commands.guild_only()  # Uniquement sur le serveur
class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="clear", description="Supprime un certain nombre de messages dans le salon actuel.")
    @app_commands.checks.has_permissions(manage_messages=True) # Vérifie si l'utilisateur a la permission de gérer les messages
    async def clear(self, interaction: discord.Interaction, amount: app_commands.Range[int, 1, 100]):
        await interaction.response.defer(ephemeral=True)

        if amount < 1:
            await interaction.response.send_message("Le nombre de messages à supprimer doit être supérieur à 0.", ephemeral=True)
            return

        messages = await interaction.channel.history(limit=amount).flatten()
        await interaction.channel.delete_messages(messages)
        await interaction.followup.send(f"{len(messages)} messages supprimés.", ephemeral=True)

    @app_commands.command(name="kick", description="Expulse un membre du serveur.")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        if not interaction.user.guild_permissions.kick_members:
            await interaction.response.send_message("Vous n'avez pas la permission d'expulser des membres.", ephemeral=True)
            return

        if member == interaction.user:
            await interaction.response.send_message("Vous ne pouvez pas vous expulser vous-même.", ephemeral=True)
            return

        if member == self.bot.user:
            await interaction.response.send_message("Je ne peux pas m'expulser moi-même.", ephemeral=True)
            return

        await member.send(f"Vous avez été expulsé du serveur {interaction.guild.name} par {interaction.user.name}. Raison : {reason}")
        await member.kick(reason=reason)
        await interaction.response.send_message(f"{member.mention} a été expulsé du serveur.\n> Raison : {reason}")

async def setup(bot):
    await bot.add_cog(Moderation(bot))