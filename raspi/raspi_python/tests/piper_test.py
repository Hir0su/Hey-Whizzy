import subprocess
import simpleaudio

text = "My name is the great wizard Whizzy!"

# Change the command to create output.wav
command = f"echo '{text}' | ./piper/piper --model en_US-joe-medium.onnx --output_file output.wav"

# Change the current working directory
cwd = "/home/whizzy/my_project_venv/Hey-Whizzy-main/raspi/piper"

# Run the command
subprocess.run(command, shell=True, cwd=cwd)

# Play the output.wav file
wave_obj = simpleaudio.WaveObject.from_wave_file(f"{cwd}/output.wav")
play_obj = wave_obj.play()

# Wait for the audio to finish playing
play_obj.wait_done()