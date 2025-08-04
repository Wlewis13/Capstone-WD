import tkinter as tk  # Import Tkinter for GUI components
from PIL import Image, ImageTk, ImageSequence  # Import PIL modules for handling images and animated GIFs
import io, requests

# Set the window background animation/theme based on the weather description
def set_background_theme(root, description):
    desc = description.lower()  # Convert description to lowercase for easier matching
    theme = "assets/backgrounds/clear.gif"  # Default background GIF (clear weather)

    # Choose background GIF file based on keywords in the weather description
    if "rain" in desc:
        theme = "assets/backgrounds/rain.gif"
    elif "snow" in desc:
        theme = "assets/backgrounds/snow.gif"
    elif "cloud" in desc:
        theme = "assets/backgrounds/cloud.gif"
    elif "storm" in desc:
        theme = "assets/backgrounds/storm.gif"

    play_gif(root, theme)  # Start playing the selected background GIF animation

# Function to play an animated GIF as the background in the given root window
def play_gif(root, gif_file):
    try:
        gif = Image.open(gif_file)  # Open the GIF file
        # Extract all frames from the GIF and convert to Tkinter-compatible PhotoImage objects
        frames = [ImageTk.PhotoImage(frame.copy().convert("RGBA")) for frame in ImageSequence.Iterator(gif)]

        # If the root window does not already have a label for the background, create one
        if not hasattr(root, "background_label"):
            root.background_label = tk.Label(root)  # Create label widget to hold the animation
            # Position the label to cover the entire root window
            root.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Internal function to update the displayed frame of the GIF periodically
        def update(index):
            frame = frames[index]  # Get current frame
            root.background_label.configure(image=frame)  # Update label image to current frame
            root.background_label.image = frame  # Keep reference to avoid garbage collection
            # Schedule next frame update after 100 milliseconds, looping back to frame 0 after the last frame
            root.after(100, update, (index + 1) % len(frames))
            

        update(0)  # Start the animation with the first frame
    except Exception as e:
        # If an error occurs (e.g., file not found), clear the background image if it exists
        if hasattr(root, "background_label"):
            root.background_label.configure(image="")

            
# ---------------- SUMMARY ----------------
# This module provides animated weather-themed backgrounds for the Tkinter GUI window.
# - The `set_background_theme()` function selects a background GIF file based on keywords like "rain", "snow", etc.
# - The `play_gif()` function loads and animates the chosen GIF in the root window using a Tkinter Label.
# - Background animations enhance the app visually to match the current weather condition.
# - If a background label isn't already present, it creates one and loops through the GIF frames.
# - GIF frames are updated every 100 milliseconds to simulate animation.
# This feature improves the user interface by making the weather dashboard visually immersive.