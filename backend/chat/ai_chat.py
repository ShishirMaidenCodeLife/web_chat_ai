# chat_with_ai.py

import openai # OpenAI python tool for interacting with GPT models
from default_values import open_ai_key # Imoprting the open_ai_key that lets access to OpenAI
from pythonosc import udp_client # importing UDP client for communication
import re

# Defineing the OSC client to show thinkng emote in VRChat when the response from Avatar is not yet delivered.
client = udp_client.SimpleUDPClient("127.0.0.1", 9000)

openai.api_key = open_ai_key

from animation.face_animation import remove_expression, check_expression
from database.past_session import format_conversation
from database.chat_db import get_conversation_to_continue_past_session
from chat.prompts_set import first_system_content


# Initializing the conversation history
global_messages_array = [
    {"role": "system", "content": first_system_content} #initial system messege
]
global_current_session_id = None

# function to chat with AI (GPT of OpenAI)
def chat_with_ai(text, session_id, continue_past_sessionnumber = None):

    global global_messages_array, global_current_session_id

    ## if new session
    if session_id != global_current_session_id:  
    # Initializing the conversation history
        global_messages_array = [
            {"role": "system", "content": first_system_content} #initial system messege
        ]
        global_current_session_id = session_id
    
    ## if to take conversation from any selected past history
    if continue_past_sessionnumber != None:
        global_messages_array = [
            {"role": "system", "content": first_system_content} #initial system messege
        ]
    
        past_msg_from_db = get_conversation_to_continue_past_session(continue_past_sessionnumber) # Taking the specific past conversation session history from db
        past_msg_in_openai_format = format_conversation(past_msg_from_db)
        global_messages_array.extend(past_msg_in_openai_format)
        print(global_messages_array)
    
    global_messages_array.append({"role": "user", "content": text}) # Adding user messege to conversation history

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo", #using the gpt3.5-turbo for response generation
        # model="gpt-4o",
        messages=global_messages_array, #Passing the conversation history to the Model.
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
        presence_penalty=0.6,
    ) 
    ai_response = response.choices[0].message.content
    print(ai_response)
    ai_response_noemotion = remove_expression(ai_response)

    global_messages_array.append({"role": "assistant", "content": ai_response_noemotion}) # Adding the AI reponse to conversation history
    
    emote_number = check_expression(ai_response)
    print("the emote is:", emote_number)

    # print(ai_response)
    # print(ai_response_noemotion)

    return ai_response_noemotion, emote_number


if __name__=="__main__":
    chat_with_ai("what was bad about world war?")
