import requests  # Import the requests library to perform HTTP requests

# OpenWeatherMap API key (used for authentication with the weather API)
API_KEY = "344177637f7ed7cb86f69139065fb056"

# URLs for current weather and 5-day forecast endpoints
WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "http://api.openweathermap.org/data/2.5/forecast"

def fetch_weather_data(city):
    """
    Fetch current weather and 5-day forecast data for a given city.

    Args:
        city (str): Name of the city to retrieve weather data for.

    Returns:
        tuple: Two dictionaries (weather, forecast) containing the current weather
               and forecast data if the request is successful.

    Raises:
        SystemExit: Stops the program and displays an error message if something goes wrong.
    """
    # Define parameters to send to the API: city name, API key, and temperature unit (Fahrenheit)
    params = {"q": city, "appid": API_KEY, "units": "imperial"}

    try:
        # Make a request to get current weather data
        weather_resp = requests.get(WEATHER_URL, params=params)
        weather_resp.raise_for_status()  # Raises error for bad status codes (e.g. 404, 500)
        weather = weather_resp.json()  # Parse the JSON response into a Python dictionary

        # Even if the HTTP status is 200, OpenWeatherMap may include an internal error in the "cod" field
        if weather.get("cod") != 200:
            raise ValueError(f"City '{city}' not found. (Error: {weather.get('message', 'Unknown')})")

        # Make a second request to get the 5-day forecast data
        forecast_resp = requests.get(FORECAST_URL, params=params)
        forecast_resp.raise_for_status()
        forecast = forecast_resp.json()

        # Similar check for forecast API response (it returns "cod" as a string)
        if forecast.get("cod") != "200":
            raise ValueError(f"Forecast data error for '{city}'. (Error: {forecast.get('message', 'Unknown')})")

        # Return both current weather and forecast data
        return weather, forecast

    # Handle various possible exceptions and stop the program with a message
    except requests.exceptions.HTTPError as http_err:
        raise SystemExit(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError:
        raise SystemExit("Network connection error.")
    except requests.exceptions.Timeout:
        raise SystemExit("The request timed out.")
    except requests.exceptions.RequestException as err:
        raise SystemExit(f"An error occurred: {err}")
    except ValueError as val_err:
        raise SystemExit(str(val_err))


# -------------------------------------------------------------
# Summary of What This Code Does:
# -------------------------------------------------------------
# - This script defines a function `fetch_weather_data(city)` that fetches both
#   current weather and 5-day forecast data for a given city using the OpenWeatherMap API.
#
# - It sends HTTP GET requests to two endpoints:
#     1. `/weather` for current weather conditions
#     2. `/forecast` for a detailed forecast
#
# - It uses an API key to authenticate requests and retrieves the data in imperial units (°F).
#
# - The function parses the JSON response and validates that the city was found and
#   the response is valid (even if status code is 200, the API might return "city not found").
#
# - If successful, it returns the weather and forecast as Python dictionaries.
#
# - If any error occurs (network error, timeout, bad response, etc.), the function will
#   print a clear error message and exit the program using `SystemExit`.
#
# - This function is a foundational part of any weather app and is responsible for communicating
#   with the API and ensuring that only valid, usable data reaches the rest of your application.
