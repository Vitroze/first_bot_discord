import discord
from discord import app_commands
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="clear", description="Supprime un certain nombre de messages dans le salon actuel.")
    async def clear(self, interaction: discord.Interaction, amount: int):
        if not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message("Vous n'avez pas la permission de gérer les messages.", ephemeral=True)
            return

        if amount < 1:
            await interaction.response.send_message("Le nombre de messages à supprimer doit être supérieur à 0.", ephemeral=True)
            return

        deleted = await interaction.channel.purge(limit=amount)
        await interaction.response.send_message(f"{len(deleted)} messages ont été supprimés.", ephemeral=True)

    @app_commands.command(name="kick", description="Expulse un membre du serveur.")
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

        await member.kick(reason=reason)
        await interaction.response.send_message(f"{member.mention} a été expulsé du serveur.")

async def setup(bot):
    await bot.add_cog(Moderation(bot))