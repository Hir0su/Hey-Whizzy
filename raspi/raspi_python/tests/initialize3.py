import wake_word
import speech_to_text
import conversation_gemini
import text_to_speech

def start():

    wake_word_text = "hey weezy"  # The wake word to detect

    # Specify the microphone index (use microphone_list.py)
    mic_index = 1  # Change this to the mic to use
    
    # -------------------------------------------------------------
    # Step 1 - wake word
    # Keep listening until the wake word is detected
    while True:
        bool_wake = wake_word.listen(wake_word_text, mic_index)

        if bool_wake:
            break  # Exit loop if wake word detected
        else:
            print("Continuing to listen for wake word...")

    # -------------------------------------------------------------
    # Step 2 - speech-to-text 
    command = speech_to_text.recognize_speech(mic_index)
    
    # -------------------------------------------------------------
    # Step 3 - send input to gemini 
    output = conversation_gemini.start_prompt(command)
    
    # -------------------------------------------------------------
    # Step 4 - gemini output to text-to-speech
    text_to_speech.start_speaking(output)

if __name__ == "__main__":
    while True:
        start()
