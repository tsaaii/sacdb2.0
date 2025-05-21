/**
 * Navigation control functionality for Swaccha Andhra Dashboard
 * Controls the hover behavior of the navigation bar
 */

document.addEventListener('DOMContentLoaded', function() {
    // Get the header element
    const header = document.querySelector('.header');
    const mobileNavToggle = document.getElementById('mobile-nav-toggle');
    
    // Mobile navigation toggle
    if (mobileNavToggle) {
      mobileNavToggle.addEventListener('click', function() {
        header.classList.toggle('active');
      });
    }
    
    // Handle scroll events to show/hide nav on mobile
    let lastScrollTop = 0;
    window.addEventListener('scroll', function() {
      // Only apply for mobile
      if (window.innerWidth <= 768) {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        // Scrolling down - hide nav
        if (scrollTop > lastScrollTop && scrollTop > 50) {
          header.classList.remove('active');
        } 
        // Scrolling up - show nav
        else if (scrollTop < lastScrollTop && scrollTop > 50) {
          header.classList.add('active');
        }
        
        lastScrollTop = scrollTop;
      }
    });
    
    // For touch devices, add a swipe down gesture at top of screen to show nav
    let touchStartY = 0;
    
    document.addEventListener('touchstart', function(e) {
      touchStartY = e.touches[0].clientY;
    }, { passive: true });
    
    document.addEventListener('touchmove', function(e) {
      if (touchStartY < 30) { // Only trigger if touch started near top of screen
        const touchY = e.touches[0].clientY;
        const touchDiff = touchY - touchStartY;
        
        // If swiping down at top of screen, show nav
        if (touchDiff > 30 && window.scrollY < 10) {
          header.classList.add('active');
        }
      }
    }, { passive: true });
    
    // Hide nav after a period of inactivity on mobile
    let navTimeout;
    const resetNavTimeout = function() {
      clearTimeout(navTimeout);
      if (window.innerWidth <= 768) {
        navTimeout = setTimeout(function() {
          header.classList.remove('active');
        }, 3000); // Hide after 3 seconds of inactivity
      }
    };
    
    // Reset timeout on user interaction
    document.addEventListener('touchstart', resetNavTimeout, { passive: true });
    document.addEventListener('touchmove', resetNavTimeout, { passive: true });
    document.addEventListener('scroll', resetNavTimeout, { passive: true });
    
    // Keep nav visible when interacting with it
    header.addEventListener('touchstart', function(e) {
      clearTimeout(navTimeout);
    }, { passive: true });
  });