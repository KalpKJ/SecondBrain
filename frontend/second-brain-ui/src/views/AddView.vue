<template>
  <div class="add-view">
    <div class="add-container glass">
      <div class="add-header">
        <h2>Add to Your Second Brain</h2>
        <p>Capture new knowledge and insights to expand your personal knowledge base</p>
      </div>

      <div class="add-form">
        <div class="form-group">
          <label for="title">Title</label>
          <input id="title" v-model="title" placeholder="Give your knowledge a title..." class="source-input" />
        </div>
        <div class="form-group">
          <label for="content">Knowledge Content</label>
          <textarea id="content" v-model="content" placeholder="Enter your knowledge, insights, or information here..."
            rows="8" class="content-input"></textarea>
        </div>

        <div class="form-group">
          <label for="tags">Tags</label>
          <div class="tags-input-container glass">
            <div class="tags-list">
              <div v-for="(tag, index) in tags" :key="index" class="tag-pill">
                {{ tag }}
                <button @click="removeTag(index)" class="tag-remove">×</button>
              </div>
              <input type="text" v-model="tagInput" @keydown.enter.prevent="addTag" @keydown.tab.prevent="addTag"
                @keydown.comma.prevent="addTag" placeholder="Add tags..." class="tag-input" />
            </div>
          </div>
        </div>

        <div class="form-group">
          <label for="source">Source (Optional)</label>
          <input type="text" id="source" v-model="source" placeholder="Book, website, article, etc."
            class="source-input" />
        </div>

        <div v-if="suggestedConnections.length > 0" class="connections-section glass">
          <h3>Suggested Connections</h3>
          <p>Your Second Brain found these related pieces of knowledge:</p>

          <div class="connections-list">
            <div v-for="(connection, index) in suggestedConnections" :key="index" class="connection-item card-glass">
              <div class="connection-content">
                <h4>{{ connection.title || 'Related Knowledge' }}</h4>
                <p>{{ truncateText(connection.content, 150) }}</p>
              </div>
              <div class="connection-tags">
                <div v-for="(tag, tagIndex) in connection.tags" :key="tagIndex" class="connection-tag">
                  {{ tag }}
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="form-actions">
          <button @click="resetForm" class="btn btn-glass">Reset</button>
          <button @click="saveKnowledge" :disabled="isLoading || !content" class="btn btn-primary">
            <span v-if="isLoading" class="loading-indicator">
              <svg class="spinner" viewBox="0 0 50 50">
                <circle class="path" cx="25" cy="25" r="20" fill="none" stroke-width="5"></circle>
              </svg>
            </span>
            <span v-else>Save to Second Brain</span>
          </button>
        </div>
      </div>

      <div v-if="notification.show" :class="['notification', `notification-${notification.type}`, 'glass']">
        <div class="notification-icon">
          <svg v-if="notification.type === 'success'" xmlns="http://www.w3.org/2000/svg" width="24" height="24"
            viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
            stroke-linejoin="round">
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
            <polyline points="22 4 12 14.01 9 11.01"></polyline>
          </svg>
          <svg v-else xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
            stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="8" x2="12" y2="12"></line>
            <line x1="12" y1="16" x2="12.01" y2="16"></line>
          </svg>
        </div>
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
import { ref, watch } from 'vue';
import { useBrainStore } from '@/stores/brain';

