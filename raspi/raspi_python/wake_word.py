import speech_recognition as sr
import subprocess
import sys

def listen(mic_index):
    recognizer = sr.Recognizer()
    microphone = sr.Microphone(device_index=mic_index)

    wake_word_list = [
        "hey weezy", 
        "hey weezy hey weezy", 
        "hey wizzy",
        "hey wizzy hey wizzy",
        "play weezy",
        "play weezy play weezy"
        ]

    print("[1]Listening for wake word...")

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        
        try:
            audio = recognizer.listen(source, timeout=5)
            print("check 1")
            text = recognizer.recognize_google(audio)
            print("check 2")

            print(f"You said: {text}")

            if text.lower() in wake_word_list:
                print("Wake word detected! Initiating speech recognition...")
                return True
            else:
                print("Not wake word...")
        except sr.WaitTimeoutError:
            print("No audio detected within the timeout period")
            #subprocess.Popen(["python", "initialize.py"])
            #sys.exit(0)  # Terminate the process
            return False
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Error connecting to Google Speech Recognition service: {e}")

    return False