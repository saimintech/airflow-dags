import requests
import json
import os
from datetime import datetime, timedelta

def get_current_weather(WEATHER_API):
    try:
        location = 'Jakarta'
        date_now = datetime.now()
        timezone = timedelta(hours=7)
        jkt_time = date_now + timezone
        jkt_time_str = jkt_time.strftime("%Y-%m-%d-%H:%M:%S")

        # Create the home directory path
        home_directory = os.path.expanduser('~')
        file_path = os.path.join(home_directory, f'{location}-{jkt_time_str}.json')

        response = requests.get(f'http://api.weatherapi.com/v1/current.json?key={WEATHER_API}&q={location}')
        response_json = response.json()

        # Save the JSON to a file in the home directory
        with open(file_path, 'w') as json_file:
            json.dump(response_json, json_file)

        print(f"Weather data saved at: {file_path}")
