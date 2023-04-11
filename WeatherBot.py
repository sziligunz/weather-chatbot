import pathlib
import json
import discord
from discord import Colour

from EmbedBuilder import BasicPrintBuilder
from WeatherResponses import Responses


async def send_simple_message(channel, message):
    await channel.send(embed=BasicPrintBuilder().new().title(message).color(Colour.red()).build())


def get_token(filename="discord-token.json"):
    """
        :param filename: The name of the token configuration file.
        :type filename: str
        :return: The token that is used to run the discord client.
        :rtype: str
    """
    path = pathlib.Path.cwd().joinpath(filename)
    token = None
    if path.exists():
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
responses = Responses()


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

    words = message.content.replace("?", "").replace("!", "").replace(".", "").replace(",", "").split(' ')
    for i in range(len(words)):
        words[i] = words[i].lower()
        words[i] = words[i].strip()
    previous_message = [m.content.strip().lower() if m.content else m.embeds[0].title.lower().strip() async for m in message.channel.history(limit=3, oldest_first=False)]

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
        await responses.get_up(message)
        return

    if 'miki' in words:
        await responses.mention_miki(message)
        return

    if 'set forecast location' in message.content.lower():
        await responses.get_forecast_location(message)
        return

    if 'lon' in words and 'lat' in words and Responses.GET_FORECAST_LOCATION.lower() in previous_message:
        await responses.set_forecast_location(message)
        return

    if 'purpose' in words:
        await responses.get_purpose(message)
        return

    if 'set forecast city' in message.content.lower():
        await responses.get_city(message)
        return

    if Responses.GET_CITY.lower() in previous_message:
        await responses.set_city(message)
        return

    if "current location" in message.content.lower():
        await responses.get_current_location(message)
        return

    if "now city" in message.content.lower():
        await responses.get_now_city(message)
        return

    if "now city" in previous_message and Responses.GET_NOW_CITY.lower() in previous_message:
        await responses.set_now_city(message)
        return

    if "today city" in message.content.lower():
        await responses.get_today_city(message)
        return

    if "today city" in previous_message and Responses.GET_NOW_CITY.lower() in previous_message:
        await responses.set_today_city(message)
        return

    if "now" in words:
        await responses.get_now(message)
        return

    if "today" in words:
        await responses.get_today(message)
        return

    # if "image" in words:
    #     await responses.get_weather_image(message)
    #     return

    if "rain" in words:
        await responses.get_rain(message)
        return

    if "help" in words:
        await responses.get_help(message)
        return

    await responses.did_not_recognize(message)


# run the chatbot client
client.run(TOKEN)
