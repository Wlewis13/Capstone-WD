import requests  # Imports the requests library to make HTTP requests to the weather API

# Your API key from OpenWeatherMap
API_KEY = "344177637f7ed7cb86f69139065fb056"

# URL for current weather data
WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather"

# URL for 5-day/3-hour forecast data
FORECAST_URL = "http://api.openweathermap.org/data/2.5/forecast"

# Function to fetch both current weather and forecast data for a given city
def fetch_weather_data(city):
    # Set up parameters to send with the request: city name, API key, and temperature units in Fahrenheit
    params = {"q": city, "appid": API_KEY, "units": "imperial"}

    # Make a GET request to the weather URL with parameters
    weather_resp = requests.get(WEATHER_URL, params=params)
    # Raise an error if the request failed (e.g. bad city name or network issue)
    weather_resp.raise_for_status()
    # Convert the response to JSON (Python dictionary)
    weather = weather_resp.json()

    # Make a GET request to the forecast URL with the same parameters
    forecast_resp = requests.get(FORECAST_URL, params=params)
    # Raise an error if the forecast request failed
    forecast_resp.raise_for_status()
    # Convert the forecast response to JSON
    forecast = forecast_resp.json()

    # Return both weather and forecast data
    return weather, forecast

