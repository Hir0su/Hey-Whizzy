import pyttsx3

def start_speaking(output):
    # Uses text-to-speech to speak the provided text.
    print(output)

    engine = pyttsx3.init()

    # Set the voice
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)  # You can change the index to select a different voice

    # Set the speech rate (words per minute)
    engine.setProperty('rate', 170)  # Adjust the rate as needed

    # Set the volume (0.0 to 1.0)
    engine.setProperty('volume', 1.0)  # Adjust the volume as needed
    
    # Speak the text
    engine.say(output)
    engine.runAndWait()

def no_pick_up():
    reply = "Sorry, I didn't quite hear you well."
    start_speaking(reply)