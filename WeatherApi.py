import json
import pathlib
import requests

from WeatherChatBotException import WeatherApiException


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


class API:

    TOKEN = get_token("weather-token.json")
    CURRENT_WEATHER = "https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API key}"
    BASIC_WEATHER_MAP = "https://tile.openweathermap.org/map/{layer}/{z}/{x}/{y}.png?appid={API key}"
    CITYNAME = "http://api.openweathermap.org/geo/1.0/direct?q={city name},{country code}&limit={limit}&appid={API key}"

    def __init__(self, location_name: str, lat=None, lon=None):
        self.location_name = location_name
        if lat is None and lon is None:
            with open(self.location_name, "r") as f:
                data = json.loads(f.readline())
                self._lat = float(data["lat"])
                self._lon = float(data["lon"])
        else:
            self._lat = lat
            self._lon = lon

    @property
    def latitude(self):
        return self._lat

    @property
    def longitude(self):
        return self._lon

    @staticmethod
    def convert_city_to_lat_lon(city_name) -> tuple:
        _url = API.CITYNAME\
            .replace("{city name}", f"{city_name}")\
            .replace("{country code}", "hu")\
            .replace("{limit}", "1")\
            .replace("{API key}", f"{API.TOKEN}")
        res = requests.get(url=_url).json()
        if not res:
            raise WeatherApiException("Couldn't convert city name to latitude and longitude", _url)
        return res[0]['lat'], res[0]['lon']
