from unittest import TestCase

import WeatherChatBotException
from WeatherApi import API


class TestAPI(TestCase):
    api = API("location-Weather-Bot-1391")

    def test_latitude(self):
        self.assertEqual(self.api.latitude, self.api._lat)

    def test_longitude(self):
        self.assertEqual(self.api.longitude, self.api._lon)

    def test_city_name(self):
        self.assertEqual(self.api.city_name, self.api._city)

    def test_convert_city_to_lat_lon(self):
        self.assertEqual((46.2744169, 20.0657989), self.api.convert_city_to_lat_lon("Kiskundorozsma"))

    def test_get_weather_now(self):
        now = self.api.get_weather_now()
        self.assertTrue("weather" in now.keys())

    def test_get_weather_now_city(self):
        now = self.api.get_weather_now(cityname="Szeged")
        self.assertTrue("weather" in now.keys())

    def test_get_weather_now_wrong_city(self):
        with self.assertRaises(WeatherChatBotException.WeatherApiException):
            self.api.get_weather_now(city_name="asdasd")

    def test_get_weather_icon(self):
        self.assertEqual(API.WEATHER_ICON.replace("{icon}", "asd"), self.api.get_weather_icon("asd"))

    def test_get_weather_5day(self):
        _5day = self.api.get_weather_5day()
        self.assertTrue("list" in _5day.keys())

    def test_get_weather_5day_city(self):
        _5day = self.api.get_weather_5day(city_name="Szeged")
        self.assertTrue("list" in _5day.keys())

    def test_get_weather_5day_wrong_city(self):
        with self.assertRaises(WeatherChatBotException.WeatherApiException):
            self.api.get_weather_5day(city_name="asdasd")
