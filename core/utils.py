import requests  # Imports the requests library to fetch the image from a URL
from PIL import Image, ImageTk  # Imports Pillow for image processing and Tkinter compatibility
import io  # Imports io to handle byte streams (used to load image data)

# Function to fetch and prepare an image icon from a URL
def fetch_icon(url, resize=(80, 80)):
    try:
        # Download the image content from the given URL
        icon_data = requests.get(url).content

        # Open the image from the byte data and resize it
        image = Image.open(io.BytesIO(icon_data)).resize(resize)

        # Convert the image into a format that Tkinter can display
        return ImageTk.PhotoImage(image)
    
    except:
        # If anything goes wrong (e.g. network issue or bad image), return None
        return None

