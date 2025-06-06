"""
callbacks/navigation_handlers.py - Navigation & Routing

Save this as: callbacks/navigation_handlers.py
"""

from dash import callback, Output, Input, State, html, no_update, callback_context
from datetime import datetime
from urllib.parse import parse_qs

# Check if OAuth is available
try:
    from auth.google_oauth import get_current_user, is_authenticated
    OAUTH_AVAILABLE = True
except ImportError:
    OAUTH_AVAILABLE = False
    def get_current_user():
        return None
    def is_authenticated():
        return False

# Import layout creation functions
from .layout_components import (
    create_public_dashboard, create_main_dashboard, create_safe_login_layout,
    create_page_with_nav, create_404_page, create_unauthorized_error_page,
    create_analytics_layout
)

# ==================== NAVIGATION ACTIVE STATE CALLBACK ====================

@callback(
    Output('nav-links', 'children'),
    [Input('url', 'pathname')],
    [State('user-session', 'data')],
    prevent_initial_call=False
)
def update_navigation_active_state(pathname, session_data):
    """Update navigation active states based on current path"""
    
    # Check if user is authenticated
    oauth_authenticated = is_authenticated() if OAUTH_AVAILABLE else False
    dash_authenticated = session_data and session_data.get('authenticated', False)
    is_auth = oauth_authenticated or dash_authenticated
    
    if not is_auth:
        return []
    
    nav_items = [
        {"title": "Dashboard", "path": "/main"},
        {"title": "Reports", "path": "/reports"},
        {"title": "Analytics", "path": "/analytics"},
        {"title": "Upload", "path": "/upload"},
        {"title": "Settings", "path": "/settings"}
    ]
    
    nav_elements = []
    for item in nav_items:
        is_active = pathname == item["path"]
        nav_elements.append(
            html.A(
                item["title"], 
                href=item["path"], 
                className=f"header-nav-link {'active' if is_active else ''}"
            )
        )
    
    return nav_elements

# ==================== URL ERROR HANDLING CALLBACK ====================

@callback(
    [Output('login-alert', 'style', allow_duplicate=True),
     Output('login-alert', 'children', allow_duplicate=True)],
    [Input('url', 'search')],
    prevent_initial_call=True
)
def handle_url_errors(search_params):
    """Handle authentication errors from URL parameters"""
    
    if not search_params:
        return {"display": "none"}, ""
    
    try:
        params = parse_qs(search_params.lstrip('?'))
        error_type = params.get('error', [None])[0]
        
        if error_type == 'unauthorized_email':
            return {
                "display": "block",
                "backgroundColor": "#fff3cd",
                "color": "#856404",
                "padding": "0.75rem",
                "borderRadius": "8px",
                "border": "1px solid #ffeaa7"
            }, [
                html.I(className="fas fa-exclamation-triangle", style={"marginRight": "0.5rem"}),
                "Access denied. Your email address is not authorized to access this dashboard. ",
                "Please contact the administrator for access."
            ]
        
        elif error_type == 'auth_failed':
            return {
                "display": "block",
                "backgroundColor": "#f8d7da",
                "color": "#721c24",
                "padding": "0.75rem",
                "borderRadius": "8px",
                "border": "1px solid #f5c6cb"
            }, [
                html.I(className="fas fa-times-circle", style={"marginRight": "0.5rem"}),
                "Authentication failed. Please try logging in again."
            ]
            
        elif error_type == 'oauth_not_configured':
            return {
                "display": "block",
                "backgroundColor": "#f8d7da",
                "color": "#721c24",
                "padding": "0.75rem",
                "borderRadius": "8px",
                "border": "1px solid #f5c6cb"
            }, [
                html.I(className="fas fa-cog", style={"marginRight": "0.5rem"}),
                "OAuth is not properly configured. Please contact the administrator."
            ]
            
    except Exception as e:
        print(f"Error parsing URL params: {e}")
    
    return {"display": "none"}, ""

