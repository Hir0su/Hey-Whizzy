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
import os
import imageio
import requests

def start():
    # Specify the microphone index (use microphone_list.py)
    # index 1 is usually the primary device used
    mic_index = 2  # Change this to the mic to use
    
    # Step 1 - wake word
    # Keep listening until the wake word is detected
    bool_wake = False
    reply = "Say \"Hey Whizzy\""
    requests.post('http://localhost:5000/reply', json={'reply': reply})
    bool_wake = wake_word.listen(mic_index)
    reply = "Greetings! What do you want to ask me about?"
    requests.post('http://localhost:5000/reply', json={'reply': reply})

    if bool_wake:
        # Step 2 - whizzy's initial response
        prompt_type = get_prompt.main_func(mic_index)
        # Step 3
        if prompt_type == 1:
            reply = "Sure! What school-related question do you want to ask?"
            requests.post('http://localhost:5000/reply', json={'reply': reply})
            # Step 3a -  get answer from db
            command = speech_to_text.recognize_speech(mic_index)
            output = fetch_request.post_command(command)
            reply = output
            requests.post('http://localhost:5000/reply', json={'reply': reply})
            text_to_speech.start_speaking(output)
        elif prompt_type == 2:
            reply = "Sure! I'll try my best answering! Ask ahead."
            requests.post('http://localhost:5000/reply', json={'reply': reply})
            # Step 3b.1 - speech-to-text
            command = speech_to_text.recognize_speech(mic_index)
            # Step 3b.2 - send input to gemini
            if command is not None:
                output = conversation_gemini.start_prompt(command)
                # Step 3b.3 - gemini output to text-to-speech
                reply = output
                requests.post('http://localhost:5000/reply', json={'reply': reply})
                text_to_speech.start_speaking(output)
            else:
                text_to_speech.no_pick_up()
        elif prompt_type == 3:
            # Step 3c
            print("go to recommendation")

if __name__ == "__main__":
    
    while True:
        start()