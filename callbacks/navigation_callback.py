"""
callbacks/navigation_callback.py - Fixed navigation callbacks with consolidated outputs

This file consolidates all navigation updates into a single callback to avoid duplicate outputs.
"""

from dash import callback, Output, Input, State, html, no_update
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

@callback(
    [Output('nav-links', 'children'),
     Output('header-actions', 'children')],
    [Input('url', 'pathname'),
     Input('user-session', 'data'),
     Input('refresh-interval', 'n_intervals')],  # Added refresh interval to update auth status
    prevent_initial_call=False  # Allow initial call to set up navigation
)
def update_navigation_consolidated(pathname, session_data, n_intervals):
    """
    Consolidated callback that handles all navigation updates.
    This is the ONLY callback that should update nav-links and header-actions.
    """
    
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
    public_routes = ['/', '/login']
    is_public_page = pathname in public_routes
    
    if not is_auth or is_public_page:
        # Public page - show login option
        nav_links = []
        
        if OAUTH_AVAILABLE:
            # Google OAuth login button
            login_button = html.A(
                [
                    html.I(className="fab fa-google", style={"marginRight": "0.5rem"}),
                    "Login with Google"
                ],
                href="/auth/login",
                className="btn btn-primary",
                style={"fontSize": "0.9rem"}
            )
        else:
            # Regular login button
            login_button = html.A(
                "Login", 
                href="/login", 
                className="btn"
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