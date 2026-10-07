from datetime import timedelta
import discord
from discord import app_commands
from discord.ext import commands
from main import printMessage
import random

printMessage("Utils", "Chargement de l'extension : utils")

CHANNEL_ANNOUNCE = 858647590337118228

class RouletteView(discord.ui.View):

    def __init__(self, player1_id: int, player2_id: int, who_play: int = None):
        super().__init__(timeout=None)  # No timeout for the view
        self.player1_id = player1_id
        self.player2_id = player2_id
        self.who_play = who_play if who_play is not None else player1_id  # Default to player1's turn
        self.bullet_max = 6

    @discord.ui.button(label="Tirer", style=discord.ButtonStyle.red, custom_id="roulette_button")
    async def button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.bullet_max <= 0:
            await interaction.response.send_message("Le jeu est terminé. Il n'y a plus de balles restantes.", ephemeral=True)
            return

        # Extract the user IDs and interaction ID from the button's custom_id
        player1_id, player2_id, who_play = self.player1_id, self.player2_id, self.who_play

        # Check if the user who clicked the button is one of the players
        if interaction.user.id not in [player1_id, player2_id]:
            await interaction.response.send_message("Vous n'êtes pas autorisé à jouer à cette partie de roulette russe.", ephemeral=True)
            return

        # WHo play ?
        if interaction.user.id != int(who_play):
            await interaction.response.send_message("Ce n'est pas votre tour de jouer.", ephemeral=True)
            return

        # Determine if the player loses or survives
        bullet_position = random.randint(1, self.bullet_max)
        if bullet_position == 1:
            # Player loses
            await interaction.response.send_message(f"{interaction.user.mention} a tiré et a perdu ! 💀", ephemeral=False, delete_after=2)

            # Update the embed to show the game is over
            embed = interaction.message.embeds[0]
            embed.title = f"Roulette Russe ({self.bullet_max - 1} Balles restantes)"
            embed.color = discord.Color.dark_red()
            embed.set_field_at(2, name="A qui le tour ?", value=f"Le jeu est terminé. {interaction.user.mention} a perdu.", inline=False)

            try:
                guild = interaction.guild
                member = guild.get_member(interaction.user.id)
                if member:
                    await member.kick(reason="Perdu à la roulette russe.")
                    printMessage("Roulette", f"{member.name}#{member.discriminator} a été expulsé du serveur pour avoir perdu à la roulette russe.")

            except Exception as e:
                printMessage("Roulette", f"Erreur lors de l'expulsion de {member.name}#{member.discriminator}: {e}")

            await interaction.message.edit(embed=embed, view=None)
        else:
            # Player survives
            await interaction.response.send_message(f"{interaction.user.mention} a tiré et a survécu ! 😅", ephemeral=False, delete_after=2)
            # Switch turns
            if interaction.user.id == player1_id:
                self.who_play = self.player2_id
                self.player1_id, self.player2_id = self.player2_id, self.player1_id
            else:
                self.who_play = self.player1_id
                self.player1_id, self.player2_id = self.player2_id, self.player1_id

            # Update the embed to show whose turn it is
            embed = interaction.message.embeds[0]
            embed.title = f"Roulette Russe ({self.bullet_max - 1} Balles restantes)"
            embed.set_field_at(2, name="A qui le tour ?", value=f"C'est au tour de <@{self.player1_id}> de tirer.", inline=False)
            await interaction.message.edit(embed=embed)

        self.bullet_max -= 1  # Decrease the number of bullets left

