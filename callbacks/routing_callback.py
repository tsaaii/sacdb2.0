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
                        html.Button("Light", className="btn btn-primary"),
                        html.Button("Dark", className="btn btn-outline"),
                        html.Button("Auto", className="btn btn-outline")
                    ])
                ])
            ])
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