import discord
from discord import app_commands
from discord.ext import commands
from main import printMessage
import yt_dlp
YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

printMessage("Utils", "Chargement de l'extension : utils")

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = []

    @app_commands.command(description="Ajoute une chanson à la file d'attente")
    async def add_song(self, interaction: discord.Interaction, song_url: str):
        self.queue.append(song_url)
        await interaction.response.send_message(f"Chanson ajoutée à la file d'attente : {song_url}")

    @app_commands.command(description="Affiche la file d'attente des chansons")
    async def show_queue(self, interaction: discord.Interaction):
        if not self.queue:
            await interaction.response.send_message("La file d'attente est vide.")
        else:
            queue_list = "\n".join(f"{index + 1}. {song}" for index, song in enumerate(self.queue))
            await interaction.response.send_message(f"File d'attente des chansons :\n{queue_list}")

    @app_commands.command(description="Supprime une chanson de la file d'attente")
    async def remove_song(self, interaction: discord.Interaction, song_index: int):
        if 0 < song_index <= len(self.queue):
            removed_song = self.queue.pop(song_index - 1)
            await interaction.response.send_message(f"Chanson supprimée de la file d'attente : {removed_song}")
        else:
            await interaction.response.send_message("Index de chanson invalide.")

    @app_commands.command(description="Joindre le vocal")
    async def join_voice(self, interaction: discord.Interaction):

        if interaction.guild.voice_client is not None:
            await interaction.guild.voice_client.disconnect()

        if interaction.user.voice:
            channel = interaction.user.voice.channel
            await channel.connect()
            await interaction.response.send_message(f"Connecté au canal vocal : {channel.name}")
        else:
            await interaction.response.send_message("Vous devez être dans un canal vocal pour que le bot puisse vous rejoindre.")

    @app_commands.command(description="Jouer le son en ligne")
    async def play_sound(self, interaction: discord.Interaction, sound_url: str):
        if interaction.guild.voice_client is None:
            await interaction.response.send_message("Le bot n'est pas connecté à un canal vocal.")
            return

        voice_client = interaction.guild.voice_client
        voice_client.stop()  # Stop any currently playing audio

        # Use yt_dlp to extract the audio from the provided URL
        with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(sound_url, download=False)
            audio_url = info['url']

        # Play the sound from the provided URL
        voice_client.play(discord.FFmpegPCMAudio(audio_url), after=lambda e: print(f"Lecture terminée : {e}"))
        await interaction.response.send_message(f"Lecture du son : {sound_url}")

    @app_commands.command(description="Arrêter le son en cours de lecture")
    async def stop_sound(self, interaction: discord.Interaction):
        if interaction.guild.voice_client is None:
            await interaction.response.send_message("Le bot n'est pas connecté à un canal vocal.")
            return

        voice_client = interaction.guild.voice_client
        voice_client.stop()
        await interaction.response.send_message("Lecture du son arrêtée.")

    @app_commands.command(description="Récupérer le tempo actuel de la chanson en cours de lecture")
    async def get_tempo(self, interaction: discord.Interaction):
        if interaction.guild.voice_client is None:
            await interaction.response.send_message("Le bot n'est pas connecté à un canal vocal.")
            return

        voice_client = interaction.guild.voice_client
        if not voice_client.is_playing():
            await interaction.response.send_message("Aucune chanson n'est en cours de lecture.")
            return

        timestamp = voice_client.source.timestamp
        timestamp_max = voice_client.source.duration
        await interaction.response.send_message(f"Le tempo actuel de la chanson en cours de lecture est : {timestamp}/{timestamp_max}")
async def setup(bot):
    await bot.add_cog(Music(bot))