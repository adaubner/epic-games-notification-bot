import discord
from discord.ext import tasks
import my_secrets
from epic_games_checker import check_games



# Global variables
CHECKING_INTERVAL = 10 # time in seconds between epic games checking


intents = discord.Intents.default()
client = discord.Client(intents=intents)

#confirmation bot is online
@client.event
async def on_ready():
    print(f"logged in as {str(client.user)}")
    await check_epic_games.start()
    
@client.event
async def on_message(message): #TODO use discord command system
    #variables
    channel=message.channel#use str() to read channel
    author=message.author
    content=message.content
    #self recursion check
    if author == client.user:
        return
    await channel.send("hello")

@tasks.loop(seconds=CHECKING_INTERVAL)
async def check_epic_games():
    new_free_games = check_games()
    if new_free_games is not None:
        print("new games discord message")



if __name__ == "__main__":
    client.run(my_secrets.discord_api_key)