<template>
    <div class="manage-view">
      <div class="manage-container glass">
        <div class="manage-header">
          <h2>Manage Your Knowledge</h2>
          <p>View, edit or remove entries from your Second Brain</p>
        </div>
        
        <div v-if="isLoading" class="loading-container">
          <div class="loading-spinner">
            <svg class="spinner" viewBox="0 0 50 50">
              <circle class="path" cx="25" cy="25" r="20" fill="none" stroke-width="5"></circle>
            </svg>
          </div>
          <p>Loading your knowledge...</p>
        </div>
        
        <div v-else-if="knowledge.length === 0" class="empty-state">
          <div class="empty-state-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
              <polyline points="14 2 14 8 20 8"></polyline>
              <line x1="16" y1="13" x2="8" y2="13"></line>
              <line x1="16" y1="17" x2="8" y2="17"></line>
              <polyline points="10 9 9 9 8 9"></polyline>
            </svg>
          </div>
          <h3>No knowledge found</h3>
          <p>Start by adding some knowledge to your Second Brain</p>
        </div>
        
        <div v-else class="knowledge-list">
          <div v-for="item in knowledge" :key="item.id" class="knowledge-item glass">
            <div class="knowledge-content">
              <h3>{{ item.metadata.title || 'Untitled Knowledge' }}</h3>
              <p>{{ truncateText(item.content, 200) }}</p>
              
              <div class="knowledge-meta">
                <div class="knowledge-tags">
                  <span v-for="(tag, tagIndex) in getTags(item.metadata.tags)" :key="tagIndex" class="tag-pill">
                    {{ tag }}
                  </span>
                </div>
                <div class="knowledge-date">
                  {{ formatDate(item.metadata.created_at) }}
                </div>
              </div>
            </div>
            
            <div class="knowledge-actions">
              <button @click="confirmDelete(item)" class="btn-delete btn-glass">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <polyline points="3 6 5 6 21 6"></polyline>
                  <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                  <line x1="10" y1="11" x2="10" y2="17"></line>
                  <line x1="14" y1="11" x2="14" y2="17"></line>
                </svg>
                Delete
              </button>
            </div>
          </div>
        </div>
        
        <!-- Confirmation Modal -->
        <div v-if="showModal" class="delete-modal">
          <div class="modal-content glass">
            <h3>Delete Knowledge</h3>
            <p>Are you sure you want to delete this knowledge? This action cannot be undone.</p>
            
            <div class="modal-actions">
              <button @click="showModal = false" class="btn-cancel btn-glass">Cancel</button>
              <button @click="deleteKnowledge" class="btn-confirm">Delete</button>
            </div>
          </div>
        </div>
        
        <!-- Notification -->
        <div v-if="notification.show" :class="['notification', `notification-${notification.type}`]">
          <div class="notification-content">
            <h4>{{ notification.title }}</h4>
            <p>{{ notification.message }}</p>
          </div>
          <button @click="closeNotification" class="notification-close">×</button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, onMounted } from 'vue';
  import { useBrainStore } from '@/stores/brain';
  
  export default {
    setup() {
      const brainStore = useBrainStore();
      const knowledge = ref([]);
      const isLoading = ref(false);
      const showModal = ref(false);
      const itemToDelete = ref(null);
      const notification = ref({
        show: false,
        type: 'success',
        title: '',
        message: ''
      });
      
      const loadKnowledge = async () => {
        try {
          isLoading.value = true;
          const response = await brainStore.getAllKnowledge();
          knowledge.value = response;
        } catch (error) {
          console.error('Error loading knowledge:', error);
          showNotification('error', 'Error', 'Failed to load your knowledge');
        } finally {
          isLoading.value = false;
        }
      };
      
      const confirmDelete = (item) => {
        itemToDelete.value = item;
        showModal.value = true;
      };
      
      const deleteKnowledge = async () => {
        if (!itemToDelete.value) return;
        
        try {
          isLoading.value = true;
          await brainStore.deleteKnowledge(itemToDelete.value.id);
          
          // Remove from local list
          knowledge.value = knowledge.value.filter(item => item.id !== itemToDelete.value.id);
          
          showNotification('success', 'Knowledge Deleted', 'Knowledge has been successfully removed');
        } catch (error) {
          console.error('Error deleting knowledge:', error);
          showNotification('error', 'Error', 'Failed to delete knowledge');
        } finally {
          isLoading.value = false;
          showModal.value = false;
          itemToDelete.value = null;
        }
      };
      
      const showNotification = (type, title, message) => {
        notification.value = {
          show: true,
          type,
          title,
          message
        };
        
        setTimeout(() => {
          closeNotification();
        }, 5000);
      };
      
      const closeNotification = () => {
        notification.value.show = false;
      };
      
      const truncateText = (text, maxLength) => {
        if (!text) return '';
        if (text.length <= maxLength) return text;
        return text.substring(0, maxLength) + '...';
      };
      
      const formatDate = (dateString) => {
        if (!dateString) return '';
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', { 
          year: 'numeric', 
          month: 'short', 
          day: 'numeric' 
        });
      };
      
      const getTags = (tagsString) => {
        if (!tagsString) return [];
        return tagsString.split(',').map(tag => tag.trim()).filter(tag => tag);
      };
      
      onMounted(() => {
        loadKnowledge();
      });
      
      return {
        knowledge,
        isLoading,
        showModal,
        notification,
        confirmDelete,
        deleteKnowledge,
        closeNotification,
        truncateText,
        formatDate,
        getTags
      };
    }
  };
  </script>
  
  <style scoped>
