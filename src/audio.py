# Author: Faycal Kilali
# This script sets up the audio for Adafruit Speaker Bonnet for Raspberry Pi.
# Below is a script to setup the hardware for adafruit if you wish to use that particular hardware

###
#sudo apt install -y wget
#pip3 install adafruit-python-shell
#wget https://github.com/adafruit/Raspberry-Pi-Installer-Scripts/raw/main/i2samp.py
#sudo -E env PATH=$PATH python3 i2samp.py

from gtts import gTTS
import os
from playsound import playsound

output = os.path.relpath("uploads/output.wav")

def synthesize_audio(text, language):
    """
    Synthesizes audio from text in a specified language and plays it.

    :param text: The text to synthesize.
    :param language: The target language code (e.g., 'en', 'fr', 'es').
    """
    try:
        # Generate the audio
        tts = gTTS(text=text, lang=language)
        output_file = output
        tts.save(output_file)

        # Play the audio
        playsound(output_file)

        # Optional: Remove the file after playback
        os.remove(output_file)

    except Exception as e:
        print(f"An error occurred: {e}")


# Example usage
if __name__ == "__main__":
    sample_text = "Hello, this is a test."
    target_language = "en"  # Change to 'fr', 'es', etc., for other languages
    synthesize_audio(sample_text, target_language)
