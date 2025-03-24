<template>
  <div class="app-container">
    <header class="app-header glass">
      <div class="container flex justify-between items-center">
        <div class="logo">
          <h1>Second Brain</h1>
        </div>
        <nav class="main-nav">
          <router-link to="/" class="nav-link">Home</router-link>
          <router-link to="/chat" class="nav-link">Chat</router-link>
          <router-link to="/add" class="nav-link">Add Knowledge</router-link>
          <router-link to="/manage" class="nav-link">Manage</router-link>
        </nav>
      </div>
    </header>

    <main class="app-main">
      <div class="container">
        <router-view />
      </div>
    </main>

    <footer class="app-footer glass">
      <div class="container">
        <p>&copy; {{ new Date().getFullYear() }} Second Brain - Your Personal Knowledge Assistant</p>
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
@import './assets/modern-theme.css';

/* Import fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@400;500;600;700&family=JetBrains+Mono&display=swap');

.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  position: relative;
  overflow: hidden;
  z-index: 2;
}

/* Decorative background elements */
.app-container::before {
  content: '';
  position: absolute;
  top: -10%;
  right: -10%;
  width: 60%;
  height: 60%;
  background: radial-gradient(circle, rgba(38, 198, 218, 0.1) 0%, rgba(38, 198, 218, 0) 70%);
  z-index: -1;
  border-radius: 50%;
}

.app-container::after {
  content: '';
  position: absolute;
  bottom: -10%;
  left: -10%;
  width: 70%;
  height: 70%;
  background: radial-gradient(circle, rgba(156, 39, 176, 0.1) 0%, rgba(156, 39, 176, 0) 70%);
  z-index: -1;
  border-radius: 50%;
}

.app-header {
  padding: var(--space-md) 0;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: var(--enhanced-glass-shadow);
  height: var(--header-height);
  width: 100%;
}

.logo h1 {
  margin-bottom: 0;
  font-size: 1.8rem;
}

.main-nav {
  display: flex;
  gap: var(--space-lg);
}

.nav-link {
  color: var(--neutral-800);
  font-weight: 500;
  padding: var(--space-sm) var(--space-md);
  border-radius: var(--radius-md);
  transition: all var(--transition-normal);
  position: relative;
}

.nav-link:hover {
  color: var(--primary-700);
  background: rgba(255, 255, 255, 0.2);
}

.nav-link.router-link-active {
  color: var(--primary-700);
  font-weight: 600;
}

.nav-link.router-link-active::after {
  content: '';
  position: absolute;
  bottom: -5px;
  left: 50%;
  transform: translateX(-50%);
  width: 20px;
  height: 3px;
  background: linear-gradient(90deg, var(--primary-500) 0%, var(--secondary-500) 100%);
  border-radius: var(--radius-full);
}

.app-main {
  flex: 1;
  padding: var(--space-xl) 0;
  width: 100%;
  box-sizing: border-box;
}

.app-footer {
  padding: var(--space-md) 0;
  text-align: center;
  color: var(--neutral-600);
  font-size: 0.9rem;
  width: 100%;
}

/* Responsive styles */
@media (max-width: 992px) {
  .app-header .container {
    flex-direction: column;
    gap: var(--space-md);
    padding-top: var(--space-sm);
    padding-bottom: var(--space-sm);
  }
  
  .app-header {
    height: auto;
  }
  
  .main-nav {
    width: 100%;
    justify-content: center;
  }
}

@media (max-width: 576px) {
  .main-nav {
    flex-direction: column;
    align-items: center;
    gap: var(--space-sm);
  }
  
  .nav-link {
    width: 100%;
    text-align: center;
  }
}
</style>