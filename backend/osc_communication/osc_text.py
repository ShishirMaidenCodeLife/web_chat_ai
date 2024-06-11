## # /chatbox/input s b n Input text into the chatbox. If b is True, send the text in s immediately, bypassing the keyboard. If b is False, open the keyboard and populate it with the provided text. n is an additional bool parameter that when set to False will not trigger the notification SFX (defaults to True if not specified). ##/chatbox/typing b Toggle the typing indicator on or off. 

import argparse
from pythonosc import udp_client

# Set OSC server address and port (usually defaults to 127.0.0.1 and 9000)
server_address = '127.0.0.1'
server_port = 9000

client = udp_client.SimpleUDPClient(server_address, server_port)
import time

def send_osc_greetings(message, send_immediately=True, trigger_notification_sfx=True):
    osc_address = '/chatbox/input'
    osc_value = message
    client.send_message(osc_address, osc_value)

def send_osc_chat_message(message, send_immediately=True, trigger_notification_sfx=True):
    """Sends a chat message to VRChat using OSC.

    Args:
        message (str): The text message to send.
        send_immediately (bool, optional): Whether to bypass the keyboard and send immediately. Defaults to True.
        trigger_notification_sfx (bool, optional): Whether to trigger the notification sound effect. Defaults to True.
    """
    words = message.split()
    for i in range(0, len(words), 16):
        chunk = ' '.join(words[i:i+16])
        osc_address = '/chatbox/input'
        osc_values = [chunk, send_immediately, trigger_notification_sfx]  # Use 'chunk' instead of 'message'
        client.send_message(osc_address, osc_values)
        time.sleep(6)

if __name__ == "__main__":
    while True:
        txt_msg = input("Enter message (type 'stop' to quit): ")
        if txt_msg == 'stop':
            break

        send_chat_message(txt_msg)  # Use the improved function
