<template>
    <div class="chat-view">
      <div class="chat-container glass">
        <div class="chat-header">
          <h2>Chat with Your Second Brain</h2>
          <p>Ask questions and get insights from your knowledge base</p>
        </div>
        
        <div class="chat-messages" ref="messagesContainer">
          <div v-if="messages.length === 0" class="empty-state">
            <div class="empty-state-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
              </svg>
            </div>
            <h3>Start a conversation</h3>
            <p>Ask a question to begin chatting with your Second Brain</p>
          </div>
          
          <div v-for="(message, index) in messages" :key="index" 
               :class="['message-wrapper', message.type === 'user' ? 'user-message-wrapper' : 'assistant-message-wrapper']">
            <div :class="['message', message.type === 'user' ? 'user-message' : 'assistant-message', message.type === 'user' ? 'dark-glass' : 'glass']">
              <div class="message-content">
                <div v-if="message.type === 'user'">
                  {{ message.content }}
                </div>
                <div v-else class="markdown-content">
                  <vue-markdown-render :source="message.content"></vue-markdown-render>
                  
                  <div v-if="message.sources && message.sources.length" class="sources">
  <div class="sources-header">
    <button @click="expandedSources = expandedSources === index ? null : index" class="sources-toggle btn-glass">
      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path>
        <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path>
      </svg>
      <span>{{ expandedSources === index ? 'Hide Sources' : 'View Sources' }} ({{ message.sources.length }})</span>
    </button>
  </div>
  <ul v-if="expandedSources === index" class="sources-list">
    <li v-for="(source, idx) in message.sources" :key="idx" class="source-item glass">
      <div class="source-title">{{ source.metadata.title }}</div>
      <div class="source-text">{{ source.text }}</div>
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
        </div>
        
        <div class="chat-input-container glass">
          <textarea 
            v-model="userInput" 
            @keydown.enter.prevent="sendMessage"
            placeholder="Ask your Second Brain something..."
            rows="2"
            class="chat-input"
          ></textarea>
          <button @click="sendMessage" :disabled="isLoading" class="send-button btn-glass">
            <span v-if="isLoading" class="loading-indicator">
              <svg class="spinner" viewBox="0 0 50 50">
                <circle class="path" cx="25" cy="25" r="20" fill="none" stroke-width="5"></circle>
              </svg>
            </span>
            <span v-else class="send-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="22" y1="2" x2="11" y2="13"></line>
                <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
              </svg>
            </span>
          </button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, computed, watch, nextTick } from 'vue';
  import { useBrainStore } from '@/stores/brain';
  import  VueMarkdownRender  from 'vue-markdown-render';
  
  export default {
    components: {
      VueMarkdownRender
    },
    setup() {
      const brainStore = useBrainStore();
      const userInput = ref('');
      const messagesContainer = ref(null);
      const expandedSources = ref(null); // Will store the index of message with expanded sources
      
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
        expandedSources,
        messagesContainer
      };
    }
  };
  </script>
  
  <style scoped>
  .chat-view {
    display: flex;
    justify-content: center;
    padding: var(--space-md) 0;
    width: 100%;
    box-sizing: border-box; 
  }
  
  .chat-container {
    width: 100%;
    max-width: 1200px;
    height: 75vh;
    min-height: 600px;
    display: flex;
    flex-direction: column;
    border-radius: var(--radius-lg);
    overflow: hidden;
    position: relative;
    margin: 0 auto;
  }
  
  /* Subtle animated gradient background */
  .chat-container::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(120deg, rgba(38, 198, 218, 0.03), rgba(156, 39, 176, 0.03), rgba(38, 198, 218, 0.03));
    background-size: 300% 300%;
    animation: gradientBackground 15s ease infinite;
    z-index: -1;
  }
  
  @keyframes gradientBackground {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
  }
  
  .chat-header {
    padding: var(--space-lg);
    text-align: center;
    border-bottom: 1px solid var(--enhanced-glass-border);
    position: relative;
    overflow: hidden;
  }
  
  .chat-header::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--primary-400), var(--secondary-400), transparent);
  }
  
  .chat-header h2 {
    margin-bottom: var(--space-xs);
    background: linear-gradient(90deg, var(--primary-600) 0%, var(--secondary-600) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-fill-color: transparent;
    font-size: 2rem;
    text-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  }
  
  .chat-header p {
    color: var(--neutral-600);
    margin-bottom: 0;
    font-size: 1.1rem;
  }

.sources-toggle {
  display: flex;
  align-items: center;
  gap: var(--space-xs);
  padding: var(--space-xs) var(--space-sm);
  font-size: 0.9rem;
  color: var(--primary-700);
  border-radius: var(--radius-md);
  transition: all var(--transition-fast);
  cursor: pointer;
}

.sources-toggle:hover {
  background: rgba(255, 255, 255, 0.5);
  transform: translateY(-1px);
}

.sources-header {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  margin-bottom: var(--space-sm);
}
  .chat-messages {
    flex: 1;
    overflow-y: auto;
    padding: var(--space-lg);
    display: flex;
    flex-direction: column;
    gap: var(--space-lg);
    background-image: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%239C27B0' fill-opacity='0.03'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
  }
  
  .empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    color: var(--neutral-500);
    text-align: center;
    padding: var(--space-xl);
  }
  
  .empty-state-icon {
    width: 100px;
    height: 100px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, var(--primary-100) 0%, var(--secondary-100) 100%);
    border-radius: 50%;
    margin-bottom: var(--space-lg);
    color: var(--primary-700);
    box-shadow: 0 10px 25px rgba(38, 198, 218, 0.2);
    position: relative;
    overflow: hidden;
  }
  
  .empty-state-icon::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(255, 255, 255, 0.2) 0%, transparent 70%);
    animation: rotate 10s linear infinite;
  }
  
  .empty-state h3 {
    font-size: 1.8rem;
    margin-bottom: var(--space-md);
    background: linear-gradient(90deg, var(--primary-700) 0%, var(--secondary-700) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-fill-color: transparent;
  }
  
  .empty-state p {
    font-size: 1.2rem;
    max-width: 500px;
  }
  
  .message-wrapper {
    display: flex;
    width: 100%;
  }
  
  .user-message-wrapper {
    justify-content: flex-end;
  }
  
  .assistant-message-wrapper {
    justify-content: flex-start;
  }
  
  .message {
    max-width: 80%;
    padding: var(--space-md) var(--space-lg);
    border-radius: var(--radius-lg);
    animation: slideUp var(--transition-normal) ease-out;
    position: relative;
    overflow: hidden;
  }
  
  .user-message {
    color: white;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  }
  
  .assistant-message {
    color: var(--neutral-800);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
  }
  
  /* Message shine effect */
  .message::after {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(
      to right,
      rgba(255, 255, 255, 0) 0%,
      rgba(255, 255, 255, 0.1) 50%,
      rgba(255, 255, 255, 0) 100%
    );
    transform: skewX(-25deg);
    transition: all 0.75s ease;
    z-index: 1;
    pointer-events: none;
  }
  
  .message:hover::after {
    left: 100%;
  }
  
  .message-content {
    line-height: 1.6;
    position: relative;
    z-index: 2;
  }
  
  .markdown-content :deep(p) {
    margin-bottom: var(--space-sm);
  }
  
  .markdown-content :deep(p:last-child) {
    margin-bottom: 0;
  }
  
  .markdown-content :deep(code) {
    font-family: var(--font-mono);
    background: rgba(0, 0, 0, 0.05);
    padding: 0.1em 0.3em;
    border-radius: var(--radius-sm);
  }
  
  .markdown-content :deep(pre) {
    background: rgba(0, 0, 0, 0.05);
    padding: var(--space-md);
    border-radius: var(--radius-md);
    overflow-x: auto;
    margin: var(--space-md) 0;
  }
  
  .markdown-content :deep(pre code) {
    background: transparent;
    padding: 0;
  }
  
  .message-timestamp {
    font-size: 0.75rem;
    color: var(--neutral-500);
    margin-top: var(--space-xs);
    text-align: right;
  }
  
  .sources {
    margin-top: var(--space-md);
    padding-top: var(--space-md);
    border-top: 1px solid var(--enhanced-glass-border);
  }
  
  .sources-header {
    display: flex;
    align-items: center;
    gap: var(--space-xs);
    margin-bottom: var(--space-sm);
    color: var(--primary-700);
  }
  
  .sources-header h4 {
    margin-bottom: 0;
    font-size: 0.9rem;
  }
  
  .sources-list {
    list-style: none;
    padding: 0;
    display: flex;
    flex-direction: column;
    gap: var(--space-sm);
  }
  
  .source-item {
    padding: var(--space-sm);
    border-radius: var(--radius-md);
    font-size: 0.85rem;
    transition: transform var(--transition-normal);
  }
  
  .source-item:hover {
    transform: translateY(-2px);
  }
  
  .source-title {
    font-weight: 600;
    margin-bottom: var(--space-xs);
    color: var(--primary-700);
  }
  
  .source-text {
    color: var(--neutral-700);
  }
  
  .chat-input-container {
    display: flex;
    padding: var(--space-md);
    border-top: 1px solid var(--enhanced-glass-border);
    gap: var(--space-sm);
    position: relative;
  }
  
  .chat-input-container::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--primary-400), var(--secondary-400), transparent);
  }
  
  .chat-input {
    flex: 1;
    padding: var(--space-md);
    border: 1px solid var(--enhanced-glass-border);
    border-radius: var(--radius-md);
    background: rgba(255, 255, 255, 0.5);
    resize: none;
    font-family: var(--font-primary);
    font-size: 1rem;
    transition: all var(--transition-fast);
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  }
  
  .chat-input:focus {
    outline: none;
    border-color: var(--primary-400);
    box-shadow: 0 0 0 3px rgba(38, 198, 218, 0.2);
    background: rgba(255, 255, 255, 0.7);
  }
  
  .send-button {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0;
    color: var(--primary-700);
    transition: all var(--transition-normal);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
    position: relative;
    overflow: hidden;
  }
  
  .send-button:hover {
    transform: translateY(-2px);
    background: rgba(255, 255, 255, 0.3);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
  }
  
  .send-button:disabled {
    opacity: 0.7;
    cursor: not-allowed;
    transform: none;
  }
  
  /* Button shine effect */
  .send-button::after {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(
      to right,
      rgba(255, 255, 255, 0) 0%,
      rgba(255, 255, 255, 0.2) 50%,
      rgba(255, 255, 255, 0) 100%
    );
    transform: skewX(-25deg);
    transition: all 0.75s ease;
  }
  
  .send-button:hover::after {
    left: 100%;
  }
  
  .loading-indicator {
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .spinner {
    animation: rotate 2s linear infinite;
    width: 24px;
    height: 24px;
  }
  
  .path {
    stroke: var(--primary-600);
    stroke-linecap: round;
    animation: dash 1.5s ease-in-out infinite;
  }
  
  @keyframes rotate {
    100% {
      transform: rotate(360deg);
    }
  }
  
  @keyframes dash {
    0% {
      stroke-dasharray: 1, 150;
      stroke-dashoffset: 0;
    }
    50% {
      stroke-dasharray: 90, 150;
      stroke-dashoffset: -35;
    }
    100% {
      stroke-dasharray: 90, 150;
      stroke-dashoffset: -124;
    }
  }
  
  @media (max-width: 1200px) {
    .chat-container {
      max-width: 100%;
    }
  }
  
  @media (max-width: 992px) {
    .chat-container {
      height: calc(100vh - 200px);
    }
  }
  
  @media (max-width: 768px) {
    .message {
      max-width: 90%;
    }
    
    .chat-header h2 {
      font-size: 1.8rem;
    }
    
    .chat-header p {
      font-size: 1rem;
    }
  }
  
  @media (max-width: 576px) {
    .chat-container {
      min-height: 500px;
    }
    
    .message {
      max-width: 95%;
    }
    
    .send-button {
      width: 50px;
      height: 50px;
    }
  }
  </style>
  