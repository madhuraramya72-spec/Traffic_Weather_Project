import json
from datetime import datetime

import requests


API_KEY = "4c3b4b92efb342aa6d4bcfb9b64f3833"


def fetch_weather():
    city = "Paris"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    response = requests.get(url)
    data = response.json()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"data/raw/weather/weather_{timestamp}.json"

    with open(file_name, "w") as file_handle:
        json.dump(data, file_handle)

    print("Weather data saved:", file_name)
    return file_name


if __name__ == "__main__":
    fetch_weather()