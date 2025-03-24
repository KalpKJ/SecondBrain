<template>
    <div class="chat-interface">
      <div class="chat-messages" ref="messagesContainer">
        <div v-for="(message, index) in messages" :key="index" :class="['message', message.type]">
          <div class="message-content">
            <div v-if="message.type === 'user'" class="user-message">
              {{ message.content }}
            </div>
            <div v-else class="assistant-message">
              <vue-markdown-render :source="message.content"></vue-markdown-render>
              
              <div v-if="message.sources && message.sources.length" class="sources">
                <h4>Sources:</h4>
                <ul>
                  <li v-for="(source, idx) in message.sources" :key="idx">
                    <strong>{{ source.metadata.title }}</strong>
                    <p>{{ source.text }}</p>
                  </li>
                </ul>
              </div>
            </div>
          </div>
          <div class="message-timestamp">
            {{ formatTimestamp(message.timestamp) }}
          </div>
        </div>
      </div>
      
      <div class="chat-input">
        <textarea 
          v-model="userInput" 
          @keydown.enter.prevent="sendMessage"
          placeholder="Ask your Second Brain something..."
          rows="3"
        ></textarea>
        <button @click="sendMessage" :disabled="isLoading">
          <span v-if="isLoading">Thinking...</span>
          <span v-else>Send</span>
        </button>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, computed, watch, nextTick } from 'vue';
  import { useBrainStore } from '@/stores/brain';
  import VueMarkdownRender from 'vue-markdown-render';
  
  export default {
    components: {
      VueMarkdownRender
    },
    setup() {
      const brainStore = useBrainStore();
      const userInput = ref('');
      const messagesContainer = ref(null);
      
      const messages = computed(() => {
        if (!brainStore.currentConversation) return [];
        return brainStore.currentConversation.messages;
      });
      
      const isLoading = computed(() => brainStore.isLoading);
      
      const sendMessage = async () => {
        if (!userInput.value.trim() || isLoading.value) return;
        
        try {
          await brainStore.queryKnowledge(userInput.value);
          userInput.value = '';
        } catch (error) {
          console.error('Error sending message:', error);
        }
      };
      
      const formatTimestamp = (timestamp) => {
        const date = new Date(timestamp);
        return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
      };
      
      // Auto-scroll to bottom when new messages arrive
      watch(messages, async () => {
        await nextTick();
        if (messagesContainer.value) {
          messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
        }
      }, { deep: true });
      
      return {
        userInput,
        messages,
        isLoading,
        sendMessage,
        formatTimestamp,
        messagesContainer
      };
    }
  };
  </script>
  
  <style scoped>
  .chat-interface {
    display: flex;
    flex-direction: column;
    height: 100%;
    max-width: 800px;
    margin: 0 auto;
  }
  
  .chat-messages {
    flex: 1;
    overflow-y: auto;
    padding: 1rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
  
  .message {
    max-width: 80%;
    padding: 0.75rem 1rem;
    border-radius: 1rem;
    position: relative;
  }
  
  .user {
    align-self: flex-end;
    background-color: #e3f2fd;
  }
  
  .assistant {
    align-self: flex-start;
    background-color: #f5f5f5;
  }
  
  .message-timestamp {
    font-size: 0.75rem;
    color: #888;
    margin-top: 0.25rem;
    text-align: right;
  }
  
  .sources {
    margin-top: 0.75rem;
    padding-top: 0.75rem;
    border-top: 1px solid #ddd;
    font-size: 0.85rem;
  }
  
  .sources h4 {
    margin-bottom: 0.5rem;
  }
  
  .sources ul {
    padding-left: 1rem;
  }
  
  .sources li {
    margin-bottom: 0.5rem;
  }
  
  .chat-input {
    padding: 1rem;
    display: flex;
    gap: 0.5rem;
    border-top: 1px solid #eee;
  }
  
  textarea {
    flex: 1;
    padding: 0.75rem;
    border: 1px solid #ddd;
    border-radius: 0.5rem;
    resize: none;
    font-family: inherit;
  }
  
  button {
    padding: 0 1.5rem;
    background-color: #2196f3;
    color: white;
    border: none;
    border-radius: 0.5rem;
    cursor: pointer;
    font-weight: bold;
  }
  
  button:disabled {
    background-color: #b0bec5;
    cursor: not-allowed;
  }
  </style>
  