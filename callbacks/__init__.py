"""
callbacks/__init__.py - Swaccha Andhra Dashboard Callbacks Package

Save this as: callbacks/__init__.py

Easy import for the entire callback system.
Simply import this package to activate all dashboard functionality.

Usage:
    # In your main app.py file:
    import callbacks
    
    # Or import specific modules:
    from callbacks import auth_handlers, navigation_handlers
    
    # Or import specific functions:
    from callbacks.master_callback import get_required_layout_components
"""

# Import the master callback module which coordinates everything
from .master_callback import (
    # Core functions
    get_current_time,
    get_required_layout_components,
    initialize_dashboard_callbacks,
    
    # Authentication functions  
    OAUTH_AVAILABLE,
    validate_user,
    is_user_authenticated,
    
    # Layout functions
    create_public_dashboard,
    create_main_dashboard, 
    create_safe_login_layout,
    
    # Debug functions
    debug_session_state,
    debug_oauth_status,
    
    # Constants
    COLORS
)

# Package metadata
__version__ = "1.0.0"
__author__ = "Swaccha Andhra Team"
__description__ = "Modular callback system for Swaccha Andhra Dashboard"

# Quick setup function
def setup_dashboard_callbacks():
    """
    Quick setup function to initialize all dashboard callbacks.
    
    Returns:
        bool: True if initialization successful
    """
    try:
        return initialize_dashboard_callbacks()
    except Exception as e:
        print(f"❌ Error initializing dashboard callbacks: {e}")
        return False

# Package info function
def get_package_info():
    """Get information about the callbacks package"""
    return {
        "version": __version__,
        "author": __author__,
        "description": __description__,
        "oauth_available": OAUTH_AVAILABLE,
        "modules": [
            "auth_handlers",
            "navigation_handlers", 
            "layout_components",
            "header_handlers",
            "utility_functions",
            "master_callback"
        ]
    }

# Export main functions for easy access
__all__ = [
    # Setup functions
    'setup_dashboard_callbacks',
    'get_package_info',
    
    # Core functions
    'get_current_time',
    'get_required_layout_components',
    
    # Authentication
    'OAUTH_AVAILABLE',
    'validate_user', 
    'is_user_authenticated',
    
    # Layouts
    'create_public_dashboard',
    'create_main_dashboard',
    'create_safe_login_layout',
    
    # Debug
    'debug_session_state',
    'debug_oauth_status',
    
    # Constants
    'COLORS'
]

print("📦 Swaccha Andhra Dashboard Callbacks Package Loaded")
print(f"   Version: {__version__}")
print(f"   OAuth Available: {'✅ Yes' if OAUTH_AVAILABLE else '❌ No'}")
print("   Ready for use!")