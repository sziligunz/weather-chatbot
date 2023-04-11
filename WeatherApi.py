import json
import pathlib
import requests

from WeatherChatBotException import WeatherApiException


# same get_token function as in WeatherBot.py but can't import it, because of circle import
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


# this class contains all the api requests to https://openweathermap.org
class API:

    TOKEN = get_token("weather-token.json")
    CURRENT_WEATHER = "https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API key}&units=metric"
    BASIC_WEATHER_MAP = "https://tile.openweathermap.org/map/{layer}/{z}/{x}/{y}.png?appid={API key}"
    CITYNAME = "http://api.openweathermap.org/geo/1.0/direct?q={city name},{country code}&limit={limit}&appid={API key}"
    WEATHER_ICON = "https://openweathermap.org/img/wn/{icon}@2x.png"
    WEATHER_TODAY = "https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API key}&units=metric"
    WEATHER_IMAGE = "https://tile.openweathermap.org/map/{layer}/{z}/{x}/{y}.png?appid={API key}"

    # we have to check if the API object gets no parameters either,
    # because Responses object creates a field of API itself
    def __init__(self, location_name: str, lat=None, lon=None):
        self.location_name = location_name
        if lat is None and lon is None:
            self.update_location()
        else:
            self._lat = lat
            self._lon = lon
            self._city = ""

    @property
    def latitude(self):
        return self._lat

    @property
    def longitude(self):
        return self._lon

    @property
    def city_name(self):
        return self._city

    def update_location(self):
        with open(self.location_name, "r") as f:
            data = json.loads(f.readline())
            self._lat = float(data["lat"])
            self._lon = float(data["lon"])
            if "city" in data.keys():
                self._city = data["city"]

    # this function converts a regular hungarian city name to latitude and longitude values
    # (the api uses latitude and longitude values in its api requests)
    @staticmethod
    def convert_city_to_lat_lon(city_name) -> tuple:
        _url = API.CITYNAME\
            .replace("{city name}", f"{city_name}")\
            .replace("{country code}", "hu")\
            .replace("{limit}", "1")\
            .replace("{API key}", API.TOKEN)
        res = requests.get(url=_url).json()
        if not res:
            raise WeatherApiException("Couldn't convert city name to latitude and longitude", _url)
        return res[0]['lat'], res[0]['lon']

    # return the current weather conditions
    def get_weather_now(self, **kwargs):
        _url = ""
        if "city_name" in kwargs.keys():
            lat, lon = API.convert_city_to_lat_lon(kwargs["city_name"])
            _url = API.CURRENT_WEATHER \
                .replace("{lat}", f"{lat}") \
                .replace("{lon}", f"{lon}") \
                .replace("{API key}", API.TOKEN)
        else:
            _url = API.CURRENT_WEATHER\
                .replace("{lat}", f"{self.latitude}")\
                .replace("{lon}", f"{self.longitude}")\
                .replace("{API key}", API.TOKEN)
        res = requests.get(url=_url).json()
        if not res:
            raise WeatherApiException("Couldn't get current weather conditions", _url)
        return res

    # return a _url string that is referring to a weather condition image
    @staticmethod
    def get_weather_icon(icon):
        _url = API.WEATHER_ICON\
            .replace("{icon}", icon)
        return _url

    # return the weather forecast for 5 days ahead in 3 hour intervals
    def get_weather_5day(self, **kwargs):
        _url = ""
        if "city_name" in kwargs.keys():
            lat, lon = API.convert_city_to_lat_lon(kwargs["city_name"])
            _url = API.WEATHER_TODAY \
                .replace("{lat}", f"{lat}") \
                .replace("{lon}", f"{lon}") \
                .replace("{API key}", API.TOKEN)
        else:
            _url = API.WEATHER_TODAY \
                .replace("{lat}", f"{self.latitude}") \
                .replace("{lon}", f"{self.longitude}") \
                .replace("{API key}", API.TOKEN)
        res = requests.get(url=_url).json()
        if not res:
            raise WeatherApiException("Couldn't get today's weather conditions", _url)
        return res

    # @staticmethod
    # def get_weather_image(self):
    #     _url = API.WEATHER_IMAGE \
    #         .replace("{API key}", API.TOKEN)\
    #         .replace("{layer}", "precipitation_new")\
    #         .replace("{z}", str(1))\
    #         .replace("{x}", str(1))\
    #         .replace("{y}", str(1))
    #     # res = requests.get(url=_url)
    #     # if not res:
    #     #     raise WeatherApiException("Couldn't get weather image", _url)
    #     # return res
    #     return _url
