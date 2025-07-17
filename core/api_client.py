import requests

API_KEY = "344177637f7ed7cb86f69139065fb056"
WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "http://api.openweathermap.org/data/2.5/forecast"

def fetch_weather_data(city):
    params = {"q": city, "appid": API_KEY, "units": "imperial"}

    try:
        # Fetch current weather data
        weather_resp = requests.get(WEATHER_URL, params=params)
        weather_resp.raise_for_status()
        weather = weather_resp.json()

        # Check if the city was found (API may return 200 OK but still say "city not found")
        if weather.get("cod") != 200:
            raise ValueError(f"City '{city}' not found. (Error: {weather.get('message', 'Unknown')})")

        # Fetch forecast data
        forecast_resp = requests.get(FORECAST_URL, params=params)
        forecast_resp.raise_for_status()
        forecast = forecast_resp.json()

        if forecast.get("cod") != "200":
            raise ValueError(f"Forecast data error for '{city}'. (Error: {forecast.get('message', 'Unknown')})")

        return weather, forecast

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
