# import speech_recognition as sr
# import subprocess
# import sys
# import os

# def listen(mic_index):
#     recognizer = sr.Recognizer()
#     microphone = sr.Microphone(device_index=mic_index)

#     wake_word_list = [
#         "hey weezy",
#         "hey weezy.",
#         "hey, weezy",
#         "hey, weezy.",   
#         "hey weezy hey weezy", 
#         "hey wizzy",
#         "hey wizzy hey wizzy",
#         "play weezy",
#         "play weezy play weezy"
#         ]

#     print("[1]Listening for wake word...")

#     with microphone as source:
#         recognizer.adjust_for_ambient_noise(source)
        
#         try:
#             audio = recognizer.listen(source, timeout=5)
#             print("check 1")
#             # text = recognizer.recognize_whisper(audio, model="tiny.en")
#             text = recognizer.recognize_vosk(audio)
#             # text = recognizer.recognize_google(audio)
#             print("check 2")

#             print(f"You said: {text.lower().strip()}")

#             if text.lower().strip() in wake_word_list:
#                 print("Wake word detected! Initiating speech recognition...")
#                 return True
#             else:
#                 print("Not wake word...")
#         except sr.WaitTimeoutError:
#             print("No audio detected within the timeout period")
#             #subprocess.Popen(["python", "initialize.py"])
#             #sys.exit(0)  # Terminate the process
#             return False
#         except sr.UnknownValueError:
#             print("Could not understand audio")
#         except sr.RequestError as e:
#             print(f"Error connecting to Google Speech Recognition service: {e}")

#     return False

import speech_recognition as sr
import os
from vosk import KaldiRecognizer, Model, SetLogLevel
import json

# Set the log level to suppress the Vosk log messages
SetLogLevel(-1)

def recognize_vosk_custom(audio_data, language='en', model_path=None):
    if model_path is None:
        model_path = "model"
    if not os.path.exists(model_path):
        return f"Please download the model and provide the path to the 'model' folder."
        exit(1)
    
    model = Model(model_path)
    rec = KaldiRecognizer(model, 16000)
    
    rec.AcceptWaveform(audio_data.get_raw_data(convert_rate=16000, convert_width=2))
    finalRecognition = rec.FinalResult()
    
    return json.loads(finalRecognition)

def listen(mic_index):
    recognizer = sr.Recognizer()
    microphone = sr.Microphone(device_index=mic_index)

    wake_word_list = [
        "hey wheezy",
        "hey weezy",
        "hey weezy.",
        "hey, weezy",
        "hey, weezy.",   
        "hey weezy hey weezy", 
        "hey wizzy",
        "hey wizzy hey wizzy",
        "play weezy",
        "play weezy play weezy",
        "hey easy"
    ]

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        
        try:
            print("[1]Listening for wake word...")
            audio = recognizer.listen(source, timeout=5)
            print("check 1")
            model_path = "/home/whizzy/my_project_venv/Hey-Whizzy-main/raspi/raspi_python/model"
            # text = recognizer.recognize_google(audio)
            result = recognize_vosk_custom(audio, model_path=model_path)
            text = result["text"]
            print("check 2")

            print(f"You said: {text.lower().strip()}")

            if text.lower().strip() in wake_word_list:
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
            print(f"Error connecting to the recognizer: {e}")

    return False