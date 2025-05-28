"""
callbacks/navigation_callback.py - Updated navigation callbacks with conditional header

This file defines callbacks for conditional navigation based on authentication status.
"""

from dash import callback, Output, Input, State, html, no_update
from dash.exceptions import PreventUpdate

# Callback to handle conditional navigation based on current page and session
@callback(
    [Output('nav-links', 'children'),
     Output('header-actions', 'children')],
    [Input('url', 'pathname'),
     Input('user-session', 'data')]
)
def update_conditional_navigation(pathname, session_data):
    """
    Update navigation and header actions based on current page and authentication status.
    
    Args:
        pathname: Current URL pathname
        session_data: User session data
        
    Returns:
        tuple: (navigation_links, header_actions)
    """
    # Check if user is authenticated
    is_authenticated = session_data and session_data.get('authenticated', False)
    
    # Public routes that don't require authentication
    public_routes = ['/', '/login']
    is_public_page = pathname in public_routes
    
    if not is_authenticated or is_public_page:
        # Public page or unauthenticated - show only login option
        nav_links = []  # No navigation links on public page
        
        header_actions = [
            # Clock display
            html.Div(id="header-clock", className="clock-display"),
            # Login button only
            html.A("Login", href="/login", className="btn")
        ]
    else:
        # Authenticated pages - show full navigation
        nav_links_data = [
            {"title": "Dashboard", "path": "/main"},
            {"title": "Reports", "path": "/reports"},
            {"title": "Analytics", "path": "/analytics"},
            {"title": "Upload", "path": "/upload"},
            {"title": "Settings", "path": "/settings"}
        ]
        
        # Create navigation links with active class for current path
        nav_links = []
        for link in nav_links_data:
            # Determine if this link should be active
            is_active = pathname == link["path"]
            
            # Create link component with appropriate active class
            nav_links.append(
                html.A(
                    link["title"], 
                    href=link["path"], 
                    className=f"header-nav-link {'active' if is_active else ''}"
                )
            )
        
        header_actions = [
            # Clock display
            html.Div(id="header-clock", className="clock-display"),
            # Show username if available
            html.Span(f"Welcome, {session_data.get('username', 'User')}", 
                     style={"color": "#FEFEFE", "marginRight": "1rem", "fontSize": "0.9rem"}),
            # Logout button for authenticated users
            html.Button("Logout", id="logout-btn", className="btn btn-accent", n_clicks=0)
        ]
    
    return nav_links, header_actions