.manage-view {
  display: flex;
  justify-content: center;
  padding: var(--space-md) 0;
  width: 100%;
  box-sizing: border-box;
}

.manage-container {
  width: 100%;
  max-width: 1200px;
  display: flex;
  flex-direction: column;
  border-radius: var(--radius-lg);
  overflow: hidden;
  position: relative;
  min-height: 600px;
}

/* Subtle animated gradient background */
.manage-container::before {
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

.manage-header {
  padding: var(--space-lg);
  text-align: center;
  border-bottom: 1px solid var(--enhanced-glass-border);
  position: relative;
  overflow: hidden;
}

.manage-header::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--primary-400), var(--secondary-400), transparent);
}

.manage-header h2 {
  margin-bottom: var(--space-xs);
  background: linear-gradient(90deg, var(--primary-600) 0%, var(--secondary-600) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-fill-color: transparent;
  font-size: 2rem;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.manage-header p {
  color: var(--neutral-600);
  margin-bottom: 0;
  font-size: 1.1rem;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 400px;
  color: var(--neutral-600);
}

.loading-spinner {
  margin-bottom: var(--space-md);
}

.spinner {
  animation: rotate 2s linear infinite;
  width: 40px;
  height: 40px;
}

.path {
  stroke: var(--primary-600);
  stroke-linecap: round;
  animation: dash 1.5s ease-in-out infinite;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 400px;
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

.knowledge-list {
  padding: var(--space-lg);
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
  overflow-y: auto;
}

.knowledge-item {
  padding: var(--space-md);
  border-radius: var(--radius-md);
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: var(--space-md);
  transition: transform var(--transition-normal);
}

.knowledge-item:hover {
  transform: translateY(-3px);
}

.knowledge-content {
  flex: 1;
}

.knowledge-content h3 {
  margin-bottom: var(--space-xs);
  color: var(--primary-700);
  font-size: 1.2rem;
}

.knowledge-content p {
  color: var(--neutral-700);
  margin-bottom: var(--space-sm);
  font-size: 0.95rem;
  line-height: 1.5;
}

.knowledge-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: var(--space-sm);
}

.knowledge-tags {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-xs);
}

.tag-pill {
  padding: var(--space-xs) var(--space-sm);
  background: linear-gradient(135deg, var(--primary-100) 0%, var(--secondary-100) 100%);
  border-radius: var(--radius-full);
  font-size: 0.8rem;
  color: var(--primary-800);
}

.knowledge-date {
  font-size: 0.85rem;
  color: var(--neutral-500);
}

.knowledge-actions {
  display: flex;
  gap: var(--space-sm);
}

.btn-delete {
  display: flex;
  align-items: center;
  gap: var(--space-xs);
  padding: var(--space-xs) var(--space-sm);
  color: var(--error);
  border-radius: var(--radius-md);
  font-size: 0.9rem;
  transition: all var(--transition-fast);
}

.btn-delete:hover {
  background: rgba(244, 67, 54, 0.1);
}

.delete-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn var(--transition-fast) ease-out;
}

.modal-content {
  width: 90%;
  max-width: 500px;
  padding: var(--space-lg);
  border-radius: var(--radius-lg);
  text-align: center;
}

.modal-content h3 {
  margin-bottom: var(--space-md);
  color: var(--primary-700);
}

.modal-content p {
  margin-bottom: var(--space-lg);
  color: var(--neutral-700);
}

.modal-actions {
  display: flex;
  justify-content: center;
  gap: var(--space-md);
}

.btn-cancel {
  padding: var(--space-sm) var(--space-md);
  border-radius: var(--radius-md);
  font-weight: 500;
  transition: all var(--transition-fast);
}

.btn-confirm {
  padding: var(--space-sm) var(--space-md);
  background: var(--error);
  color: white;
  border: none;
  border-radius: var(--radius-md);
  font-weight: 500;
  transition: all var(--transition-fast);
}

.btn-confirm:hover {
  background: var(--error-dark);
  transform: translateY(-2px);
}

.notification {
  position: fixed;
  bottom: 20px;
  right: 20px;
  display: flex;
  align-items: center;
  padding: var(--space-md);
  border-radius: var(--radius-md);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  animation: slideUp var(--transition-normal) ease-out;
  z-index: 1000;
  background: white;
}

.notification-success {
  border-left: 4px solid var(--success);
}

.notification-error {
  border-left: 4px solid var(--error);
}

.notification-content {
  margin-right: var(--space-md);
}

.notification-content h4 {
  margin-bottom: var(--space-xs);
  font-size: 1.1rem;
}

.notification-content p {
  margin-bottom: 0;
  font-size: 0.9rem;
  color: var(--neutral-600);
}

.notification-close {
  background: none;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  color: var(--neutral-500);
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

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideUp {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

@media (max-width: 1200px) {
  .manage-container {
    max-width: 100%;
  }
}

@media (max-width: 768px) {
  .knowledge-item {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .knowledge-actions {
    align-self: flex-end;
  }
  
  .manage-header h2 {
    font-size: 1.8rem;
  }
  
  .manage-header p {
    font-size: 1rem;
  }
}

@media (max-width: 576px) {
  .modal-content {
    width: 95%;
  }
  
  .modal-actions {
    flex-direction: column;
    gap: var(--space-sm);
  }
  
  .notification {
    left: 20px;
    right: 20px;
  }
}
</style>