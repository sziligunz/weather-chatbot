# Weather Chatbot

*This repository is created for 2022/23/2 Python programozás a gyakorlatban course by __AQ56DX__*

----

## Description
This project is a discord chatbot written in python. The purpose of this application is to provide fast and easy access
to basic weather data.

----

## Features

- Get current weather conditions *(this is from pre saved city locations)*
- Get weather conditions for the whole day *(this is from pre saved city locations)*
- Get if there's going to be any rain during the current day
- Get current weather from a city of your choice
- Get weather conditions for the whole day from a city of you choice

*Disclaimer: weather data querying works only with hungarian cities.
International querying has not been implemented yet.*

----

## Work in progress

- International weather forecast querying
- Weather images

----

## Flake8

- `WeatherBot.py`:
  - line too long
- `WeatherResponses.py`:
  - line too long
- `WeatherApi.py`:
  - line too long
- `EmbedBuilder.py`:
  - line too long
- `WeatherChatBotException.py`:
  - ✅

----

## Pep8

- `WeatherBot.py`:
  - line too long
- `WeatherResponses.py`:
  - line too long
- `WeatherApi.py`:
  - line too long
- `EmbedBuilder.py`:
  - line too long
- `WeatherChatBotException.py`:
  - line too long

----

# Unittest

| Name                       | Statements | Missed  | Covered |
|----------------------------|------------|---------|---------|
| EmbedBuilder.py            | 58         | 36      | 38%     |
| WeatherApi.py              | 72         | 6       | 92%     |
| WeatherChatBotException.py | 13         | 4       | 69%     |
| WeatherResponses.py        | 222        | 130     | 41%     |
| **TOTAL**                  | **455**    | **212** | **53%** |
