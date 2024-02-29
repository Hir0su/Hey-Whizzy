import time
import google.generativeai as genai
import wake_word
import speech_to_text
import conversation_gemini
import text_to_speech
import subprocess

# Function to periodically update a timestamp
def update_timestamp(timestamp):
    return time.time()

def start():
    wake_word_text = "hey weezy"  # The wake word to detect
    mic_index = 1  # Change this to the mic to use
    
    # Initialize the last activity timestamp
    last_activity_time = time.time()
    
    while True:
        # Update the last activity timestamp
        last_activity_time = update_timestamp(last_activity_time)

        # Keep listening until the wake word is detected
        bool_wake = False
        bool_wake = wake_word.listen(wake_word_text, mic_index)

        if bool_wake:
            command = speech_to_text.recognize_speech(mic_index)
            output = conversation_gemini.start_prompt(command)
            text_to_speech.start_speaking(output)

        # Check if there has been any activity in the last 30 seconds
        custom_time = 10
        if time.time() - last_activity_time >= custom_time:
            print(f"No activity detected for {custom_time} seconds. Restarting initialize.py...")
            subprocess.Popen(["python", "initialize.py"])  # Restart initialize.py
            return  # Exit the current instance of initialize.py

if __name__ == "__main__":
    start()
