# This file has code for 2 functions: one to detect the Greeting and other for transcibing the speech chat.

import speech_recognition as sr # for recoginizing speech from any audio source and translating it to text.
from default_values import VB_Cable_B_channel, WAKE_WORD # importing the VB_Cable_B_channel index from default.py, and predined Wake_word "hello"

# Initializing speech recognizer
recognizer = sr.Recognizer()

# Defining a function to take audio from VR-chat and recoginising if the audio is wake word or not for activating the AI.
def detect_wake_word():
    
    with sr.Microphone(device_index=VB_Cable_B_channel) as source: # using CABLE-B Output (VB-Audio Cable B) having input channels to receive audio from VR-chat app. 
        print("Listening for wake word...")
        try:
            audio = recognizer.listen(source, timeout=5) #Timeout after 5 seconds
        except sr.WaitTimeoutError:
            print("Timeout occurred, no audio detected.")
            return False

    # Check for wake word
    try:
        if WAKE_WORD in recognizer.recognize_google(audio).lower():
            print(f"Wake word detected!")
            return True # Return True if wake word is detected
        else:
            print("Wake word not detected.")
            return False
    except sr.UnknownValueError:
        print("Unable to understand audio")
        return False

def transcribe_user_input():
    with sr.Microphone(device_index=VB_Cable_B_channel) as source: # The device index is set to one of the VB CABLE B Output ( Having input Channel) that listens from VR to python. Also, in windows audio settings we have to set Cable B input for vr app output device to pass audio here.)
        print("Listening for user input...")
        try:
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text # returning the transcribed text
        except sr.UnknownValueError:
            print("Unable to understand audio")
            return None
