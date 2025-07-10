import tkinter as tk  # Import Tkinter for GUI components
from core.utils import fetch_icon  # Import function to fetch weather icons from URLs

# Function to fill a given panel with weather info for a city
def populate_weather_panel(panel, city, data):
    panel.configure(bg="white")  # Set panel background color to white

    # Display city name as a bold label at the top
    tk.Label(panel, text=f"{city}", font=("Arial", 16, "bold"), bg="white").pack(pady=5)

    # Build URL for the weather icon image using the icon code from data
    icon_url = f"http://openweathermap.org/img/wn/{data['icon']}@2x.png"
    icon_img = fetch_icon(icon_url)  # Fetch and prepare the icon image

    if icon_img:  # If the icon was successfully fetched
        lbl = tk.Label(panel, image=icon_img, bg="white")  # Create label with the icon image
        lbl.image = icon_img  # Keep a reference to avoid garbage collection
        lbl.pack()

    # Show temperature, condition, humidity, sunrise, and sunset as labels
    tk.Label(panel, text=f"Temperature: {data['temperature']}°F", font=("Arial", 12), bg="white").pack()
    tk.Label(panel, text=f"Condition: {data['description']}", font=("Arial", 12), bg="white").pack()
    tk.Label(panel, text=f"Humidity: {data['humidity']}%", font=("Arial", 12), bg="white").pack()
    tk.Label(panel, text=f"Sunrise: {data['sunrise']}", font=("Arial", 12), bg="white", fg="orange").pack()
    tk.Label(panel, text=f"Sunset: {data['sunset']}", font=("Arial", 12), bg="white", fg="darkred").pack()

    display_allergen_icons(panel)  # Add allergen icons below the weather info

# Function to show allergen icons (like pollen and dust) in a panel
def display_allergen_icons(panel):
    from PIL import Image, ImageTk  # Import here to avoid global dependency if not used

    # List of allergen types and their icon image file paths
    allergens = [("Pollen", "assets/icons/pollen.png"), ("Dust", "assets/icons/dust.png")]

    row = tk.Frame(panel, bg="white")  # Create a frame to hold allergen icons side-by-side
    row.pack(pady=5)

    for name, icon_file in allergens:
        try:
            # Open allergen icon image and resize to 40x40 pixels
            img = Image.open(icon_file).resize((40, 40))
            icon = ImageTk.PhotoImage(img)
            # Create a label with image above text, green text color
            lbl = tk.Label(row, image=icon, text=name, compound="top", bg="white", fg="green", font=("Arial", 9))
            lbl.image = icon  # Keep reference to avoid garbage collection
            lbl.pack(side="left", padx=10)  # Pack icons side by side with some spacing
        except:
            # If image loading fails, just show text with "Low" level in green
            tk.Label(row, text=f"{name}: Low", fg="green", bg="white").pack(side="left", padx=10)

# Function to display a 7-day weather forecast vertically in a parent frame
def display_weekly_forecast(parent_frame, forecast_data):
    frame = tk.Frame(parent_frame, bg="white")  # Frame to contain the forecast section
    frame.pack(pady=10)

    # Title label for the forecast section
    title = tk.Label(frame, text="7-Day Forecast", font=("Arial", 14, "bold"), bg="white")
    title.pack(anchor="w", padx=10)

    day_frame = tk.Frame(frame, bg="white")  # Frame to hold individual day panels horizontally
    day_frame.pack(fill="x")

    # Loop through forecast list every 8th entry (roughly daily data points)
    for i in range(0, 40, 8):
        day = forecast_data["list"][i]
        date = day["dt_txt"].split(" ")[0]  # Extract just the date part
        temp = int(day["main"]["temp"])  # Round temperature to integer
        desc = day["weather"][0]["description"].capitalize()  # Weather description
        icon_code = day["weather"][0]["icon"]  # Icon code for weather
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"  # Icon URL
        icon_img = fetch_icon(icon_url, resize=(50, 50))  # Fetch and resize icon

        bg = get_day_background(desc)  # Get background color based on weather

        # Create a fixed-size panel for each day with border and background color
        panel = tk.Frame(day_frame, bd=1, relief="solid", bg=bg, width=140, height=170)
        panel.pack_propagate(0)  # Prevent child widgets from resizing the panel
        panel.pack(side="left", padx=5, pady=5)  # Pack side by side with spacing

        tk.Label(panel, text=date[-5:], font=("Arial", 10, "bold"), bg=bg).pack()  # Show day (MM-DD)
        if icon_img:
            lbl = tk.Label(panel, image=icon_img, bg=bg)  # Show weather icon
            lbl.image = icon_img  # Keep reference
            lbl.pack()
        tk.Label(panel, text=f"{temp}°F", font=("Arial", 10), bg=bg).pack()  # Show temperature
        tk.Label(panel, text=desc, font=("Arial", 9), bg=bg, wraplength=100).pack()  # Show description

# Function to display forecast horizontally with simpler panels (used for two-city comparison)
def display_horizontal_forecast(panel, forecast_data):
    frame = tk.Frame(panel, bg="white")  # Container frame for horizontal forecast
    frame.pack(pady=10)

    # Loop through forecast list every 8th entry to get daily data
    for i in range(0, 40, 8):
        day = forecast_data["list"][i]
        date = day["dt_txt"].split(" ")[0]  # Date string
        temp = int(day["main"]["temp"])  # Temperature integer
        icon_code = day["weather"][0]["icon"]  # Icon code
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}.png"  # Icon URL (smaller size)
        icon_img = fetch_icon(icon_url, resize=(40, 40))  # Fetch icon

        day_frame = tk.Frame(frame, bg="white")  # Frame for each day in horizontal row
        day_frame.pack(side="left", padx=5)

        tk.Label(day_frame, text=date[-5:], font=("Arial", 10), bg="white").pack()  # Date label
        if icon_img:
            lbl = tk.Label(day_frame, image=icon_img, bg="white")  # Icon label
            lbl.image = icon_img  # Keep reference
            lbl.pack()
        tk.Label(day_frame, text=f"{temp}°F", font=("Arial", 10), bg="white").pack()  # Temperature label

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
        return "#ffffff"  # Default white background
