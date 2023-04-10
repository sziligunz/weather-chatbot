import discord
from discord import Embed

import WeatherApi


class BasicPrintBuilder:
    def __init__(self):
        self._color = None
        self._title = None
        self._description = None
        self._embed = Embed(type="rich")

    def color(self, color: int | discord.Color):
        self._color = color
        return self

    def title(self, title: str):
        self._title = title
        return self

    def description(self, description: str):
        self._description = description
        return self

    def build(self):
        self._embed.color = self._color
        self._embed.title = self._title
        self._embed.description = self._description
        return self._embed

    def new(self):
        self._embed = Embed()
        return self


class WeatherReportBuilder(BasicPrintBuilder):
    def __init__(self):
        super().__init__()

    def thumbnail(self, link: str):
        self._embed.set_thumbnail(url=link)
        return self

    def set_most_common_thumbnail(self, forecasts: list):
        urls = dict()
        for i in forecasts:
            _index = i['weather'][0]['icon']
            if _index not in urls.keys():
                urls[_index] = 0
            urls[_index] += 1
        sorted_urls = sorted(urls.items(), key=lambda x: x[1], reverse=True)
        self._embed.set_thumbnail(url=WeatherApi.API.get_weather_icon(sorted_urls[0][0]))
        return self

    # Adding arguments to the embed
    def __add__(self, other):
        if isinstance(other, dict) and "name" in other.keys() and "value" in other.keys():
            if "inline" in other.keys():
                self._embed.add_field(name=other["name"], value=other["value"], inline=other["inline"])
            else:
                self._embed.add_field(name=other["name"], value=other["value"], inline=True)
            if "index" in other.keys():
                self._embed.insert_field_at(other["index"], name=other["name"], value=other["value"], inline=True)
        return self
