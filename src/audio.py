# Author: Faycal Kilali
# This script sets up the audio for Adafruit Speaker Bonnet for Raspberry Pi.
# Below is a script to setup the hardware for adafruit if you wish to use that particular hardware

###
#sudo apt install -y wget
#pip3 install adafruit-python-shell
#wget https://github.com/adafruit/Raspberry-Pi-Installer-Scripts/raw/main/i2samp.py
#sudo -E env PATH=$PATH python3 i2samp.py

import gtts
#from gtts import gTTS
import os
#import vlc
#import subprocess
#from playsound import playsound
#import simpleaudio as sa
#from pydub import AudioSegment
#from pydub.playback import play
#from audioplayer import AudioPlayer
from pygame import mixer

output = os.path.relpath("uploads/output.mp3")

def synthesize_audio(text, language):
    """
    Synthesizes audio from text in a specified language and plays it.

    :param text: The text to synthesize.
    :param language: The target language code (e.g., 'en', 'fr', 'es').
    """
    try:
        # Generate the audio
        tts = gtts.gTTS(text=text, lang=language)
        output_file = output
        tts.save(output_file)

        # Play the audio
        #p = vlc.MediaPlayer("file:///" + output_file)
        #p.play()
        mixer.init()
        mixer.music.load(output_file)
        mixer.music.play()
        # Wait for the sound to finish playing
        while mixer.music.get_busy():
            continue  # Loop until the audio is finished playing

        #AudioPlayer(output_file).play(block=True)
        #sound = AudioSegment.from_wav(output_file)
        #play(sound)
        #subprocess.run(['aplay', output_file], check=True)
        #wave_obj = sa.WaveObject.from_wav_file(output_file)
        #play_obj = wave_obj.play()
        #play_obj.wait_done()
        #playsound(output_file)

        # Optional: Remove the file after playback
        #os.remove(output_file)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        mixer.quit()
        #pass

# Example usage
if __name__ == "__main__":
    sample_text = "Hello, this is a test."
    target_language = "en"  # Change to 'fr', 'es', etc., for other languages
    synthesize_audio(sample_text, target_language)
