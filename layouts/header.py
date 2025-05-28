"""
layouts/header.py - Header component

This file defines the header component with navigation and status indicators.
"""

from dash import html

def create_header():
    """
    Create the header component with navigation and auto-refresh indicator.
    
    Returns:
        dash component: The header component
    """
    header = html.Header(className="header", children=[
        html.Div(className="container", children=[
            html.Div(className="header-content", children=[
                # Logo & Title
                html.Div(className="header-title", children=[
                    html.H1("Swaccha Andhra Dashboard")
                ]),
                
                # Navigation
                html.Nav(className="header-nav", children=[
                    html.A("Dashboard", href="/", className="header-nav-link"),
                    html.A("Reports", href="/reports", className="header-nav-link"),
                    html.A("Analytics", href="/analytics", className="header-nav-link"),
                    html.A("Upload", href="/upload", className="header-nav-link"),
                    html.A("Settings", href="/settings", className="header-nav-link")
                ], id="nav-links"),
                
                # Right side actions
                html.Div(className="header-actions", children=[
                    # Auto-refresh indicator
                    html.Div(className="auto-refresh-indicator", children=[
                        html.I(className="fas fa-sync-alt"),
                        html.Span("Auto-refreshing")
                    ]),
                    
                    # Clock display
                    html.Div(id="header-clock", className="clock-display"),
                    
                    # Login button
                    html.A("Login", href="/login", className="btn")
                ])
            ])
        ])
    ])
    
    return header