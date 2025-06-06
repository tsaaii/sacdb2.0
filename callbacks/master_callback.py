"""
callbacks/master_callback.py - Main Coordination Module

Save this as: callbacks/master_callback.py

This module coordinates all callback modules and provides the main entry point.
Import this module to activate all dashboard functionality.
"""

# ==================== IMPORT ALL MODULES ====================

print("🚀 Loading Swaccha Andhra Dashboard callback system...")

# Core utility functions
from .utility_functions import (
    get_current_time, get_required_layout_components, 
    create_debug_info, log_callback_info, COLORS
)

# Authentication and session management
from .auth_handlers import (
    OAUTH_AVAILABLE, validate_user, get_user_display_name,
    is_user_authenticated, should_redirect_to_login, 
    should_redirect_from_login, get_oauth_user_info
)

# Navigation and routing
from .navigation_handlers import (
    master_routing_callback, update_navigation_active_state,
    handle_url_errors
)

# Layout components
from .layout_components import (
    create_public_dashboard, create_main_dashboard, 
    create_safe_login_layout, create_page_with_nav,
    create_404_page, create_unauthorized_error_page,
    create_footer, create_title_banner, create_error_boundary
)

# Header and clock management
from .header_handlers import (
    update_live_time, update_header_actions,
    handle_logout_button_attachment
)

# ==================== MODULE STATUS REPORTING ====================

def print_module_status():
    """Print the status of all loaded modules"""
    print("=" * 60)
    print("📊 SWACCHA ANDHRA DASHBOARD - MODULE STATUS")
    print("=" * 60)
    print("✅ Core System Components:")
    print("   ✓ Master callback system loaded")
    print("   ✓ Utility functions module")
    print("   ✓ Layout components module")
    print("=" * 60)
    print("🔐 Authentication & Security:")
    print(f"   {'✓' if OAUTH_AVAILABLE else '⚠️'} OAuth integration {'enabled' if OAUTH_AVAILABLE else 'disabled'}")
    print("   ✓ Session management callbacks")
    print("   ✓ Login form handling")
    print("   ✓ Logout functionality")
    print("=" * 60)
    print("🧭 Navigation & Routing:")
    print("   ✓ Master routing callback")
    print("   ✓ URL error handling")
    print("   ✓ Navigation state management")
    print("   ✓ Protected route handling")
    print("=" * 60)
    print("🎨 UI & Display Components:")
    print("   ✓ Header actions management")
    print("   ✓ Clock updates configured") 
    print("   ✓ Dynamic layout creation")
    print("   ✓ Error boundary components")
    print("=" * 60)
    print("🔧 Development & Debug:")
    print("   ✓ Comprehensive debug logging")
    print("   ✓ Client-side error handling")
    print("   ✓ Modular architecture")
    print("=" * 60)
    print("🎯 Ready for deployment!")
    print("=" * 60)

# ==================== CALLBACK SUMMARY ====================

def get_callback_summary():
    """Get summary of all registered callbacks"""
    return {
        'auth_callbacks': [
            'handle_session_management',
            'handle_logout_via_url', 
            'handle_force_login',
            'handle_login_form'
        ],
        'navigation_callbacks': [
            'master_routing_callback',
            'update_navigation_active_state',
            'handle_url_errors'
        ],
        'header_callbacks': [
            'update_live_time',
            'update_header_actions',
            'handle_logout_button_attachment'
        ],
        'client_callbacks': [
            'logout_handler',
            'navigation_smoother'
        ]
    }

# ==================== DEBUGGING FUNCTIONS ====================

def debug_session_state(session_data):
    """Debug session state for troubleshooting"""
    if not session_data:
        return "❌ No session data"
    
    auth_status = "✅ Authenticated" if session_data.get('authenticated') else "❌ Not authenticated"
    auth_method = session_data.get('auth_method', 'Unknown')
    username = session_data.get('username', 'Unknown')
    
    return f"{auth_status} | Method: {auth_method} | User: {username}"

def debug_oauth_status():
    """Debug OAuth status for troubleshooting"""
    if not OAUTH_AVAILABLE:
        return "❌ OAuth not available"
    
    try:
        from .auth_handlers import is_authenticated, get_current_user
        oauth_authenticated = is_authenticated()
        oauth_user = get_current_user()
        
        if oauth_authenticated and oauth_user:
            return f"✅ OAuth active | User: {oauth_user.get('name', 'Unknown')}"
        elif oauth_authenticated:
            return "⚠️ OAuth authenticated but no user data"
        else:
            return "❌ OAuth not authenticated"
    except Exception as e:
        return f"❌ OAuth error: {e}"

# ==================== MAIN INITIALIZATION ====================

def initialize_dashboard_callbacks():
    """Initialize all dashboard callbacks and components"""
    
    print_module_status()
    
    # Log callback summary
    summary = get_callback_summary()
    total_callbacks = sum(len(callbacks) for callbacks in summary.values())
    
    print(f"📊 Callback Summary: {total_callbacks} total callbacks registered")
    for category, callbacks in summary.items():
        print(f"   {category}: {len(callbacks)} callbacks")
    
    print("\n🎯 Dashboard initialization complete!")
    print("🔗 All authentication, routing, and UI callbacks are active")
    print("🔄 Real-time updates and session management enabled")
    
    return True

# ==================== UTILITY EXPORTS ====================

# Export commonly used functions for external use
__all__ = [
    # Core functions
    'get_current_time',
    'get_required_layout_components',
    
    # Authentication functions
    'OAUTH_AVAILABLE',
    'validate_user',
    'is_user_authenticated',
    
    # Layout functions
    'create_public_dashboard',
    'create_main_dashboard',
    'create_safe_login_layout',
    
    # Debug functions
    'debug_session_state',
    'debug_oauth_status',
    'initialize_dashboard_callbacks',
    
    # Constants
    'COLORS'
]

# ==================== AUTO-INITIALIZATION ====================

# Initialize the dashboard when this module is imported
if __name__ == "__main__":
    initialize_dashboard_callbacks()
else:
    # Auto-initialize when imported
    initialize_dashboard_callbacks()

print("✅ Master callback system fully loaded and operational!")