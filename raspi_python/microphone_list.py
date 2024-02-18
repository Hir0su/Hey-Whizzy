import speech_recognition as sr

def list_microphones():
    microphones = sr.Microphone.list_microphone_names()
    for i, mic_name in enumerate(microphones):
        print(f"Microphone {i}: {mic_name}")

list_microphones()
