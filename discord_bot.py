import discord
from discord import app_commands
from discord.ext import tasks

from dotenv import load_dotenv
from os import getenv
import json

from epic_games_checker import check_games


# Global variables
CHECKING_INTERVAL = 10  # time in seconds between epic games checking


intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# Key: guild id
# Value: list of channels
# whitelist_channels = {}  # TODO sql


@tree.command(name="help")
async def help(interaction):
    await interaction.response.send_message("help page here")


# TODO remove channel command
@tree.command(
    name="add_channel",
    description="Notifies this channel about new games"
)
async def add_channel(interacion):
    await interacion.response.send_message(f'Will notify channel "{interacion.channel}" about new games.')
    guild_id = str(interacion.guild_id)
    channel_id = interacion.channel_id
    with open(r"whitelist_channels.json") as f:
        whitelist_channels = json.load(f)
    # Does the guild currently exist in the whitelist
    
    if guild_id not in whitelist_channels:
        whitelist_channels[guild_id] = list()
    # If channel is new, add it
    if channel_id in whitelist_channels[guild_id]:
        return
    whitelist_channels[guild_id].append(channel_id)
    with open(r"whitelist_channels.json", "w") as f:
        json.dump(whitelist_channels, f)
    


# confirmation bot is online
@client.event
async def on_ready():
    print(f"logged in as {str(client.user)}")
    await tree.sync()
    await check_epic_games.start()


@tasks.loop(seconds=CHECKING_INTERVAL)
async def check_epic_games():
    new_free_games = check_games()
    if len(new_free_games) != 0:
        print(new_free_games)  # TODO debug
        
        with open(r"whitelist_channels.json") as f:
            whitelist_channels = json.load(f)
        
        for guild_id, channels in whitelist_channels.items():
            for channel_id in channels:
                guild_id = int(guild_id)
                channel = client.get_guild(guild_id).get_channel(channel_id)
                await channel.send("New free games:\n" + str(new_free_games))


if __name__ == "__main__":
    load_dotenv()
    discord_token = getenv("DISCORD_TOKEN")
    client.run(discord_token)
