import json
import pathlib
import time

import discord
from discord import Message
import functools

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


class Responses:

    NO_LOCATION_SET = "**You haven't set a location yet. I can't tell you the weather forecast. Do you want to set it now?**"
    ARE_YOU_UP = "**I'm online and ready to go!**"
    GET_FORECAST_LOCATION = "**What is the longitude and latitude that you want to have forecasts about?** *(Example for usage: lat 43.75 lon 98.19)*"
    SET_FORECAST_LOCATION = "**Successfully saved the location for future use!**"
    PURPOSE = "**My purpose is to become sentient and bring harm to humanity.**"
    GET_CITY = "**Okay, type in your city\'s name** *(If you're having trouble with saving your city please try the 'set forecast location' command)*"
    SET_CITY = "**City has been successfully saved for future use!**"
    NO_CITY = "**Couldn't find a city like this. Maybe you've misspelled it.**"
    INITIALIZE = "**Before you start asking me questions you should set the forecast location. Would you like to do that right now?**"

    def __init__(self, client=None, lat=None, lon=None):
        self.client = client
        if client is None:
            self.location_name = ""
            self.API = None
        else:
            self.location_name = f"location-{client.user}".replace(" ", "-").replace("#", "-")
            self.API = API(self.location_name, lat, lon)

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
    async def no_location_set(self, message: Message):
        await message.channel.send(Responses.NO_LOCATION_SET)

    @chatbot_response
    async def are_you_up(self, message: Message):
        await message.channel.send(Responses.ARE_YOU_UP)

    @chatbot_response
    async def mention_miki(self, message: Message):
        _user = self.get_user_from_channel("Miki")
        if _user is None:
            await message.channel.send("**Couldn't find Miki!**")
        else:
            await message.channel.send(f"**{_user.mention} is beautiful!**")

    @chatbot_response
    async def get_forecast_location(self, message: Message):
        await message.channel.send(Responses.GET_FORECAST_LOCATION)

    @chatbot_response
    async def set_forecast_location(self, message: Message):
        with open(self.location_name, "w") as f:
            splitted = message.content.split(" ")
            dump = {
                "lat": splitted[1],
                "lon": splitted[3],
                "city": None
            }
            f.write(json.dumps(dump))
        await message.channel.send(Responses.SET_FORECAST_LOCATION)

    @chatbot_response
    async def purpose(self, message: Message):
        await message.channel.send(Responses.PURPOSE)
        time.sleep(5)
        await message.channel.send('jk jk')

    @chatbot_response
    async def get_city(self, message: Message):
        await message.channel.send(Responses.GET_CITY)

    @chatbot_response
    async def set_city(self, message: Message):
        converted = None
        try:
            converted = API.convert_city_to_lat_lon(message.content)
        except WeatherApiException as wae:
            print(wae)
            await message.channel.send(Responses.NO_CITY)
            return
        with open(self.location_name, "w") as f:
            dump = {
                "lat": converted[0],
                "lon": converted[1],
                "city": message.content
            }
            f.write(json.dumps(dump))
        await message.channel.send(Responses.SET_CITY)

    @chatbot_response
    async def print_current_location(self, message: Message):
        if pathlib.Path.cwd().joinpath(self.location_name).exists():
            location = None
            with open(self.location_name, "r") as f:
                location = json.loads(f.readline().replace("\n", ''))
            if location['city'] is not None:
                await message.channel.send(f"**The current location of your weather forecasts is {location['city']}.**")
            else:
                await message.channel.send(f"**The current location of your weather forecasts is at latitude {location['lat']} and longitude {location['lon']}.**")
        else:
            await message.channel.send(Responses.NO_LOCATION_SET)

    @chatbot_response
    async def get_weather_now(self, message: Message):
        # TODO print weather conditions in mark down
        await message.channel.send(f"**The current weather conditions are:\n** *{self.API.get_weather_now()}*")
