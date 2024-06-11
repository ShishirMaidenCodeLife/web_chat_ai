
# Importing necessary libraries/modules
import pyttsx3 # Python libraray to translate text to speech
# from gtts import gTTS # alternative library to translate text to speech
import pygame # multimedia functions for playing sound
from io import BytesIO #for handling binary data as a file-like object

# dependencies for streaming audio to a destination by converting to wav file
import pyaudio
import wave
from default_values import VB_Cable_A_channel

from pythonosc import udp_client #  Module for sending OSC messages over UDP to pass text for speech bubble.
import osc_communication.osc_emote


# Function to speak text to VR
def speak_text_to_vr(text):

    output_device_index = VB_Cable_A_channel # setting output cable to send audio from python file to vrchat app.

    # converting and saving audio to a wav file
    output_file = "audio/audio_file/output_to_vr.wav"
    engine = pyttsx3.init()
    engine.save_to_file(text, output_file)
    engine.runAndWait() # Run and wait for text-to-speech conversion

    CHUNK = 1024
    with wave.open(output_file, 'rb') as wf:
        sample_rate = wf.getframerate() 
         # Initialize PyAudio
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()), # Set audio format based on WAV file parameters
                        channels=wf.getnchannels(),
                        rate=sample_rate,
                        output=True,
                        output_device_index=output_device_index)
        
         # Reading and streaming audio data in chunks
        data = wf.readframes(CHUNK)
        while data:
            stream.write(data)
            data = wf.readframes(CHUNK)
        
        # Stopping and closing audio stream
        stream.stop_stream()
        stream.close()
        p.terminate()

  
