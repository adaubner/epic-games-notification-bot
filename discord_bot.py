import discord
from discord import app_commands
from discord.ext import tasks

from dotenv import load_dotenv
from os import getenv
import json

from epic_games_checker import check_games


# Global variables
CHECKING_INTERVAL = 2  # time in seconds between epic games checking


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
        with open(r"whitelist_channels.json") as f:
            whitelist_channels = json.load(f)
        
        for guild_id, channels in whitelist_channels.items():
            for channel_id in channels:
                guild_id = int(guild_id)
                channel = client.get_guild(guild_id).get_channel(channel_id)
                game_embeds = [create_game_embed(game) for game in new_free_games]
                msg = "New free game!"
                if(len(new_free_games) > 1):
                    msg = "New free games!"
                await channel.send(msg, embeds=game_embeds)


def create_game_embed(game: dict):
    embed = discord.Embed(
        title=game["title"],
        description=game["description"]
    )
    embed.add_field(
        name = "free after",
        value = game["free_after"],
        inline=True
    )
    embed.add_field(
        name="free until",
        value=game["free_until"],
        inline=True
    )
    if game["image"] is not None:
        embed.set_image(url=game["image"])
    return embed

def start():
    load_dotenv()
    discord_token = getenv("DISCORD_TOKEN")
    client.run(discord_token)
