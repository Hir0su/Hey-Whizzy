import pyttsx3
import os

def checker():
    # count_id = 0
    # for voice in voices:
    #     print(f"Voice: {count_id}")
    #     print(" - ID: %s" % voice.id)
    #     print(" - Name: %s" % voice.name)
    #     print(" - Languages: %s" % voice.languages)
    #     print(" - Gender: %s" % voice.gender)
    #     print(" - Age: %s" % voice.age)
    #     print("\n")
    #     count_id+=1
    count_check = 0
    for voice in voices:
        print(f"Voice: {voice.name}, Language: {voice.languages}, ID: {count_check}")
        count_check+=1

def run():
    output = "Greetings, a very good morning to you!"
    engine = pyttsx3.init()

    # Set the voice
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[17].id)  # You can change the index to select a different voice

    # Set the speech rate (words per minute)
    engine.setProperty('rate', 170)  # Adjust the rate as needed

    # Set the volume (0.0 to 1.0)
    engine.setProperty('volume', 1.0)  # Adjust the volume as needed
    
    # Speak the text
    engine.say(output)
    engine.runAndWait()

import os

def text_to_speech(text, voice, pitch=50, speed=170, volume=100):
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

    os.system(f"flite -voice {voice} -t '{text}' -o temp.wav")
    os.system(f"aplay -q temp.wav")  # Assuming you're on a Linux system and using ALSA for audio playback


engine = pyttsx3.init()
voices = engine.getProperty('voices')
# checker()
# run()
text_to_speech("Greetings, a very good morning to you?", voice='rms', pitch=60, speed=300, volume=100)