# Importing library for fastAPI
from fastapi import FastAPI, Body, Depends
from fastapi.middleware.cors import CORSMiddleware

# Import necessary libraries for OpenAI API interaction
import openai

# Importing local functions from the modules
from audio.vr_listen import detect_wake_word, transcribe_user_input
from chat.ai_chat import chat_with_ai
from audio.vr_speak import speak_text_to_vr
from osc_communication.osc_emote import facial_express, facial_express_remove, thinking_express
from osc_communication.osc_text import send_osc_chat_message
from threading import Thread

# Importing Database code from the module
from database.chat_db import insert_conversation_data, create_table, get_all_conversations, get_conversation_by_id, get_conversations_by_actual_session, get_conversations_by_source, get_conversations_all_sessions, get_conversation_all_sessions_with_breaktoken, get_conversation_to_continue_past_session


#Importing uuid for session management
from uuid import uuid4  

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

global_session_id = None
global_continue_past_session = None

def create_new_session():
    global global_session_id
    global_session_id = str(uuid4())
    create_table()

@app.get("/")
async def read_root():
    return {"fastAPI is working!"}

@app.get("/newsession") # endpoint for creating new session id when user press start new chat in vrchat.
async def new_sessions():
    create_new_session()
    return {"session id recorded"}

@app.get("/continue_past_session/{clicked_session_no}")
async def load_past_session(clicked_session_no: str):
    global global_continue_past_session
    create_new_session()
    print ("Clicked Session is ",clicked_session_no)
    global_continue_past_session = clicked_session_no
    past_msg_on_the_clicked_session = get_conversation_to_continue_past_session(clicked_session_no)

    return {"Past messages": past_msg_on_the_clicked_session}

# to get the conversation in sorted order and kept by session seperated using <chat_session_break_token> (in string format for passing to String Loader in Udon Sharp)
@app.get("/chat_history")
async def conversation_history_all_sessions():
    conversations_in_string = get_conversation_all_sessions_with_breaktoken()
    print(conversations_in_string)
    return conversations_in_string


# endpoint for processing the query, saving in db and also responding the ai answer back
@app.get("/message/{message}")
async def read_item(message: str, query_param: str = None):
    global global_continue_past_session
    user_msg = message
    try:
        ai_response_noemotion, emote_number = chat_with_ai(user_msg, global_session_id, global_continue_past_session)
        answer = ai_response_noemotion
        # print("The ques:", msg)
        # print("The ans:", answer)

        facial_express(emote_number)

        # Define functions to be executed concurrently
        def send_message():
            send_osc_chat_message(ai_response_noemotion)
        
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

        # Insert data into the database
        insert_conversation_data(global_session_id, 'FastAPI', user_msg, answer)

        if global_continue_past_session != None:
            global_continue_past_session = None # making the global global_continue_past_session again none ( this will stop passing past session context while making second conversation once started, as we require it for first conversation only.)
        msg_to_show_in_VRChat = "User: " + user_msg + "\n" + "AI: " + answer
        # return {"User": user_msg, "AI": answer}

        conversations_in_string = get_conversation_all_sessions_with_breaktoken()
        # print(conversations_in_string)
        msg_to_show_in_VRChat = conversations_in_string

        return msg_to_show_in_VRChat

    except Exception as e:
        print(f"Error during processing: {e}")
        return {"error": "An error occurred while processing your request."}


## Other unused Endponts for retriving data from database
# Endpoint to retrieve all conversation history
@app.get("/chat_history/all")
async def conversation_history():
    conversations = get_all_conversations()
    return {"conversation_history": conversations}

# Endpoint to retrieve conversation history by session id
@app.get("/chat_history/db_id/{id}")
async def conversation_history_by_id(id: str):
    conversations = get_conversation_by_id(id)
    return {"conversation_history": conversations}

# Endpoint to retrieve conversation history by Uuid4 session value
@app.get("/chat_history/db_session/{uuid_session_id}")
async def conversation_history_by_actual_session(session_id: str):
    conversations = get_conversations_by_actual_session(session_id)
    return {"conversation_history": conversations}

# Endpoint to retrieve conversation history by source (e.g., 'FastAPI' or 'run.py')
@app.get("/chat_history/source/{source}")
async def conversation_history_by_source(source: str):
    conversations = get_conversations_by_source(source)
    return {"conversation_history": conversations}

