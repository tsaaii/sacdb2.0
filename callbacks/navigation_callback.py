"""
callbacks/navigation_callback.py - Navigation callbacks

This file defines callbacks related to navigation and routing.
"""

from dash import callback, Output, Input, State, html, no_update
from dash.exceptions import PreventUpdate

# Callback to handle active navigation link highlighting
@callback(
    Output('nav-links', 'children'),
    [Input('url', 'pathname')]
)
def update_active_link(pathname):
    """
    Update the active link in the navigation based on current URL.
    
    Args:
        pathname: Current URL pathname
        
    Returns:
        list: Updated navigation link components
    """
    # Define navigation links and their paths
    nav_links = [
        {"title": "Dashboard", "path": "/"},
        {"title": "Reports", "path": "/reports"},
        {"title": "Analytics", "path": "/analytics"},
        {"title": "Upload", "path": "/upload"},
        {"title": "Settings", "path": "/settings"}
    ]
    
    # Create navigation links with active class for current path
    links = []
    for link in nav_links:
        # Determine if this link should be active
        is_active = pathname == link["path"] or (pathname == "/" and link["path"] == "/")
        
        # Create link component with appropriate active class
        links.append(
            html.A(
                link["title"], 
                href=link["path"], 
                className=f"header-nav-link {'active' if is_active else ''}"
            )
        )
    
    return links