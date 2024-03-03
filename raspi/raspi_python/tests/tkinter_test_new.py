import tkinter as tk
from PIL import Image, ImageTk
import os

def create_bottom_frame(root, image_path):
    # Create a frame for the bottom part (image)
    bottom_frame = tk.Frame(root, bg="white")
    bottom_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    # Load the image
    image = Image.open(image_path)
    photo = ImageTk.PhotoImage(image)

    # Create a label to display the image
    image_label = tk.Label(bottom_frame, image=photo)
    image_label.image = photo  # Keep a reference to avoid garbage collection
    image_label.pack(fill=tk.BOTH, expand=True)

def create_top_frame(root, container_size, text):
    # Create a frame for the top part (container with label)
    top_frame = tk.Frame(root, bg="white")
    top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Create the square container
    container = tk.Canvas(top_frame, width=container_size, height=container_size, bg="white", highlightthickness=5, highlightbackground="black")
    container.pack(pady=50)  # Add some padding at the top

    # Calculate the coordinates for the square
    x1 = 0
    y1 = 0
    x2 = container_size
    y2 = container_size

    # Draw the square with a stroke
    container.create_rectangle(x1, y1, x2, y2, outline="black")

    # Add text inside the container
    text_label = tk.Label(container, text=text, font=("Helvetica", 24), bg="white")
    text_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

def create_window(window_width, window_height):
    # Create the main window
    root = tk.Tk()
    root.geometry(f"{window_width}x{window_height}")
    return root

def main():
    # Set parameters
    window_width = 1080
    window_height = 1920
    current_directory = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(current_directory, "kufufuku.jpg")  # Image filename
    container_size = 500
    text = "Hello World"

    # Create the main window
    root = create_window(window_width, window_height)

    # Create the bottom frame with image
    create_bottom_frame(root, image_path)

    # Create the top frame with container and label
    create_top_frame(root, container_size, text)

    # Run the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()
