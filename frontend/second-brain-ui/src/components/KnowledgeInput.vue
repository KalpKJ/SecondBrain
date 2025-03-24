<template>
    <div class="knowledge-input">
      <h2>Add to Your Second Brain</h2>
      
      <div class="form-group">
        <label for="title">Title</label>
        <input 
          type="text" 
          id="title" 
          v-model="title" 
          placeholder="Give your knowledge a title"
        />
      </div>
      
      <div class="form-group">
        <label for="content">Content</label>
        <textarea 
          id="content" 
          v-model="content" 
          placeholder="Enter the knowledge you want to save..."
          rows="10"
        ></textarea>
      </div>
      
      <div class="form-group">
        <label for="tags">Tags (comma separated)</label>
        <input 
          type="text" 
          id="tags" 
          v-model="tagsInput" 
          placeholder="productivity, notes, ideas"
        />
      </div>
      
      <div class="form-group">
        <label for="source">Source (optional)</label>
        <input 
          type="text" 
          id="source" 
          v-model="source" 
          placeholder="Book, website, conversation, etc."
        />
      </div>
      
      <div v-if="suggestions.length > 0" class="suggestions">
        <h3>Suggested Connections</h3>
        <ul>
          <li v-for="(suggestion, index) in suggestions" :key="index">
            <strong>{{ suggestion.entity }}</strong>: {{ suggestion.reason }}
          </li>
        </ul>
      </div>
      
      <div class="actions">
        <button @click="resetForm" class="secondary">Reset</button>
        <button @click="saveKnowledge" :disabled="isLoading || !isValid">
          <span v-if="isLoading">Saving...</span>
          <span v-else>Save to Second Brain</span>
        </button>
      </div>
      
      <div v-if="error" class="error-message">
        {{ error }}
      </div>
      
      <div v-if="success" class="success-message">
        {{ success }}
      </div>
    </div>
  </template>
  
  <script>
  import { ref, computed, watch } from 'vue';
  import { useBrainStore } from '@/stores/brain';
  
  export default {
    setup() {
      const brainStore = useBrainStore();
      
      const title = ref('');
      const content = ref('');
      const tagsInput = ref('');
      const source = ref('');
      const error = ref('');
      const success = ref('');
      const suggestions = ref([]);
      
      const isLoading = computed(() => brainStore.isLoading);
      
      const tags = computed(() => {
        return tagsInput.value
          .split(',')
          .map(tag => tag.trim())
          .filter(tag => tag.length > 0);
      });
      
      const isValid = computed(() => {
        return title.value.trim().length > 0 && content.value.trim().length > 0;
      });
      
      // Debounced function to get suggestions
      let suggestionTimeout = null;
      const getSuggestions = () => {
        if (suggestionTimeout) clearTimeout(suggestionTimeout);
        
        if (content.value.trim().length < 50) return;
        
        suggestionTimeout = setTimeout(async () => {
          try {
            const result = await brainStore.suggestConnections(content.value);
            suggestions.value = result;
          } catch (err) {
            console.error('Error getting suggestions:', err);
          }
        }, 1000);
      };
      
      // Watch for content changes to update suggestions
      watch(content, getSuggestions);
      
      const saveKnowledge = async () => {
        if (!isValid.value) return;
        
        error.value = '';
        success.value = '';
        
        try {
          const metadata = {
            title: title.value,
            tags: tags.value,
            source: source.value
          };
          
          const result = await brainStore.addKnowledge(content.value, metadata);
          success.value = 'Successfully added to your Second Brain!';
          resetForm();
        } catch (err) {
          error.value = 'Failed to save knowledge: ' + (err.message || 'Unknown error');
        }
      };
      
      const resetForm = () => {
        title.value = '';
        content.value = '';
        tagsInput.value = '';
        source.value = '';
        suggestions.value = [];
        error.value = '';
      };
      
      return {
        title,
        content,
        tagsInput,
        source,
        error,
        success,
        suggestions,
        isLoading,
        isValid,
        saveKnowledge,
        resetForm
      };
    }
  };
  </script>
  
  <style scoped>
  .knowledge-input {
    max-width: 800px;
    margin: 0 auto;
    padding: 1rem;
  }
  
  .form-group {
    margin-bottom: 1.5rem;
  }
  
  label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: bold;
  }
  
  input, textarea {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid #ddd;
    border-radius: 0.5rem;
    font-family: inherit;
  }
  
  textarea {
    resize: vertical;
  }
  
  .actions {
    display: flex;
    gap: 1rem;
    justify-content: flex-end;
    margin-top: 1.5rem;
  }
  
  button {
    padding: 0.75rem 1.5rem;
    background-color: #2196f3;
    color: white;
    border: none;
    border-radius: 0.5rem;
    cursor: pointer;
    font-weight: bold;
  }
  
  button.secondary {
    background-color: #f5f5f5;
    color: #333;
  }
  
  button:disabled {
    background-color: #b0bec5;
    cursor: not-allowed;
  }
  
  .error-message {
    margin-top: 1rem;
    padding: 0.75rem;
    background-color: #ffebee;
    color: #c62828;
    border-radius: 0.5rem;
  }
  
  .success-message {
    margin-top: 1rem;
    padding: 0.75rem;
    background-color: #e8f5e9;
    color: #2e7d32;
    border-radius: 0.5rem;
  }
  
  .suggestions {
    margin-top: 1.5rem;
    padding: 1rem;
    background-color: #f5f5f5;
    border-radius: 0.5rem;
  }
  
  .suggestions h3 {
    margin-top: 0;
    margin-bottom: 0.75rem;
  }
  
  .suggestions ul {
    padding-left: 1.5rem;
  }
  
  .suggestions li {
    margin-bottom: 0.5rem;
  }
  </style>
  