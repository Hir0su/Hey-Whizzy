# python libraries
import speech_recognition as sr
import google.generativeai as genai

# project imports
import wake_word
import speech_to_text
import conversation_gemini
import text_to_speech

def start():
    while True:
    
        wake_word_text = "hey weezy"  # The wake word to detect

        # Specify the microphone index (use microphone_list.py)
        mic_index = 1  # Change this to the mic to use

        # Initialize the recognizer with a specific microphone
        recognizer = sr.Recognizer()
        microphone = sr.Microphone(device_index=mic_index)

        # -------------------------------------------------------------
        # Step 1 - wake word
        # Keep listening until the wake word is detected
        while wake_word.start_listening(wake_word_text, recognizer, microphone):
            pass  # Continue listening

        # -------------------------------------------------------------
        # Step 2 - speech-to-text 
        command = speech_to_text.start_listening(recognizer, microphone)

        # -------------------------------------------------------------
        # Step 3 - send input to gemini 
        output = conversation_gemini.start_prompt(command)
        
        # -------------------------------------------------------------
        # Step 4 - gemini output to text-to-speech
        text_to_speech.start_speaking(output)


if __name__ == "__main__":
    while True:
        start()