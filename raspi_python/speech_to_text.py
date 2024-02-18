import speech_recognition as sr

def recognize_speech(recognizer, audio):
            
    try:
        # Recognize speech using Google Web Speech API
        print("Recognizing...")
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print(f"Error connecting to Google Speech Recognition service: {e}")

def start_listening(recognizer, microphone):
    with microphone as source:
        print("Listening for audio...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=5)

    return recognize_speech(recognizer, audio)

    # if recognized_text != "None" or None:
    #     print("working good")