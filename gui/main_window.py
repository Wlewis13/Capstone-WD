import tkinter as tk
from tkinter import ttk, messagebox, Toplevel
from PIL import Image, ImageTk, ImageSequence
from datetime import datetime
import threading
import math
import calendar

from core.api_client import fetch_weather_data
from core.weather_data import process_weather_and_forecast
from core.file_export import save_weather_to_csv
from gui.components import (
    populate_weather_panel,
    display_weekly_forecast,
    display_horizontal_forecast
)
from gui.themes import set_background_theme

NAVY_BLUE = "#000080"
WHITE = "#ffffff"
DARK_BG = "#1a1a1a"
LIGHT_BG = WHITE

ZODIAC_HOROSCOPES = {
    "Aries": "It's National Curry Goat Day, make yourself Invisible.",
    "Taurus": "Burger!!!, Cheese on Mines.",
    "Gemini": "You are an undiagnosed Bi-polar Case - Seek Help!.",
    "Cancer": "You are a Crab, a Crab!!! of all things a Crab, Go blow some Bubbles.",
    "Leo": "You are just a house Cat that had steriods in their milk, Relax go Meow & Catch a Mice.",
    "Virgo": "The Virgin, Righttttt: the lie detector determined that was a LIE!.",
    "Libra": "You are going to need alot of Meds before anyone can consider you Balanced.",
    "Scorpio": "You are a Shrimp with a stinger, that has a paralzying taste, go Detox.",
    "Sagittarius": "You are a Horse with a Bow and Arrow, you are not a Centaur, humble yourself.",
    "Capricorn": "Jackie Chan(Who am I?), you are a Goat with a Fish tail, pick a specie!.",
    "Pisces": "How you fall for the bait on the hook trick everytime? smarten up!.",
    "Aquarius": "Look at them, Staring at You:Yes we are who TF we say we are! Act Accordingly & Move around!!!."
}

class WeatherApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Weather Dashboard by Wendell Lewis, First of His Name")
        self.root.geometry("1200x700")
        self.root.resizable(False, False)

        self.frames = []
        self.settings = {
            "forecast_layout": "Zoomed Out"
        }

        self.setup_ui()

    def toggle_city_inputs(self, event=None):
        if self.view_mode.get() == "Two Cities":
            self.city2_entry.grid()
        else:
            self.city2_entry.grid_remove()
            self.city2_entry.delete(0, tk.END)

    def view_weather(self):
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        city1 = self.city1_entry.get().strip()
        city2 = self.city2_entry.get().strip()

        if not city1:
            messagebox.showwarning("Input Error", "Please enter at least one city.")
            return

        try:
            weather1, forecast1 = fetch_weather_data(city1)
            data1 = process_weather_and_forecast(weather1, forecast1)

            if self.view_mode.get() == "One City":
                panel = tk.Frame(self.result_frame, bd=2, relief="groove", width=1150, bg="#ffffff")
                panel.pack(padx=10, pady=10, fill="x")
                populate_weather_panel(panel, city1, data1)
                if self.settings["forecast_layout"] == "Zoomed In":
                    display_horizontal_forecast(panel, data1["forecast"])
                else:
                    display_weekly_forecast(self.result_frame, data1["forecast"])
            else:
                panel = tk.LabelFrame(self.result_frame, bd=2, relief="ridge", width=550, bg="#ffffff", text=f"{city1} Forecast", font=("Arial", 10, "bold"))
                panel.grid(row=0, column=0, padx=10, pady=10, sticky="n")
                populate_weather_panel(panel, city1, data1)
                display_horizontal_forecast(panel, data1["forecast"], bordered=True)

            if self.view_mode.get() == "Two Cities":
                if not city2:
                    messagebox.showwarning("Input Error", "Please enter the second city.")
                    return
                weather2, forecast2 = fetch_weather_data(city2)
                data2 = process_weather_and_forecast(weather2, forecast2)

                panel2 = tk.LabelFrame(self.result_frame, bd=2, relief="ridge", width=550, bg="#ffffff", text=f"{city2} Forecast", font=("Arial", 10, "bold"))
                panel2.grid(row=0, column=1, padx=10, pady=10, sticky="n")
                populate_weather_panel(panel2, city2, data2)
                display_horizontal_forecast(panel2, data2["forecast"], bordered=True)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch weather data. Please try again.\n\n{e}")

    def save_to_csv(self):
        city = self.city1_entry.get().strip()
        if not city:
            messagebox.showwarning("Save CSV", "Please enter a city and view its weather before saving.")
            return
        try:
            weather, forecast = fetch_weather_data(city)
            data = process_weather_and_forecast(weather, forecast)
            file_path = save_weather_to_csv(city, data)
            messagebox.showinfo("Save CSV", f"Weather data for {city} was saved successfully.\n\n{file_path}")
        except Exception as e:
            messagebox.showerror("Save CSV Error", f"Failed to save CSV.\n\n{e}")

    def show_moon_calendar(self):
        win = Toplevel(self.root)
        win.title("Moon Calendar")
        win.geometry("400x400")
        win.config(bg=WHITE)

        now = datetime.now()
        year, month = now.year, now.month

        tk.Label(win, text=f"{calendar.month_name[month]} {year}", font=("Arial", 16, "bold"), fg=NAVY_BLUE, bg=WHITE).pack(pady=10)

        frame = tk.Frame(win, bg=WHITE)
        frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(frame, bg=WHITE, highlightthickness=0)
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable = tk.Frame(canvas, bg=WHITE)

        scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def moon_phase(date):
            diff = date - datetime(2001, 1, 1)
            days = diff.days + (diff.seconds / 86400)
            lunations = 0.20439731 + (days * 0.03386319269)
            phase_index = int((lunations % 1) * 8 + 0.5) % 8
            phases = [
                ("New Moon", "🌑"),
                ("Waxing Crescent", "🌒"),
                ("First Quarter", "🌓"),
                ("Waxing Gibbous", "🌔"),
                ("Full Moon", "🌕"),
                ("Waning Gibbous", "🌖"),
                ("Last Quarter", "🌗"),
                ("Waning Crescent", "🌘")
            ]
            return phases[phase_index]

        for day in range(1, calendar.monthrange(year, month)[1] + 1):
            date_obj = datetime(year, month, day)
            phase_name, phase_icon = moon_phase(date_obj)
            if phase_name in ["New Moon", "First Quarter", "Full Moon", "Last Quarter"]:
                label = tk.Label(scrollable, text=f"{date_obj.strftime('%B %d, %Y')} - {phase_icon} {phase_name}",
                                 font=("Arial", 12), fg=NAVY_BLUE, bg=WHITE, anchor="w", padx=10, pady=5)
                label.pack(fill="x", pady=2)

    def show_settings_menu(self):
        win = Toplevel(self.root)
        win.title("Settings")
        win.geometry("300x200")
        win.config(bg=WHITE)

        tk.Label(win, text="Forecast View Layout:", font=("Arial", 12), bg=WHITE, fg=NAVY_BLUE).pack(pady=10)
        layout_var = tk.StringVar(value=self.settings.get("forecast_layout", "Weekly"))
        layout_menu = ttk.Combobox(win, textvariable=layout_var, values=["Zoomed Out", "Zoomed In"], state="readonly")
        layout_menu.pack(pady=5)

        def save_settings():
            self.settings["forecast_layout"] = layout_var.get()
            messagebox.showinfo("Saved", "Settings have been saved, Click view weather again.")
            win.destroy()

        tk.Button(win, text="Save", command=save_settings, bg=WHITE, fg=NAVY_BLUE).pack(pady=10)

    def setup_ui(self):
        self.background_label = tk.Label(self.root)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.input_frame = tk.Frame(self.root, bg=WHITE, bd=2, relief="groove")
        self.input_frame.pack(pady=10)

        style = ttk.Style()
        style.configure("TCombobox", foreground=NAVY_BLUE, fieldbackground=WHITE, background=WHITE)

        self.view_mode = tk.StringVar(value="Select an Option")
        mode_menu = ttk.Combobox(
            self.input_frame,
            textvariable=self.view_mode,
            values=["Select an Option", "One City", "Two Cities"],
            width=15,
            state="readonly",
            style="TCombobox"
        )
        mode_menu.grid(row=0, column=0, padx=5)
        mode_menu.bind("<<ComboboxSelected>>", self.toggle_city_inputs)

        entry_style = {"bg": WHITE, "fg": NAVY_BLUE, "insertbackground": NAVY_BLUE}
        button_style = {"bg": WHITE, "fg": NAVY_BLUE, "activebackground": "#e6e6ff", "activeforeground": NAVY_BLUE, "relief": "raised"}

        self.city1_entry = tk.Entry(self.input_frame, width=20, **entry_style)
        self.city1_entry.grid(row=0, column=1, padx=5)

        self.city2_entry = tk.Entry(self.input_frame, width=20, **entry_style)
        self.city2_entry.grid(row=0, column=2, padx=5)
        self.city2_entry.grid_remove()

        tk.Button(self.input_frame, text="View Weather", command=self.view_weather, **button_style).grid(row=0, column=3, padx=5)
        tk.Button(self.input_frame, text="🌙 Moon Calendar", command=self.show_moon_calendar, **button_style).grid(row=0, column=4, padx=5)
        tk.Button(self.input_frame, text="♟ Horoscope", command=self.show_horoscope_popup, **button_style).grid(row=0, column=5, padx=5)
        tk.Button(self.input_frame, text="Save CSV", command=self.save_to_csv, **button_style).grid(row=0, column=6, padx=5)
        tk.Button(self.input_frame, text="⚙️ Settings", command=self.show_settings_menu, **button_style).grid(row=0, column=7, padx=5)

        self.result_frame = tk.Frame(self.root, bg="lightblue", bd=2, relief="groove")
        self.result_frame.pack(fill="both", expand=True)

    def show_horoscope_popup(self):
        win = Toplevel(self.root)
        win.title("Today's Horoscope")
        win.geometry("400x250")
        win.config(bg=WHITE)

        tk.Label(win, text="Select Your Zodiac Sign", font=("Arial", 14, "bold"), fg=NAVY_BLUE, bg=WHITE).pack(pady=10)

        zodiac_var = tk.StringVar()
        zodiac_menu = ttk.Combobox(win, textvariable=zodiac_var, values=list(ZODIAC_HOROSCOPES.keys()), state="readonly", width=20)
        zodiac_menu.pack(pady=5)

        result_label = tk.Label(win, text="", wraplength=350, font=("Arial", 12), fg=NAVY_BLUE, bg=WHITE, justify="left")
        result_label.pack(pady=10)

        def show_reading():
            sign = zodiac_var.get()
            if sign:
                reading = ZODIAC_HOROSCOPES.get(sign, "No reading available.")
                result_label.config(text=f"{sign}:\n{reading}")

        tk.Button(win, text="Get Horoscope", command=show_reading, bg=WHITE, fg=NAVY_BLUE).pack(pady=5)

    def run(self):
        self.root.mainloop()
