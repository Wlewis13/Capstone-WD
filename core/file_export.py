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
