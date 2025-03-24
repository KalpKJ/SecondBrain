<template>
  <div class="home-view">
    <div class="hero-section glass animate-fadeIn">
      <div class="hero-content">
        <h1 class="hero-title">Your Second Brain</h1>
        <p class="hero-subtitle">Store, organize, and interact with your knowledge using the power of AI</p>
        <div class="hero-actions">
          <router-link to="/chat" class="btn btn-primary">Chat with Your Knowledge</router-link>
          <router-link to="/add" class="btn btn-glass">Add New Knowledge</router-link>
        </div>
      </div>
      <div class="hero-graphic">
        <div class="brain-graphic">
          <div class="brain-circle"></div>
          <div class="brain-connection"></div>
          <div class="brain-node"></div>
          <div class="brain-connection"></div>
          <div class="brain-node"></div>
        </div>
      </div>
    </div>

    <div class="features-section">
      <h2 class="section-title">Unlock Your Knowledge Potential</h2>
      
      <div class="features-grid">
        <div class="feature-card card-glass animate-slideUp">
          <div class="feature-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-2.3zM7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3"></path>
            </svg>
          </div>
          <h3>Capture</h3>
          <p>Save ideas, insights, and information from any source to build your knowledge base.</p>
        </div>
        
        <div class="feature-card card-glass animate-slideUp" style="animation-delay: 0.1s">
          <div class="feature-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="4" y1="9" x2="20" y2="9"></line>
              <line x1="4" y1="15" x2="20" y2="15"></line>
              <line x1="10" y1="3" x2="8" y2="21"></line>
              <line x1="16" y1="3" x2="14" y2="21"></line>
            </svg>
          </div>
          <h3>Organize</h3>
          <p>Automatically categorize and connect your knowledge with semantic understanding.</p>
        </div>
        
        <div class="feature-card card-glass animate-slideUp" style="animation-delay: 0.2s">
          <div class="feature-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
            </svg>
          </div>
          <h3>Distill</h3>
          <p>Extract the essence of your notes and find connections between ideas.</p>
        </div>
        
        <div class="feature-card card-glass animate-slideUp" style="animation-delay: 0.3s">
          <div class="feature-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
            </svg>
          </div>
          <h3>Express</h3>
          <p>Interact with your knowledge through natural language conversations.</p>
        </div>
      </div>
    </div>

    <div class="cta-section glass">
      <h2>Ready to expand your mind?</h2>
      <p>Start adding knowledge to your Second Brain and see how it transforms your thinking.</p>
      <router-link to="/add" class="btn btn-primary">Get Started Now</router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomeView'
}
</script>

<style scoped>
.home-view {
  display: flex;
  flex-direction: column;
  gap: var(--space-2xl);
  width: 100%;
}

.hero-section {
  display: flex;
  align-items: center;
  padding: var(--space-2xl);
  border-radius: var(--radius-lg);
  overflow: hidden;
  position: relative;
  min-height: 500px;
  
}

.hero-content {
  flex: 1;
  z-index: 1;
}

.hero-title {
  font-size: 3.5rem;
  margin-bottom: var(--space-md);
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.hero-subtitle {
  font-size: 1.25rem;
  color: var(--neutral-700);
  margin-bottom: var(--space-xl);
  max-width: 600px;
}

.hero-actions {
  display: flex;
  gap: var(--space-md);
}

.hero-graphic {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
}

.brain-graphic {
  position: relative;
  width: 400px;
  height: 400px;
}

.brain-circle {
  position: absolute;
  width: 350px;
  height: 350px;
  border-radius: 50%;
  background: linear-gradient(135deg, rgba(38, 198, 218, 0.1) 0%, rgba(156, 39, 176, 0.1) 100%);
  border: 2px solid rgba(255, 255, 255, 0.1);
  top: 25px;
  left: 25px;
  animation: pulse 4s infinite ease-in-out;
  box-shadow: 0 0 30px rgba(38, 198, 218, 0.2);
}

.brain-node {
  position: absolute;
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--primary-400) 0%, var(--secondary-400) 100%);
  box-shadow: 0 0 30px rgba(38, 198, 218, 0.4);
}

.brain-node:nth-child(3) {
  top: 50px;
  left: 70px;
  animation: pulse 3s infinite ease-in-out;
}

.brain-node:nth-child(5) {
  bottom: 70px;
  right: 60px;
  animation: pulse 3.5s infinite ease-in-out;
  animation-delay: 0.5s;
}

.brain-connection {
  position: absolute;
  height: 4px;
  background: linear-gradient(90deg, var(--primary-400) 0%, var(--secondary-400) 100%);
  transform-origin: left center;
  box-shadow: 0 0 10px rgba(38, 198, 218, 0.3);
}

.brain-connection:nth-child(2) {
  width: 180px;
  top: 80px;
  left: 100px;
  transform: rotate(30deg);
}

.brain-connection:nth-child(4) {
  width: 220px;
  bottom: 120px;
  left: 100px;
  transform: rotate(-20deg);
}

.section-title {
  text-align: center;
  margin-bottom: var(--space-xl);
  font-size: 2.5rem;
}

.features-section {
  padding: var(--space-xl) 0;
  width: 100%;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: var(--space-lg);
}

.feature-card {
  padding: var(--space-lg);
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  height: 100%;
}

.feature-icon {
  width: 80px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--primary-100) 0%, var(--secondary-100) 100%);
  border-radius: 50%;
  margin-bottom: var(--space-md);
  color: var(--primary-700);
  box-shadow: 0 10px 20px rgba(38, 198, 218, 0.15);
}

.feature-card h3 {
  margin-bottom: var(--space-sm);
  color: var(--primary-700);
  font-size: 1.5rem;
}

.cta-section {
  text-align: center;
  padding: var(--space-2xl);
  border-radius: var(--radius-lg);
  margin-bottom: var(--space-2xl);
  background: var(--enhanced-glass-bg);
  position: relative;
  overflow: hidden;
}

.cta-section::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(38, 198, 218, 0.05) 0%, rgba(156, 39, 176, 0.05) 50%, transparent 70%);
  z-index: -1;
  animation: rotate 20s linear infinite;
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.cta-section h2 {
  margin-bottom: var(--space-md);
  font-size: 2.5rem;
}

.cta-section p {
  margin-bottom: var(--space-lg);
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
  font-size: 1.2rem;
}

@media (max-width: 1200px) {
  .brain-graphic {
    width: 350px;
    height: 350px;
  }
  
  .brain-circle {
    width: 300px;
    height: 300px;
  }
}

@media (max-width: 992px) {
  .hero-section {
    flex-direction: column;
    padding: var(--space-xl);
    text-align: center;
  }
  
  .hero-title {
    font-size: 3rem;
  }
  
  .hero-subtitle {
    margin-left: auto;
    margin-right: auto;
  }
  
  .hero-actions {
    justify-content: center;
  }
  
  .hero-graphic {
    margin-top: var(--space-xl);
  }
  
  .features-grid {
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  }
}

@media (max-width: 576px) {
  .hero-section {
    padding: var(--space-lg);
  }
  
  .hero-title {
    font-size: 2.5rem;
  }
  
  .hero-actions {
    flex-direction: column;
    width: 100%;
    gap: var(--space-md);
  }
  
  .brain-graphic {
    width: 280px;
    height: 280px;
  }
  
  .brain-circle {
    width: 240px;
    height: 240px;
  }
  
  .brain-node {
    width: 60px;
    height: 60px;
  }
  
  .cta-section h2 {
    font-size: 2rem;
  }
  
  .cta-section p {
    font-size: 1rem;
  }
}
</style>
