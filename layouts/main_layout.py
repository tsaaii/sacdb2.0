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
        
        # Header hover trigger area
        html.Div(className="header-hover-area"),
        
        # Header Component
        html.Header(className="header", children=[
            html.Div(className="container", children=[
                html.Div(className="header-content", children=[
                    # Logo & Title
                    html.Div(className="header-title", children=[
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
        
        # Dashboard Title Banner with Logos
        html.Div(className="dashboard-title-banner", children=[
            html.Div(className="container", children=[
                html.Div(className="dashboard-title-content", children=[
                    # Left Logo
                    html.Img(src="/assets/img/left.png", alt="Left Logo", className="dashboard-logo left-logo"),
                    
                    # Title Container
                    html.Div(className="dashboard-title-container", children=[
                        html.H1("Swaccha Andhra", className="dashboard-main-title"),
                        html.H2("Waste Remediation Project", className="dashboard-subtitle"),
                        html.H3("Real-time Monitoring Dashboard", className="dashboard-subheading"),
                        
                        # Status bar with auto-refresh and timestamp
                        html.Div(className="dashboard-status-bar", children=[
                            # Auto-refresh indicator
                            html.Div(className="auto-refresh-indicator", children=[
                                html.I(className="fas fa-sync-alt"),
                                html.Span("Auto-refreshing")
                            ]),
                            
                            # Update timestamp
                            html.Div(id="dashboard-timestamp", className="dashboard-timestamp", children=[
                                html.I(className="far fa-clock"),
                                html.Span("Last updated: "),
                                html.Span(id="update-time")
                            ])
                        ])
                    ]),
                    
                    # Right Logo
                    html.Img(src="/assets/img/right.png", alt="Right Logo", className="dashboard-logo right-logo")
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
                        html.Span("Swaccha Andhra Corporation")
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
        ),
        
        # Data refresh interval
        dcc.Interval(
            id='refresh-interval',
            interval=60000,  # 1 minute
            n_intervals=0
        )
    ])
    
    return layout