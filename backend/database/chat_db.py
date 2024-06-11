import sqlite3

# Establishing a connection to the SQLite database named AI_avatar_conversation_data inside the database/DB folder.
conn = sqlite3.connect('database/DB/AI_avatar_conversation_data.db')
# conn = sqlite3.connect('DB/AI_avatar_conversation_data.db')
c = conn.cursor()

# Function to create the conversation history table if it doesn't exist ( our table will have fields for id (Pk), chat session id, source (ie: either text (fastapi) or speech (run.py), user messege and AI response) ).
def create_table():
    c.execute('''CREATE TABLE IF NOT EXISTS conversation_history (
                 id INTEGER PRIMARY KEY,
                 session_id TEXT,
                 source TEXT,
                 message TEXT,
                 response TEXT,
                 timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                 )''')
    conn.commit()

# Function to insert conversation data into the database
def insert_conversation_data(session_id, source, message, response):
    c.execute("INSERT INTO conversation_history (session_id, source, message, response) VALUES (?, ?, ?, ?)", (session_id, source, message, response))
    conn.commit()

# Function to retrieve all conversation history
def get_all_conversations():
    c.execute("SELECT * FROM conversation_history")
    conversations = c.fetchall()
    return conversations

# Function to retrieve conversation history by ID
def get_conversation_by_id(conversation_id):
    c.execute("SELECT * FROM conversation_history WHERE id=?", (conversation_id,))
    conversation = c.fetchone()
    return conversation

# Function to retrieve conversation history by session ID
def get_conversations_by_actual_session(session_id):
    c.execute("SELECT * FROM conversation_history WHERE session_id=?", (session_id,))
    conversations = c.fetchall()
    return conversations

# Function to retrieve conversation history by source (e.g., 'FastAPI' or 'run.py')
def get_conversations_by_source(source):
    c.execute("SELECT * FROM conversation_history WHERE source=?", (source,))
    conversations = c.fetchall()
    return conversations

# Getting all conversation and sorting them in timestamp and grouped by session id. This is actually passed for history to VRChat to display all history.
def get_conversations_all_sessions():
    c.execute("SELECT session_id, source, message, response, timestamp FROM conversation_history ORDER BY timestamp DESC, session_id;")
    all_rows = c.fetchall()
    
    all_sessions = []
    current_session = None
    session_messages = []
    
    
    for row in all_rows:
        session_id, source, message, response, timestamp = row
        
        if session_id != current_session:
            if current_session is not None:
                all_sessions.append(session_messages)
                session_messages = []
            current_session = session_id
            
        session_messages.append(("User: "+message))
        session_messages.append(("AI: "+response))
    
    if session_messages:  # Append the last session messages
        all_sessions.append(session_messages)
    
    return all_sessions



def add_session_break_token(conversations):
    conversation_string = ""
    session_count = 0
    for conv_lists in conversations:
        # conversation_string += "\nSession " +str(session_count)+ "\n"
        conversation_string += "\n<chat_session_break_token> \n Session " +str(session_count)+ "\n"
        for each_conv in conv_lists:
            conversation_string += each_conv + "\n"
        session_count += 1
    # print(conversation_string)
    return conversation_string

# adding break token to the database past conversation history data. (need to be Called by fastAPI inner funciton to return to VRChat as history).
def get_conversation_all_sessions_with_breaktoken():
    conversations = get_conversations_all_sessions()
    conversation_string = add_session_break_token(conversations)
    return conversation_string


#splitting code for the chat_session_break_token and passing each session. (need to be Called by chat AI function as the past context)
def get_conversation_to_continue_past_session(id):
    id = int(id)
    all_sess = get_conversation_all_sessions_with_breaktoken()
    sessions = [session for session in all_sess.split("<chat_session_break_token>")]
    current_session_history = sessions[id]
    return current_session_history
    