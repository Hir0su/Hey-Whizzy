import speech_recognition as sr
import os
from vosk import KaldiRecognizer, Model, SetLogLevel
import json
import simpleaudio as sa
import requests

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

def play_wav_file():
    file_path = "/home/whizzy/my_project_venv/Hey-Whizzy-main/raspi/raspi_python/sounds/beep_down.wav"
    wave_obj = sa.WaveObject.from_wave_file(file_path)
    play_obj = wave_obj.play()
    play_obj.wait_done()  # Wait until sound is done playing

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
        "hey easy",
        "hey rese",
        "abc",
        "a b c",
        "play music",
        "hey busy"
    ]

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        print("check 0")
        
        try:
            print("[1]Listening for wake word...")
            requests.post('http://localhost:5000/idle')
            audio = recognizer.listen(source, timeout=5)
            requests.post('http://localhost:5000/idle_stop')
            print("check 1")
            #initialize.update_label("Recognizing",30)
            model_path = "/home/whizzy/my_project_venv/Hey-Whizzy-main/raspi/raspi_python/model"
            text = recognizer.recognize_google(audio)
            # result = recognize_vosk_custom(audio, model_path=model_path)
            # text = result["text"]
            print("check 2")
            play_wav_file()

            print(f"You said: {text.lower().strip()}")

            if text.lower().strip() in wake_word_list:
                print("Wake word detected! Initiating speech recognition...")
                requests.post('http://localhost:5000/change_background', json={'index': 2})
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