class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.all_parts = []  # Liste pour stocker toutes les parties de roulette russe

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


    @app_commands.command()
    async def dm(self, interaction: discord.Interaction, user: discord.User | discord.Role):
        try:
            if isinstance(user, discord.Role):
                members = user.members
                if not members:
                    await interaction.response.send_message(f"Aucun membre avec le rôle {user.name}.", ephemeral=True)
                    return

                for member in members:
                    if member.bot:
                        continue  # Ignore les bots

                    try:
                        await member.send(f"(Message pour le rôle ``{user.name}``) Voici le site de Vitroze : https://vitroze-dev.fr/")
                    except discord.Forbidden:
                        printMessage("Utils", f"Impossible d'envoyer un message à {member.name}#{member.discriminator}.")
                await interaction.response.send_message(f"Le message a été envoyé à tous les membres avec le rôle {user.name}.", ephemeral=True)
                return

            if user.bot:
                await interaction.response.send_message("Vous ne pouvez pas envoyer de message à un bot.", ephemeral=True)
                return


            embed = discord.Embed(
                title = "Message de Vitroze",
                description = """Voici le site de Vitroze:
                > https://vitroze-dev.fr
                """,
                color = discord.Color.yellow(),
                url = "https://vitroze-dev.fr",
                timestamp = discord.utils.utcnow()
            )
            embed.add_field(name="Lien du site", value="[Cliquez ici](https://vitroze-dev.fr)", inline=False)

            await user.send(embed=embed)
            await interaction.response.send_message(f"Le message a été envoyé à {user.mention}.", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message(f"Je ne peux pas envoyer de message à {user.mention}.", ephemeral=True)

    @app_commands.command(description="Soit tu gagnes soit tu meurs")
    async def roulette(self, interaction: discord.Interaction, member: discord.Member):
        if member.bot:
            await interaction.response.send_message("Vous ne pouvez pas jouer avec un bot.", ephemeral=True)
            return

        if member.id == interaction.user.id:
            await interaction.response.send_message("Vous ne pouvez pas jouer contre vous-même.", ephemeral=True)
            return

        if any(interaction.user.id in game for game in self.all_parts):
            await interaction.response.send_message("Vous êtes déjà dans une partie de roulette russe.", ephemeral=True)
            return

        if any(member.id in game for game in self.all_parts):
            await interaction.response.send_message(f"{member.mention} est déjà dans une partie de roulette russe.", ephemeral=True)
            return

        embed = discord.Embed(
            title="Roulette Russe (6 Balles restantes)",
            description=f"{interaction.user.mention} a défié {member.mention} à une partie de roulette russe !",
            color=discord.Color.red(),
            timestamp=discord.utils.utcnow()
        )

        # Add button
        who_play = random.choice([interaction.user, member])
        embed.add_field(name="Instructions", value="Cliquez sur le bouton ci-dessous pour tirer.", inline=False)
        embed.add_field(name="Règles", value="1. Chaque joueur tire à tour de rôle.\n2. Si vous tirez la balle, vous perdez.\n3. Si vous survivez, c'est au tour de l'autre joueur.", inline=False)
        embed.add_field(name="A qui le tour ?", value=f"C'est au tour de {who_play.mention} de tirer.", inline=False)
        embed.set_footer(text="Bonne chance !")

        view = RouletteView(interaction.user.id, member.id, who_play.id)
        await interaction.response.send_message(f"<@{interaction.user.id}> vs <@{member.id}>", embed=embed, view=view)
        message = await interaction.original_response()  # Get the original message sent by the bot
        self.all_parts.append([interaction.user.id, member.id, view])  # Store the game state

        print("Roulette", f"Nouvelle partie de roulette russe entre {interaction.user.name}#{interaction.user.discriminator} et {member.name}#{member.discriminator}.")

        await discord.utils.sleep_until(discord.utils.utcnow() + timedelta(seconds=300))  # Wait for 300 seconds (5 minutes)
        self.all_parts = [game for game in self.all_parts if game[2] != view]  # Remove the game from the list
        view.stop()  # Stop the view to disable the button

        embed.title = "Roulette Russe (Partie terminée)"
        embed.color = discord.Color.dark_gray()
        embed.set_field_at(2, name="A qui le tour ?", value="Le jeu est terminé.", inline=False)

        await message.edit(embed=embed, view=None)  # Edit the message to indicate the game is over

    @app_commands.command()
    async def send_announce(self, interaction: discord.Interaction, message: str):
        channel = self.bot.get_channel(CHANNEL_ANNOUNCE)
        if channel is None:
            await interaction.response.send_message("Le salon d'annonce n'a pas été trouvé.", ephemeral=True)
            return

        embed = discord.Embed(
            title="Annonce de Vitroze",
            description=message,
            color=discord.Color.green(),
            timestamp=discord.utils.utcnow()
        )
        embed.set_footer(text=f"Annonce par {interaction.user}", icon_url=interaction.user.avatar.url)

        await channel.send("@everyone", embed=embed)
        await interaction.response.send_message("L'annonce a été envoyée avec succès.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Utils(bot))