import tkinter as tk
from tkinter import Frame, Label  # Import Tkinter for GUI components
from tkintermapview import TkinterMapView  # Import TkinterMapView for map display
from PIL import Image, ImageTk
import requests
import io

from core.api_client import API_KEY  # ✅ Import your existing API key

# def show_precipitation_map(parent, lat, lon):
#     print(f"Showing map for lat={lat}, lon={lon}")
#     # Your existing code to load and display the precipitation map goes here


# def show_precipitation_map(city, lat, lon, forecast):
#     # 🔍 Estimate total precipitation from the forecast data
#     total_precip = sum(item.get("rain", {}).get("3h", 0) for item in forecast.get("list", []))

#     # 📊 Determine the severity level
#     if total_precip > 30:
#         level = "Extreme"
#     elif total_precip > 20:
#         level = "Heavy"
#     elif total_precip > 10:
#         level = "Moderate"
#     else:
#         level = "Light"

#     # 🗺️ Generate map URL using OpenWeather Tile service (use zoom 6–10 for best view)
#     static_map_url = f"https://tile.openweathermap.org/map/precipitation_new/6/{int(lon)}/{int(lat)}.png?appid={API_KEY}"

#     try:
#         # 🌐 Fetch the static image
#         resp = requests.get(static_map_url)
#         image = Image.open(io.BytesIO(resp.content)).resize((400, 300))
#         photo = ImageTk.PhotoImage(image)
#     except Exception as e:
#         print(f"Map loading failed: {e}")
#         photo = None

#     # 🪟 Create pop-up window
#     win = tk.Toplevel()
#     win.title(f"Precipitation Map - {city}")
#     win.geometry("450x400")
#     tk.Label(win, text=f"Precipitation Level: {level}", font=("Arial", 14)).pack(pady=10)

#     # 🖼️ Show image if available, else show error
#     if photo:
#         lbl = Label(win, image=photo)
#         lbl.image = photo  # keep a reference!
#         lbl.pack()
#     else:
#         tk.Label(win, text="Unable to load precipitation map.", fg="red").pack()

import tkinter as tk
from tkintermapview import TkinterMapView

# Determine precipitation level based on mm/hr value
def get_precip_level(precip_value):
    if precip_value >= 30:
        return "Extreme"
    elif precip_value >= 15:
        return "Heavy"
    elif precip_value >= 5:
        return "Moderate"
    elif precip_value > 0:
        return "Light"
    else:
        return "None"

# Display precipitation panel with level and button to view map
def display_precipitation_panel(parent, city, precip_value, lat, lon):
    frame = tk.Frame(parent, bg="white", bd=2, relief="groove")
    frame.pack(pady=10, padx=10, fill="x")

    level = get_precip_level(precip_value)
    tk.Label(frame, text=f"Precipitation in {city}: {level}",
             font=("Arial", 12, "bold"), fg="blue", bg="white").pack(pady=5)

    if lat is not None and lon is not None:
        # Button to open the map in a pop-up
        tk.Button(frame, text="Show Precipitation Map",
                  command=lambda: show_precipitation_map(lat, lon)).pack(pady=5)
    else:
        tk.Label(frame, text="Location coordinates not available.",
                 fg="red", bg="white").pack()

# Show map with marker for the given coordinates
def show_precipitation_map(lat, lon):
    map_window = tk.Toplevel()
    map_window.title("Precipitation Map")
    map_window.geometry("600x400")

    map_widget = TkinterMapView(map_window, width=600, height=400, corner_radius=0)
    map_widget.pack(fill="both", expand=True)
    map_widget.set_position(lat, lon)
    map_widget.set_zoom(8)
    map_widget.set_marker(lat, lon, text="Selected City")
