<template>
  <div class="chat-app-container">
    <div class="sidebar">
      <button @click="startNewSession">New Chat Session + </button>
      <br>
      <!-- <button @click="fetchChatHistory">History</button> -->
      <div v-if="chatHistory.length" class="history-container">
        <div v-for="(session, index) in chatHistory" :key="index" class="history-session" @click="loadSession(index)">
          <!-- Use <br> tags to render line breaks -->
          <span v-html="formatSession(session)"></span>
        </div>
      </div>
    </div>
      <div v-if="show_chat_window" class="chat-window">
        <div class="chat-window">
          <div class="messages">
            <div v-for="(message, index) in messages" :key="index" :class="['message', message.sender]">
              <div class="message-content">{{ message.text }}</div>
            </div>
          </div>
          <div class="input-container">
            <input v-model="userMessage" @keyup.enter="sendMessage" placeholder="Type your message..." />
            <button @click="sendMessage">Send</button>
          </div>
        </div>
      </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ChatBox',
  data() {
    return {
      userMessage: '',
      messages: [],
      chatHistory: [],  // To store chat history sessions
      show_chat_window: false,
    };
  },
  methods: {
    async sendMessage() {
      if (this.userMessage.trim() === '') return;

      // Add user's message to the chat
      this.messages.push({ sender: 'user', text: this.userMessage });

      // Send the message to the backend
      try {
        const response = await axios.post('/message', { user_msg_fe: this.userMessage });

        // Add the response from the backend to the chat
        this.messages.push({ sender: 'bot', text: response.data["AI"] });

        this.fetchChatHistory()

      } catch (error) {
        console.error('Error sending message:', error);
        this.messages.push({ sender: 'bot', text: 'Sorry, something went wrong.' });
      }

      // Clear the input field
      this.userMessage = '';
    },

    async fetchChatHistory() {
      try {
        const response = await axios.get('/chat_history');
        // Split chat sessions by the break token
        this.chatHistory = response.data.split('<chat_session_break_token>');
      } catch (error) {
        console.error('Error fetching chat history:', error);
      }
    },

    async startNewSession() {
      try {
        await axios.get('/newsession');
        this.messages = [];
        this.userMessage = '';
        this.show_chat_window = true;
        // const response = await axios.get('/chat_history');
        // // Split chat sessions by the break token
        // this.chatHistory = response.data.split('<chat_session_break_token>');
        this.fetchChatHistory()

      } catch (error) {
        console.error('Error starting new session:', error);
      }
    },

    loadSession(index) {
      // Set messages to the selected session
      this.messages = this.chatHistory[index];
      
      // Call the backend endpoint with the clicked session number
      this.loadPastSession(index); // Assuming session numbers start from 1
    },
    async loadPastSession(clickedSessionNo) {
      try {
        const response = await axios.get(`/continue_past_session/${clickedSessionNo}`);
        console.log(response.data); // Handle the response as needed
        this.messages = [];
        this.userMessage = '';

        
        this.messages.push({ sender: 'bot', text: response.data["Past messages"] })
        // this.messages.push({ sender: 'bot', text: this.chatHistory[clickedSessionNo]})

      } catch (error) {
        console.error('Error loading past session:', error);
      }
    },
    formatSession(session) {
      // Replace \n with <br> for line breaks
      return session.replace(/\n\n/g, '<br>').replace(/\n/g, '<br>').replace('<User_msg_is>:', '<br> User:').replace('<AI_msg_is>:','<br> AI:');
    }
  }
};


</script>

<style scoped>
.chat-app-container {
  display: flex;
  width: 800px;
  margin: 0 auto;
  border: 1px solid #ccc;
  border-radius: 10px;
  overflow: hidden;
}

.sidebar {
  width: 200px;
  border-right: 1px solid #ccc;
  display: flex;
  flex-direction: column;
  padding: 20px;
}

.chat-window {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 20px;
}

.messages {
  flex: 1;
  overflow-y: auto;
  max-height: 400px;
  margin-bottom: 10px;
}

.message {
  padding: 10px;
  margin: 5px 0;
  border-radius: 5px;
}

.message.user {
  background-color: #e0f7fa;
  align-self: flex-end;
}

.message.bot {
  background-color: #f1f8e9;
  align-self: flex-start;
}

.input-container {
  display: flex;
}

input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

button {
  padding: 10px;
  margin-left: 10px;
  border: none;
  background-color: #007bff;
  color: white;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}

.history-container {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  overflow-y: auto; /* Added to enable scrolling */
  max-height: 200px; /* Example height, adjust as needed */
}

.history-session {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  margin-bottom: 5px;
  cursor: pointer;
}

.history-session:hover {
  background-color: #f0f0f0;
}
</style>
