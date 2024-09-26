import json
from urllib.request import urlopen, Request
from urllib.error import HTTPError

# Replace with your actual API key
api_key = "022febae84cab5e86145bc72b9c7dc9a"
# Replace with your desired location
location = "London"

# API endpoint for OpenWeatherMap
url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}"

# Make a GET request to the API
try:
    with urlopen(Request(url)) as response:
        # Check if the request was successful
        if response.status == 200:
            # Read and decode the response
            data = json.loads(response.read().decode())
            print("Weather Data:")
            print(data)
        else:
            print(f"Failed to get data: {response.status}")
            print("Response content:", response.read().decode())
except HTTPError as e:
    print(f"HTTP Error: {e.code}")
    print("Response content:", e.read().decode())
except Exception as e:
    print(f"Error: {e}")

