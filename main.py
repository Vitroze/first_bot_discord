import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
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
    print(f"[VitrozeBot - {MODULE}] {message}")

def printError(MODULE, message):
    print(f"[VitrozeBot - {MODULE}] ERREUR : {message}")

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
            synced = await self.bot.tree.sync(guild=guild)
            printMessage("RegisterCommands", f"Commandes slash synchronisées : {len(synced)}")
            self.synced = True
        except Exception as e:
            printError("RegisterCommands", f"Erreur ({type(e).__name__}) lors de la synchronisation des commandes : {e}")

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

@bot.event
async def on_member_join(member):
    print(f"Test {member}")
    await member.send("Bienvenue à toi sur le serveur")

# @bot.tree.command(name="ping", description="Réponse ?")
# async def ping(interaction: discord.Interaction, text: str, number:int, boolean: bool = False) -> None:
#     print(f"Texte : {text} ; {number} ; {boolean}")
#     await interaction.response.send_message("Boom", delete_after=1.0)

# bot.run(os.getenv("DISCORD_TOKEN"))
