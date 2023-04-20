import discord
from discord.ext import tasks
import my_secrets




# Global variables
CHECKING_INTERVAL = 10 # time in seconds between epic games checking


intents = discord.Intents.default()
client = discord.Client(intents=intents)

#confirmation bot is online
@client.event
async def on_ready():
    print(f"logged in as {str(client.user)}")
    await check_epic_games.start()
    # TODO Why does code not run here? vv
    print(f"epic games checker started with polling rate of {CHECKING_INTERVAL}sec")
    
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
    print("hello")



if __name__ == "__main__":
    client.run(my_secrets.discord_api_key)