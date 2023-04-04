import pathlib

import discord
import pathlib
import json


def get_token(filename="discord-token.json"):
    """
        :param filename: The name of the token configuration file.
        :type filename: str
        :return: The token that is used to run the discord client.
        :rtype: str
    """
    path = pathlib.Path.cwd().joinpath(filename).__str__()
    token = None
    with open(path, "r") as f:
        token = json.load(f)['token']
    return token


# Necessary setup in order to create event handlers
TOKEN = get_token()
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'Connection initiated with discord client: {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('Are you up?') or 'up' in message.content:
        await message.channel.send("Yes, I'm online and ready to go!")

client.run(TOKEN)