export default {
  setup() {
    const brainStore = useBrainStore();
    const title = ref('');
    const content = ref('');
    const tagInput = ref('');
    const tags = ref([]);
    const source = ref('');
    const suggestedConnections = ref([]);
    const isLoading = ref(false);
    const notification = ref({
      show: false,
      type: 'success',
      title: '',
      message: ''
    });

    // Debounced function to get connection suggestions
    let suggestionTimeout = null;
    const getSuggestions = () => {
      if (suggestionTimeout) clearTimeout(suggestionTimeout);

      if (content.value.length < 50) {
        suggestedConnections.value = [];
        return;
      }

      suggestionTimeout = setTimeout(async () => {
        try {
          isLoading.value = true;
          const connections = await brainStore.suggestConnections(content.value);
          suggestedConnections.value = connections;
        } catch (error) {
          console.error('Error getting suggestions:', error);
        } finally {
          isLoading.value = false;
        }
      }, 1000);
    };

    // Watch for content changes to update suggestions
    watch(content, () => {
      getSuggestions();
    });

    const addTag = () => {
      const tag = tagInput.value.trim();
      if (tag && !tags.value.includes(tag)) {
        tags.value.push(tag);
      }
      tagInput.value = '';
    };

    const removeTag = (index) => {
      tags.value.splice(index, 1);
    };

    const saveKnowledge = async () => {
      if (!content.value.trim()) return;

      try {
        isLoading.value = true;

        const metadata = {
          title: title.value,
          source: source.value,
          tags: tags.value,
          created_at: new Date().toISOString()
        };

        await brainStore.addKnowledge(content.value, metadata);

        showNotification(
          'success',
          'Knowledge Saved!',
          'Your knowledge has been successfully added to your Second Brain.'
        );

        resetForm();
      } catch (error) {
        console.error('Error saving knowledge:', error);
        showNotification(
          'error',
          'Error Saving Knowledge',
          'There was a problem saving your knowledge. Please try again.'
        );
      } finally {
        isLoading.value = false;
      }
    };

    const resetForm = () => {
      title.value = '';
      content.value = '';
      tags.value = [];
      tagInput.value = '';
      source.value = '';
      suggestedConnections.value = [];
    };

    const showNotification = (type, title, message) => {
      notification.value = {
        show: true,
        type,
        title,
        message
      };

      // Auto-hide notification after 5 seconds
      setTimeout(() => {
        closeNotification();
      }, 5000);
    };

    const closeNotification = () => {
      notification.value.show = false;
    };

    const truncateText = (text, maxLength) => {
      if (text.length <= maxLength) return text;
      return text.substring(0, maxLength) + '...';
    };

    return {
      title,
      content,
      tagInput,
      tags,
      source,
      suggestedConnections,
      isLoading,
      notification,
      addTag,
      removeTag,
      saveKnowledge,
      resetForm,
      closeNotification,
      truncateText
    };
  }
};
</script>

<style scoped>
.add-view {
  display: flex;
  justify-content: center;
  padding: var(--space-md) 0;
  width: 100%;
}

.add-container {
  width: 100%;
  max-width: 1200px;
  display: flex;
  flex-direction: column;
  border-radius: var(--radius-lg);
  overflow: hidden;
  position: relative;
}

/* Subtle animated gradient background */
.add-container::before {
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
  0% {
    background-position: 0% 50%;
  }

  50% {
    background-position: 100% 50%;
  }

  100% {
    background-position: 0% 50%;
  }
}

.add-header {
  padding: var(--space-lg);
  text-align: center;
  border-bottom: 1px solid var(--enhanced-glass-border);
  position: relative;
  overflow: hidden;
}

.add-header::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--primary-400), var(--secondary-400), transparent);
}

