/**
 * Splash screen functionality for the Swaccha Andhra Dashboard PWA
 * This script handles the PWA splash screen during launch
 */

document.addEventListener('DOMContentLoaded', function() {
    // Check if running as installed PWA
    const isInStandaloneMode = () => 
      (window.matchMedia('(display-mode: standalone)').matches) || 
      (window.navigator.standalone) || 
      document.referrer.includes('android-app://');
  
    // Only show splash screen when running as installed app
    if (isInStandaloneMode()) {
      // Create the splash screen element
      const splashScreen = document.createElement('div');
      splashScreen.className = 'pwa-splash-screen';
      splashScreen.innerHTML = `
        <img src="/assets/img/logo-white.png" alt="Swaccha Andhra" class="pwa-splash-logo">
        <h1 class="pwa-splash-title">Swaccha Andhra</h1>
        <p class="pwa-splash-subtitle">Waste Management Dashboard</p>
        <div class="pwa-splash-loader"></div>
      `;
      
      // Add splash screen to the document
      document.body.appendChild(splashScreen);
      
      // Hide splash screen after app loads (with minimum display time)
      const minDisplayTime = 1500; // 1.5 seconds minimum display time
      const startTime = Date.now();
      
      window.addEventListener('load', () => {
        const elapsedTime = Date.now() - startTime;
        const remainingTime = Math.max(0, minDisplayTime - elapsedTime);
        
        // Ensure splash screen displays for at least the minimum time
        setTimeout(() => {
          splashScreen.classList.add('hidden');
          
          // Remove from DOM after transition completes
          setTimeout(() => {
            splashScreen.remove();
          }, 500);
        }, remainingTime);
      });
    }
    
    // Add offline indicator to header if needed
    const updateOfflineIndicator = () => {
      const headerActions = document.querySelector('.header-actions');
      const existingIndicator = document.querySelector('.offline-indicator');
      
      if (!navigator.onLine && !existingIndicator && headerActions) {
        const indicator = document.createElement('div');
        indicator.className = 'offline-indicator';
        indicator.innerHTML = '<i class="fas fa-wifi-slash"></i> Offline';
        headerActions.prepend(indicator);
      } else if (navigator.onLine && existingIndicator) {
        existingIndicator.remove();
      }
    };
    
    // Check offline status on load
    updateOfflineIndicator();
    
    // Update indicator when online/offline status changes
    window.addEventListener('online', updateOfflineIndicator);
    window.addEventListener('offline', updateOfflineIndicator);
  });