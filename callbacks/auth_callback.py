"""
callbacks/auth_callback.py - Enhanced Authentication with proper redirect

This file handles login/logout functionality with guaranteed redirect.
"""

from dash import callback, Output, Input, State, no_update, clientside_callback, ClientsideFunction
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
     Output('login-success-trigger', 'data')],
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
        
        # Return success data and trigger redirect
        return False, "", user_data, {'redirect': True, 'url': '/main'}
    else:
        # Authentication failed
        return True, "Invalid username or password. Please try again.", no_update, no_update

# Clientside callback for immediate redirect
clientside_callback(
    """
    function(trigger_data) {
        if (trigger_data && trigger_data.redirect) {
            window.location.href = trigger_data.url;
        }
        return window.dash_clientside.no_update;
    }
    """,
    Output('login-redirect-dummy', 'children'),
    Input('login-success-trigger', 'data'),
    prevent_initial_call=True
)

@callback(
    Output('url', 'pathname', allow_duplicate=True),
    [Input('logout-btn', 'n_clicks')],
    prevent_initial_call=True
)
def handle_logout(n_clicks):
    """Handle logout functionality."""
    if not n_clicks or n_clicks == 0:
        raise PreventUpdate
    
    return "/"

@callback(
    Output('user-session', 'data', allow_duplicate=True),
    [Input('url', 'pathname')],
    [State('user-session', 'data')],
    prevent_initial_call=True
)
def clear_session_on_logout(pathname, session_data):
    """Clear session data when navigating to public pages."""
    if pathname == "/" and session_data and session_data.get('authenticated'):
        return {}
    return no_update

# Protection callback for authenticated routes
@callback(
    Output('auth-redirect', 'pathname'),
    [Input('url', 'pathname'),
     Input('user-session', 'data')]
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