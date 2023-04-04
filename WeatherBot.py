import discord
import pathlib
import json
import WeatherResponses


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
responses = WeatherResponses.WeatherResponses(client)


@client.event
async def on_ready():
    print(f'Connection initiated with discord client: {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('Are you up?') or 'up' in message.content:
        await responses.are_you_up(message)

    if 'miki' in message.content.lower():
        await responses.mention_miki(message)

    if 'set forecast location' in message.content.lower():
        await responses.get_forecast_location(message)

    if 'lon' in message.content.lower() and 'lat' in message.content.lower():
        await responses.set_forecast_location(message)

client.run(TOKEN)
