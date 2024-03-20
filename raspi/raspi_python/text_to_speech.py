import pyttsx3
import os

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
    """
    Convert text to speech using flite.

    Parameters:
        text (str): The text to be converted to speech.
        voice (str): The name of the voice to use. Default is 'rms'.
        pitch (int): The pitch of the voice (range: 0-99). Default is 50. 50-90
        speed (int): The speed of speech (range: 60-500). Default is 170. 60-500
        volume (int): The volume of the speech (range: 0-100). Default is 100. 0-100
    """

    # available voices in flite: 
    # kal awb_time kal16 awb rms slt

    os.system(f"flite -voice {voice} -t \"{output}\" -o temp.wav")
    os.system(f"aplay -q temp.wav")  # Assuming you're on a Linux system and using ALSA for audio playback

def no_pick_up():
    reply = "Sorry, I didn't quite hear you well."
    start_speaking(reply)