"""
callbacks/auth_handlers.py - Authentication & Session Management

Save this as: callbacks/auth_handlers.py
"""

from dash import callback, Output, Input, State, html, no_update
from datetime import datetime
from urllib.parse import parse_qs

# Check if OAuth is available
try:
    from auth.google_oauth import get_current_user, is_authenticated
    OAUTH_AVAILABLE = True
    print("✓ OAuth module loaded successfully")
except ImportError:
    OAUTH_AVAILABLE = False
    print("⚠️ OAuth module not available - using fallback functions")
    
    def get_current_user():
        return None
    
    def is_authenticated():
        return False

# ==================== SESSION MANAGEMENT CALLBACK ====================

@callback(
    Output('user-session', 'data', allow_duplicate=True),
    [Input('url', 'pathname')],
    [State('user-session', 'data')],
    prevent_initial_call=True
)
def handle_session_management(pathname, current_session):
    """Handle session management and OAuth sync - simplified"""
    
    print(f"🔍 SESSION DEBUG - Session management triggered:")
    print(f"  - pathname: {pathname}")
    print(f"  - current_session: {current_session}")
    
    # Skip session management for logout routes (handled by URL logout callback)
    if pathname in ['/logout', '/auth/logout']:
        print(f"🔍 SESSION DEBUG - Skipping session management for logout route: {pathname}")
        return no_update
    
    # Skip session management for login and public pages to avoid auto-login
    if pathname in ['/', '/login']:
        print(f"🔍 SESSION DEBUG - Skipping session management for public/login page: {pathname}")
        return no_update
    
    # Only try to create OAuth sessions for protected routes
    protected_routes = ['/main', '/reports', '/analytics', '/upload', '/settings']
    if pathname in protected_routes and OAUTH_AVAILABLE and not (current_session and current_session.get('authenticated')):
        try:
            oauth_user = get_current_user()
            oauth_authenticated = is_authenticated()
            
            print(f"🔍 SESSION DEBUG - OAuth check for protected route:")
            print(f"  - oauth_authenticated: {oauth_authenticated}")
            print(f"  - oauth_user: {oauth_user}")
            
            if oauth_authenticated and oauth_user:
                print(f"✅ SESSION DEBUG - Creating new OAuth session for user: {oauth_user.get('name', 'Unknown')}")
                new_session = {
                    'user_id': oauth_user.get('id'),
                    'username': oauth_user.get('name', oauth_user.get('email', 'User')),
                    'email': oauth_user.get('email'),
                    'picture': oauth_user.get('picture'),
                    'authenticated': True,
                    'auth_method': 'google_oauth'
                }
                print(f"  - New session: {new_session}")
                return new_session
                
        except Exception as e:
            print(f"❌ SESSION DEBUG - Session sync error: {e}")
    
    print("🔍 SESSION DEBUG - No session changes needed")
    return no_update

# ==================== LOGOUT HANDLING VIA URL CHANGES ====================

@callback(
    [Output('user-session', 'data', allow_duplicate=True),
     Output('url', 'pathname', allow_duplicate=True)],
    [Input('url', 'pathname'),
     Input('url', 'search')],
    [State('user-session', 'data')],
    prevent_initial_call=True
)
def handle_logout_via_url(pathname, search_params, session_data):
    """Handle logout by detecting URL changes and logout parameters"""
    
    print(f"🔍 LOGOUT URL DEBUG - URL Handler triggered:")
    print(f"  - pathname: {pathname}")
    print(f"  - search_params: {search_params}")
    print(f"  - session_data: {session_data}")
    
    # Handle logout routes
    if pathname in ['/logout', '/auth/logout']:
        print(f"✅ LOGOUT URL DEBUG - Logout route detected: {pathname}")
        print(f"  - Clearing session and redirecting to home with logout flag")
        print(f"  - Previous session: {session_data}")
        
        # Clear session and redirect to home with logout flag so login page works
        return {}, '/?logout=true&completed=true'
    
    # Handle logout parameter in URL (for client-side triggered logouts)
    if search_params and ('logout=true' in search_params or 'source=dashboard' in search_params):
        print("✅ LOGOUT URL DEBUG - Logout parameter detected")
        print(f"  - Search params: {search_params}")
        print(f"  - Clearing session")
        print(f"  - Previous session: {session_data}")
        
        # Clear session but don't redirect (let master routing handle it)
        return {}, no_update
    
    print("🔍 LOGOUT URL DEBUG - No logout action needed")
    return no_update, no_update

