import pyttsx3
import subprocess
import simpleaudio

# Tkinter imports
import tkinter as tk

# Global variables to store the Tkinter root and label widget
root = None
output_label = None

def start_speaking(output):
    global root, output_label

    # Change the command to create output.wav
    command = f"echo \"{output}\" | ./piper/piper --model en_US-joe-medium.onnx --output_file output.wav"

    # Change the current working directory
    cwd = "/home/whizzy/my_project_venv/Hey-Whizzy-main/raspi/piper"

    # Run the command
    subprocess.run(command, shell=True, cwd=cwd)

    # Play the output.wav file
    wave_obj = simpleaudio.WaveObject.from_wave_file(f"{cwd}/output.wav")
    play_obj = wave_obj.play()

    # Wait for the audio to finish playing
    play_obj.wait_done()

def no_pick_up():
    reply = "Sorry, I didn't quite hear you well."
    start_speaking(reply)