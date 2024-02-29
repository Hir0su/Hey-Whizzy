import speech_recognition as sr

def recognize_speech(mic_index):
    recognizer = sr.Recognizer()
    microphone = sr.Microphone(device_index=mic_index)

    print("[2]Listening for audio...")  

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)

        try:
            audio = recognizer.listen(source, timeout=5)
            print("check 1")
            text = recognizer.recognize_google(audio)
            print("check 2")

            print(f"You said: {text}")
            return text
        except sr.WaitTimeoutError:
            err = "WaitTimeoutError"
            print("No audio detected within the timeout period")
            return err
        except sr.UnknownValueError as e:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Error connecting to Google Speech Recognition service: {e}")