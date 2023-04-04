import requests
from WeatherBot import get_token


class API:

    TOKEN = get_token("weather-token.json")
    CURRENT_WEATHER = "https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API key}"
    BASIC_WEATHER_MAP = "https://tile.openweathermap.org/map/{layer}/{z}/{x}/{y}.png?appid={API key}"

    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon
