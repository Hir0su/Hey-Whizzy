import pyttsx3

def start_speaking(text):
    # Uses text-to-speech to speak the provided text.

    engine = pyttsx3.init()

    # Set the voice
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[2].id)  # You can change the index to select a different voice

    # Set the speech rate (words per minute)
    engine.setProperty('rate', 150)  # Adjust the rate as needed

    # Set the volume (0.0 to 1.0)
    engine.setProperty('volume', 1.0)  # Adjust the volume as needed

    # Speak the text
    engine.say(text)
    engine.runAndWait()

start_speaking("A very good morning to you traveler. What kind of adventure do we foresee today?")