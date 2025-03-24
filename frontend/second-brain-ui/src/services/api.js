import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://localhost:5000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

export default {
  // Direct API calls (bypassing n8n)
  addKnowledge(content, metadata) {
    return apiClient.post('/knowledge', {
      content,
      metadata
    });
  },

  deleteKnowledge(documentId) {
    return apiClient.delete(`/knowledge/${documentId}`);
  },
  // Add a method to fetch all knowledge
  getAllKnowledge() {
    return apiClient.get('/knowledge');
  },
  
  queryKnowledge(query, filter = null, n_results = 5) {
    return apiClient.post('/query', {
      query,
      filter,
      n_results
    });
  },
  
  suggestConnections(content) {
    return apiClient.post('/suggest', {
      content
    });
  }
};
