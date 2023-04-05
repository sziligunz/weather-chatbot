import json
import pathlib
import time
from discord import Message
import functools
from WeatherChatBotException import ChatBotException
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
    def __init__(self, client):
        self.client = client

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
    async def are_you_up(self, message: Message):
        await message.channel.send("**I'm online and ready to go!**")

    @chatbot_response
    async def mention_miki(self, message: Message):
        _user = self.get_user_from_channel("Miki")
        if _user is None:
            await message.channel.send("**Couldn't find Miki!**")
        else:
            await message.channel.send(f"**{_user.mention} is beautiful!**")

    @chatbot_response
    async def get_forecast_location(self, message: Message):
        await message.channel.send("**What is the longitude and latitude that you want to have forecasts about?** "
                                   "*(Example for usage: lon 43.75 lat 98.19)*")

    @chatbot_response
    async def set_forecast_location(self, message: Message):
        with open("location", "w") as f:
            splitted = message.content.split(" ")
            dump = {
                "lat": splitted[1],
                "lon": splitted[3],
                "city": None
            }
            f.write(json.dumps(dump))
        await message.channel.send("**Successfully saved the location for future use!**")

    @chatbot_response
    async def purpose(self, message: Message):
        await message.channel.send('**My purpose is to become sentient and bring harm to humanity.**')
        time.sleep(5)
        await message.channel.send('jk jk')

    @chatbot_response
    async def get_city(self, message:Message):
        await message.channel.send('**Okay, type in your city\'s name**')

    @chatbot_response
    async def set_city(self, message: Message):
        converted = API.convert_city_to_lat_lon(message.content)
        with open("location", "w") as f:
            dump = {
                "lat": converted[0],
                "lon": converted[1],
                "city": message.content
            }
            f.write(json.dumps(dump))
        await message.channel.send('**City has been successfully saved for future use!**')

    @chatbot_response
    async def print_current_location(self, message: Message):
        if pathlib.Path.cwd().joinpath("location").exists():
            location = None
            with open("location", "r") as f:
                location = json.loads(f.readline().replace("\n", ''))
            if location['city'] is not None:
                await message.channel.send(f"**The current location of your weather forecasts is {location['city']}.**")
            else:
                await message.channel.send(f"**The current location of your weather forecasts is at latitude {location['lat']} and longitude {location['lon']}.**")
        else:
            await message.channel.send("**You haven't set a location for your forecasts yet.**")
