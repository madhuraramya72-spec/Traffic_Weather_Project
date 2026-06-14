import json
from datetime import datetime

import requests


API_KEY = "9kBzyTxPtmYG7swMhjbhZLZraESVKVFh"


def fetch_traffic():
    url = "https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?point=48.8566,2.3522&key=" + API_KEY

    response = requests.get(url)
    data = response.json()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"data/raw/traffic/traffic_{timestamp}.json"

    with open(file_name, "w") as file_handle:
        json.dump(data, file_handle)

    print("Traffic data saved")
    return file_name


if __name__ == "__main__":
    fetch_traffic()