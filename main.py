import os
import asyncio
import discord
import traceback
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

# Color codes for console output
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

# @bot.event
# async def on_ready():
#     print(f"Connecté en tant que {bot.user}")
#     try:
#         synced = await bot.tree.sync()
#         print(f"Commandes slash synchronisées : {len(synced)}")
#     except Exception as e:
#         print(e)

def printMessage(MODULE, message):
    print(f"{bcolors.OKGREEN}[VitrozeBot - {MODULE}] {message}{bcolors.ENDC}")

def printError(MODULE, message):
    print(f"{bcolors.FAIL}[VitrozeBot - {MODULE}] ERREUR : {message}{bcolors.ENDC}")

all_salutations = [
    "salut",
    "bonjour",
    "bonsoir",
    "coucou",
    "hello",
    "hi",
    "hey",
    "yo",
    "salutations",
]

class RegisterCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.synced = False

    @commands.Cog.listener()
    async def on_ready(self):
        if self.synced:
            return

        try:
            guild = discord.Object(id=858647206394200064)
            printMessage("Main", f"Connecté en tant que {self.bot.user}")
            self.bot.tree.copy_global_to(guild=guild)
            self.bot.tree.on_error = self.on_log_error

            synced = await self.bot.tree.sync(guild=guild)
            printMessage("RegisterCommands", f"Commandes slash synchronisées : {len(synced)}")
            self.synced = True
        except Exception as e:
            printError("RegisterCommands", f"Erreur ({type(e).__name__}) lors de la synchronisation des commandes : {e}")

    @commands.Cog.listener()
    async def on_log_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        printError("RegisterCommands", f"Erreur ({type(error).__name__}) lors de l'exécution de la commande '{interaction.command.name}' : {error}")
        printError("RegisterCommands", f"Traceback : {traceback.format_exc()}")
        await interaction.response.send_message(f"Une erreur est survenue lors de l'exécution de la commande. Si vous êtes un administrateur, veuillez vérifier les logs pour plus d'informations.", ephemeral=True)

    @commands.Cog.listener()
    async def on_error(self, event_method, *args, **kwargs):
        printError("Main", f"Erreur ({type(event_method).__name__}) dans l'événement {event_method.__name__} : {args}, {kwargs}")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        printMessage("Main", f"Nouvel utilisateur : {member.name}#{member.discriminator} ({member.id})")
        try:
            await member.send(f"Bienvenue à toi sur le serveur {member.guild.name} !")
        except discord.Forbidden:
            printError("Main", f"Impossible d'envoyer un message privé à {member.name}#{member.discriminator}.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        printMessage("Main", f"Message reçu : {message.content} de {message.author}")

        for salutation in all_salutations:
            if message.content.lower().startswith(salutation):
                await message.channel.send(f"{salutation.capitalize()} {message.author.mention} !")
                await message.add_reaction("👋")
                break

async def main():
    os.system("cls" if os.name == "nt" else "clear")  # Clear the console for better readability

    async with bot:
        for filename in os.listdir("./commands"):
            if filename.endswith(".py"):
                printMessage("RegisterCommands", f"Chargement de l'extension : {filename[:-3]}")
                await bot.load_extension(f"commands.{filename[:-3]}")


        await bot.add_cog(RegisterCommands(bot))
        await bot.start(os.getenv("DISCORD_TOKEN"))

if __name__ == "__main__":
    asyncio.run(main())

# @bot.tree.command(name="ping", description="Réponse ?")
# async def ping(interaction: discord.Interaction, text: str, number:int, boolean: bool = False) -> None:
#     print(f"Texte : {text} ; {number} ; {boolean}")
#     await interaction.response.send_message("Boom", delete_after=1.0)

# bot.run(os.getenv("DISCORD_TOKEN"))
