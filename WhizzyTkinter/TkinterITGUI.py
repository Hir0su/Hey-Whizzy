import tkinter as tk
from PIL import Image, ImageTk

class ImageApp:
    def __init__(self, master):
        self.master = master
        self.master.title("HeyWhizzy!")
        self.master.attributes('-fullscreen', True)
        self.frame = tk.Frame(master)
        self.frame.pack(expand=True, padx=10, pady=10)

        # Load main image
        self.main_image = Image.open("MMCLlogo.png")
        self.main_image = self.main_image.resize((600, 600))
        self.photo_main = ImageTk.PhotoImage(self.main_image)

        # Load additional images
        self.maps_image = Image.open("MCLMap.jpg")
        self.calendar_image = Image.open("MCLCallendar2024.png")
        self.return_image = Image.open("MMCLlogo.png")
        self.bottom_right_image = Image.open("Fauna.jpg")

        # Resize additional images
        self.maps_image = self.maps_image.resize((639, 345))
        self.calendar_image = self.calendar_image.resize((1366, 720))
        self.return_image = self.return_image.resize((600, 600))
        self.bottom_right_image = self.bottom_right_image.resize((250, 250))

        # Convert images to Tkinter-compatible format
        self.photo_maps = ImageTk.PhotoImage(self.maps_image)
        self.photo_calendar = ImageTk.PhotoImage(self.calendar_image)
        self.photo_return = ImageTk.PhotoImage(self.return_image)
        self.photo_bottom_right = ImageTk.PhotoImage(self.bottom_right_image)

        # Create main image label
        self.label_main = tk.Label(self.frame, image=self.photo_main)
        self.label_main.pack(padx=5, pady=5)

        # Create bottom right image label
        self.label_bottom_right = tk.Label(self.master, image=self.photo_bottom_right)
        self.label_bottom_right.place(relx=1.0, rely=1.0, anchor="se")

        # Create input box
        self.input_entry = tk.Entry(self.frame)
        self.input_entry.pack(pady=5)
        self.input_entry.focus_set()

        # Set up text variable and trace it for changes
        self.input_text = tk.StringVar()
        self.input_entry["textvariable"] = self.input_text
        self.input_text.trace_add("write", self.process_input)

    def display_image(self, image):
        # Hide previous main image
        self.label_main.pack_forget()
        # Display new main image
        self.label_main.config(image=image)
        self.label_main.image = image
        self.label_main.pack(padx=5, pady=5)

        # Elif for image display
    def process_input(self, *args):
        text = self.input_text.get().lower()
        current_image = self.label_main.cget("image")
        if "maps" in text:
            self.display_image(self.photo_maps)
        elif "calendar" in text:
            self.display_image(self.photo_calendar)
        elif "return" in text:
            self.display_image(self.photo_return)
        else:
            self.display_image(self.photo_main)

def main():
    root = tk.Tk()
    app = ImageApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()