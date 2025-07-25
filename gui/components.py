import tkinter as tk
from core.utils import fetch_icon  # Utility to fetch and resize weather icons
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Embed matplotlib in Tkinter
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image, ImageTk
import requests
from io import BytesIO

def get_day_background(desc):
    desc = desc.lower()
    if "rain" in desc:
        return "#add8e6"
    elif "cloud" in desc:
        return "#d3d3d3"
    elif "snow" in desc:
        return "#f0f8ff"
    elif "storm" in desc:
        return "#778899"
    elif "sun" in desc or "clear" in desc:
        return "#fffacd"
    else:
        return "#ffffff"

def populate_weather_panel(panel, city, data):
    bg_color = get_day_background(data['description'])
    panel.configure(bg=bg_color)

    tk.Label(panel, text=f"{city}", font=("Arial", 16, "bold"), bg=bg_color, fg="navy").pack(pady=5)
    icon_url = f"http://openweathermap.org/img/wn/{data['icon']}@2x.png"
    icon_img = fetch_icon(icon_url)
    if icon_img:
        lbl = tk.Label(panel, image=icon_img, bg=bg_color)
        lbl.image = icon_img
        lbl.pack()

    tk.Label(panel, text=f"Temperature: {data['temperature']}°F", font=("Arial", 12), bg=bg_color, fg="navy").pack()
    tk.Label(panel, text=f"Condition: {data['description']}", font=("Arial", 12), bg=bg_color, fg="navy").pack()
    tk.Label(panel, text=f"Humidity: {data['humidity']}%", font=("Arial", 12), bg=bg_color, fg="navy").pack()
    tk.Label(panel, text=f"Sunrise: {data['sunrise']}", font=("Arial", 12), bg=bg_color, fg="orange").pack()
    tk.Label(panel, text=f"Sunset: {data['sunset']}", font=("Arial", 12), bg=bg_color, fg="darkred").pack()

    display_allergen_icons(panel, bg_color)

def display_allergen_icons(panel, bg_color="#ffffff"):
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

def display_weekly_forecast(parent_frame, forecast_data):
    outer_frame = tk.Frame(parent_frame, bg="white")
    outer_frame.pack(fill="both", expand=True, pady=10)

    canvas = tk.Canvas(outer_frame, bg="white")
    v_scrollbar = tk.Scrollbar(outer_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="white")

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    scrollable_frame.bind("<Configure>", on_frame_configure)
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=v_scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    v_scrollbar.pack(side="right", fill="y")

    tk.Label(scrollable_frame, text="5-Day Forecast", font=("Arial", 14, "bold"), bg="white", fg="navy").pack(padx=10, pady=5)

    day_frame = tk.Frame(scrollable_frame, bg="white")
    day_frame.pack(anchor="center")

    daily_data = []

    for i in range(0, 40, 8):
        day = forecast_data["list"][i]
        date = day["dt_txt"].split(" ")[0]
        temp = int(day["main"]["temp"])
        desc = day["weather"][0]["description"].capitalize()
        icon_code = day["weather"][0]["icon"]
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        icon_img = fetch_icon(icon_url, resize=(50, 50))
        bg = get_day_background(desc)

        daily_data.append((date[-5:], temp, icon_url, desc.lower()))

        panel = tk.Frame(day_frame, bd=1, relief="solid", bg=bg, width=140, height=170)
        panel.pack_propagate(0)
        panel.pack(side="left", padx=10, pady=10)

        tk.Label(panel, text=date[-5:], font=("Arial", 10, "bold"), bg=bg, fg="navy").pack()
        if icon_img:
            lbl = tk.Label(panel, image=icon_img, bg=bg)
            lbl.image = icon_img
            lbl.pack()
        tk.Label(panel, text=f"{temp}°F", font=("Arial", 10), bg=bg, fg="navy").pack()
        tk.Label(panel, text=desc, font=("Arial", 9), bg=bg, fg="navy", wraplength=100).pack()

    graph_frame = tk.Frame(scrollable_frame, bg="white")
    graph_frame.pack(pady=10)
    graph_canvas = None

    def toggle_graph():
        nonlocal graph_canvas
        if graph_canvas and graph_canvas.get_tk_widget().winfo_ismapped():
            graph_canvas.get_tk_widget().pack_forget()
            toggle_btn.config(text="Show Forecast Graph")
        else:
            if not graph_canvas:
                graph_canvas = show_forecast_graph(graph_frame, daily_data)
            else:
                graph_canvas.draw()
                graph_canvas.get_tk_widget().pack(pady=10)
            toggle_btn.config(text="Hide Forecast Graph")

    toggle_btn = tk.Button(graph_frame, text="Show Forecast Graph", command=toggle_graph)
    toggle_btn.pack()

def show_forecast_graph(parent, daily_data):
    dates = [d[0] for d in daily_data]
    temps = [d[1] for d in daily_data]
    icon_urls = [d[2] for d in daily_data]
    conditions = [d[3] for d in daily_data]

    fig, ax = plt.subplots(figsize=(6, 3))

    colors = []
    for cond in conditions:
        if "rain" in cond:
            colors.append("blue")
        elif "cloud" in cond:
            colors.append("gray")
        elif "clear" in cond or "sun" in cond:
            colors.append("orange")
        else:
            colors.append("green")

    ax.plot(dates, temps, marker='o', color="black", linestyle='--')

    for i, (date, temp, icon_url) in enumerate(zip(dates, temps, icon_urls)):
        try:
            img_data = requests.get(icon_url).content
            img = Image.open(BytesIO(img_data)).resize((30, 30))
            imagebox = OffsetImage(img, zoom=1)
            ab = AnnotationBbox(imagebox, (date, temp + 2), frameon=False)
            ax.add_artist(ab)
        except:
            pass
        ax.text(date, temp - 2, f"{temp}°F", ha="center", fontsize=8, color="navy")

    ax.set_title("5-Day Temperature Forecast", fontsize=12, color="navy")
    ax.set_xlabel("Date", color="navy")
    ax.set_ylabel("Temp (°F)", color="navy")
    ax.grid(True)
    ax.set_ylim(min(temps) - 10, max(temps) + 15)
    ax.tick_params(colors='navy')

    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=10)
    return canvas

def display_horizontal_forecast(panel, forecast_data, bordered=False):
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

        if bordered:
            day_frame = tk.Frame(frame, bg=bg, bd=2, relief="groove", padx=5, pady=5)
        else:
            day_frame = tk.Frame(frame, bg=bg, padx=5, pady=5)

        day_frame.pack(side="left", padx=5)

        tk.Label(day_frame, text=date[-5:], font=("Arial", 10), bg=bg, fg="navy").pack()
        if icon_img:
            lbl = tk.Label(day_frame, image=icon_img, bg=bg)
            lbl.image = icon_img
            lbl.pack()
        tk.Label(day_frame, text=f"{temp}°F", font=("Arial", 10), bg=bg, fg="navy").pack()
