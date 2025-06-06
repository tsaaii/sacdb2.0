"""
callbacks/navigation_callback.py - Fixed navigation callbacks with error handling

This file consolidates all navigation updates and handles missing components gracefully.
"""

from dash import callback, Output, Input, State, html, no_update, clientside_callback
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

@callback(
    [Output('nav-links', 'children', allow_duplicate=True),
     Output('header-actions', 'children', allow_duplicate=True)],
    [Input('url', 'pathname'),
     Input('user-session', 'data'),
     Input('refresh-interval', 'n_intervals')],
    prevent_initial_call=False
)
def update_navigation_safe(pathname, session_data, n_intervals):
    """
    Safely update navigation components only when they exist.
    """
    try:
        # Check authentication from multiple sources
        oauth_authenticated = is_authenticated() if OAUTH_AVAILABLE else False
        dash_authenticated = session_data and session_data.get('authenticated', False)
        
        is_auth = oauth_authenticated or dash_authenticated
        
        # Get user info
        if OAUTH_AVAILABLE and oauth_authenticated:
            current_user = get_current_user()
        else:
            current_user = session_data
        
        # Public routes
        public_routes = ['/', '/login', '/auth/login', '/auth/callback']
        is_public_page = pathname in public_routes
        
        if not is_auth or is_public_page:
            # Public page - minimal navigation
            nav_links = []
            
            # Simple Login button for header (goes to login page with all options)
            login_button = html.A(
                "Login", 
                href="/login", 
                className="btn btn-primary",
                style={"fontSize": "0.9rem"}
            )
            
            header_actions = [
                html.Div(id="header-clock", className="clock-display"),
                login_button
            ]
        else:
            # Authenticated user - show full navigation
            nav_links_data = [
                {"title": "Dashboard", "path": "/main"},
                {"title": "Reports", "path": "/reports"},
                {"title": "Analytics", "path": "/analytics"},
                {"title": "Upload", "path": "/upload"},
                {"title": "Settings", "path": "/settings"}
            ]
            
            nav_links = []
            for link in nav_links_data:
                is_active = pathname == link["path"]
                nav_links.append(
                    html.A(
                        link["title"], 
                        href=link["path"], 
                        className=f"header-nav-link {'active' if is_active else ''}"
                    )
                )
            
            # User info display
            user_name = "User"
            user_email = ""
            user_picture = None
            
            if current_user:
                user_name = current_user.get('name', current_user.get('username', 'User'))
                user_email = current_user.get('email', '')
                user_picture = current_user.get('picture')
            
            # Create user profile section
            user_profile = []
            if user_picture:
                user_profile.append(
                    html.Img(
                        src=user_picture,
                        style={
                            "width": "28px",
                            "height": "28px", 
                            "borderRadius": "50%",
                            "marginRight": "0.5rem"
                        }
                    )
                )
            
            user_profile.append(
                html.Span(
                    user_name.split()[0] if user_name else "User",
                    style={
                        "color": "#FEFEFE",
                        "fontSize": "0.9rem",
                        "marginRight": "1rem"
                    }
                )
            )
            
            # Logout button
            if OAUTH_AVAILABLE:
                logout_href = "/auth/logout"
                logout_text = "Logout"
            else:
                logout_href = "/"
                logout_text = "Logout"
            
            header_actions = [
                html.Div(id="header-clock", className="clock-display"),
                html.Div(user_profile, style={"display": "flex", "alignItems": "center"}),
                html.A(logout_text, href=logout_href, className="btn btn-accent")
            ]
        
        return nav_links, header_actions
        
    except Exception as e:
        print(f"Navigation callback error: {e}")
        # Return safe defaults
        return [], [html.Div(id="header-clock", className="clock-display")]

# Clientside callback to safely check if navigation elements exist before updating
clientside_callback(
    """
    function(pathname, session_data, n_intervals) {
        // Check if navigation elements exist before allowing server callback
        const navLinks = document.getElementById('nav-links');
        const headerActions = document.getElementById('header-actions');
        
        if (!navLinks || !headerActions) {
            console.log('Navigation elements not found, skipping update');
            return window.dash_clientside.no_update;
        }
        
        // Elements exist, allow server callback to proceed
        return true;
    }
    """,
    Output('navigation-check', 'data'),
    [Input('url', 'pathname'),
     Input('user-session', 'data'),
     Input('refresh-interval', 'n_intervals')],
    prevent_initial_call=True
)

# Additional defensive callback for pages without navigation
@callback(
    Output('page-navigation-status', 'data'),
    Input('url', 'pathname'),
    prevent_initial_call=True
)
def check_page_navigation_status(pathname):
    """
    Check if current page should have navigation elements.
    """
    pages_with_nav = ['/main', '/reports', '/analytics', '/upload', '/settings']
    return {'has_navigation': pathname in pages_with_nav}