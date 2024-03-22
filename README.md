# Hey Whizzy
## Capstone 2023IT07
Capstone Project of:
Andrei Magbuhat, John Tiu, Neil Guingcangco, and Owen Santos

We pray we pass!

# Guide

## What to install in Raspi

### Updating the Software of Raspi
```
sudo apt update
sudo apt upgrade
```

### Updating Python for Raspi
```
sudo apt-get update
sudo apt-get install python3-pip
sudo apt-get install python3-venv
```

### Getting the Python directory
```
(Get-Command python).Source
```

### For Creation of Virtual Environment (venv)
```
python3 -m venv ~/my_project_venv
```

### Steps in activating the venv
```
source ~/my_project_venv/bin/activate
cd my_project_venv
code . 
```

### Explanation of steps above
```
ls = dir in windows
cd = cd in windows
code . = to run vs code on the selected directory
```

### Things to update globally
```
sudo apt-get install portaudio19-dev
sudo apt-get install flac
sudo apt-get install alsa-utils
sudo apt-get install pulseaudio pulseaudio-utils
sudo apt-get install libasound2-dev
sudo apt-get install espeak
sudo apt-get install espeak-ng
sudo apt-get install flite
```

### Things to update inside the venv (when venv is activated)
```
pip install --upgrade pip
pip install --upgrade pip setuptools
pip install wheel
pip install pyaudio
pip install git+https://github.com/openai/whisper.git soundfile
pip install vosk
pip install setuptools_rust
pip install TTS
pip install scipy
pip install simpleaudio
pip install Flask-MySQLdb
```

### Installing Piper TTS
`wget https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_arm64.tar.gz`
Create a folder named piper, extract this on the folder.
Then download the voice model
```
https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/joe/medium/en_US-joe-medium.onnx?download=true
https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/joe/medium/en_US-joe-medium.onnx.json
```
Ctrl + S on the .json file to save it because there is download button for this.
Reminder on the piper execution, you need the script to be /piper/piper.

### To use Vosk
Place the vosk model at the same folder of initialize.py.
Name the vosk model folder -> 'model'.

## Other fixes

### Check this out to fix ALSA errors on Raspi.
https://github.com/Uberi/speech_recognition/issues/182

### Things to install to fix such errors (when venv is activated)
`pip install sounddevice`
Remember to put this on the .py files if you need speech_recognition running.
`import sounddevice`

### If there is error on pip package installation (when venv is activated)
`pip cache purge`

### Mic problems outside coding
`alsamixer`
Use on the terminal to select default mic

## Bootstrap
- https://getbootstrap.com/docs/5.3/getting-started/introduction/
- https://getbootstrap.com/docs/5.3/examples/

## For flask

### Installation of Flask
```
pip install flask
pip install Flask-MySQLdb
pip install werkzeug
```

### Server preparation
- Run xampp
- Run raspi_flask.py

### Changes made for flask to work on the network

- Run xampp with administrator mode.
- Allow python on the firewall (on searchbar "allow").
- Change code on app.run(debug=True, host='0.0.0.0').
- Make sure all devices (to be used) are connected on the same network.
