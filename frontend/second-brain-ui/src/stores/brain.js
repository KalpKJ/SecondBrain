import { defineStore } from 'pinia';
import api from '@/services/api';

export const useBrainStore = defineStore('brain', {
  state: () => ({
    conversations: [],
    currentConversation: null,
    isLoading: false,
    error: null
  }),
  
  actions: {
    async addKnowledge(content, metadata) {
        this.isLoading = true;
        this.error = null;
        
        try {
          // Convert any array values in metadata to strings
          const processedMetadata = {...metadata};
          if (processedMetadata.tags && Array.isArray(processedMetadata.tags)) {
            processedMetadata.tags = processedMetadata.tags.join(',');
          }
          
          // Process any other potential array fields
          Object.keys(processedMetadata).forEach(key => {
            if (Array.isArray(processedMetadata[key])) {
              processedMetadata[key] = processedMetadata[key].join(',');
            }
          });
          
          const response = await api.addKnowledge(content, processedMetadata);
          return response.data;
        } catch (error) {
          this.error = error.message || 'Failed to add knowledge';
          throw error;
        } finally {
          this.isLoading = false;
        }
      },
    
    async queryKnowledge(query, filter = null, n_results = 5) {
      this.isLoading = true;
      this.error = null;
      
      try {
        const response = await api.queryKnowledge(query, filter, n_results);
        
        // Add to conversation history
        if (!this.currentConversation) {
          this.currentConversation = {
            id: Date.now(),
            messages: []
          };
          this.conversations.push(this.currentConversation);
        }
        
        this.currentConversation.messages.push({
          type: 'user',
          content: query,
          timestamp: new Date().toISOString()
        });
        
        this.currentConversation.messages.push({
          type: 'assistant',
          content: response.data.response,
          sources: response.data.sources,
          timestamp: new Date().toISOString()
        });
        
        return response.data;
      } catch (error) {
        this.error = error.message || 'Failed to query knowledge';
        throw error;
      } finally {
        this.isLoading = false;
      }
    },
    // Add to the actions section
async deleteKnowledge(documentId) {
  this.isLoading = true;
  this.error = null;
  
  try {
    const response = await api.deleteKnowledge(documentId);
    return response.data;
  } catch (error) {
    this.error = error.message || 'Failed to delete knowledge';
    throw error;
  } finally {
    this.isLoading = false;
  }
},

async getAllKnowledge() {
  this.isLoading = true;
  this.error = null;
  
  try {
    const response = await api.getAllKnowledge();
    return response.data;
  } catch (error) {
    this.error = error.message || 'Failed to fetch knowledge';
    throw error;
  } finally {
    this.isLoading = false;
  }
},
    
    async suggestConnections(content) {
      this.isLoading = true;
      this.error = null;
      
      try {
        const response = await api.suggestConnections(content);
        return response.data.suggestions;
      } catch (error) {
        this.error = error.message || 'Failed to suggest connections';
        throw error;
      } finally {
        this.isLoading = false;
      }
    },
    
    startNewConversation() {
      this.currentConversation = {
        id: Date.now(),
        messages: []
      };
      this.conversations.push(this.currentConversation);
    }
  }
});
