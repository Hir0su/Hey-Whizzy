# module imports
import wake_word
import speech_to_text
import conversation_gemini
import text_to_speech
import get_prompt
import fetch_request
import sounddevice
# tkinter imports
import tkinter as tk
from tkinter import ttk, CENTER
from PIL import ImageTk, Image
import tkinter.font as tkfont
import os


def start():
    # Specify the microphone index (use microphone_list.py)
    # index 1 is usually the primary device used
    mic_index = 2  # Change this to the mic to use

    # Step 1 - wake word
    # Keep listening until the wake word is detected
    bool_wake = False
    bool_wake = wake_word.listen(mic_index)

    if bool_wake:
        # Step 2 - whizzy's initial response
        prompt_type = get_prompt.main_func(mic_index)
        # Step 3
        if prompt_type == 1:
            # Step 3a -  get answer from db
            command = speech_to_text.recognize_speech(mic_index)
            output = fetch_request.post_command(command)
            update_label(output)  # Update the label with the output
            text_to_speech.start_speaking(output)
        elif prompt_type == 2:
            # Step 3b.1 - speech-to-text
            command = speech_to_text.recognize_speech(mic_index)
            # Step 3b.2 - send input to gemini
            if command is not None:
                output = conversation_gemini.start_prompt(command)
                # Step 3b.3 - gemini output to text-to-speech
                update_label(output)  # Update the label with the output
                text_to_speech.start_speaking(output)
            else:
                text_to_speech.no_pick_up()
        elif prompt_type == 3:
            # Step 3c
            print("go to recommendation")

def update_label(output):
    label.config(text=output)
    root.update()

def adjust_font_size(label, text, max_width, max_height):
    # Start with a large font size
    font_size = 50
    
    # Create a font object with the initial font size
    font = tkfont.Font(font=label['font'])
    
    # Keep reducing the font size until the text fits within the label's dimensions
    while font.measure(text) > max_width or font.metrics("linespace") > max_height:
        font_size -= 1
        font.configure(size=font_size)
    
    # Update the label's font with the adjusted font
    label.configure(font=font)

if __name__ == "__main__":
    root = tk.Tk()

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
    bg_label = ttk.Label(root, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Set the label width based on the windowS width
    label_width = int(window_width * 0.93)
    label_height = 565  # Placeholder height, just as needed

    label = ttk.Label(
        root, 
        text="Hey Whizzy", 
        font=("Montserrat ExtraBold",), 
        foreground="#ffffff", 
        background="#222222",
        anchor=CENTER,
        wraplength=label_width
    )

    # # Update the label height and position
    label.place(x=20, y=20, width=label_width, height=label_height)
    
    root.update()

    while True:
        start()