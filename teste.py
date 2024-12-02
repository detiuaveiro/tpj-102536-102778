import os
os.environ['SDL_VIDEODRIVER'] = 'dummy'  # Prevent Pygame from creating a window

import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename(
    initialdir="SETTINGS_FOLDER",
    title="Select file",
    filetypes=(("json files", "*.json"),)
)
