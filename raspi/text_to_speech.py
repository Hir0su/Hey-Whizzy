import pyttsx3
import subprocess
import simpleaudio
import requests
import lxml

def start_speaking(output):
    # Change the command to create output.wav
    command = f"echo \"{output}\" | ./piper/piper --model en_US-joe-medium.onnx --output_file output.wav"

    # Change the current working directory
    cwd = "/home/whizzy/my_project_venv/Hey-Whizzy-main/raspi/piper"

    # Run the command
    subprocess.run(command, shell=True, cwd=cwd)

    # Play the output.wav file
    wave_obj = simpleaudio.WaveObject.from_wave_file(f"{cwd}/output.wav")
    play_obj = wave_obj.play()
    print("audio played")

    # Send the reply to the backend UI
    requests.post('http://localhost:5000/reply', json={'reply': output})

    # Wait for the audio to finish playing
    play_obj.wait_done()
    print("audio finished")

    # Send a message to the frontend to stop the talking animation
    requests.post('http://localhost:5000/stop_talking')

def start_speaking_small(output, image_data):
    # Change the command to create output.wav
    command = f"echo \"{output}\" | ./piper/piper --model en_US-joe-medium.onnx --output_file output.wav"

    # Change the current working directory
    cwd = "/home/whizzy/my_project_venv/Hey-Whizzy-main/raspi/piper"

    # Run the command
    subprocess.run(command, shell=True, cwd=cwd)

    # Play the output.wav file
    wave_obj = simpleaudio.WaveObject.from_wave_file(f"{cwd}/output.wav")
    play_obj = wave_obj.play()
    print("audio played")

    # Send the reply to the backend UI
    requests.post('http://localhost:5000/reply', json={'reply': output})
    requests.post('http://localhost:5000/image_data', json={'image_data': image_data})

    # Wait for the audio to finish playing
    play_obj.wait_done()
    print("audio finished")

    # Send a message to the frontend to stop the talking animation
    requests.post('http://localhost:5000/stop_talking')

def start_speaking_large(output):
    print("working for reply large")

    # Change the command to create output.wav
    command = f"echo \"{output}\" | ./piper/piper --model en_US-joe-medium.onnx --output_file output.wav"

    # Change the current working directory
    cwd = "/home/whizzy/my_project_venv/Hey-Whizzy-main/raspi/piper"

    # Run the command
    subprocess.run(command, shell=True, cwd=cwd)

    # Play the output.wav file
    wave_obj = simpleaudio.WaveObject.from_wave_file(f"{cwd}/output.wav")
    play_obj = wave_obj.play()
    print("audio played")

    # Send the reply to the backend UI
    requests.post('http://localhost:5000/reply_large', json={'reply': output})

    # Wait for the audio to finish playing
    play_obj.wait_done()
    print("audio finished")

    # Send a message to the frontend to stop the talking animation
    requests.post('http://localhost:5000/stop_talking')

def no_pick_up():
    reply = "Sorry, I didn't quite hear you well."
    start_speaking(reply)

def set_reply(output, reply_type, image_data):
    if reply_type == 1:
        start_speaking_large(output)
    elif reply_type == 2:
        start_speaking_small(output, image_data)