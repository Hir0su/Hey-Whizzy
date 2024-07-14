import os
import time
import pygame

def play_sound(filename):
    pygame.mixer.init()
    sound = pygame.mixer.Sound(filename)
    sound.play()

    # Add a delay to ensure the sound is played in its entirety
    pygame.time.wait(int(sound.get_length() * 1000))

def main():
    # Get the current directory
    current_directory = os.path.dirname(os.path.abspath(__file__))
    # Construct the file path to the sound file
    sound_file = os.path.join(current_directory, "sounds", "granted.wav")

    # Your voice assistant code here

    # Play sound effect when ready to receive input
    play_sound(sound_file)  # Pass the constructed file path to the play_sound function

if __name__ == "__main__":
    main()
