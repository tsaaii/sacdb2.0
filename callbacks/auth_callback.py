"""
callbacks/auth_callback.py - Fixed Authentication with No Login Alert Conflicts

This file handles authentication routing without conflicting with login form callbacks.
The login form callbacks are now handled in routing_callback.py
"""

from dash import callback, Output, Input, State, no_update, callback_context
from dash.exceptions import PreventUpdate

# Check if Google OAuth is available
try:
    from auth.google_oauth import get_current_user, is_authenticated
    OAUTH_AVAILABLE = True
except ImportError:
    OAUTH_AVAILABLE = False
    def get_current_user():
        return None
    def is_authenticated():
        return False

# Your existing simple authentication function (kept as fallback)
def validate_user(username, password):
    """Simple authentication - used when OAuth is not available"""
    valid_users = {
        'admin': 'password123',
        'user': 'password456', 
        'test': 'test123'
    }
    
    if username in valid_users and valid_users[username] == password:
        return {'id': username, 'username': username, 'role': 'user'}
    return None

# Main authentication and routing callback (NO login form dependencies)
@callback(
    [Output('user-session', 'data', allow_duplicate=True),
     Output('url', 'pathname', allow_duplicate=True)],
    [Input('url', 'pathname'),
     Input('url', 'search')],
    [State('user-session', 'data')],
    prevent_initial_call=True
)
def handle_auth_routing(pathname, search_params, session_data):
    """
    Handles authentication state management and routing protection.
    This callback does NOT handle login form elements to avoid conflicts.
    """
    ctx = callback_context
    
    if not ctx.triggered:
        raise PreventUpdate
    
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    # Handle URL pathname changes (route protection)
    if trigger_id == 'url' and pathname:
        # Public routes that don't require authentication
        public_routes = ['/', '/login', '/auth/login', '/auth/callback', '/auth/logout']
        
        if pathname in public_routes:
            return no_update, no_update
        
        # Check authentication for protected routes
        oauth_authenticated = is_authenticated() if OAUTH_AVAILABLE else False
        dash_authenticated = session_data and session_data.get('authenticated', False)
        
        if not (oauth_authenticated or dash_authenticated):
            # Redirect to appropriate login page
            if OAUTH_AVAILABLE:
                return no_update, '/login'  # Changed to /login instead of /auth/login
            else:
                return no_update, '/login'
        
        # Clear session when user navigates to home page while authenticated
        if pathname == '/' and session_data and session_data.get('authenticated'):
            return {}, no_update
    
    return no_update, no_update

# Session synchronization callback (keeps session in sync with OAuth)
@callback(
    Output('current-user-info', 'data'),
    [Input('refresh-interval', 'n_intervals')],
    [State('user-session', 'data')],
    prevent_initial_call=True
)
def sync_user_session(n_intervals, session_data):
    """
    Synchronize user session with OAuth status.
    Updates every minute to keep session fresh.
    """
    if OAUTH_AVAILABLE:
        try:
            oauth_user = get_current_user()
            oauth_authenticated = is_authenticated()
            
            if oauth_authenticated and oauth_user:
                # Return OAuth user info
                return {
                    'user_id': oauth_user.get('id'),
                    'username': oauth_user.get('name', oauth_user.get('email', 'User')),
                    'email': oauth_user.get('email'),
                    'picture': oauth_user.get('picture'),
                    'authenticated': True,
                    'auth_method': 'google_oauth'
                }
            elif session_data and session_data.get('authenticated'):
                # Return traditional login info
                return session_data
            else:
                # No authentication
                return {}
        except Exception as e:
            print(f"Error syncing user session: {e}")
            return session_data or {}
    else:
        # OAuth not available, return session data
        return session_data or {}

# Authentication status check callback
@callback(
    Output('page-access-check', 'children'),
    [Input('url', 'pathname')],
    [State('user-session', 'data'),
     State('current-user-info', 'data')],
    prevent_initial_call=True
)
def check_page_access(pathname, session_data, user_info):
    """
    Check if user has access to the current page.
    Provides feedback without conflicting with other callbacks.
    """
    
    # Protected routes
    protected_routes = ['/main', '/reports', '/analytics', '/upload', '/settings']
    
    if pathname in protected_routes:
        # Check authentication
        oauth_authenticated = is_authenticated() if OAUTH_AVAILABLE else False
        dash_authenticated = session_data and session_data.get('authenticated', False)
        
        if not (oauth_authenticated or dash_authenticated):
            print(f"Access denied to {pathname} - user not authenticated")
            return "access_denied"
        else:
            print(f"Access granted to {pathname}")
            return "access_granted"
    
    return "public_page"

# OAuth logout handling (if OAuth is available)
if OAUTH_AVAILABLE:
    @callback(
        [Output('user-session', 'data', allow_duplicate=True),
         Output('url', 'pathname', allow_duplicate=True)],
        [Input('url', 'pathname')],
        [State('user-session', 'data')],
        prevent_initial_call=True
    )
    def handle_oauth_logout(pathname, session_data):
        """
        Handle OAuth logout when user visits logout routes.
        """
        if pathname == '/auth/logout':
            # Clear local session and redirect
            return {}, '/'
        
        return no_update, no_update

# Session cleanup callback
@callback(
    Output('user-session', 'data', allow_duplicate=True),
    [Input('url', 'pathname')],
    [State('user-session', 'data')],
    prevent_initial_call=True
)
def cleanup_session_on_logout(pathname, session_data):
    """
    Clean up session data when user explicitly logs out.
    """
    logout_routes = ['/logout', '/auth/logout']
    
    if pathname in logout_routes:
        print("Cleaning up user session on logout")
        return {}
    
    return no_update

# Debug callback for development (optional)
@callback(
    Output('page-navigation-status', 'data'),
    [Input('url', 'pathname'),
     Input('current-user-info', 'data')],
    prevent_initial_call=True
)
def update_navigation_status(pathname, user_info):
    """
    Update navigation status for debugging and conditional rendering.
    """
    is_authenticated_user = bool(user_info and user_info.get('authenticated'))
    
    return {
        'current_page': pathname,
        'is_authenticated': is_authenticated_user,
        'auth_method': user_info.get('auth_method') if user_info else None,
        'user_name': user_info.get('username') if user_info else None
    }

# REMOVED: All login form related callbacks are now in routing_callback.py
# This prevents the duplicate output conflicts

print("✓ Auth callback loaded - no login form conflicts")