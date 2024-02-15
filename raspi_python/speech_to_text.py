import speech_recognition as sr

def list_microphones():
    microphones = sr.Microphone.list_microphone_names()
    for i, mic_name in enumerate(microphones):
        print(f"Microphone {i}: {mic_name}")

def recognize_speech():
    # Specify the microphone index (you can find it in system settings)
    mic_index = 3  # Change this to mic of use

    # Initialize the recognizer with a specific microphone
    recognizer = sr.Recognizer()
    microphone = sr.Microphone(device_index=mic_index)

    while True:
        # Open the specified microphone and start recording
        with microphone as source:
            print("Say something:")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=5)
            

        try:
            # Recognize speech using Google Web Speech API
            print("Recognizing...")
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Error connecting to Google Speech Recognition service: {e}")

if __name__ == "__main__":
    
    recognize_speech()
    #list_microphones()