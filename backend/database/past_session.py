# from database.chat_db import get_conversation_to_continue_past_session
from database.chat_db import get_conversation_to_continue_past_session

def format_conversation(session_log):
    conversation = []
    lines = session_log.strip().split('\n')
    
    for line in lines:
        if line.startswith('User:'):
            conversation.append({"role": "user", "content": line[len('User:'):].strip()})
        elif line.startswith('AI:'):
            conversation.append({"role": "assistant", "content": line[len('AI:'):].strip()})
    
    return conversation

## testing the format conversion
if __name__ == "__main__":
    global_messages_array = [
            {"role": "system", "content": "Your are an AI Assistant who gives anwers to user query in very short"} #initial system messege
        ]
  
    id = 1
    all_sess = get_conversation_to_continue_past_session(id)
    # print(all_sess)
    formatted_conversation = format_conversation(all_sess)
    # print(formatted_conversation)
    global_messages_array.extend(formatted_conversation)
    print(global_messages_array)
