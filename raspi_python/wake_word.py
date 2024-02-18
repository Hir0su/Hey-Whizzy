import speech_recognition as sr

def listen(recognizer, audio, wake_word):
    # Listens for the wake word and initiates speech recognition if detected.

    # Returns:
    # bool: True if the wake word is not detected or an error occurs, False otherwise.
    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)

        # Check if the wake word is detected
        if wake_word in text.lower():
            print("Wake word detected! Initiating speech recognition...")
            # Call the speech_to_text.start() function if needed
            # speech_to_text.start()
            return False  # Return False to indicate wake word detection
        else:
            print("Not wake word...")
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("Error connecting to Google Speech Recognition service:", e)
    
    return True  # Return True if wake word not detected or error occurred

def start_listening(wake_word, recognizer, microphone):
   # Starts listening for the wake word.
    
    with microphone as source:
        print("Listening for wake word...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=5)

    # Call the listen function with the provided arguments
    return listen(recognizer, audio, wake_word)

