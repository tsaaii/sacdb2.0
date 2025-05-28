"""
layouts/login_layout.py - Login page layout with authentication

This file defines the login page layout with logo and auth integration.
"""

from dash import html, dcc
import dash_bootstrap_components as dbc

def create_login_layout():
    """
    Create the login page layout with logo and authentication form.
    
    Returns:
        dash component: The complete login layout
    """
    
    return html.Div(className="login-page-container", children=[
        # Login form container
        html.Div(className="login-container", children=[
            # Logo section
            html.Div(className="login-logo-section", children=[
                html.Img(
                    src="/assets/img/logo.png", 
                    alt="Swaccha Andhra Logo",
                    className="login-logo"
                ),
                html.H1("Swaccha Andhra", className="login-title"),
                html.P("Waste Management Dashboard", className="login-subtitle")
            ]),
            
            # Alert for login errors
            html.Div(id="login-alert-container", children=[
                dbc.Alert(
                    "Invalid username or password. Please try again.",
                    id="login-alert",
                    dismissable=True,
                    is_open=False,
                    color="danger",
                    className="login-alert"
                )
            ]),
            
            # Login form
            html.Div(className="login-form", children=[
                # Username field
                html.Div(className="form-group", children=[
                    html.Label("Username", htmlFor="login-username", className="form-label"),
                    html.Div(className="input-group", children=[
                        html.I(className="fas fa-user input-icon"),
                        dcc.Input(
                            id="login-username",
                            type="text",
                            placeholder="Enter your username",
                            className="form-control login-input",
                            required=True
                        )
                    ])
                ]),
                
                # Password field
                html.Div(className="form-group", children=[
                    html.Label("Password", htmlFor="login-password", className="form-label"),
                    html.Div(className="input-group", children=[
                        html.I(className="fas fa-lock input-icon"),
                        dcc.Input(
                            id="login-password",
                            type="password",
                            placeholder="Enter your password",
                            className="form-control login-input",
                            required=True
                        )
                    ])
                ]),
                
                # Login button
                html.Button(
                    [
                        html.I(className="fas fa-sign-in-alt", style={"marginRight": "0.5rem"}),
                        "Log In to Dashboard"
                    ],
                    id="login-submit-btn",
                    className="btn btn-primary login-button",
                    n_clicks=0
                ),
                
                # Forgot password link
                html.Div(className="login-footer", children=[
                    html.A(
                        "Forgot your password?",
                        href="#",
                        className="forgot-password-link"
                    )
                ])
            ])
        ]),
        
        # Footer section
        html.Footer(className="login-page-footer", children=[
            html.P("© 2025 Advitia Labs • Made in Andhra Pradesh", 
                   className="footer-text")
        ]),
        
        # Hidden div to store login status
        html.Div(id="login-status", style={"display": "none"}),
        
        # Store for user session
        dcc.Store(id="user-session", storage_type="session"),
        
        # Store for login success trigger
        dcc.Store(id="login-success-trigger"),
        
        # Redirect components
        dcc.Location(id="login-redirect", refresh=True),
        dcc.Location(id="auth-redirect", refresh=True),
        
        # Dummy div for clientside callback
        html.Div(id="login-redirect-dummy", style={"display": "none"})
    ], style={
        "backgroundColor": "#FFFBF5",
        "minHeight": "100vh",
        "display": "flex",
        "flexDirection": "column",
        "justifyContent": "space-between"
    })