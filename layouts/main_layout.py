"""
layouts/main_layout.py - Updated main layout with global session management

This file defines the main layout with session store available globally.
"""

from dash import html, dcc
import dash_bootstrap_components as dbc

def create_main_layout():
    """
    Create the main application layout with global session management.
    
    Returns:
        dash component: The main layout structure with global session
    """
    # Define color constants
    DARK_GREEN = "#2D5E40"  # Primary green color
    
    layout = html.Div(className="main-app-container", children=[
        # Global components that need to be available everywhere
        dcc.Location(id='url', refresh=False),
        dcc.Store(id="user-session", storage_type="session", data={}),
        dcc.Store(id="current-user-info", storage_type="memory"),
        
        # Header hover trigger area
        html.Div(className="header-hover-area"),
        
        # Header Component - Will be conditionally rendered
        html.Header(id="main-header", className="header", children=[
            html.Div(className="container", children=[
                html.Div(className="header-content", children=[
                    # Logo & Title
                    html.Div(className="header-title", children=[
                        html.H1("Swaccha Andhra Dashboard")
                    ]),
                    
                    # Navigation - will be updated by callback
                    html.Nav(className="header-nav", children=[], id="nav-links"),
                    
                    # Right side actions - will be updated by callback
                    html.Div(className="header-actions", children=[], id="header-actions")
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
                            html.H2("Real-Time Monitoring Dashboard for Legacy Waste Reclamation", className="dashboard-subtitle")
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
        ),
        
        # Access check div for callbacks
        html.Div(id="page-access-check", children=[])
    ])
    
    return layout