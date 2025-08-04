import csv
import os
from datetime import datetime

def save_weather_to_csv(city, data, folder="exports"):
    """
    Saves current weather and forecast data to a CSV file.
    """
    os.makedirs(folder, exist_ok=True)
    filename = f"{folder}/{city}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        # Write current weather summary
        writer.writerow(["City", "Temperature (F)", "Humidity (%)", "Condition", "Sunrise", "Sunset"])
        writer.writerow([
            city,
            data["temperature"],
            data["humidity"],
            data["description"],
            data["sunrise"],
            data["sunset"]
        ])

        writer.writerow([])  # Empty row for spacing

        # Write 5-day forecast (8 data points per day ≈ every 3 hours)
        writer.writerow(["Date", "Time", "Temp (F)", "Condition"])
        for entry in data["forecast"]["list"]:
            dt_txt = entry["dt_txt"]  # e.g. "2025-07-10 15:00:00"
            date, time = dt_txt.split()
            temp = entry["main"]["temp"]
            condition = entry["weather"][0]["description"]
            writer.writerow([date, time, temp, condition])

    return filename

# ----------------------------------------------------------------------
# Summary of What This Code Does:
# ----------------------------------------------------------------------
# This script defines a function called `save_weather_to_csv()` that takes three parameters:
#   - `city`: The name of the city (used for labeling the file and CSV content).
#   - `data`: A dictionary that includes both current weather data and 5-day forecast data.
#   - `folder`: (optional) The folder where the CSV file will be saved. Defaults to "exports".

# Here's how the function works:

# 1. It creates the specified folder if it doesn't exist using `os.makedirs()`.
# 2. It generates a unique filename using the city name and the current timestamp (down to seconds).
#    Example: exports/Atlanta_20250804_194523.csv
# 3. It opens the file in write mode with UTF-8 encoding.
# 4. It writes a row of headers and a single row of current weather data:
#    - Temperature, Humidity, Weather Description, Sunrise, Sunset
# 5. It leaves a blank row for separation.
# 6. Then, it writes the forecast data:
#    - Each forecast entry includes date, time, temperature, and weather condition.
#    - The forecast data comes from `data["forecast"]["list"]` (typically 8 entries per day).
#    - These entries reflect 3-hour interval predictions from the OpenWeatherMap API.

# 7. After writing all data, the function returns the full path to the created CSV file.

# This function is useful for exporting weather reports in a format that can be easily opened
# in spreadsheet programs like Excel, shared via email, or archived for later analysis.
