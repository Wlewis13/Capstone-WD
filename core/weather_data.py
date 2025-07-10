import datetime  # Imports datetime to work with timestamps and convert them to readable times

# Function to process raw weather and forecast data into a simpler dictionary
def process_weather_and_forecast(weather, forecast):
    # Extract weather description and capitalize the first letter
    desc = weather["weather"][0]["description"].capitalize()

    # Convert sunrise timestamp to a formatted time string (e.g., "06:45 AM")
    sunrise = datetime.datetime.fromtimestamp(weather["sys"]["sunrise"]).strftime("%I:%M %p")
    # Convert sunset timestamp to a formatted time string (e.g., "07:30 PM")
    sunset = datetime.datetime.fromtimestamp(weather["sys"]["sunset"]).strftime("%I:%M %p")

    # Create a dictionary containing key weather info and the forecast data
    data = {
        "temperature": weather["main"]["temp"],  # Current temperature
        "humidity": weather["main"]["humidity"],  # Current humidity percentage
        "description": desc,  # Weather description text
        "icon": weather["weather"][0]["icon"],  # Weather icon code
        "sunrise": sunrise,  # Formatted sunrise time
        "sunset": sunset,  # Formatted sunset time
        "forecast": forecast,  # Full forecast data passed in
    }
    # Return the organized weather data dictionary
    return data

