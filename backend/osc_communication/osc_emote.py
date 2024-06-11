##WORKS FOR ALEX Avatar##

import argparse
from pythonosc import udp_client

client = udp_client.SimpleUDPClient('127.0.0.1', 9000)

def thinking_express():
    ## for thinking dots.
    osc_address = '/chatbox/typing'
    osc_value = True
    client.send_message(osc_address, osc_value)


def facial_express(emo_val):
    # Define the OSC address and message to send
    osc_address = '/avatar/parameters/Face/Facial'
    osc_value = emo_val

    # Send the OSC message
    client.send_message(osc_address, osc_value)

def facial_express_remove():
    # Define the OSC address and message to send
    osc_address = '/avatar/parameters/Face/Facial'
    osc_value = 0

    # Send the OSC message
    client.send_message(osc_address, osc_value)


if __name__=="__main__":
    while True:
        emo_val=int(input("enter the value of emote 0 to 5"))
        facial_express(emo_val)