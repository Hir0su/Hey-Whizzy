import sounddevice

import speech_recognition as sr
def list_microphones():
    microphones = sr.Microphone.list_microphone_names()
    for i, mic_name in enumerate(microphones):
        print(f"Microphone {i}: {mic_name}")
list_microphones()

# # IF ABOVE CODE IS NOT WORKING
# # TEST CODE ALTERNATIVE FOR RASPI
# import speech_recognition as sr
# for index, name in enumerate(sr.Microphone.list_microphone_names()):
#     print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))
