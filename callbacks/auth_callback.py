"""
callbacks/auth_callback.py - Complete Fixed Authentication System

This file handles login/logout functionality with proper error handling.
"""

from dash import callback, Output, Input, State, no_update, clientside_callback
from dash.exceptions import PreventUpdate
import dash

# Simple authentication function
def validate_user(username, password):
    """Simple authentication - replace with your auth.py integration"""
    # Default test users
    valid_users = {
        'admin': 'password123',
        'user': 'password456',
        'test': 'test123'
    }
    
    if username in valid_users and valid_users[username] == password:
        return {'id': username, 'username': username, 'role': 'user'}
    return None

@callback(
    [Output('login-alert', 'is_open'),
     Output('login-alert', 'children'),
     Output('user-session', 'data'),
     Output('url', 'pathname', allow_duplicate=True)],
    [Input('login-submit-btn', 'n_clicks')],
    [State('login-username', 'value'),
     State('login-password', 'value'),
     State('user-session', 'data')],
    prevent_initial_call=True
)
def handle_login(n_clicks, username, password, session_data):
    """
    Handle login form submission and authentication.
    """
    if not n_clicks or n_clicks == 0:
        raise PreventUpdate
    
    # Validate inputs
    if not username or not password:
        return True, "Please enter both username and password.", no_update, no_update
    
    # Attempt authentication
    user = validate_user(username.strip(), password)
    
    if user:
        # Authentication successful
        user_data = {
            'user_id': user['id'],
            'username': user['username'], 
            'role': user.get('role', 'user'),
            'authenticated': True
        }
        
        # Return success data and redirect to main page
        return False, "", user_data, '/main'
    else:
        # Authentication failed
        return True, "Invalid username or password. Please try again.", no_update, no_update

# Use a more robust logout system with clientside callback
clientside_callback(
    """
    function(n_clicks) {
        if (n_clicks && n_clicks > 0) {
            // Clear all session storage
            if (typeof(Storage) !== "undefined") {
                sessionStorage.clear();
            }
            // Force redirect to home page
            window.location.href = '/';
            return true;
        }
        return window.dash_clientside.no_update;
    }
    """,
    Output('current-user-info', 'data'),
    Input('logout-btn', 'n_clicks'),
    prevent_initial_call=True
)

# Protection callback for authenticated routes
@callback(
    Output('url', 'pathname', allow_duplicate=True),
    [Input('url', 'pathname')],
    [State('user-session', 'data')],
    prevent_initial_call=True
)
def protect_routes(pathname, session_data):
    """Redirect unauthenticated users from protected routes."""
    # Public routes that don't require authentication
    public_routes = ['/', '/login']
    
    # If on public route, no redirect needed
    if pathname in public_routes:
        return no_update
    
    # If not authenticated and trying to access protected route
    if not session_data or not session_data.get('authenticated'):
        return '/login'
    
    # User is authenticated, allow access
    return no_update

# Callback to clear session when navigating to home page
@callback(
    Output('user-session', 'data', allow_duplicate=True),
    [Input('url', 'pathname')],
    [State('user-session', 'data')],
    prevent_initial_call=True
)
def clear_session_on_home(pathname, session_data):
    """Clear session when user navigates to home page."""
    if pathname == '/' and session_data and session_data.get('authenticated'):
        return {}
    return no_update