"""
callbacks/session_callback.py - Consolidated Session Management

This file handles ALL user session updates in one place to avoid conflicts.
Replace both auth_callback.py and the session parts of routing_callback.py with this.
"""

from dash import callback, Output, Input, State, no_update, callback_context
from dash.exceptions import PreventUpdate
from urllib.parse import parse_qs

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

# ====================== CONSOLIDATED SESSION MANAGEMENT ======================

@callback(
    [Output('user-session', 'data'),
     Output('url', 'pathname', allow_duplicate=True)],
    [Input('login-submit-btn', 'n_clicks'),
     Input('url', 'pathname'),
     Input('url', 'search'),
     Input('refresh-interval', 'n_intervals')],
    [State('login-username', 'value'),
     State('login-password', 'value'),
     State('user-session', 'data')],
    prevent_initial_call=True
)
def manage_user_session(login_clicks, pathname, search_params, n_intervals, 
                       username, password, current_session):
    """
    Consolidated callback that handles ALL user session management:
    - Traditional login form submission
    - OAuth session synchronization
    - Route protection and redirects
    - Session cleanup
    """
    
    ctx = callback_context
    if not ctx.triggered:
        raise PreventUpdate
    
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    # ============= HANDLE LOGIN FORM SUBMISSION =============
    if trigger_id == 'login-submit-btn' and login_clicks and login_clicks > 0:
        if not username or not password:
            # Don't update session for validation errors
            return no_update, no_update
        
        # Validate credentials
        valid_users = {
            'admin': 'password123',
            'user': 'password456', 
            'test': 'test123'
        }
        
        if username.strip() in valid_users and valid_users[username.strip()] == password:
            # Successful login
            user_data = {
                'user_id': username.strip(),
                'username': username.strip(),
                'role': 'user',
                'authenticated': True,
                'auth_method': 'traditional'
            }
            return user_data, '/main'
        else:
            # Invalid credentials - don't update session
            return no_update, no_update
    
    # ============= HANDLE ROUTE PROTECTION =============
    elif trigger_id == 'url' and pathname:
        # Public routes that don't require authentication
        public_routes = ['/', '/login', '/auth/login', '/auth/callback', '/auth/logout']
        
        # Handle logout routes
        if pathname in ['/logout', '/auth/logout']:
            print("User logging out - clearing session")
            return {}, '/'
        
        # If on public route, maintain current session but don't redirect
        if pathname in public_routes:
            return no_update, no_update
        
        # Check authentication for protected routes
        oauth_authenticated = is_authenticated() if OAUTH_AVAILABLE else False
        dash_authenticated = current_session and current_session.get('authenticated', False)
        
        # If not authenticated and trying to access protected route
        if not (oauth_authenticated or dash_authenticated):
            print(f"Access denied to {pathname} - redirecting to login")
            return no_update, '/login'
        
        # If authenticated but on login page, redirect to main
        if (oauth_authenticated or dash_authenticated) and pathname == '/login':
            return no_update, '/main'
        
        # Clear session when navigating to home while authenticated (optional)
        if pathname == '/' and current_session and current_session.get('authenticated'):
            return {}, no_update
    
    # ============= HANDLE OAUTH SESSION SYNC =============
    elif trigger_id == 'refresh-interval':
        # Sync with OAuth every minute if available
        if OAUTH_AVAILABLE:
            try:
                oauth_user = get_current_user()
                oauth_authenticated = is_authenticated()
                
                if oauth_authenticated and oauth_user:
                    # Update session with OAuth user info
                    oauth_session = {
                        'user_id': oauth_user.get('id'),
                        'username': oauth_user.get('name', oauth_user.get('email', 'User')),
                        'email': oauth_user.get('email'),
                        'picture': oauth_user.get('picture'),
                        'authenticated': True,
                        'auth_method': 'google_oauth'
                    }
                    
                    # Only update if different from current session
                    if oauth_session != current_session:
                        return oauth_session, no_update
                        
                elif current_session and current_session.get('auth_method') == 'google_oauth':
                    # OAuth session expired, clear it
                    print("OAuth session expired - clearing session")
                    return {}, '/login'
                    
            except Exception as e:
                print(f"Error syncing OAuth session: {e}")
    
    # ============= HANDLE URL ERROR PARAMETERS =============
    elif trigger_id == 'url' and search_params:
        # Handle OAuth callback errors by clearing session
        try:
            params = parse_qs(search_params.lstrip('?'))
            error_type = params.get('error', [None])[0]
            
            if error_type in ['unauthorized_email', 'auth_failed', 'oauth_not_configured']:
                print(f"OAuth error: {error_type} - clearing session")
                return {}, no_update
                
        except Exception:
            pass
    
    # Default: no changes
    return no_update, no_update

# ====================== USER INFO CALLBACK ======================

@callback(
    Output('current-user-info', 'data'),
    [Input('user-session', 'data')],
    prevent_initial_call=True
)
def update_current_user_info(session_data):
    """
    Update current user info based on session data.
    This is separate to avoid circular dependencies.
    """
    if session_data and session_data.get('authenticated'):
        return session_data
    else:
        return {}

# ====================== PAGE ACCESS CHECK ======================

@callback(
    Output('page-access-check', 'children'),
    [Input('url', 'pathname'),
     Input('current-user-info', 'data')],
    prevent_initial_call=True
)
def check_page_access(pathname, user_info):
    """
    Simple page access check for debugging and conditional rendering.
    """
    
    protected_routes = ['/main', '/reports', '/analytics', '/upload', '/settings']
    
    if pathname in protected_routes:
        is_authenticated_user = bool(user_info and user_info.get('authenticated'))
        return "authenticated" if is_authenticated_user else "not_authenticated"
    
    return "public"

# ====================== NAVIGATION STATUS ======================

@callback(
    Output('page-navigation-status', 'data'),
    [Input('url', 'pathname'),
     Input('current-user-info', 'data')],
    prevent_initial_call=True
)
def update_navigation_status(pathname, user_info):
    """
    Update navigation status for conditional rendering.
    """
    return {
        'current_page': pathname,
        'is_authenticated': bool(user_info and user_info.get('authenticated')),
        'auth_method': user_info.get('auth_method') if user_info else None,
        'user_name': user_info.get('username') if user_info else None,
        'user_email': user_info.get('email') if user_info else None,
        'user_picture': user_info.get('picture') if user_info else None
    }

print("✓ Consolidated session management loaded - no conflicts")