.add-header h2 {
  margin-bottom: var(--space-xs);
  background: linear-gradient(90deg, var(--primary-600) 0%, var(--secondary-600) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-fill-color: transparent;
  font-size: 2rem;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.add-header p {
  color: var(--neutral-600);
  margin-bottom: 0;
  font-size: 1.1rem;
}

.add-form {
  padding: var(--space-lg);
  display: flex;
  flex-direction: column;
  gap: var(--space-lg);
}

.content-input,
.source-input {
  width: 100%;
  padding: var(--space-md);
  border: 1px solid var(--enhanced-glass-border);
  border-radius: var(--radius-md);
  background: rgba(255, 255, 255, 0.5);
  font-family: var(--font-primary);
  font-size: 1rem;
  transition: all var(--transition-fast);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.content-input:focus,
.source-input:focus {
  outline: none;
  border-color: var(--primary-400);
  box-shadow: 0 0 0 3px rgba(38, 198, 218, 0.2);
  background: rgba(255, 255, 255, 0.7);
}

.content-input {
  resize: vertical;
  min-height: 200px;
}

.tags-input-container {
  padding: var(--space-sm);
  border-radius: var(--radius-md);
  background: rgba(255, 255, 255, 0.5);
  transition: all var(--transition-fast);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.tags-input-container:focus-within {
  box-shadow: 0 0 0 3px rgba(38, 198, 218, 0.2);
  background: rgba(255, 255, 255, 0.7);
}

.tags-list {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-sm);
  align-items: center;
}

.tag-pill {
  display: flex;
  align-items: center;
  gap: var(--space-xs);
  padding: var(--space-xs) var(--space-sm);
  background: linear-gradient(135deg, var(--primary-100) 0%, var(--secondary-100) 100%);
  border-radius: var(--radius-full);
  font-size: 0.9rem;
  font-weight: 500;
  color: var(--primary-800);
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  transition: all var(--transition-fast);
  animation: slideUp var(--transition-normal) ease-out;
}

.tag-pill:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.tag-remove {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.2rem;
  line-height: 1;
  color: var(--primary-700);
  padding: 0 2px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.tag-input {
  flex: 1;
  min-width: 120px;
  border: none;
  background: transparent;
  padding: var(--space-xs) var(--space-sm);
  font-family: var(--font-primary);
  font-size: 0.9rem;
}

.tag-input:focus {
  outline: none;
}

.connections-section {
  padding: var(--space-lg);
  border-radius: var(--radius-lg);
  animation: fadeIn var(--transition-normal) ease-in-out;
}

.connections-section h3 {
  margin-bottom: var(--space-sm);
  color: var(--primary-700);
}

.connections-section p {
  margin-bottom: var(--space-md);
  color: var(--neutral-600);
}

.connections-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
}

.connection-item {
  padding: var(--space-md);
  border-radius: var(--radius-md);
  transition: transform var(--transition-normal), box-shadow var(--transition-normal);
  animation: slideUp var(--transition-normal) ease-out;
}

.connection-item:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.05);
}

.connection-content h4 {
  margin-bottom: var(--space-xs);
  color: var(--primary-700);
}

.connection-content p {
  margin-bottom: var(--space-sm);
  color: var(--neutral-700);
  font-size: 0.95rem;
}

.connection-tags {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-xs);
}

.connection-tag {
  padding: var(--space-xs) var(--space-sm);
  background: linear-gradient(135deg, var(--primary-100) 0%, var(--secondary-100) 100%);
  border-radius: var(--radius-full);
  font-size: 0.8rem;
  color: var(--primary-800);
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--space-md);
  margin-top: var(--space-md);
}

.loading-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
}

.spinner {
  animation: rotate 2s linear infinite;
  width: 20px;
  height: 20px;
  margin-right: var(--space-xs);
}

.path {
  stroke: white;
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

.notification {
  position: fixed;
  bottom: 20px;
  right: 20px;
  display: flex;
  align-items: flex-start;
  padding: var(--space-md);
  border-radius: var(--radius-md);
  max-width: 400px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  animation: slideUp var(--transition-normal) ease-out;
  z-index: 1000;
}

.notification-success {
  border-left: 4px solid var(--success);
}

.notification-error {
  border-left: 4px solid var(--error);
}

.notification-icon {
  margin-right: var(--space-md);
  display: flex;
  align-items: center;
  justify-content: center;
}

.notification-success .notification-icon {
  color: var(--success);
}

.notification-error .notification-icon {
  color: var(--error);
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
  margin-left: var(--space-md);
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

@media (max-width: 1200px) {
  .add-container {
    max-width: 100%;
  }
}

@media (max-width: 768px) {
  .add-header h2 {
    font-size: 1.8rem;
  }

  .add-header p {
    font-size: 1rem;
  }

  .form-actions {
    flex-direction: column;
  }

  .form-actions button {
    width: 100%;
  }

  .notification {
    max-width: 90%;
    left: 5%;
    right: 5%;
  }
}

@media (max-width: 576px) {
  .add-form {
    padding: var(--space-md);
  }
}
</style>