import pyttsx3
import subprocess
import simpleaudio

# def start_speaking(output):
#     # Uses text-to-speech to speak the provided text.
#     print(output)

#     engine = pyttsx3.init()

#     # Set the voice
#     voices = engine.getProperty('voices')
#     engine.setProperty('voice', voices[11].id)  # You can change the index to select a different voice

#     # Set the speech rate (words per minute)
#     engine.setProperty('rate', 170)  # Adjust the rate as needed

#     # Set the volume (0.0 to 1.0)
#     engine.setProperty('volume', 1.0)  # Adjust the volume as needed
    
#     # Speak the text
#     engine.say(output)
#     engine.runAndWait()

def start_speaking(output, voice='rms', pitch=60, speed=300, volume=100):

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