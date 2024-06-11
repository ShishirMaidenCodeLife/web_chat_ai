
import audio.audio_dev as audio_ch
from non_share_values import open_ai_key_value

try:
    # automatically assigning channels values 
    VB_Cable_B_channel = audio_ch.VB_Cable_B_channel
    VB_Cable_A_channel = audio_ch.VB_Cable_A_channel
except AttributeError:
    try:
        # manually assigning channels values
        VB_Cable_B_channel = 3 # CABLE-B Output (VB-Audio Cable B) having input channels. Takes audio from vrchat
        VB_Cable_A_channel = 10 # CABLE-A Input (VB-Audio Cable A) having output channels.  Sends audio to vrchat
    except Exception:
        raise Exception("Unable to set channel values. Please refer to 'python audio_dev.py --all_channels' in the terminal and set the values here accordingly.")

open_ai_key= open_ai_key_value

avatar_name = "MY_AI"
WAKE_WORD = "hello"  # any wake word