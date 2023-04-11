from unittest import TestCase

from WeatherChatBotException import WeatherApiException, ChatBotException
from WeatherApi import API
from WeatherResponses import Responses


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
        with self.assertRaises(WeatherApiException):
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
        with self.assertRaises(WeatherApiException):
            self.api.get_weather_5day(city_name="asdasd")


class TestResponses(TestCase):
    responses = Responses()

    async def test_did_not_recognize(self):
        with self.assertRaises(ChatBotException):
            await self.responses.did_not_recognize()

    async def test_no_location_set(self):
        with self.assertRaises(ChatBotException):
            await self.responses.did_not_recognize()

    async def test_get_up(self):
        with self.assertRaises(ChatBotException):
            await self.responses.did_not_recognize()

    async def test_mention_miki(self):
        with self.assertRaises(ChatBotException):
            await self.responses.did_not_recognize()

    async def test_get_forecast_location(self):
        with self.assertRaises(ChatBotException):
            await self.responses.did_not_recognize()

    async def test_set_forecast_location(self):
        with self.assertRaises(ChatBotException):
            await self.responses.did_not_recognize()

    async def test_get_purpose(self):
        with self.assertRaises(ChatBotException):
            await self.responses.did_not_recognize()

    async def test_get_city(self):
        with self.assertRaises(ChatBotException):
            await self.responses.did_not_recognize()

    async def test_set_city(self):
        with self.assertRaises(ChatBotException):
            await self.responses.did_not_recognize()

    async def test_get_current_location(self):
        with self.assertRaises(ChatBotException):
            await self.responses.did_not_recognize()

    async def test_get_now(self):
        with self.assertRaises(ChatBotException):
            await self.responses.did_not_recognize()

    async def test_get_today(self):
        with self.assertRaises(ChatBotException):
            await self.responses.did_not_recognize()

    async def test_get_rain(self):
        with self.assertRaises(ChatBotException):
            await self.responses.did_not_recognize()

    async def test_get_help(self):
        with self.assertRaises(ChatBotException):
            await self.responses.did_not_recognize()

    async def test_get_now_city(self):
        with self.assertRaises(ChatBotException):
            await self.responses.did_not_recognize()

    async def test_set_now_city(self):
        with self.assertRaises(ChatBotException):
            await self.responses.did_not_recognize()

    async def test_get_today_city(self):
        with self.assertRaises(ChatBotException):
            await self.responses.did_not_recognize()

    async def test_set_today_city(self):
        with self.assertRaises(ChatBotException):
            await self.responses.did_not_recognize()
