import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import os

class ImageApp:
    def __init__(self, master):
        self.master = master
        self.master.title("HeyWhizzy!")
        self.master.attributes('-fullscreen', True)
        self.frame = tk.Frame(master)
        self.frame.pack(expand=True, padx=10, pady=10)

        # Get the directory of the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Load main image
        main_image_path = os.path.join(script_dir, "MMCLlogo.png")
        self.main_image = Image.open(main_image_path)
        self.main_image = self.main_image.resize((600, 600))
        self.photo_main = ImageTk.PhotoImage(self.main_image)

        # Load additional images
        maps_image_path = os.path.join(script_dir, "MCLMap.jpg")
        calendar_image_path = os.path.join(script_dir, "MCLCallendar2024.png")
        return_image_path = os.path.join(script_dir, "MMCLlogo.png")

        self.maps_image = Image.open(maps_image_path)
        self.calendar_image = Image.open(calendar_image_path)
        self.return_image = Image.open(return_image_path)

        # Resize additional images
        self.maps_image = self.maps_image.resize((639, 345))
        self.photo_maps = ImageTk.PhotoImage(self.maps_image)

        self.calendar_image = self.calendar_image.resize((1366, 720))
        self.photo_calendar = ImageTk.PhotoImage(self.calendar_image)
        
        self.return_image = self.return_image.resize((600, 600))
        self.photo_return = ImageTk.PhotoImage(self.return_image)

        # Placeholder for extra images
        qr_maps_path = os.path.join(script_dir, "QRmaps.png")
        qr_calendar_path = os.path.join(script_dir, "QRcalendar.jpg")

        self.photo_extra_maps = Image.open(qr_maps_path).resize((250, 250))
        self.photo_extra_maps = ImageTk.PhotoImage(self.photo_extra_maps)

        self.photo_extra_calendar = Image.open(qr_calendar_path).resize((250, 250))
        self.photo_extra_calendar = ImageTk.PhotoImage(self.photo_extra_calendar)

        # Create main image label
        self.label_main = tk.Label(self.frame, image=self.photo_main)
        self.label_main.pack(padx=5, pady=5)

        # Create input box
        self.input_entry = tk.Entry(self.frame)
        self.input_entry.pack(pady=5)
        self.input_entry.focus_set()

        # Set up text variable and trace it for changes
        self.input_text = tk.StringVar()
        self.input_entry["textvariable"] = self.input_text
        self.input_text.trace_add("write", self.process_input)

        # Load GIFs for bottom right image
        gif1_path = os.path.join(script_dir, "Faunagif1.gif")
        gif2_path = os.path.join(script_dir, "Faunagif2.gif")

        self.gif1 = self.load_animated_gif(gif1_path)
        self.gif2 = self.load_animated_gif(gif2_path)

        # Create bottom right image label
        self.label_bottom_right = tk.Label(self.master)
        self.label_bottom_right.place(relx=1.0, rely=1.0, anchor="se")
        self.gif1 = [frame.resize((250, 250)) for frame in self.gif1]
        self.gif2 = [frame.resize((250, 250)) for frame in self.gif2]
        self.photo_gif1 = [ImageTk.PhotoImage(frame) for frame in self.gif1]
        self.photo_gif2 = [ImageTk.PhotoImage(frame) for frame in self.gif2]

        # Create bottom left image labels (initially hidden)
        self.label_extra_maps = tk.Label(self.master, image=self.photo_extra_maps)
        self.label_extra_maps.pack(side='left', anchor='sw')
        self.label_extra_maps.pack_forget()

        self.label_extra_calendar = tk.Label(self.master, image=self.photo_extra_calendar)
        self.label_extra_calendar.pack(side='left', anchor='sw')
        self.label_extra_calendar.pack_forget()

        # Start playing the GIF
        self.play_gif(self.photo_gif1)

    def load_animated_gif(self, path):
        gif = Image.open(path)
        frames = [frame.copy() for frame in ImageSequence.Iterator(gif)]
        return frames

    def play_gif(self, gif_frames, index=0):
        if hasattr(self, 'current_gif'):
            self.master.after_cancel(self.current_gif)
        frame = gif_frames[index]
        self.label_bottom_right.config(image=frame)
        self.label_bottom_right.image = frame
        index = (index + 1) % len(gif_frames)
        self.current_gif = self.master.after(100, self.play_gif, gif_frames, index)

    def display_image(self, image):
        # Hide previous main image
        self.label_main.pack_forget()
        # Display new main image
        self.label_main.config(image=image)
        self.label_main.image = image
        self.label_main.pack(padx=5, pady=5)

    def process_input(self, *args):
        text = self.input_text.get().lower()
        images = {
            "map": self.photo_maps,
            "calendar": self.photo_calendar,
            "return": self.photo_return
        }
        qr_keywords = ["qr code for " + keyword for keyword in images.keys()]
        detected_keywords = []

        # Detect all keywords, QR code combinations, and normal keywords
        for word in text.split():
            if word in images:
                detected_keywords.append(word)
            elif any(qr_keyword in word for qr_keyword in qr_keywords):
                for keyword in images.keys():
                    if "qr code for " + keyword in word:
                        detected_keywords.append(keyword)
                        break

        if detected_keywords:
            # Show corresponding main image
            self.display_image(images[detected_keywords[-1]])
            self.play_gif(self.photo_gif2)
            self.master.after(5000, lambda: self.play_gif(self.photo_gif1))
            # Show the corresponding extra image if QR code is detected
            if "qr code for " + detected_keywords[-1] in text:
                if detected_keywords[-1] == "map":
                    self.label_extra_maps.pack()
                    self.label_extra_calendar.pack_forget()
                elif detected_keywords[-1] == "calendar":
                    self.label_extra_maps.pack_forget()
                    self.label_extra_calendar.pack()
            else:
                # Hide extra images if not specified with QR code
                self.label_extra_maps.pack_forget()
                self.label_extra_calendar.pack_forget()
        else:
            self.display_image(self.photo_main)
            self.play_gif(self.photo_gif1)
            # Hide all extra images
            self.label_extra_maps.pack_forget()
            self.label_extra_calendar.pack_forget()

    def set_input_text(self, text):
        # Set the text in the input entry
        self.input_entry.delete(0, tk.END)
        self.input_entry.insert(tk.END, text)


def main():
    root = tk.Tk()
    app = ImageApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
