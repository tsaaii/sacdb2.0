"""
callbacks/routing_callback.py - Updated routing callback with public vs authenticated routes

This file defines routing for both public and authenticated pages.
"""

from dash import callback, Output, Input, html

# Import existing layouts
try:
    from layouts.public_landing import create_public_dashboard
except ImportError:
    def create_public_dashboard():
        return html.Div(className="container", children=[
            html.H2("Welcome to Swaccha Andhra Dashboard"),
            html.P("Please login to access the full dashboard.")
        ])

try:
    from layouts.analytics_layout import create_analytics_layout
except ImportError:
    def create_analytics_layout():
        return html.Div(className="container", children=[
            html.H2("Analytics"),
            html.P("Analytics functionality will be available soon.")
        ])

def create_main_dashboard():
    """Create the main authenticated dashboard"""
    return html.Div(className="container", children=[
        # Page header
        html.Div(className="page-header", style={"margin": "0.5rem 0"}, children=[
            html.H2("Main Dashboard", style={"margin": "0 0 0.25rem 0"}),
            html.P("Full access dashboard with all features.", style={"margin": "0", "fontSize": "0.9rem"})
        ]),
        
        # Main content in a grid layout
        html.Div(style={
            "display": "grid",
            "gridTemplateColumns": "repeat(auto-fit, minmax(250px, 1fr))",
            "gap": "1rem",
            "margin": "1rem 0"
        }, children=[
            # Real-time Monitoring Card
            html.Div(style={
                "background": "white",
                "borderRadius": "10px",
                "padding": "1rem",
                "boxShadow": "0 2px 8px rgba(0, 0, 0, 0.06)",
                "border": "1px solid #E8E4D0"
            }, children=[
                html.Div(style={"display": "flex", "alignItems": "center", "marginBottom": "0.5rem"}, children=[
                    html.I(className="fas fa-tachometer-alt", style={"color": "#4A7E64", "marginRight": "0.5rem"}),
                    html.H3("Live Monitoring", style={"margin": "0", "fontSize": "1rem", "color": "#2D5E40"})
                ]),
                html.P("Real-time waste collection tracking", style={"margin": "0", "color": "#8B4513", "fontSize": "0.9rem"}),
                html.Div(style={"marginTop": "0.5rem"}, children=[
                    html.Div("• Active vehicles: 12", style={"fontSize": "0.8rem", "color": "#4A7E64"}),
                    html.Div("• Collection in progress: 5", style={"fontSize": "0.8rem", "color": "#4A7E64"}),
                    html.Div("• Daily target: 87% complete", style={"fontSize": "0.8rem", "color": "#4A7E64"})
                ])
            ]),
            
            # Data Management Card
            html.Div(style={
                "background": "white",
                "borderRadius": "10px",
                "padding": "1rem",
                "boxShadow": "0 2px 8px rgba(0, 0, 0, 0.06)",
                "border": "1px solid #E8E4D0"
            }, children=[
                html.Div(style={"display": "flex", "alignItems": "center", "marginBottom": "0.5rem"}, children=[
                    html.I(className="fas fa-database", style={"color": "#F2C94C", "marginRight": "0.5rem"}),
                    html.H3("Data Management", style={"margin": "0", "fontSize": "1rem", "color": "#2D5E40"})
                ]),
                html.P("Upload and manage waste collection data", style={"margin": "0", "color": "#8B4513", "fontSize": "0.9rem"}),
                html.Div(style={"marginTop": "1rem"}, children=[
                    html.A("Upload Data", href="/upload", className="btn btn-primary", style={"fontSize": "0.8rem", "width": "100%"})
                ])
            ]),
            
            # Advanced Analytics Card
            html.Div(style={
                "background": "white",
                "borderRadius": "10px",
                "padding": "1rem",
                "boxShadow": "0 2px 8px rgba(0, 0, 0, 0.06)",
                "border": "1px solid #E8E4D0"
            }, children=[
                html.Div(style={"display": "flex", "alignItems": "center", "marginBottom": "0.5rem"}, children=[
                    html.I(className="fas fa-chart-line", style={"color": "#C74A3C", "marginRight": "0.5rem"}),
                    html.H3("Advanced Analytics", style={"margin": "0", "fontSize": "1rem", "color": "#2D5E40"})
                ]),
                html.P("Detailed insights and trend analysis", style={"margin": "0", "color": "#8B4513", "fontSize": "0.9rem"}),
                html.Div(style={"marginTop": "1rem"}, children=[
                    html.A("View Analytics", href="/analytics", className="btn btn-outline", style={"fontSize": "0.8rem", "width": "100%"})
                ])
            ]),
            
            # Reports Card
            html.Div(style={
                "background": "white",
                "borderRadius": "10px",
                "padding": "1rem",
                "boxShadow": "0 2px 8px rgba(0, 0, 0, 0.06)",
                "border": "1px solid #E8E4D0"
            }, children=[
                html.Div(style={"display": "flex", "alignItems": "center", "marginBottom": "0.5rem"}, children=[
                    html.I(className="fas fa-file-alt", style={"color": "#8B4513", "marginRight": "0.5rem"}),
                    html.H3("Reports", style={"margin": "0", "fontSize": "1rem", "color": "#2D5E40"})
                ]),
                html.P("Generate and download reports", style={"margin": "0", "color": "#8B4513", "fontSize": "0.9rem"}),
                html.Div(style={"marginTop": "1rem"}, children=[
                    html.A("View Reports", href="/reports", className="btn", style={"fontSize": "0.8rem", "width": "100%"})
                ])
            ])
        ]),
        
        # Key Performance Indicators
        html.Div(style={
            "background": "white",
            "borderRadius": "10px",
            "padding": "1.5rem",
            "boxShadow": "0 2px 8px rgba(0, 0, 0, 0.06)",
            "border": "1px solid #E8E4D0",
            "marginTop": "1.5rem"
        }, children=[
            html.H3("Today's Performance", style={"color": "#2D5E40", "marginBottom": "1rem"}),
            html.Div(style={"display": "grid", "gridTemplateColumns": "repeat(auto-fit, minmax(150px, 1fr))", "gap": "1rem"}, children=[
                html.Div(style={"textAlign": "center"}, children=[
                    html.Div("385", style={"fontSize": "1.5rem", "fontWeight": "700", "color": "#8B4513"}),
                    html.Div("MT Collected Today", style={"fontSize": "0.75rem", "color": "#A67C52"})
                ]),
                html.Div(style={"textAlign": "center"}, children=[
                    html.Div("12", style={"fontSize": "1.5rem", "fontWeight": "700", "color": "#8B4513"}),
                    html.Div("Active Vehicles", style={"fontSize": "0.75rem", "color": "#A67C52"})
                ]),
                html.Div(style={"textAlign": "center"}, children=[
                    html.Div("87%", style={"fontSize": "1.5rem", "fontWeight": "700", "color": "#4A7E64"}),
                    html.Div("Target Achievement", style={"fontSize": "0.75rem", "color": "#A67C52"})
                ]),
                html.Div(style={"textAlign": "center"}, children=[
                    html.Div("5", style={"fontSize": "1.5rem", "fontWeight": "700", "color": "#8B4513"}),
                    html.Div("Areas Covered", style={"fontSize": "0.75rem", "color": "#A67C52"})
                ]),
                html.Div(style={"textAlign": "center"}, children=[
                    html.Div("95%", style={"fontSize": "1.5rem", "fontWeight": "700", "color": "#4A7E64"}),
                    html.Div("Machine Efficiency", style={"fontSize": "0.75rem", "color": "#A67C52"})
                ])
            ])
        ])
    ])

