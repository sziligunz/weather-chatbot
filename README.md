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

## Unittest

| Name                       | Statements | Missed  | Covered |
|----------------------------|------------|---------|---------|
| EmbedBuilder.py            | 58         | 36      | 38%     |
| WeatherApi.py              | 72         | 6       | 92%     |
| WeatherChatBotException.py | 13         | 4       | 69%     |
| WeatherResponses.py        | 222        | 130     | 41%     |
| **TOTAL**                  | **455**    | **212** | **53%** |

----

## Installation

1. Clone the repository: `git clone https://github.com/sziligunz/weather-chatbot`
2. Create virtual environment: `virtualenv venv`
3. Activate virtual environment: `venv/Scripts/activate`
4. Install requirements: `pip install -r requirements.txt`
5. Add the token files to root: 
   1. `discord-token.json`:
      ```javascript
      {
        "token": "MTA5MjQyNjM5MjIwMjkxOTk5Nw.GMKWh1.GE3opKoPCjkf1Cex-lQNoTl6AgJ8qZ7pxrYTwU",
        "creation-time": "2023-04-03T14:44:00"
      }
      ```
   2. `weather-token.json`:
      ```javascript
      {
        "token": "5fa35ae8d45a16ee2ac3f922580e8bef",
        "creation-time": "2023-04-04T15:11:00"
      }
      ```
6. Launch the bot: `python WeatherBot.py`
