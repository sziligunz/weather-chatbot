import datetime
import json
import pathlib
import time

from discord import Message, Embed, Colour
import functools

from EmbedBuilder import *
from WeatherChatBotException import ChatBotException, WeatherApiException
from WeatherApi import API


def chatbot_response(func):
    @functools.wraps(func)
    async def inner(*args, **kwargs):
        if args[1] is None:
            raise ChatBotException("There has been no message to be received")
        print(f"Chatbot have been asked '{args[1].content}' by user {args[1].author}")
        return await func(*args, **kwargs)
    return inner


def interactive(func):
    @functools.wraps(func)
    async def inner(*args, **kwargs):
        res = None
        async with args[1].channel.typing():
            time.sleep(0.5)
            res = await func(*args, **kwargs)
        return res
    return inner


class Responses:

    NO_LOCATION_SET = "You haven't set a location yet. I can't tell you the weather forecast. Do you want to set it now?"
    ARE_YOU_UP = "I'm online and **ready** to go!"
    GET_FORECAST_LOCATION = "What is the longitude and latitude that you want to have forecasts about? *(Example for usage: lat 43.75 lon 98.19)*"
    SET_FORECAST_LOCATION = "Location has been **successfully** saved for future use!"
    PURPOSE = "My purpose is to become sentient and bring harm to humanity."
    GET_CITY = "Okay, type in your city's name *(If you're having trouble with saving your city please try the 'set forecast location' command)*"
    SET_CITY = "City has been **successfully** saved for future use!"
    NO_CITY = "**Couldn't find** a city like this. Maybe you've misspelled it."
    INITIALIZE = "Before you start asking me questions you should set the forecast location. Would you like to do that right now?"
    WRONG_FORECAST_LOCATION_FORMAT = "You gave the location in a wrong format. *(Example for usage: lat 43.75 lon 98.19)*"
    DID_NOT_RECOGNIZE = "I don't recognize your question in my implementaion. *(Try using the 'help' command)*"

    def __init__(self, client=None, lat=None, lon=None):
        self.client = client
        if client is None:
            self.location_name = ""
            self.API = None
        else:
            self.location_name = f"location-{client.user}".replace(" ", "-").replace("#", "-")
            self.API = API(self.location_name, lat, lon)
        self.bb = BasicPrintBuilder()

    def get_user_from_channel(self, user_name, channel_name="weather-chatbot"):
        """
        Returns a discord.User from the given channel. If there is no
        given channel_name the function searches in the weather-bot channel

        :param user_name: The name of the user to search for
        :type user_name: str
        :param channel_name: The name of the channel to search in
        :type channel_name: str
        :return: discord.User
        """
        _user = None
        for channel in self.client.get_all_channels():
            if channel.name == channel_name:
                for member in channel.members:
                    if member.name.lower() == user_name.lower():
                        _user = member
                        break
                break
        return _user

    @chatbot_response
    @interactive
    async def did_not_recognize(self, message: Message):
        await message.channel.send(embed=self.bb.new().title(Responses.DID_NOT_RECOGNIZE).color(Colour.red()).build())

    @chatbot_response
    @interactive
    async def no_location_set(self, message: Message):
        await message.channel.send(embed=self.bb.new().title(Responses.NO_LOCATION_SET).color(Colour.green()).build())

    @chatbot_response
    @interactive
    async def are_you_up(self, message: Message):
        await message.channel.send(embed=self.bb.new().title(Responses.ARE_YOU_UP).color(Colour.green()).build())

    @chatbot_response
    @interactive
    async def mention_miki(self, message: Message):
        _user = self.get_user_from_channel("Miki")
        if _user is None:
            await message.channel.send(embed=self.bb.new().title("Couldn't find Miki!").color(Colour.red()).build())
        else:
            await message.channel.send(f"{_user.mention}")
            await message.channel.send(embed=self.bb.new().title(f"Miki is beautiful!").color(Colour.teal()).build())

    @chatbot_response
    @interactive
    async def get_forecast_location(self, message: Message):
        await message.channel.send(
            embed=self.bb.new().title(Responses.GET_FORECAST_LOCATION).color(Colour.green()).build()
        )

    @chatbot_response
    @interactive
    async def set_forecast_location(self, message: Message):
        splitted = [s.lower().strip() for s in message.content.split(" ")]
        if "lat" in splitted and "lon" in splitted and len(splitted) == 4:
            with open(self.location_name, "w") as f:
                dump = {
                    "lat": float(splitted[1]),
                    "lon": float(splitted[3]),
                    "city": None
                }
                f.write(json.dumps(dump))
            await message.channel.send(
                embed=self.bb.new().title(Responses.SET_FORECAST_LOCATION).color(Colour.green()).build()
            )
        else:
            await message.channel.send(
                embed=self.bb.new().title(Responses.WRONG_FORECAST_LOCATION_FORMAT).color(Colour.red()).build()
            )

    @chatbot_response
    @interactive
    async def purpose(self, message: Message):
        await message.channel.send(embed=self.bb.new().title(Responses.PURPOSE).color(Colour.dark_magenta()).build())
        time.sleep(5)
        await message.channel.send(embed=self.bb.new().title('jk jk').color(Colour.green()).build())

    @chatbot_response
    @interactive
    async def get_city(self, message: Message):
        await message.channel.send(embed=self.bb.new().title(Responses.GET_CITY).color(Colour.green()).build())

    @chatbot_response
    @interactive
    async def set_city(self, message: Message):
        converted = None
        try:
            converted = API.convert_city_to_lat_lon(message.content)
        except WeatherApiException as wae:
            print(wae)
            await message.channel.send(embed=self.bb.new().color(Colour.red()).title(Responses.NO_CITY).build())
            return
        with open(self.location_name, "w") as f:
            dump = {
                "lat": converted[0],
                "lon": converted[1],
                "city": message.content
            }
            f.write(json.dumps(dump))
        await message.channel.send(embed=self.bb.new().color(Colour.green()).title(Responses.SET_CITY).build())

    @chatbot_response
    @interactive
    async def print_current_location(self, message: Message):
        self.bb.new()
        if pathlib.Path.cwd().joinpath(self.location_name).exists():
            self.bb.color(Colour.green())
            location = None
            with open(self.location_name, "r") as f:
                location = json.loads(f.readline().replace("\n", ''))
            if location['city'] is not None:
                self.bb.title(f"The current location of your weather forecasts is **{location['city']}.**")
            else:
                self.bb.title(f"The current location of your weather forecasts is at latitude **{location['lat']}** and longitude **{location['lon']}.**")
        else:
            self.bb.color(Colour.red()).title(Responses.NO_LOCATION_SET)
        await message.channel.send(embed=self.bb.build())

    @chatbot_response
    @interactive
    async def get_weather_now(self, message: Message):
        current = self.API.get_weather_now()
        time.sleep(0.5)
        builder = WeatherReportBuilder()
        builder.title("Current Weather Conditions")\
            .color(11342935)\
            .description(f"Here is forecast on the weather at {datetime.datetime.now().strftime('%H:%M')}")\
            .thumbnail(API.get_weather_icon(current['weather'][0]['icon']))
        builder += {"name": "Temperature", "value": f"{round(current['main']['temp'])} °C"}
        builder += {"name": "Condition", "value": f"{current['weather'][0]['description']}"}
        if "rain" in current.keys():
            builder += {"name": "Rain", "value": f"Rain: **{int(current['rain']['1h'])}** mm"}
        if "snow" in current.keys():
            builder += {"name": "Snow", "value": f"Snow: **{int(current['snow']['1h'])}** mm"}
        await message.channel.send(embed=builder.build())

    @chatbot_response
    async def get_day_forecast(self, message: Message):
        pass
