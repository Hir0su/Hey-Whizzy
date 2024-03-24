# main_ui.py
import tkinter as tk
from PIL import ImageTk, Image
import os

def initialize_gui():
    root.title("My Application")

    # Get the screen height
    screen_height = root.winfo_screenheight()

    # Set the window size to fit vertically on the screen
    window_height = screen_height - 100
    window_width = int(window_height * 9 / 16)

    root.geometry(f"{window_width}x{window_height}+0+0")

    # Get the absolute path of the background image
    script_dir = os.path.dirname(os.path.abspath(__file__))
    bg_image_path = os.path.join(script_dir, "ui", "main_screen_1.png")

    # Load the background image
    bg_image = Image.open(bg_image_path)
    bg_photo = ImageTk.PhotoImage(bg_image.resize((window_width, window_height)))

    # Create a label with the background image
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Create a label for the output text
    output_label = tk.Label(root, text="Whizzy", font=("Arial", 20), fg="#172852", bg="#ed0000")
    output_label.place(x=20, y=20)  # Adjust the position as needed

    root.mainloop()

root = tk.Tk()
initialize_gui()