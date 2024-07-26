# Hey Whizzy
## Capstone 2023IT07
Capstone Project of:
Andrei Magbuhat, John Tiu, Neil Guingcangco, and Owen Santos.

<a href="https://github.com/Hir0su/Hey-Whizzy/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Hir0su/Hey-Whizzy" />
</a>

[Hey Whizzy's Windows Port Repository](https://github.com/andododo/Hey-Whizzy-Windows-Port)
[Hey Whizzy's Admin Website Repository](https://github.com/Hir0su/Hey-Whizzy-Admin-Website)

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
sudo apt-get install python3-pyqt5
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
pip install flask-socketio
pip install pillow
pip install imageio
```

### Installing React.js
Download using nvm (choices) for the above command
- https://nodejs.org/en/download/package-manager/#debian-and-ubuntu-based-linux-distributions-1

In the raspi_python folder:
```
npx create-react-app frontend
npm install axios
npm install socket.io-client
```
A README file will be created on how to use the React, please check.
TL: use `npm start` on the frontend folder using cli


### Installing Piper TTS
```
wget https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_arm64.tar.gz
```
Create a folder named piper, extract this on the folder.
Then download the voice model and json file.
- https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/joe/medium/en_US-joe-medium.onnx?download=true
- https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/joe/medium/en_US-joe-medium.onnx.json

Ctrl + S on the .json file to save it because there is download button for this.
Reminder on the piper execution, you need the script to be /piper/piper.

### To use Vosk
Place the vosk model at the same folder of initialize.py.
Name the vosk model folder -> 'model'.

## Other fixes

### Check this out to fix ALSA errors on Raspi.
https://github.com/Uberi/speech_recognition/issues/182

### Things to install to fix such errors (when venv is activated)
```
pip install sounddevice
```
Remember to put this on the .py files if you need speech_recognition running.
```
import sounddevice
```

### If there is error on pip package installation (when venv is activated)
```
pip cache purge
```

### Mic problems outside coding
```
alsamixer
```
Use on the terminal to select default mic

## Bootstrap
- https://getbootstrap.com/docs/5.3/getting-started/introduction/
- https://getbootstrap.com/docs/5.3/examples/

## Gemini API
```
pip install google.generativeai
pip install generativeai
```

### Get Gemini API key
- https://ai.google.dev/

## For Flask

### Installation of Flask
```
pip install flask
pip install Flask-MySQLdb
pip install werkzeug
pip install Flask-Mail
```

### Server preparation
- Run xampp
- Run raspi_flask.py

### Changes made for flask to work on the network

- Run xampp on administrator mode.
- Allow python on the firewall (on searchbar "allow").
- Change code on app.run(debug=True, host='0.0.0.0').
- Make sure all devices (to be used) are connected on the same network.
- Make sure that the requests has the right ip address pointer and port (ex. 192.168.0.15:5000)

## For Search feature

### Installation for Search
```
Install these libraries first
```
- pip install nltk
- pip install scikit-learn

### Search Preparation
- Create new file
- Name it install.py
- Run this script
```
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```
- This is a required data for the library nltk
- This will download the necessary data for tokenization and stop word removal.

### Final Piece
- Create a new file, call it text_preprocessing.py
- Call this on your initialize.py or app.py
```
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

def preprocess_text(text):
    # Tokenize the text into words
    tokens = word_tokenize(text.lower())

    # Remove stop words
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [w for w in tokens if not w.lower() in stop_words]

    # Perform stemming
    stemmer = PorterStemmer()
    stemmed_tokens = [stemmer.stem(w) for w in filtered_tokens]

    # Join the stemmed tokens back into a string
    preprocessed_text = ' '.join(stemmed_tokens)

    return preprocessed_text
```
