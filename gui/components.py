import tkinter as tk  # Import Tkinter for GUI components
from core.utils import fetch_icon  # Import function to fetch weather icons from URLs

# Function to determine background color based on weather description text
def get_day_background(desc):
    desc = desc.lower()  # Convert description to lowercase for matching
    if "rain" in desc:
        return "#add8e6"  # Light blue for rain
    elif "cloud" in desc:
        return "#d3d3d3"  # Light gray for clouds
    elif "snow" in desc:
        return "#f0f8ff"  # Very light blue for snow
    elif "storm" in desc:
        return "#778899"  # Slate gray for storm
    elif "sun" in desc or "clear" in desc:
        return "#fffacd"  # Light yellow for sunny/clear
    else:
        return "#ffffff"  # Default white

# Function to fill a given panel with weather info for a city
def populate_weather_panel(panel, city, data):
    bg_color = get_day_background(data['description'])  # Set background based on weather

    panel.configure(bg=bg_color)

    # Display city name
    tk.Label(panel, text=f"{city}", font=("Arial", 16, "bold"), bg=bg_color).pack(pady=5)

    icon_url = f"http://openweathermap.org/img/wn/{data['icon']}@2x.png"
    icon_img = fetch_icon(icon_url)

    if icon_img:
        lbl = tk.Label(panel, image=icon_img, bg=bg_color)
        lbl.image = icon_img
        lbl.pack()

    # Weather details
    tk.Label(panel, text=f"Temperature: {data['temperature']}°F", font=("Arial", 12), bg=bg_color).pack()
    tk.Label(panel, text=f"Condition: {data['description']}", font=("Arial", 12), bg=bg_color).pack()
    tk.Label(panel, text=f"Humidity: {data['humidity']}%", font=("Arial", 12), bg=bg_color).pack()
    tk.Label(panel, text=f"Sunrise: {data['sunrise']}", font=("Arial", 12), bg=bg_color, fg="orange").pack()
    tk.Label(panel, text=f"Sunset: {data['sunset']}", font=("Arial", 12), bg=bg_color, fg="darkred").pack()

    display_allergen_icons(panel, bg_color)

# Function to show allergen icons (like pollen and dust) in a panel
def display_allergen_icons(panel, bg_color="#ffffff"):
    from PIL import Image, ImageTk

    allergens = [("Pollen", "assets/icons/pollen.png"), ("Dust", "assets/icons/dust.png")]

    row = tk.Frame(panel, bg=bg_color)
    row.pack(pady=5)

    for name, icon_file in allergens:
        try:
            img = Image.open(icon_file).resize((40, 40))
            icon = ImageTk.PhotoImage(img)
            lbl = tk.Label(row, image=icon, text=name, compound="top", bg=bg_color, fg="green", font=("Arial", 9))
            lbl.image = icon
            lbl.pack(side="left", padx=10)
        except:
            tk.Label(row, text=f"{name}: Low", fg="green", bg=bg_color).pack(side="left", padx=10)

# Function to display a 5-day weather forecast vertically
def display_weekly_forecast(parent_frame, forecast_data):
    frame = tk.Frame(parent_frame, bg="white")
    frame.pack(pady=10)

    title = tk.Label(frame, text="5-Day Forecast", font=("Arial", 14, "bold"), bg="white")
    title.pack(anchor="w", padx=10)

    day_frame = tk.Frame(frame, bg="white") 
    day_frame.pack(fill="x")

    for i in range(0, 40, 8):
        day = forecast_data["list"][i]
        date = day["dt_txt"].split(" ")[0]
        temp = int(day["main"]["temp"])
        desc = day["weather"][0]["description"].capitalize()
        icon_code = day["weather"][0]["icon"]
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        icon_img = fetch_icon(icon_url, resize=(50, 50))

        bg = get_day_background(desc)

        panel = tk.Frame(day_frame, bd=1, relief="solid", bg=bg, width=140, height=170)
        panel.pack_propagate(0)
        panel.pack(side="left", padx=5, pady=5)

        tk.Label(panel, text=date[-5:], font=("Arial", 10, "bold"), bg=bg).pack()
        if icon_img:
            lbl = tk.Label(panel, image=icon_img, bg=bg)
            lbl.image = icon_img
            lbl.pack()
        tk.Label(panel, text=f"{temp}°F", font=("Arial", 10), bg=bg).pack()
        tk.Label(panel, text=desc, font=("Arial", 9), bg=bg, wraplength=100).pack()

# Function to display forecast horizontally (for two-city comparison)
def display_horizontal_forecast(panel, forecast_data):
    frame = tk.Frame(panel, bg="white")
    frame.pack(pady=10)

    for i in range(0, 40, 8):
        day = forecast_data["list"][i]
        date = day["dt_txt"].split(" ")[0]
        temp = int(day["main"]["temp"])
        desc = day["weather"][0]["description"]
        icon_code = day["weather"][0]["icon"]
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}.png"
        icon_img = fetch_icon(icon_url, resize=(40, 40))

        bg = get_day_background(desc)

        day_frame = tk.Frame(frame, bg=bg)
        day_frame.pack(side="left", padx=5)

        tk.Label(day_frame, text=date[-5:], font=("Arial", 10), bg=bg).pack()
        if icon_img:
            lbl = tk.Label(day_frame, image=icon_img, bg=bg)
            lbl.image = icon_img
            lbl.pack()
        tk.Label(day_frame, text=f"{temp}°F", font=("Arial", 10), bg=bg).pack()

