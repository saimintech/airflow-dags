import requests
import json
import os
from datetime import datetime, timedelta

def get_current_weather(WEATHER_API):
    try:
        location = 'Lahore'
        date_now = datetime.now()
        timezone = timedelta(hours=7)
        jkt_time = date_now + timezone
        jkt_time_str = jkt_time.strftime("%Y-%m-%d-%H:%M:%S")

        # Create the home directory path
        home_directory = os.path.expanduser('~')
        file_path = os.path.join(home_directory, f'{location}-{jkt_time_str}.json')

        response = requests.get(f'http://api.weatherapi.com/v1/current.json?key={WEATHER_API}&q={location}')
        weather_api_data = response.json()

        webapp_url = 'https://script.google.com/macros/s/AKfycbwmh82pjRk21Y8Y7spKvqPFWy7TmOYiz5sXR_-YDuLN7segrJqP4QgFPLbx-15eViCl4g/exec'
        # Post the weather data to the web app
        post_data_to_webapp(weather_api_data, webapp_url)

        # Save the JSON to a file in the home directory
        #with open(file_path, 'w') as json_file:
            #json.dump(response_json, json_file)

        print(f"Weather data saved is added to the sheet")

# Function to flatten the JSON data
def flatten_json(json_data, parent_key='', sep='_'):
    flattened = {}
    for key, value in json_data.items():
        new_key = f"{parent_key}{sep}{key}" if parent_key else key
        if isinstance(value, dict):
            flattened.update(flatten_json(value, new_key, sep=sep))
        else:
            flattened[new_key] = value
    return flattened

def post_data_to_webapp(json_data, webapp_url):
    # Flatten the JSON
    flattened_data = flatten_json(json_data)
    
    # Post the data to the webapp
    response = requests.post(webapp_url, json=flattened_data)
    
    if response.status_code == 200:
        print("Data posted successfully!")
    else:
        print(f"Failed to post data. Status code: {response.status_code}")

# Weather API response
 
# Replace with your web app URL
webapp_url = "https://your-webapp-url"


