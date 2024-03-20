# module imports
import wake_word
import speech_to_text
import conversation_gemini
import text_to_speech
import get_prompt
import sounddevice

def start():

    # Specify the microphone index (use microphone_list.py)
    # index 1 is usually the primary device used
    mic_index = 2  # Change this to the mic to use
    
    # -------------------------------------------------------------
    # Step 1 - wake word
    # Keep listening until the wake word is detected
    bool_wake = False
    bool_wake = wake_word.listen(mic_index)

    if bool_wake == True:
        # -------------------------------------------------------------
        # Step 2 - whizzy's initial response
        prompt_type = get_prompt.main_func(mic_index)
        # -------------------------------------------------------------
        # Step 3
        if prompt_type == 1: 
            # Step 3a -  get answer from db
            command = speech_to_text.recognize_speech(mic_index)
            print("Connecting to DB")
        elif prompt_type == 2: 
            # Step 3b.1 - speech-to-text 
            command = speech_to_text.recognize_speech(mic_index)
            # Step 3b.2 - send input to gemini
            if command is not None:
                output = conversation_gemini.start_prompt(command)
                # Step 3b.3 - gemini output to text-to-speech
                text_to_speech.start_speaking(output)
            else:
                text_to_speech.no_pick_up()
        elif prompt_type == 3:
            # Step 3c
            print("go to recommendation")

if __name__ == "__main__":
    while True:
      start()