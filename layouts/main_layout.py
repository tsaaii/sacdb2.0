"""
layouts/main_layout.py - Updated main layout for no-scroll design

This file defines the main layout with proper height distribution to ensure
header, content, and footer are all visible without scrolling.
"""

from dash import html, dcc
import dash_bootstrap_components as dbc

def create_main_layout():
    """
    Create the main application layout with no-scroll design.
    
    Returns:
        dash component: The main layout structure optimized for viewport fitting
    """
    # Define color constants
    DARK_GREEN = "#2D5E40"  # Primary green color
    
    layout = html.Div(className="main-app-container", children=[
        # URL Routing
        dcc.Location(id='url', refresh=False),
        
        # Header hover trigger area
        html.Div(className="header-hover-area"),
        
        # Header Component - Fixed and compact
        html.Header(className="header", children=[
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
                        # Clock display
                        html.Div(id="header-clock", className="clock-display"),
                        
                        # Login button
                        html.A("Login", href="/login", className="btn")
                    ])
                ])
            ])
        ]),
        
        # Compact Dashboard Title Banner
        html.Div(className="dashboard-title-banner", children=[
            html.Div(className="container", children=[
                html.Div(className="dashboard-title-wrapper", children=[
                    # Status indicators - compact and positioned
                    html.Div(className="dashboard-status-indicators", children=[
                        # Auto-refresh indicator
                        html.Div(className="refresh-indicator", children=[
                            html.I(id="refresh-indicator", className="fas fa-sync-alt fa-spin", 
                                  style={"color": DARK_GREEN, "fontSize": "0.9rem", "marginRight": "0.3rem"}),
                            html.Span("Auto-refresh", className="refresh-text")
                        ]),
                        
                        # Time display
                        html.Div(id="live-time", className="live-time")
                    ]),
                    
                    # Main title content with logos - more compact
                    html.Div(className="dashboard-title-content", children=[
                        # Left Logo
                        html.Img(src="/assets/img/left.png", alt="Left Logo", className="dashboard-logo left-logo"),
                        
                        # Title Container
                        html.Div(className="dashboard-title-container", children=[
                            html.H1("Swaccha Andhra", className="dashboard-main-title"),
                            html.H2("Real-Time Monitoring Dashboard for Legacy Waste Reclamation", className="dashboard-subtitle")  # Shortened subtitle
                        ]),
                        
                        # Right Logo
                        html.Img(src="/assets/img/right.png", alt="Right Logo", className="dashboard-logo right-logo")
                    ])
                ])
            ])
        ]),
        
        # Main content - flexible height
        html.Main(className="dashboard-main-content", children=[
            html.Div(id='page-content', className="page-content-wrapper")
        ]),
        
        # Compact Footer
        html.Footer(className="footer", children=[
            html.Div(className="container", children=[
                html.Div(className="footer-content", children=[

                    # Footer Links - more compact
                    html.Div(className="footer-links", children=[
                        html.A("About", href="/about", className="footer-link"),
                        html.A("Help", href="/help", className="footer-link"),
                        html.A("Contact", href="/contact", className="footer-link")
                    ]),
                    
                    # Copyright
                    html.Div(className="footer-copyright", children=[
                        "© 2025 Advitia Labs"
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