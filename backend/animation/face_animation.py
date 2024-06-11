## this file has two functions: 1 for removing expression from text found from second functionfunciton . 2. the second function for finding the emotion on the response text, which can be used for facial expression in avatar.

import re

emotions_dict={ 
    '[face:normal]':1,
    '[face:happy]':2, 
    '[face:Shocked]':3, 
    '[face:Angry]':4, 
    '[face:Disturbed]':5
}

def remove_expression(ai_response_emotion):
    emotion_animation_regex = r"\[(face:\w+)\]|\[animation:\w+\]"  # Combined pattern
    ai_response_noemotion = re.sub(emotion_animation_regex, "", ai_response_emotion) #removed emotion patterns from the response
    return (ai_response_noemotion)

def check_expression(ai_response_emotion):
    emotion_animation_regex = r"\[(face:\w+)\]|\[animation:\w+\]"  # Combined pattern
     ## tracking the emotion
    match = re.search(emotion_animation_regex, ai_response_emotion)
    # If a match is found, extract the emotion
    if match:
        extracted_emotion = match.group(0)
        # print(f"Extracted emotion: {extracted_emotion}")
        if extracted_emotion in emotions_dict:
            emotion_number = emotions_dict[extracted_emotion]
            # print("emotion_value:",emotion_number)

            return emotion_number
    else:
        default_emote = 1
        return default_emote


