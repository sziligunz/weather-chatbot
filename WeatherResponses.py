import json

from discord import Message
import functools
from WeatherChatBotException import ChatBotException


def chatbot_response(func):
    @functools.wraps(func)
    async def inner(*args, **kwargs):
        print("Chatbot have been asked...")
        if args[1] is None:
            raise ChatBotException("There has been no message to be received")
        return await func(*args, **kwargs)
    return inner


class WeatherResponses:
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
                "lon": splitted[3]
            }
            f.write(json.dumps(dump))
        await message.channel.send("**Succesfully saved the location for future use!**")