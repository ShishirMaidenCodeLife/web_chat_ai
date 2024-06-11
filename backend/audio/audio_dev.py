## Running this file using the all_channel arg in termilnal ie: "python audio_dev.py --all_channels" will list out all the available audio devices and virtual channels. The Output channels, input channels and their sampling rate details are provided. 
## By default running this file with "python audio_dev.py" will provide only sets the VB_Cable_B_channel and VB_Cable_A_channel with correct index values so that they can be leveraged.
## Note: For gettin


import sys
import pyaudio

# # Define VB_Cable_B_channel and VB_Cable_A_channel as global variables
# VB_Cable_B_channel = None
# VB_Cable_A_channel = None

def print_devices(input_devices, output_devices, vb_audio_input_devices, vb_audio_output_devices):
    # Print all devices
    print("\nLISING ALL INPUT AND OUTPUT DEVICES:")
    print("\nAll Input Devices:")
    print("---------------------------------------------------------------------------------------------------------------")
    print("Device Index   | Device Name                                 | Max Input Channels | Default Sample Rate | Host API")
    print("---------------------------------------------------------------------------------------------------------------")
    for device in input_devices:
        print("{:<14} | {:<60} | {:<18} | {:<18} | {}".format(
            device['index'], device['name'], device['maxInputChannels'], 
            device['defaultSampleRate'], device['hostApi']))

    # Print all output devices
    print("\nAll Output Devices:")
    print("---------------------------------------------------------------------------------------------------------------")
    print("Device Index   | Device Name                                 | Max Output Channels | Default Sample Rate | Host API")
    print("---------------------------------------------------------------------------------------------------------------")
    for device in output_devices:
        print("{:<14} | {:<60} | {:<20} | {:<18} | {}".format(
            device['index'], device['name'], device['maxOutputChannels'], 
            device['defaultSampleRate'], device['hostApi']))

    # Print VB-Audio input devices
    print("\nVB-AUDIO LISTS")
    print("\nVB-Audio Input Devices:")
    print("---------------------------------------------------------------------------------------------------------------")
    print("Device Index   | Device Name                                 | Max Input Channels | Default Sample Rate | Host API")
    print("---------------------------------------------------------------------------------------------------------------")
    for device in vb_audio_input_devices:
        print("{:<14} | {:<45} | {:<18} | {:<18} | {}".format(
            device['index'], device['name'], device['maxInputChannels'], 
            device['defaultSampleRate'], device['hostApi']))

    # Print VB-Audio output devices
    print("\nVB-Audio Output Devices:")
    print("---------------------------------------------------------------------------------------------------------------")
    print("Device Index   | Device Name                                 | Max Output Channels | Default Sample Rate | Host API")
    print("---------------------------------------------------------------------------------------------------------------")
    for device in vb_audio_output_devices:
        print("{:<14} | {:<60} | {:<20} | {:<18} | {}".format(
            device['index'], device['name'], device['maxOutputChannels'], 
            device['defaultSampleRate'], device['hostApi']))


  
    
# Initialize PyAudio
p = pyaudio.PyAudio()

# Get the number of available devices
num_devices = p.get_device_count()

# Separate input and output devices
input_devices = []
output_devices = []

# Loop through all devices and categorize them as input or output
for i in range(num_devices):
    device_info = p.get_device_info_by_index(i)
    if device_info['maxInputChannels'] > 0:
        input_devices.append(device_info)
    if device_info['maxOutputChannels'] > 0:
        output_devices.append(device_info)

# Filter devices containing "VB-Audio"
vb_audio_input_devices = [device for device in input_devices if 'VB-Audio' in device['name']]
vb_audio_output_devices = [device for device in output_devices if 'VB-Audio' in device['name']]

# Find specific devices withn in VB-Audio devices ie: Extracting the information of all Cable B and Cable A channels.
VB_Cable_B_input = next((device for device in vb_audio_input_devices if 'CABLE-B' in device['name']), None)
VB_Cable_A_output = next((device for device in vb_audio_output_devices if 'CABLE-A' in device['name']), None)

# Extracting the index of of Cable B input and Cable A output channels
VB_Cable_B_channel = VB_Cable_B_input['index'] if VB_Cable_B_input else None
VB_Cable_A_channel = VB_Cable_A_output['index'] if VB_Cable_A_output else None

# Terminate PyAudio
p.terminate()


if __name__ == "__main__":
    print("\n-----------------------------------------------------------------------------------")
    print("pass '--all_channels' in as terminal arg to get info about all the channels")
    print("-----------------------------------------------------------------------------------")
    print("Sampling any one supporting channel for both B and A channel")
    print("VB_Cable_B_channel =", VB_Cable_B_channel)
    print("VB_Cable_A_channel =", VB_Cable_A_channel)
    if len(sys.argv) > 1 and sys.argv[1] == "--all_channels":
        print_devices(input_devices, output_devices, vb_audio_input_devices, vb_audio_output_devices)