def create_reports_layout():
    """Create reports layout"""
    return html.Div(className="container", children=[
        html.H2("Reports"),
        html.P("Comprehensive reporting and data export functionality."),
        html.Div(className="content-section", children=[
            html.H3("Available Reports"),
            html.Ul(children=[
                html.Li("Daily Collection Summary"),
                html.Li("Weekly Performance Report"),
                html.Li("Monthly Analytics"),
                html.Li("Equipment Utilization"),
                html.Li("Area-wise Progress")
            ])
        ])
    ])

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
    if pathname == '/' or pathname is None:
        # Public landing page
        return create_public_dashboard()
    elif pathname == '/main':
        # Main authenticated dashboard
        return create_main_dashboard()
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
                        html.Button("Light", id="light-theme", className="btn btn-primary", n_clicks=0),
                        html.Button("Dark", id="dark-theme", className="btn btn-outline", n_clicks=0),
                        html.Button("Auto", id="auto-theme", className="btn btn-outline", n_clicks=0)
                    ])
                ]),
                html.Div(className="settings-option", children=[
                    html.Label("Navigation Bar"),
                    html.Div(className="settings-controls", children=[
                        html.Button("Show on Hover", id="nav-hover", className="btn btn-primary", n_clicks=0),
                        html.Button("Always Show", id="nav-show", className="btn btn-outline", n_clicks=0)
                    ])
                ])
            ])
        ])
    elif pathname == '/login':
        # Import login layout
        try:
            from layouts.login_layout import create_login_layout
            return create_login_layout()
        except ImportError:
            # Fallback login page if login_layout.py is not available
            return html.Div(className="container", children=[
                html.H2("Login"),
                html.P("Please log in to access the full dashboard features."),
                html.Div(className="form-container", children=[
                    html.Div(className="form-group", children=[
                        html.Label("Username"),
                        html.Input(type="text", className="form-control", placeholder="Enter username")
                    ]),
                    html.Div(className="form-group", children=[
                        html.Label("Password"),
                        html.Input(type="password", className="form-control", placeholder="Enter password")
                    ]),
                    html.A("Login to Dashboard", href="/main", className="btn btn-primary", 
                           style={"width": "100%", "textAlign": "center", "display": "block"}),
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
                html.A("Go to Home", href="/", className="btn btn-primary")
            ])
        ])