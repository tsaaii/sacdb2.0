// Register the service worker for Swaccha Andhra Dashboard PWA
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
      navigator.serviceWorker.register('/service-worker.js')
        .then(function(registration) {
          console.log('ServiceWorker registration successful with scope: ', registration.scope);
          
          // Check for updates to the Service Worker
          registration.addEventListener('updatefound', () => {
            const newWorker = registration.installing;
            
            newWorker.addEventListener('statechange', () => {
              if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                showUpdateNotification();
              }
            });
          });
        })
        .catch(function(err) {
          console.log('ServiceWorker registration failed: ', err);
        });
    });
    
    // Listen for controller change to refresh the page
    let refreshing = false;
    navigator.serviceWorker.addEventListener('controllerchange', () => {
      if (!refreshing) {
        refreshing = true;
        window.location.reload();
      }
    });
  }
  
  // Function to show update notification
  function showUpdateNotification() {
    const notification = document.createElement('div');
    notification.className = 'pwa-update-notification';
    notification.innerHTML = `
      <div class="pwa-update-content">
        <div class="pwa-update-icon">
          <i class="fas fa-sync-alt"></i>
        </div>
        <div class="pwa-update-message">
          <p>A new version of this app is available.</p>
        </div>
        <button class="pwa-update-button">Update Now</button>
      </div>
    `;
    
    document.body.appendChild(notification);
    
    // Handle update click
    const updateButton = notification.querySelector('.pwa-update-button');
    updateButton.addEventListener('click', () => {
      if (navigator.serviceWorker.controller) {
        // Skip waiting to activate the new service worker
        navigator.serviceWorker.controller.postMessage({ action: 'skipWaiting' });
        
        // Remove the notification
        notification.remove();
      }
    });
  }
  
  // Check if the app is installed or can be installed
  window.addEventListener('load', () => {
    let deferredPrompt;
    const installContainer = document.getElementById('install-container');
    const installButton = document.getElementById('install-button');
    
    // Hide the install button initially
    if (installContainer) {
      installContainer.style.display = 'none';
    }
    
    // Listen for the beforeinstallprompt event
    window.addEventListener('beforeinstallprompt', (e) => {
      // Prevent Chrome 67 and earlier from automatically showing the prompt
      e.preventDefault();
      
      // Stash the event so it can be triggered later
      deferredPrompt = e;
      
      // Show the install button if it exists
      if (installContainer) {
        installContainer.style.display = 'block';
        
        // Handle install button click
        installButton.addEventListener('click', () => {
          // Show the install prompt
          deferredPrompt.prompt();
          
          // Wait for the user to respond to the prompt
          deferredPrompt.userChoice.then((choiceResult) => {
            if (choiceResult.outcome === 'accepted') {
              console.log('User accepted the install prompt');
              // Hide the button after installation
              installContainer.style.display = 'none';
            } else {
              console.log('User dismissed the install prompt');
            }
            
            // Clear the deferredPrompt variable
            deferredPrompt = null;
          });
        });
      }
    });
    
    // Handle the appinstalled event
    window.addEventListener('appinstalled', (e) => {
      console.log('Application was installed');
      // Hide the install button if it exists
      if (installContainer) {
        installContainer.style.display = 'none';
      }
    });
  });
  
  // Handle online/offline status changes
  window.addEventListener('online', () => {
    showConnectivityStatus(true);
  });
  
  window.addEventListener('offline', () => {
    showConnectivityStatus(false);
  });
  
  // Function to show connectivity status
  function showConnectivityStatus(isOnline) {
    // Remove any existing connectivity status notifications
    const existingNotification = document.querySelector('.connectivity-notification');
    if (existingNotification) {
      existingNotification.remove();
    }
    
    // Create new notification
    const notification = document.createElement('div');
    notification.className = 'connectivity-notification ' + (isOnline ? 'online' : 'offline');
    
    notification.innerHTML = isOnline 
      ? '<i class="fas fa-wifi"></i> You are back online!'
      : '<i class="fas fa-wifi-slash"></i> You are offline. Some features may be unavailable.';
    
    document.body.appendChild(notification);
    
    // Auto-remove notification after 5 seconds
    setTimeout(() => {
      notification.classList.add('fadeout');
      setTimeout(() => {
        notification.remove();
      }, 500);
    }, 5000);
  }