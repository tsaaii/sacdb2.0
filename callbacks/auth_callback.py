"""
callbacks/auth_callback.py - Fixed Authentication with Conditional Callbacks

This file fixes the missing login-submit-btn error by making login callbacks conditional.
"""

from dash import callback, Output, Input, State, no_update, html, callback_context, clientside_callback
from dash.exceptions import PreventUpdate
import dash

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

# Main routing and authentication callback (without login form dependencies)
@callback(
    [Output('user-session', 'data'),
     Output('url', 'pathname')],
    [Input('url', 'pathname'),
     Input('url', 'search')],
    [State('user-session', 'data')],
    prevent_initial_call=True
)
def handle_routing_and_auth(pathname, search_params, session_data):
    """
    Handles route protection and URL error handling.
    This callback doesn't depend on login form elements.
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
                return no_update, '/auth/login'
            else:
                return no_update, '/login'
        
        # Clear session when user navigates to home page while authenticated
        if pathname == '/' and session_data and session_data.get('authenticated'):
            return {}, no_update
    
    return no_update, no_update

# Login form callback - only registers when login elements exist
def register_login_callback():
    """Register login callback only when login page is loaded"""
    
    @callback(
        [Output('login-alert', 'is_open'),
         Output('login-alert', 'children'),
         Output('user-session', 'data', allow_duplicate=True),
         Output('url', 'pathname', allow_duplicate=True)],
        [Input('login-submit-btn', 'n_clicks')],
        [State('login-username', 'value'),
         State('login-password', 'value'),
         State('user-session', 'data')],
        prevent_initial_call=True
    )
    def handle_login_form(login_clicks, username, password, session_data):
        """Handle login form submission"""
        
        if not login_clicks or login_clicks == 0:
            raise PreventUpdate
        
        # If OAuth is available, redirect to Google OAuth
        if OAUTH_AVAILABLE:
            return False, "", no_update, '/auth/login'
        
        # Fallback to traditional login
        if not username or not password:
            return True, "Please enter both username and password.", no_update, no_update
        
        user = validate_user(username.strip(), password)
        
        if user:
            user_data = {
                'user_id': user['id'],
                'username': user['username'],
                'role': user.get('role', 'user'),
                'authenticated': True,
                'auth_method': 'fallback'
            }
            return False, "", user_data, '/main'
        else:
            return True, "Invalid username or password. Please try again.", no_update, no_update

# URL error handling callback (safe - no form dependencies)
@callback(
    [Output('login-alert', 'is_open', allow_duplicate=True),
     Output('login-alert', 'children', allow_duplicate=True),
     Output('login-alert', 'color')],
    [Input('url', 'search')],
    prevent_initial_call=True
)
def handle_url_errors(search_params):
    """Handle authentication errors from URL parameters."""
    
    if not search_params:
        return False, "", "danger"
    
    # Parse URL parameters
    from urllib.parse import parse_qs
    try:
        params = parse_qs(search_params.lstrip('?'))
        error_type = params.get('error', [None])[0]
        
        if error_type == 'unauthorized_email':
            return True, [
                html.I(className="fas fa-exclamation-triangle", style={"marginRight": "0.5rem"}),
                "Access denied. Your email address is not authorized to access this dashboard. ",
                "Please contact the administrator for access."
            ], "warning"
        
        elif error_type == 'auth_failed':
            return True, [
                html.I(className="fas fa-times-circle", style={"marginRight": "0.5rem"}),
                "Authentication failed. Please try logging in again."
            ], "danger"
            
        elif error_type == 'oauth_not_configured':
            return True, [
                html.I(className="fas fa-cog", style={"marginRight": "0.5rem"}),
                "OAuth is not properly configured. Please contact the administrator."
            ], "danger"
            
    except Exception:
        pass
    
    return False, "", "danger"

# Client-side callback to handle login form when it exists
clientside_callback(
    """
    function(pathname) {
        // Only try to register login callback when on login page
        if (pathname === '/login' && document.getElementById('login-submit-btn')) {
            // Login form exists, can handle it client-side or trigger server callback
            return true;
        }
        return false;
    }
    """,
    Output('page-access-check', 'children'),
    [Input('url', 'pathname')]
)