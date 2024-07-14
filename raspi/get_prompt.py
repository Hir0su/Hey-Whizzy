import pyttsx3
import text_to_speech
import speech_to_text
import requests

def prompt_school():
    requests.post('http://localhost:5000/change_background', json={'index': 3})
    response = "Sure! What school-related question do you want to ask?"
    text_to_speech.start_speaking(response)

def prompt_general():
    requests.post('http://localhost:5000/change_background', json={'index': 4})
    response = "Sure! I'll try my best answering! Ask ahead."
    text_to_speech.start_speaking(response)

def prompt_other():
    response = "Sure! What other stuff do you want to know about?"
    text_to_speech.start_speaking(response)

def prompt_wrong():
    response = (
        f"I can help you if it's a school-related question "
        f"or just a question in general."
    )
    
    text_to_speech.start_speaking(response)

def prompt_none():
    response = "Sorry, I didn't quite hear you well."
    text_to_speech.no_pick_up()

def greetings():
    response = "Greetings! What do you want to ask me about?"
    text_to_speech.start_speaking(response)
    
def get_prompt(prompt):
    keywords = {
        "school": 1,
        "schools": 1,
        "school's": 1,
        "general": 2,
        "asdf": 3,
        "asdfasdfasdf": 3,
        "waittimeouterror": 4
    }

    if prompt is not None:
        for keyword, index in keywords.items():
            if keyword in prompt.lower().strip():
                if index == 1:
                    prompt_school()
                    return index
                elif index == 2:
                    prompt_general()
                    return index
                elif index == 3:
                    prompt_other()
                    return index
                elif index == 4:
                    prompt_none()
                break
        else:
            prompt_wrong()
    else:
        prompt_none()
    
def main_func(mic_index):
    greetings()
    user_prompt = speech_to_text.recognize_speech(mic_index)
    print(f"get_prompt.py: {user_prompt}")
    prompt_type = get_prompt(user_prompt)
    print(prompt_type)
    return prompt_type