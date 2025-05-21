"""
callbacks/routing_callback.py - Main routing callback

This file defines the main callback for URL routing to different pages.
"""

from dash import callback, Output, Input, html
from layouts.public_landing import create_public_dashboard
from layouts.report_layout import create_reports_layout
from layouts.analytics_layout import create_analytics_layout

@callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    """
    Route to the appropriate page layout based on URL.
    
    Args:
        pathname: Current URL pathname
        
    Returns:
        dash.components: The page layout for the requested route
    """
    # Route to appropriate layout based on pathname
    if pathname == '/':
        return create_public_dashboard()
    elif pathname == '/reports':
        return create_reports_layout()
    elif pathname == '/analytics':
        return create_analytics_layout()
    elif pathname == '/upload':
        return html.Div(className="container", children=[
            html.H2("Upload Data"),
            html.P("Upload waste collection data and reports."),
            html.Div(className="upload-section", children=[
                html.Div(className="upload-container", children=[
                    html.I(className="fas fa-cloud-upload-alt upload-icon"),
                    html.P("Drag and drop files here or click to browse"),
                    html.Button("Browse Files", className="btn btn-primary"),
                    html.P("Accepted formats: CSV, Excel, PDF", className="upload-formats")
                ])
            ]),
            # Demo info panels
            html.Div([
                html.H3("Information Panels", className="mt-4"),
                html.P("These color-coded panels can be used to display custom messages:"),
                
                # Yellow info panel
                html.Div(className="info-panel panel-yellow", children=[
                    html.Div(className="info-panel-title", children="Notification"),
                    html.Div(className="info-panel-body", children="This is a yellow notification panel for alerts and important updates.")
                ]),
                
                # Green info panel
                html.Div(className="info-panel panel-green", children=[
                    html.Div(className="info-panel-title", children="Success"),
                    html.Div(className="info-panel-body", children="This is a green panel to indicate successful operations or positive information.")
                ]),
                
                # Red info panel
                html.Div(className="info-panel panel-red", children=[
                    html.Div(className="info-panel-title", children="Warning"),
                    html.Div(className="info-panel-body", children="This is a red panel to highlight warnings or critical information.")
                ])
            ])
        ])
    elif pathname == '/settings':
        return html.Div(className="container", children=[
            html.H2("Settings"),
            html.P("Customize your dashboard experience."),
            html.Div(className="settings-section", children=[
                html.H3("Display Settings"),
                html.Div(className="settings-option", children=[
                    html.Label("Theme Mode"),
                    html.Div(className="settings-controls", children=[
                        html.Button("Light", id="light-theme", className="btn theme-btn", **{"data-theme": "light"}, n_clicks=0),
                        html.Button("Dark", id="dark-theme", className="btn theme-btn", **{"data-theme": "dark"}, n_clicks=0),
                        html.Button("Auto", id="auto-theme", className="btn theme-btn", **{"data-theme": "auto"}, n_clicks=0)
                    ])
                ]),
                html.Div(className="settings-option", children=[
                    html.Label("Navigation Bar"),
                    html.Div(className="settings-controls", children=[
                        html.Button("Show on Hover", id="nav-hover", className="btn btn-primary", n_clicks=0),
                        html.Button("Always Show", id="nav-show", className="btn btn-outline", n_clicks=0)
                    ])
                ]),
                
                # Info section with theme instructions
                html.Div(className="info-panel panel-yellow mt-4", children=[
                    html.Div(className="info-panel-title", children="Theme Settings Help"),
                    html.Div(className="info-panel-body", children=[
                        html.P("• Light: Always use light theme"),
                        html.P("• Dark: Always use dark theme"),
                        html.P("• Auto: Follow your device's system theme preference")
                    ])
                ])
            ]),
            
            # Hidden script to initialize theme buttons
            html.Script("""
                document.addEventListener('DOMContentLoaded', function() {
                    // Get current theme
                    const currentTheme = localStorage.getItem('theme') || 'light';
                    
                    // Update button states
                    const buttons = document.querySelectorAll('.theme-btn');
                    buttons.forEach(btn => {
                        if (btn.getAttribute('data-theme') === currentTheme) {
                            btn.classList.add('btn-primary');
                            btn.classList.remove('btn-outline');
                        } else {
                            btn.classList.add('btn-outline');
                            btn.classList.remove('btn-primary');
                        }
                    });
                    
                    // Add click handlers
                    document.getElementById('light-theme').addEventListener('click', function() {
                        window.switchTheme('light');
                    });
                    
                    document.getElementById('dark-theme').addEventListener('click', function() {
                        window.switchTheme('dark');
                    });
                    
                    document.getElementById('auto-theme').addEventListener('click', function() {
                        window.switchTheme('auto');
                    });
                    
                    // Navigation settings
                    document.getElementById('nav-hover').addEventListener('click', function() {
                        localStorage.setItem('navMode', 'hover');
                        this.classList.add('btn-primary');
                        this.classList.remove('btn-outline');
                        document.getElementById('nav-show').classList.add('btn-outline');
                        document.getElementById('nav-show').classList.remove('btn-primary');
                    });
                    
                    document.getElementById('nav-show').addEventListener('click', function() {
                        localStorage.setItem('navMode', 'show');
                        this.classList.add('btn-primary');
                        this.classList.remove('btn-outline');
                        document.getElementById('nav-hover').classList.add('btn-outline');
                        document.getElementById('nav-hover').classList.remove('btn-primary');
                    });
                });
            """)
        ])
    elif pathname == '/login':
        return html.Div(className="container", children=[
            html.H2("Login"),
            html.P("Please log in to access more features."),
            html.Div(className="form-container", children=[
                html.Div(className="form-group", children=[
                    html.Label("Username"),
                    html.Input(type="text", className="form-control")
                ]),
                html.Div(className="form-group", children=[
                    html.Label("Password"),
                    html.Input(type="password", className="form-control")
                ]),
                html.Button("Login", className="btn btn-primary"),
                html.A("Forgot Password?", href="#", className="form-link")
            ])
        ])
    else:
        # 404 page
        return html.Div(className="container", children=[
            html.Div(className="error-container", children=[
                html.H1("404", className="error-code"),
                html.H2("Page Not Found", className="error-title"),
                html.P("The page you requested does not exist."),
                html.A("Go to Dashboard", href="/", className="btn btn-primary")
            ])
        ])