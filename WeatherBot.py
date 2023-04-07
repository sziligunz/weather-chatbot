import discord
import pathlib
import json
from WeatherResponses import Responses


async def send_simple_message(channel, message):
    await channel.send(message)


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
LOCATION_NAME = ""
responses: Responses = Responses()


@client.event
async def on_ready():
    global responses, LOCATION_NAME
    print(f'Connection initiated with discord client: {client.user}')
    # create responses
    LOCATION_NAME = f"location-{client.user}".replace(" ", "-").replace("#", "-")
    if not pathlib.Path.cwd().joinpath(LOCATION_NAME).exists():
        for channel in client.get_all_channels():
            if channel.name == "weather-chatbot":
                await send_simple_message(channel, Responses.INITIALIZE)
                responses = Responses(client, 46.253, 20.14824)
        pass
    else:
        responses = Responses(client)


@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return

    words = message.content.split(' ')
    for i in range(len(words)):
        words[i] = words[i].lower()
        words[i] = words[i].strip()
    previous_message = [m.content.strip().lower() async for m in message.channel.history(limit=3, oldest_first=False)]

    # check if at initialize there is no location file and set it if the user asks it
    if not pathlib.Path().cwd().joinpath(LOCATION_NAME).exists() and Responses.INITIALIZE.lower() in previous_message and "yes" in words:
        await responses.get_city(message)
        return
    if not pathlib.Path().cwd().joinpath(LOCATION_NAME).exists() and Responses.GET_CITY.lower() in previous_message:
        await responses.set_city(message)
        return

    # check if the location file has been destroyed and set it if the user asks it
    if not pathlib.Path().cwd().joinpath(LOCATION_NAME).exists() and Responses.INITIALIZE.lower() not in previous_message and "yes" not in words:
        await responses.no_location_set(message)
        return
    if not pathlib.Path().cwd().joinpath(LOCATION_NAME).exists() and "yes" in words and Responses.NO_LOCATION_SET.lower() in previous_message and Responses.INITIALIZE.lower() not in previous_message:
        await responses.get_city(message)
        return
    if not pathlib.Path().cwd().joinpath(LOCATION_NAME).exists() and Responses.GET_CITY.lower() in previous_message and Responses.INITIALIZE.lower() not in previous_message:
        await responses.set_city(message)
        return

    if 'up' in words:
        await responses.are_you_up(message)

    if 'miki' in words:
        await responses.mention_miki(message)

    if 'set forecast location' in message.content.lower():
        await responses.get_forecast_location(message)
        return

    if 'lon' in words and 'lat' in words and Responses.GET_FORECAST_LOCATION.lower() in previous_message:
        await responses.set_forecast_location(message)

    if 'purpose' in words:
        await responses.purpose(message)

    if 'set forecast city' in message.content.lower():
        await responses.get_city(message)
        return

    if Responses.GET_CITY.lower() in previous_message:
        await responses.set_city(message)

    if "current location" in message.content.lower():
        await responses.print_current_location(message)

    if "now" in words:
        await responses.get_weather_now(message)


# run the chatbot client
client.run(TOKEN)
