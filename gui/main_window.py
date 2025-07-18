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

class WeatherApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Weather Dashboard by Wendell Lewis")
        self.root.geometry("1200x700")
        self.root.resizable(False, False)

        self.clock_panel = None
        self.clock_label = None
        self.clock_canvas = None
        self.bg_animation = None
        self.frames = []

        self.setup_ui()

    def setup_ui(self):
        self.background_label = tk.Label(self.root)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Input frame with white bg and navy blue text
        self.input_frame = tk.Frame(self.root, bg=WHITE, bd=2, relief="groove")
        self.input_frame.pack(pady=10)

        self.view_mode = tk.StringVar(value="Select an Option")
        mode_menu = ttk.Combobox(
            self.input_frame,
            textvariable=self.view_mode,
            values=["Select an Option", "One City", "Two Cities"],
            width=15,
            state="readonly",
            foreground=NAVY_BLUE,
            background=WHITE,
        )
        mode_menu.grid(row=0, column=0, padx=5)
        mode_menu.bind("<<ComboboxSelected>>", self.toggle_city_inputs)

        # Style normal tk widgets with navy text on white bg
        entry_style = {"bg": WHITE, "fg": NAVY_BLUE, "insertbackground": NAVY_BLUE}
        button_style = {"bg": WHITE, "fg": NAVY_BLUE, "activebackground": "#e6e6ff", "activeforeground": NAVY_BLUE, "relief": "raised"}

        self.city1_entry = tk.Entry(self.input_frame, width=20, **entry_style)
        self.city1_entry.grid(row=0, column=1, padx=5)

        self.city2_entry = tk.Entry(self.input_frame, width=20, **entry_style)
        self.city2_entry.grid(row=0, column=2, padx=5)
        self.city2_entry.grid_remove()

        tk.Button(self.input_frame, text="View Weather", command=self.view_weather, **button_style).grid(row=0, column=3, padx=10)
        tk.Button(self.input_frame, text="Save CSV", command=self.save_to_csv, **button_style).grid(row=0, column=4, padx=10)
        tk.Button(self.input_frame, text="🕒 Show Clock", command=self.toggle_clock_panel, **button_style).grid(row=0, column=5, padx=5)
        tk.Button(self.input_frame, text="🌙 Moon Calendar", command=self.show_moon_calendar, **button_style).grid(row=0, column=6, padx=5)

        self.result_frame = tk.Frame(self.root, bg="lightblue", bd=2, relief="groove")
        self.result_frame.pack(fill="both", expand=True)

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

            self.set_time_based_background(data1["description"])

            if self.view_mode.get() == "One City":
                panel = tk.Frame(self.result_frame, bd=2, relief="groove", width=1150, bg="#ffffff")
                panel.pack(padx=10, pady=10, fill="x")
                populate_weather_panel(panel, city1, data1)
                display_weekly_forecast(self.result_frame, data1["forecast"])
            else:
                panel = tk.Frame(self.result_frame, bd=2, relief="groove", width=550, bg="#ffffff")
                panel.grid(row=0, column=0, padx=10, pady=10, sticky="n")
                populate_weather_panel(panel, city1, data1)
                display_horizontal_forecast(panel, data1["forecast"])

            if self.view_mode.get() == "Two Cities":
                if not city2:
                    messagebox.showwarning("Input Error", "Please enter the second city.")
                    return
                weather2, forecast2 = fetch_weather_data(city2)
                data2 = process_weather_and_forecast(weather2, forecast2)

                panel2 = tk.Frame(self.result_frame, bd=2, relief="groove", width=550, bg="#ffffff")
                panel2.grid(row=0, column=1, padx=10, pady=10, sticky="n")
                populate_weather_panel(panel2, city2, data2)
                display_horizontal_forecast(panel2, data2["forecast"])
        except Exception as e:
            messagebox.showerror("Error", "Please check spelling and try again.")

    def save_to_csv(self):
        city = self.city1_entry.get().strip()
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city first.")
            return
        try:
            weather, forecast = fetch_weather_data(city)
            data = process_weather_and_forecast(weather, forecast)
            file_path = save_weather_to_csv(city, data)
            messagebox.showinfo("Success", f"Weather data saved to:\n{file_path}")
        except Exception:
            messagebox.showerror("Error", "Weather data failed to save.")

    def toggle_clock_panel(self):
        if self.clock_panel and self.clock_panel.winfo_exists():
            self.clock_panel.destroy()
            self.clock_panel = None
        else:
            self.clock_panel = tk.Frame(self.result_frame, bg="black", width=200, height=200)
            self.clock_panel.place(x=950, y=10)
            self.clock_canvas = tk.Canvas(self.clock_panel, width=180, height=180, bg="black", highlightthickness=0)
            self.clock_canvas.pack()
            self.clock_label = tk.Label(self.clock_panel, text="", bg="black", fg="white", font=("Arial", 10))
            self.clock_label.pack()
            self.update_clock()

    def update_clock(self):
        if not self.clock_canvas:
            return

        now = datetime.now()
        self.clock_canvas.delete("all")
        self.clock_canvas.create_oval(10, 10, 170, 170, fill="white", outline="")

        for hour in range(1, 13):
            angle = math.radians((hour * 30) - 90)
            x = 90 + 70 * math.cos(angle)
            y = 90 + 70 * math.sin(angle)
            self.clock_canvas.create_text(x, y, text=str(hour), fill="black", font=("Arial", 8, "bold"))

        sec = now.second
        min = now.minute
        hour = now.hour % 12

        def angle(length, unit, scale):
            rad = math.radians((unit * 6 if scale == 60 else unit * 30) - 90)
            return 90 + length * math.cos(rad), 90 + length * math.sin(rad)

        sx, sy = angle(60, sec, 60)
        mx, my = angle(50, min, 60)
        hx, hy = angle(40, hour + min / 60, 12)

        self.clock_canvas.create_line(90, 90, sx, sy, fill="red", width=1)
        self.clock_canvas.create_line(90, 90, mx, my, fill="blue", width=2)
        self.clock_canvas.create_line(90, 90, hx, hy, fill="black", width=4)

        self.clock_label.config(text=now.strftime("%A %I:%M:%S %p"))
        self.clock_panel.after(1000, self.update_clock)

    def set_time_based_background(self, desc):
        desc = desc.lower()
        hour = datetime.now().hour
        is_night = hour < 6 or hour >= 18

        if "rain" in desc:
            bg_file = "assets/backgrounds/rain_night.gif" if is_night else "assets/backgrounds/rain.gif"
        elif "cloud" in desc:
            bg_file = "assets/backgrounds/clouds_night.gif" if is_night else "assets/backgrounds/clouds.gif"
        elif "sun" in desc or "clear" in desc:
            bg_file = "assets/backgrounds/night_clear.gif" if is_night else "assets/backgrounds/clear.gif"
        else:
            bg_file = "assets/backgrounds/default.gif"

        try:
            gif = Image.open(bg_file)
            self.frames = [ImageTk.PhotoImage(f.copy().convert("RGBA")) for f in ImageSequence.Iterator(gif)]
            self.animate_background(0)
        except Exception:
            pass

    def animate_background(self, index):
        if not self.frames:
            return
        self.background_label.config(image=self.frames[index])
        self.root.after(100, lambda: self.animate_background((index + 1) % len(self.frames)))

    def show_moon_calendar(self):
        cal_win = Toplevel(self.root)
        cal_win.title("Moon Phase Calendar")
        cal_win.geometry("400x400")
        cal_win.config(bg=WHITE)

        now = datetime.now()
        year = now.year
        month = now.month

        cal = calendar.monthcalendar(year, month)

        header = tk.Label(cal_win, text=f"{calendar.month_name[month]} {year}", font=("Arial", 16, "bold"), fg=NAVY_BLUE, bg=WHITE)
        header.pack(pady=10)

        days_frame = tk.Frame(cal_win, bg=WHITE)
        days_frame.pack()
        for day in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]:
            lbl = tk.Label(days_frame, text=day, width=5, font=("Arial", 10, "bold"), fg=NAVY_BLUE, bg=WHITE)
            lbl.pack(side="left")

        dates_frame = tk.Frame(cal_win, bg=WHITE)
        dates_frame.pack()

        def moon_phase(date):
            diff = date - datetime(2001, 1, 1)
            days = diff.days + (diff.seconds / 86400)
            lunations = 0.20439731 + (days * 0.03386319269)
            phase_index = int((lunations % 1) * 8 + 0.5) % 8
            phases = ["🌑", "🌒", "🌓", "🌔", "🌕", "🌖", "🌗", "🌘"]
            return phases[phase_index]

        for week in cal:
            week_frame = tk.Frame(dates_frame, bg=WHITE)
            week_frame.pack()
            for day in week:
                if day == 0:
                    lbl = tk.Label(week_frame, text="", width=5, height=2, bg=WHITE)
                else:
                    date_obj = datetime(year, month, day)
                    phase = moon_phase(date_obj)
                    lbl = tk.Label(week_frame, text=f"{day}\n{phase}", width=5, height=2, font=("Arial", 10), fg=NAVY_BLUE, bg=WHITE)
                lbl.pack(side="left")

    def run(self):
        self.root.mainloop()