# ==================== FORCE LOGIN CALLBACK ====================

@callback(
    Output('user-session', 'data', allow_duplicate=True),
    [Input('url', 'search')],
    [State('url', 'pathname')],
    prevent_initial_call=True
)
def handle_force_login(search_params, pathname):
    """Handle force login requests"""
    
    if pathname == '/login' and search_params and 'force=true' in search_params:
        print("🔍 FORCE LOGIN - Forcing session clear for login page")
        return {}
    
    return no_update

# ==================== LOGIN FORM CALLBACK ====================

@callback(
    [Output('login-alert', 'style'),
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
    """Handle login form submission - FIXED: proper validation"""
    
    if not login_clicks or login_clicks == 0:
        return {"display": "none"}, "", no_update, no_update
    
    # If OAuth is available, redirect to Google OAuth
    if OAUTH_AVAILABLE:
        return {"display": "none"}, "", no_update, '/auth/login'
    
    # Fallback to traditional login
    if not username or not password:
        return {
            "display": "block",
            "backgroundColor": "#fff3cd",
            "color": "#856404",
            "padding": "0.75rem",
            "borderRadius": "8px",
            "border": "1px solid #ffeaa7"
        }, "⚠️ Please enter both username and password.", no_update, no_update
    
    # FIXED: Proper validation with debug info
    print(f"🔐 Login attempt: username='{username}', password='{password}'")
    user = validate_user(username.strip(), password)
    print(f"🔐 Validation result: {user}")
    
    if user:
        user_data = {
            'user_id': user['id'],
            'username': user['username'],
            'role': user.get('role', 'user'),
            'authenticated': True,
            'auth_method': 'fallback'
        }
        print(f"✅ Login successful: {user_data}")
        return {"display": "none"}, "", user_data, '/main'
    else:
        print(f"❌ Login failed for username: {username}")
        return {
            "display": "block",
            "backgroundColor": "#f8d7da",
            "color": "#721c24",
            "padding": "0.75rem",
            "borderRadius": "8px",
            "border": "1px solid #f5c6cb"
        }, "❌ Invalid username or password. Please try again.", no_update, no_update

# ==================== AUTHENTICATION UTILITY FUNCTIONS ====================

def validate_user(username, password):
    """Simple authentication validation - FIXED: correct password for 'user'"""
    valid_users = {
        'admin': 'password123',
        'user': 'password456',  # FIXED: This should work now
        'test': 'test123'
    }
    
    if username in valid_users and valid_users[username] == password:
        return {'id': username, 'username': username, 'role': 'user'}
    return None

def get_user_display_name(session_data):
    """Get user display name from session data"""
    if not session_data:
        return "User"
    
    name = session_data.get('name') or session_data.get('username') or session_data.get('email', 'User')
    # Return first name only
    return name.split()[0] if name else "User"

def is_user_authenticated(session_data):
    """Check if user is authenticated from any source"""
    oauth_auth = is_authenticated() if OAUTH_AVAILABLE else False
    dash_auth = session_data and session_data.get('authenticated', False)
    return oauth_auth or dash_auth

def should_redirect_to_login(pathname, session_data):
    """Determine if user should be redirected to login"""
    protected_routes = ['/main', '/reports', '/analytics', '/upload', '/settings']
    return pathname in protected_routes and not is_user_authenticated(session_data)

def should_redirect_from_login(pathname, session_data):
    """Determine if authenticated user should be redirected from login page"""
    return pathname == '/login' and is_user_authenticated(session_data)

# ==================== OAUTH UTILITY FUNCTIONS ====================

def get_oauth_user_info():
    """Get current OAuth user information safely"""
    if not OAUTH_AVAILABLE:
        return None, False
    
    try:
        oauth_user = get_current_user()
        oauth_authenticated = is_authenticated()
        return oauth_user, oauth_authenticated
    except Exception as e:
        print(f"Error getting OAuth user info: {e}")
        return None, False

def create_oauth_session(oauth_user):
    """Create session data from OAuth user information"""
    if not oauth_user:
        return None
    
    return {
        'user_id': oauth_user.get('id'),
        'username': oauth_user.get('name', oauth_user.get('email', 'User')),
        'email': oauth_user.get('email'),
        'picture': oauth_user.get('picture'),
        'authenticated': True,
        'auth_method': 'google_oauth'
    }

print("✓ Authentication handlers module loaded successfully")