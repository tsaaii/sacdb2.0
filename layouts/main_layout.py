"""
layouts/main_layout.py - Main layout structure

This file defines the common layout elements used across the application.
"""

from dash import html, dcc
import dash_bootstrap_components as dbc

def create_main_layout():
    """
    Create the main application layout structure.
    
    Returns:
        dash component: The main layout structure with header, content area, and footer
    """
    layout = html.Div([
        # URL Routing
        dcc.Location(id='url', refresh=False),
        
        # Header Component
        html.Header(className="header", children=[
            html.Div(className="container", children=[
                html.Div(className="header-content", children=[
                    # Logo & Title
                    html.Div(className="header-title", children=[
                        html.Img(src="/assets/img/logo.png", alt="Swaccha Andhra", className="header-logo"),
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
                        # Clock display
                        html.Div(id="header-clock", className="clock-display"),
                        
                        # Login button
                        html.A("Login", href="/login", className="btn")
                    ])
                ])
            ])
        ]),
        
        # Main content
        html.Main(id='page-content'),
        
        # Footer component
        html.Footer(className="footer", children=[
            html.Div(className="container", children=[
                html.Div(className="footer-content", children=[
                    # Logo
                    html.Div(className="footer-logo", children=[
                        html.Img(src="/assets/img/logo-white.png", alt="Swaccha Andhra"),
                        html.Span("Swaccha Andhra")
                    ]),
                    
                    # Links
                    html.Div(className="footer-links", children=[
                        html.A("About", href="/about", className="footer-link"),
                        html.A("Help", href="/help", className="footer-link"),
                        html.A("Contact", href="/contact", className="footer-link"),
                        html.A("Policy", href="/policy", className="footer-link")
                    ]),
                    
                    # Copyright
                    html.Div(className="footer-copyright", children=[
                        "© 2025 Advitia Labs • Made in Andhra Pradesh"
                    ])
                ])
            ])
        ]),
        
        # Clock interval for updating time
        dcc.Interval(
            id='clock-interval',
            interval=1000,  # 1 second
            n_intervals=0
        )
    ])
    
    return layout