# ==================== MASTER ROUTING CALLBACK ====================

@callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname'),
     Input('url', 'search'),
     Input('refresh-interval', 'n_intervals'),
     Input('user-session', 'data')],  # FIXED: Added user-session as input to react to login
    prevent_initial_call=False
)
def master_routing_callback(pathname, search_params, n_intervals, session_data):
    """
    MASTER CALLBACK - Handles routing and page content
    """
    
    ctx = callback_context
    
    print(f"🔍 ROUTING DEBUG - Master routing triggered:")
    print(f"  - pathname: {pathname}")
    print(f"  - search_params: {search_params}")
    print(f"  - session_data: {session_data}")
    print(f"  - callback_context: {[t['prop_id'] for t in ctx.triggered] if ctx.triggered else 'None'}")
    
    # Initialize session data - FIXED: Use the passed session_data
    current_session = session_data or {}
    
    # Define protected routes
    protected_routes = ['/main', '/reports', '/analytics', '/upload', '/settings']
    
    # Handle OAuth session sync on refresh
    if ctx.triggered and ctx.triggered[0]['prop_id'].split('.')[0] == 'refresh-interval' and OAUTH_AVAILABLE:
        print("🔍 ROUTING DEBUG - Refresh interval triggered - checking OAuth sync")
        try:
            oauth_user = get_current_user()
            oauth_authenticated = is_authenticated()
            
            print(f"  - oauth_authenticated: {oauth_authenticated}")
            print(f"  - oauth_user: {oauth_user}")
            
            if oauth_authenticated and oauth_user:
                current_session = {
                    'user_id': oauth_user.get('id'),
                    'username': oauth_user.get('name', oauth_user.get('email', 'User')),
                    'email': oauth_user.get('email'),
                    'picture': oauth_user.get('picture'),
                    'authenticated': True,
                    'auth_method': 'google_oauth'
                }
                print(f"  - Updated session: {current_session}")
        except Exception as e:
            print(f"❌ ROUTING DEBUG - OAuth sync error: {e}")
    
    # Handle URL error parameters
    if search_params:
        print(f"🔍 ROUTING DEBUG - Processing search params: {search_params}")
        try:
            params = parse_qs(search_params.lstrip('?'))
            error_type = params.get('error', [None])[0]
            debug_info = params.get('debug', [None])[0]
            
            print(f"  - error_type: {error_type}")
            print(f"  - debug_info: {debug_info}")
            
            if error_type == 'unauthorized_email':
                print("✅ ROUTING DEBUG - Showing unauthorized error page")
                return create_unauthorized_error_page()
                
        except Exception as e:
            print(f"❌ ROUTING DEBUG - Error parsing search params: {e}")
    
    # Check authentication - FIXED: Use current_session consistently
    oauth_authenticated = is_authenticated() if OAUTH_AVAILABLE else False
    dash_authenticated = current_session.get('authenticated', False)
    is_auth = oauth_authenticated or dash_authenticated
    
    print(f"🔍 ROUTING DEBUG - Authentication check:")
    print(f"  - oauth_authenticated: {oauth_authenticated}")
    print(f"  - dash_authenticated: {dash_authenticated}")
    print(f"  - is_auth: {is_auth}")
    
    # Route protection and content determination
    if pathname == '/' or pathname is None:
        print("✅ ROUTING DEBUG - Showing public dashboard")
        return create_public_dashboard()
        
    elif pathname == '/login':
        print(f"🔍 LOGIN DEBUG - Login page requested")
        print(f"  - oauth_authenticated: {oauth_authenticated}")
        print(f"  - dash_authenticated: {dash_authenticated}")
        print(f"  - is_auth: {is_auth}")
        print(f"  - current_session: {current_session}")
        
        # FIXED: Check if this is a logout redirect by looking at search params
        logout_context = False
        if search_params:
            logout_context = 'logout=true' in search_params or 'source=dashboard' in search_params
            print(f"  - logout_context: {logout_context}")
        
        # If coming from logout, force show login page regardless of OAuth status
        if logout_context:
            print("✅ LOGIN DEBUG - Coming from logout - forcing login page display")
            return create_safe_login_layout()
        
        # For OAuth users, we need to be more careful about when to redirect
        if is_auth:
            # Double-check OAuth status if it's an OAuth user
            if OAUTH_AVAILABLE and oauth_authenticated:
                try:
                    oauth_user = get_current_user()
                    if oauth_user and oauth_user.get('email'):
                        print("✅ LOGIN DEBUG - OAuth user confirmed active - redirecting to dashboard")
                        return create_main_dashboard()
                    else:
                        print("⚠️ LOGIN DEBUG - OAuth authenticated but no user data - showing login")
                        return create_safe_login_layout()
                except Exception as e:
                    print(f"❌ LOGIN DEBUG - OAuth check failed: {e} - showing login")
                    return create_safe_login_layout()
            else:
                print("✅ LOGIN DEBUG - Traditional user authenticated - redirecting to dashboard")
                return create_main_dashboard()
        
        print("✅ LOGIN DEBUG - No authentication detected - showing login layout")
        return create_safe_login_layout()
        
    elif pathname in ['/logout', '/auth/logout']:
        # Handle logout - FIXED: Always show public dashboard after logout
        print(f"✅ ROUTING DEBUG - Logout route accessed: {pathname}")
        print("✅ ROUTING DEBUG - Forcing public dashboard display")
        
        # Always show public dashboard for logout routes
        return create_public_dashboard()
        
    elif pathname in protected_routes:
        if not is_auth:
            # Redirect unauthenticated users to login
            print(f"❌ ROUTING DEBUG - Access denied to {pathname} - not authenticated, redirecting to login")
            return html.Div([
                html.Script(f"console.log('Redirecting to login from {pathname}'); window.location.href = '/login';"),
                html.H2("Redirecting to login...")
            ])
        
        print(f"✅ ROUTING DEBUG - Access granted to {pathname}")
        # Serve protected content
        if pathname == '/main':
            print("✅ ROUTING DEBUG - Showing main dashboard")
            return create_main_dashboard()
        elif pathname == '/reports':
            content = [
                html.H2("Reports", style={"color": "#2D5E40"}),
                html.P("Comprehensive reporting and data export functionality.", style={"color": "#8B4513"})
            ]
            print("✅ ROUTING DEBUG - Showing reports page")
            return create_page_with_nav("Reports", content, "Reports")
        elif pathname == '/analytics':
            try:
                analytics_content = create_analytics_layout()
                if hasattr(analytics_content, 'children') and analytics_content.children:
                    content = analytics_content.children
                else:
                    content = [html.H2("Analytics"), html.P("Analytics functionality coming soon.")]
            except:
                content = [html.H2("Analytics"), html.P("Analytics functionality coming soon.")]
            print("✅ ROUTING DEBUG - Showing analytics page")
            return create_page_with_nav("Analytics", content, "Analytics")
        elif pathname == '/upload':
            content = [
                html.H2("Upload Data", style={"color": "#2D5E40"}),
                html.P("Upload waste collection data and reports.", style={"color": "#8B4513"})
            ]
            print("✅ ROUTING DEBUG - Showing upload page")
            return create_page_with_nav("Upload", content, "Upload")
        elif pathname == '/settings':
            content = [
                html.H2("Settings", style={"color": "#2D5E40"}),
                html.P("Customize your dashboard experience.", style={"color": "#8B4513"})
            ]
            print("✅ ROUTING DEBUG - Showing settings page")
            return create_page_with_nav("Settings", content, "Settings")
    else:
        # 404 page
        print(f"❌ ROUTING DEBUG - 404 page for pathname: {pathname}")
        return create_404_page()

print("✓ Navigation handlers module loaded successfully")