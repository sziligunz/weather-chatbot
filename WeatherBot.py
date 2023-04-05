import discord
import pathlib
import json
from WeatherResponses import Responses


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
intents.members = True  # very important setting, otherwise bot wouldn't see other users
intents.message_content = True
client = discord.Client(intents=intents)
responses = Responses(client)


@client.event
async def on_ready():
    print(f'Connection initiated with discord client: {client.user}')


@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return

    words = message.content.split(' ')
    for i in range(len(words)):
        words[i] = words[i].lower()
        words[i] = words[i].strip()
    previous_message = [m async for m in message.channel.history(limit=10, oldest_first=False)][2]

    if 'up' in words:
        await responses.are_you_up(message)

    if 'miki' in words:
        await responses.mention_miki(message)

    if 'set forecast location' in message.content.lower():
        await responses.get_forecast_location(message)

    if 'lon' in words and 'lat' in words:
        await responses.set_forecast_location(message)

    if 'purpose' in words:
        await responses.purpose(message)

    if 'set forecast city' in message.content.lower():
        await responses.get_city(message)

    if previous_message.content.lower().strip() == 'set forecast city':
        await responses.set_city(message)

    if "current location" in message.content.lower():
        await responses.print_current_location(message)

client.run(TOKEN)
