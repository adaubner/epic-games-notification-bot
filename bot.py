import epic_api_fetch#my own code, might break
import discord
import json
#####################################################################
#Andy Daubner (daubner.andy@gmail.com)
#24/07/21
#
#Async app to run python bot that fetches data from epic games.
#!!!DON'T UPLOAD config.json TO GITHUB!!!
#
#####################################################################

#global variables, will require restart if changed
config=json.load(open('config.json'))
TOKEN=config['discord_token']
CMD_TAG=config['command_prefix']
CHNL_WHITELIST=config['whitelisted_channels']


client=discord.Client()

#confirmation bot is online
@client.event
async def on_ready():
	print('logged in as '+str(client.user))


@client.event
async def on_message(message):
	#variables
	channel=message.channel#use str() to read channel
	author=message.author
	content=message.content
	#self recursion check
	if author == client.user:
		return
	#whitelisted channel
	if str(channel) not in CHNL_WHITELIST:
		return
	#TODO Main logic
	if content.startswith(CMD_TAG):
		command=content[len(CMD_TAG):]#stores everything but the command tag
		#help
		if command.startswith('help'):
			await channel.send('this is the temporary help page')
		#TODO add more commands



#############runtime###############

if __name__=="__main__":
	client.run(TOKEN)