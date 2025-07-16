import tkinter as tk  # Import Tkinter for GUI components
from core.file_export import save_weather_to_csv
from tkinter import ttk, messagebox  # Import themed widgets and message boxes
from core.api_client import fetch_weather_data  # Function to fetch weather info from API
from core.weather_data import process_weather_and_forecast  # Process raw API data into usable form
from gui.components import (  # Import GUI helper functions to build the interface
    populate_weather_panel,
    display_weekly_forecast,
    display_horizontal_forecast,
    display_allergen_icons,
)
from gui.themes import set_background_theme  # Function to set background animation/theme based on weather

# Main application class for the weather dashboard
class WeatherApp:
    def __init__(self):
        self.root = tk.Tk()  # Create main window
        self.root.title("Weather Dashboard by Wendell Lewis")  # Set window title
        self.root.geometry("1200x700")  # Set fixed window size

        self.setup_ui()  # Build the UI components

    # Setup the main user interface elements
    def setup_ui(self):
        input_frame = tk.Frame(self.root, bg="lightblue", bd=2, relief="groove")  # Frame for city input controls
        input_frame.pack(pady=10)  # Add padding above and below

        # Dropdown to select view mode: Select a City, One City, or Two Cities
        self.view_mode = tk.StringVar(value="Select an Option")  # Initial dropdown value
        mode_menu = ttk.Combobox(
            input_frame,
            textvariable=self.view_mode,
            values=["Select an Option", "One City","Two Cities"],  # Dropdown options
            width=15,
            state="readonly",  # User can only select, not type
        )
        mode_menu.grid(row=0, column=0, padx=5)  # Place dropdown in grid
        mode_menu.bind("<<ComboboxSelected>>", self.toggle_city_inputs)  # Call toggle when selection changes

        self.city1_entry = tk.Entry(input_frame, width=20)  # Text box for first city
        self.city1_entry.grid(row=0, column=1, padx=5)  # Place next to dropdown

        self.city2_entry = tk.Entry(input_frame, width=20)  # Text box for second city (hidden by default)
        self.city2_entry.grid(row=0, column=2, padx=5)
        self.city2_entry.grid_remove()  # Hide second city input initially

        # Button to trigger weather fetch and display
        tk.Button(input_frame, text="View Weather", command=self.view_weather).grid(
            row=0, column=3, padx=10
        )

        tk.Button(input_frame, text="Save CSV", command=self.save_to_csv).grid(
        row=0, column=4, padx=10
        )  # Button to save weather data to CSV


        # Frame to show the weather results, fills available space
        self.result_frame = tk.Frame(self.root, bg="lightblue", bd=2, relief="groove")
        self.result_frame.pack(fill="both", expand=True)

    # Show or hide second city input based on dropdown selection
    def toggle_city_inputs(self, event=None):
        if self.view_mode.get() == "Two Cities":
            self.city2_entry.grid()  # Show second city input
        elif self.view_mode.get() in ["One City", "Select an Option"]:
            self.city2_entry.grid_remove()  # Hide second city input
            self.city2_entry.delete(0, tk.END)  # Clear second city input field

    # Fetch and display weather data based on user input
    def view_weather(self):
        # Clear any previous weather results from the result frame
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        city1 = self.city1_entry.get().strip()  # Get and trim city1 input
        city2 = self.city2_entry.get().strip()  # Get and trim city2 input (may be empty)

        if not city1:
            messagebox.showwarning("Input Error", "Please enter at least one city.")  # Warn if city1 is empty
            return

        try:
            # Fetch weather and forecast data for city1
            weather1, forecast1 = fetch_weather_data(city1)
            data1 = process_weather_and_forecast(weather1, forecast1)
            # Change background theme based on city1 weather description
            set_background_theme(self.root, data1["description"])

            # If viewing one city, display full-width panel with weekly forecast
            if self.view_mode.get() == "One City":
                panel = tk.Frame(self.result_frame, bd=2, relief="groove", width=1150, bg="#ffffff")
                panel.pack(padx=10, pady=10, fill="x")  # Fill horizontally with padding
                populate_weather_panel(panel, city1, data1)  # Fill panel with city1 weather info
                display_weekly_forecast(self.result_frame, data1["forecast"])  # Show 5-day forecast

            else:
                # For "Select a City" or "Two Cities" mode, show smaller panel with horizontal forecast
                panel = tk.Frame(self.result_frame, bd=2, relief="groove", width=550, bg="#ffffff")
                panel.grid(row=0, column=0, padx=10, pady=10, sticky="n")
                populate_weather_panel(panel, city1, data1)
                display_horizontal_forecast(panel, data1["forecast"])

            # If viewing two cities, validate and fetch data for city2 as well
            if self.view_mode.get() == "Two Cities":
                if not city2:
                    messagebox.showwarning("Input Error", "Please enter the second city.")  # Warn if city2 missing
                    return
                weather2, forecast2 = fetch_weather_data(city2)
                data2 = process_weather_and_forecast(weather2, forecast2)

                # Display city2 info side-by-side with city1
                panel2 = tk.Frame(self.result_frame, bd=2, relief="groove", width=550, bg="#ffffff")
                panel2.grid(row=0, column=1, padx=10, pady=10, sticky="n")
                populate_weather_panel(panel2, city2, data2)
                display_horizontal_forecast(panel2, data2["forecast"])

        except Exception as e:
            # Show error if API call fails or data is invalid
            messagebox.showerror("Error", "Please check spelling and try again.")
    def save_to_csv(self):
        city = self.city1_entry.get().strip()

        if not city:
            messagebox.showwarning("Input Error", "Please enter a city first.")
            return

        try:
            # Fetch and process the weather data again
            weather, forecast = fetch_weather_data(city)
            data = process_weather_and_forecast(weather, forecast)

            # Save to CSV
            file_path = save_weather_to_csv(city, data)

            # Let the user know it worked
            messagebox.showinfo("Success", f"Weather data saved to:\n{file_path}")
        except Exception:
            messagebox.showerror("Error", "Weather data failed to dave.")

    # Start the Tkinter event loop to run the app
    def run(self):
        self.root.mainloop()
