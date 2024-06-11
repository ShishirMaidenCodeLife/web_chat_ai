# importing the functions from the modules
from audio.vr_listen import detect_wake_word, transcribe_user_input
from chat.ai_chat import chat_with_ai
from audio.vr_speak import speak_text_to_vr
from osc_communication.osc_emote import facial_express, facial_express_remove, thinking_express
from osc_communication.osc_text import send_osc_chat_message
from threading import Thread

#importing database connection code
from database.chat_db import create_table, insert_conversation_data

#Importing uuid for session management
from uuid import uuid4  

if __name__ == "__main__":

    # creating an empty database first:
    create_table()

    # loop until the wake word is detected
    while not detect_wake_word():
        pass
    print("Wake word detected! Starting user input loop...")
    greetings_phrase = "Hello! How can I help you?"
    thinking_express()
    speak_text_to_vr(greetings_phrase) # Passing Simple greeting response to the "hello" wakeup word.
    send_osc_chat_message(greetings_phrase)
    session_id = str(uuid4()) # allocating the session id automatically when the user says hello to start the conversation first.

    while True:
        user_input = transcribe_user_input() # Changing the audio input from VRchat app to text.
        if user_input:
            # Creating new session in case use wants it . For this the user can say new session.
            if user_input.lower() == "start new chat session":
                session_id = str(uuid4())
                continue ## to skip the rest of the loop and starts over if user says new session.

            # showing thinking sign :
            thinking_express()
            
            ai_response_noemotion, emote_number = chat_with_ai(user_input,session_id) # Passing the corresponding text transcipiton to AI for reponse generation
            print(f"AI: {ai_response_noemotion}") # printing the reponse in console.

            facial_express(emote_number)
            # Define functions to be executed concurrently
            def send_message():
                send_osc_chat_message(ai_response_noemotion)

            # def express_emotion():
            #     facial_express(emote_number)

            def speak_response():
                speak_text_to_vr(ai_response_noemotion)

            # Create threads for each function
            thread_send_message = Thread(target=send_message)
            # thread_express_emotion = Thread(target=express_emotion)
            thread_speak_response = Thread(target=speak_response)

            # Start all threads
            thread_send_message.start()
            # thread_express_emotion.start()
            thread_speak_response.start()

            # # Wait for all threads to finish
            # thread_send_message.join()
            # thread_express_emotion.join()
            thread_speak_response.join()

            facial_express_remove()

            insert_conversation_data(session_id, 'run.py', user_input, ai_response_noemotion)
            
            print("\n")
        else:
            print("Waiting for user input...") # No user input is detected for user input.