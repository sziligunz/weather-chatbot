import datetime
import json
import pathlib
import time
import functools

from discord import Message, Colour

from EmbedBuilder import BasicPrintBuilder, WeatherReportBuilder
from WeatherChatBotException import ChatBotException, WeatherApiException
from WeatherApi import API


# simple decorator: if there's no message given for the bot to answer to raise a custom error
def chatbot_response(func):
    @functools.wraps(func)
    async def inner(*args, **kwargs):
        if len(args) == 1:
            raise ChatBotException("There has been no message to be received")
        print(f"Chatbot have been asked '{args[1].content}' by user {args[1].author}")
        return await func(*args, **kwargs)
    return inner


# simple decorator: simulates the bot typing in the responses
def interactive(func):
    @functools.wraps(func)
    async def inner(*args, **kwargs):
        res = None
        async with args[1].channel.typing():
            time.sleep(0.5)
            res = await func(*args, **kwargs)
        return res
    return inner


# this class contains all the responses that the bot makes and the logic behind them
class Responses:

    # BOT responses, could read them out of a file, but for sake of convenience this is a better solution
    NO_LOCATION_SET = "You haven't set a location yet. I can't tell you the weather forecast. Do you want to set it now?"
    ARE_YOU_UP = "I'm online and ready to go!"
    GET_FORECAST_LOCATION = "What is the longitude and latitude that you want to have forecasts about? *(Example for usage: lat 43.75 lon 98.19)*"
    SET_FORECAST_LOCATION = "Location has been successfully saved for future use!"
    PURPOSE = "My purpose is to become sentient and bring harm to humanity."
    GET_CITY = "Okay, type in your city's name *(If you're having trouble with saving your city please try the 'set forecast location' command)*"
    SET_CITY = "City has been successfully saved for future use!"
    NO_CITY = "Couldn't find a city like this. Maybe you've misspelled it."
    INITIALIZE = "Before you start asking me questions you should set the forecast location. Would you like to do that right now?"
    WRONG_FORECAST_LOCATION_FORMAT = "You gave the location in a wrong format. *(Example for usage: lat 43.75 lon 98.19)*"
    DID_NOT_RECOGNIZE = "I don't recognize your question. *(Try using the 'help' command)*"
    GET_NOW_CITY = "Alright, give me a city name."

    # have to check if there's no input in __init__(),
    # because in WeatherBot.py (line 38) we create one without any parameter
    def __init__(self, client=None, lat=None, lon=None):
        self.client = client
        if client is None:
            self.location_name = ""
            self.API = None
        else:
            self.location_name = f"location-{client.user}".replace(" ", "-").replace("#", "-")
            self.API = API(self.location_name, lat, lon)
        # these embed builder objects makes the responses so much nicer
        self.bb = BasicPrintBuilder()
        self.wrb = WeatherReportBuilder()

    # used for getting a member of the channel
    def get_user_from_channel(self, user_name, channel_name="weather-chatbot"):
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
    async def get_up(self, message: Message):
        await message.channel.send(embed=self.bb.new().title(Responses.ARE_YOU_UP).color(Colour.green()).build())

    @chatbot_response
    @interactive
    async def mention_miki(self, message: Message):
        _user = self.get_user_from_channel("Miki")
        if _user is None:
            await message.channel.send(embed=self.bb.new().title("Couldn't find Miki!").color(Colour.red()).build())
        else:
            await message.channel.send(f"{_user.mention}")
            await message.channel.send(embed=self.bb.new().title("Miki is beautiful!").color(Colour.teal()).build())

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
            self.API.update_location()
            await message.channel.send(
                embed=self.bb.new().title(Responses.SET_FORECAST_LOCATION).color(Colour.green()).build()
            )
        else:
            await message.channel.send(
                embed=self.bb.new().title(Responses.WRONG_FORECAST_LOCATION_FORMAT).color(Colour.red()).build()
            )

    @chatbot_response
    @interactive
    async def get_purpose(self, message: Message):
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
        self.API.update_location()
        await message.channel.send(embed=self.bb.new().color(Colour.green()).title(Responses.SET_CITY).build())

    @chatbot_response
    @interactive
    async def get_current_location(self, message: Message):
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
    async def get_now(self, message: Message, **kwargs):
        current = None
        try:
            if "city_name" in kwargs.keys():
                current = self.API.get_weather_now(city_name=kwargs["city_name"])
            else:
                current = self.API.get_weather_now()
        except WeatherApiException as wae:
            print(wae)
            await message.channel.send(embed=self.bb.new().title(Responses.NO_CITY).color(Colour.red()).build())
            return
        time.sleep(0.5)
        self.wrb.new().title("Current Weather Conditions")\
            .color(11342935)\
            .description(f"Here is forecast on the weather at {datetime.datetime.now().strftime('%H:%M')}")\
            .thumbnail(API.get_weather_icon(current['weather'][0]['icon']))
        if "city_name" in kwargs.keys():
            self.wrb.location(f"Report from {kwargs['city_name']}")
        else:
            self.wrb.attach_location(self.API)
        # adding custom fields to the embeds
        self.wrb += {"name": "Temperature", "value": f"{round(current['main']['temp'])} °C"}
        self.wrb += {"name": "Condition", "value": f"{current['weather'][0]['description']}"}
        if "rain" in current.keys():
            self.wrb += {"name": "Rain", "value": f"Rain: **{int(current['rain']['1h'])}** mm"}
        if "snow" in current.keys():
            self.wrb += {"name": "Snow", "value": f"Snow: **{int(current['snow']['1h'])}** mm"}
        await message.channel.send(embed=self.wrb.build())

    @chatbot_response
    @interactive
    async def get_today(self, message: Message, **kwargs):
        _5day = None
        try:
            if "city_name" in kwargs.keys():
                _5day = self.API.get_weather_5day(city_name=kwargs["city_name"])
            else:
                _5day = self.API.get_weather_5day()
        except WeatherApiException as wae:
            print(wae)
            await message.channel.send(embed=self.bb.new().title(Responses.NO_CITY).color(Colour.red()).build())
            return
        time.sleep(0.5)
        today = [m for m in _5day['list'] if datetime.datetime.now() < datetime.datetime.fromtimestamp(m['dt']) <
                 datetime.datetime.now() + datetime.timedelta(days=1)]
        self.wrb.new()\
            .title("Today's Weather Conditions")\
            .color(11342935)\
            .set_most_common_thumbnail(today)\
            .description("Forecasts from " +
                         f"{datetime.datetime.fromtimestamp(today[0]['dt']).strftime('%m-%d %H:%M')} to " +
                         f"{datetime.datetime.fromtimestamp(today[-1]['dt']).strftime('%m-%d %H:%M')}")
        if "city_name" in kwargs.keys():
            self.wrb.location(f"Report from {kwargs['city_name']}")
        else:
            self.wrb.attach_location(self.API)
        for _3h in today:
            self.wrb\
                + {"name": "Time", "value": f"{datetime.datetime.fromtimestamp(_3h['dt']).strftime('%H:%M')}"}\
                + {"name": "Temperature", "value": f"{round(_3h['main']['temp'])} °C"}\
                + {"name": "Condition", "value": f"{_3h['weather'][0]['description']}"}
            if "rain" in _3h.keys():
                self.wrb += {"name": "Rain", "value": f"**{float(_3h['rain']['3h'])}** mm", "inline": "False"}
            if "snow" in _3h.keys():
                self.wrb += {"name": "Snow", "value": f"**{float(_3h['snow']['3h'])}** mm", "inline": "False"}
        await message.channel.send(embed=self.wrb.build())

    # @chatbot_response
    # @interactive
    # async def get_weather_image(self, message: Message):
    #     await message.channel.send(embed=self.bb.new().title("asd").color(Colour.green())\
    #     .build().set_image(url=self.API.get_weather_image()))

    @chatbot_response
    @interactive
    async def get_rain(self, message: Message):
        _5day = self.API.get_weather_5day()
        time.sleep(0.5)
        today = [m for m in _5day['list'] if datetime.datetime.now() < datetime.datetime.fromtimestamp(m['dt']) <
                 datetime.datetime.now() + datetime.timedelta(days=1)]
        self.wrb.new()\
            .title("Rain")\
            .color(11342935)\
            .description("There won't be any rain today.")\
            .attach_location(self.API)
        for i in today:
            if "rain" in i.keys():
                self.wrb.description("There will be rain today.")\
                    .thumbnail(API.get_weather_icon(i["weather"][0]["icon"]))
                break
            elif "snow" in i.keys():
                self.wrb.description("There will be snow today.")\
                    .thumbnail(API.get_weather_icon(i["weather"][0]["icon"]))
                break
        for i in today:
            if "rain" in i.keys():
                self.wrb + {"name": "Time", "value": f"{datetime.datetime.fromtimestamp(i['dt']).strftime('%H:%M')}"}\
                    + {"name": "Rain", "value": f"{i['rain']['3h']} mm"} + {"empty": True}
            if "snow" in i.keys():
                self.wrb + {"name": "Time", "value": f"{datetime.datetime.fromtimestamp(i['dt']).strftime('%H:%M')}"}\
                    + {"name": "Snow", "value": f"{i['snow']['3h']} mm "} + {"empty": True}
        await message.channel.send(embed=self.wrb.build())

    @chatbot_response
    @interactive
    async def get_help(self, message: Message):
        # these could be read out of a file too, but still for sake of convenience this is better
        self.wrb.new().title("Help").color(Colour.green()).description("Here are the commands that you can use.")\
            + {"name": "are you up", "value": "Prints if the bot is online.", "inline": "False"}\
            + {"name": "set forecast location", "value": "Sets the location of the weather forecasts.", "inline": "False"}\
            + {"name": "set forecast city", "value": "Sets the city location of the weather forecasts.", "inline": "False"}\
            + {"name": "current location", "value": "Prints the current forecast location.", "inline": "False"}\
            + {"name": "now", "value": "Prints the current weather conditions.", "inline": "False"}\
            + {"name": "today", "value": "Prints today's weather conditions", "inline": "False"}\
            + {"name": "rain", "value": "Prints if there's going to be any rain today.", "inline": "False"}
        await message.channel.send(embed=self.wrb.build())

    @chatbot_response
    @interactive
    async def get_now_city(self, message: Message):
        await message.channel.send(embed=self.bb.new().color(Colour.green()).title(Responses.GET_NOW_CITY).build())

    @chatbot_response
    @interactive
    async def set_now_city(self, message: Message):
        await self.get_now(message, city_name=message.content)

    @chatbot_response
    @interactive
    async def get_today_city(self, message: Message):
        await message.channel.send(embed=self.bb.new().color(Colour.green()).title(Responses.GET_NOW_CITY).build())

    @chatbot_response
    @interactive
    async def set_today_city(self, message: Message):
        await self.get_today(message, city_name=message.content)
