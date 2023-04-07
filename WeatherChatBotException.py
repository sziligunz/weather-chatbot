class ChatBotException(Exception):
    def __init__(self, message):
        super().__init__(self)
        self.message = message

    def __str__(self):
        return self.message


class WeatherApiException(Exception):
    def __init__(self, message, API):
        super().__init__(self)
        self.message = message
        self.API = API

    def __str__(self):
        return f"{self.message}.\nThe API request was: {self.API}"
