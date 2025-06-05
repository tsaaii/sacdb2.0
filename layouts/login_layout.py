"""
layouts/login_layout.py - Updated login layout with Google OAuth support

This file updates your existing login layout to support Google OAuth
while maintaining the current design and fallback options.
"""

from dash import html, dcc
import dash_bootstrap_components as dbc

def create_login_layout():
    """
    Create the login page layout with Google OAuth integration.
    Maintains your existing design while adding OAuth support.
    """
    
    # Check if OAuth is available
    try:
        from auth.google_oauth import oauth
        OAUTH_AVAILABLE = True
    except ImportError:
        OAUTH_AVAILABLE = False
    
    return html.Div(className="login-page-container", children=[
        # Login form container
        html.Div(className="login-container", children=[
            # Logo section (keeping your existing design)
            html.Div(className="login-logo-section", children=[
                html.Img(
                    src="/assets/img/right.png", 
                    alt="Swaccha Andhra Logo",
                    className="login-logo"
                ),
                html.H1("Swaccha Andhra", className="login-title"),
                html.P("Waste Management Dashboard", className="login-subtitle")
            ]),
            
            # Alert for login errors (keeping your existing alert system)
            html.Div(id="login-alert-container", children=[
                dbc.Alert(
                    "Invalid credentials. Please try again.",
                    id="login-alert",
                    dismissable=True,
                    is_open=False,
                    color="danger",
                    className="login-alert"
                )
            ]),
            
            # Main login content - changes based on OAuth availability
            html.Div(id="login-form", children=[
                create_oauth_login() if OAUTH_AVAILABLE else create_fallback_login()
            ])
        ]),
        
        # Footer section (keeping your existing footer)
        html.Footer(className="login-page-footer", children=[
            html.P("© 2025 Advitia Labs • Made in Andhra Pradesh", 
                   className="footer-text")
        ])
    ], style={
        "backgroundColor": "#FFFBF5",
        "minHeight": "100vh",
        "display": "flex",
        "flexDirection": "column",
        "justifyContent": "space-between"
    })

def create_oauth_login():
    """Create Google OAuth login interface"""
    return html.Div(className="oauth-login-form", children=[
        # Main OAuth login button
        html.Div(style={"textAlign": "center", "marginBottom": "2rem"}, children=[
            html.A(
                [
                    html.I(className="fab fa-google", style={
                        "fontSize": "1.5rem", 
                        "marginRight": "1rem",
                        "color": "#4285F4"
                    }),
                    html.Span("Continue with Google", style={"fontSize": "1.1rem"})
                ],
                href="/auth/login",
                className="oauth-login-button",
                style={
                    "display": "inline-flex",
                    "alignItems": "center",
                    "justifyContent": "center",
                    "width": "100%",
                    "padding": "1rem 2rem",
                    "backgroundColor": "white",
                    "color": "#2D5E40",
                    "border": "2px solid #E8E4D0",
                    "borderRadius": "12px",
                    "textDecoration": "none",
                    "fontWeight": "600",
                    "transition": "all 0.3s ease",
                    "boxShadow": "0 2px 8px rgba(0, 0, 0, 0.1)"
                },
                id="google-login-btn"
            )
        ]),
        
        # Security and access information
        html.Div(className="oauth-info-section", children=[
            # Access information
            html.Div(style={
                "backgroundColor": "#F8F4E6",
                "padding": "1.5rem",
                "borderRadius": "8px",
                "marginBottom": "1.5rem",
                "border": "1px solid #E8E4D0"
            }, children=[
                html.Div(style={"display": "flex", "alignItems": "center", "marginBottom": "1rem"}, children=[
                    html.I(className="fas fa-shield-alt", style={"color": "#4A7E64", "marginRight": "0.5rem", "fontSize": "1.2rem"}),
                    html.H4("Authorized Access Only", style={"margin": "0", "color": "#2D5E40", "fontSize": "1rem"})
                ]),
                html.P("This dashboard requires authorized access. Only approved email addresses can log in.", 
                       style={"margin": "0", "color": "#8B4513", "fontSize": "0.9rem"})
            ]),
            
            # What happens after login
            html.Div(style={"marginBottom": "1.5rem"}, children=[
                html.H4("After logging in, you'll have access to:", style={"color": "#2D5E40", "marginBottom": "1rem", "fontSize": "1rem"}),
                html.Ul(style={"paddingLeft": "1.5rem", "color": "#8B4513"}, children=[
                    html.Li("Real-time waste management data"),
                    html.Li("Analytics and reporting tools"),
                    html.Li("Progress tracking and insights"),
                    html.Li("Data upload and management features")
                ])
            ]),
            
            # Contact information
            html.Div(style={
                "textAlign": "center",
                "padding": "1rem",
                "backgroundColor": "rgba(45, 94, 64, 0.1)",
                "borderRadius": "8px"
            }, children=[
                html.P([
                    html.I(className="fas fa-envelope", style={"marginRight": "0.5rem"}),
                    "Need access? Contact the administrator at ",
                    html.A("admin@advitialabs.com", href="mailto:admin@advitialabs.com", 
                           style={"color": "#2D5E40", "fontWeight": "600"})
                ], style={"margin": "0", "fontSize": "0.9rem", "color": "#8B4513"})
            ])
        ])
    ])

def create_fallback_login():
    """Create fallback login form when OAuth is not available"""
    return html.Div(className="fallback-login-form", children=[
        # Warning about OAuth not being available
        html.Div(className="alert alert-info", style={"marginBottom": "1.5rem"}, children=[
            html.I(className="fas fa-info-circle", style={"marginRight": "0.5rem"}),
            "Google OAuth is not configured. Using fallback authentication."
        ]),
        
        # Traditional login form (keeping your existing design)
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
            
            # Test credentials info
            html.Div(className="test-credentials", style={
                "marginTop": "1.5rem",
                "padding": "1rem",
                "backgroundColor": "#F8F4E6",
                "borderRadius": "8px",
                "border": "1px solid #E8E4D0"
            }, children=[
                html.H5("Test Credentials:", style={"color": "#2D5E40", "marginBottom": "0.5rem"}),
                html.P("Username: admin, Password: password123", style={"margin": "0", "fontSize": "0.9rem", "color": "#8B4513"}),
                html.P("Username: test, Password: test123", style={"margin": "0", "fontSize": "0.9rem", "color": "#8B4513"})
            ])
        ])
    ])

# Additional CSS for OAuth login button hover effects
OAUTH_LOGIN_CSS = """
<style>
.oauth-login-button:hover {
    background-color: #F8F4E6 !important;
    border-color: #2D5E40 !important;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
}

.oauth-login-button:active {
    transform: translateY(0);
}

.oauth-info-section {
    animation: fadeIn 0.5s ease-in;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Enhanced styling for the fallback form */
.fallback-login-form .login-input:focus {
    border-color: #2D5E40;
    box-shadow: 0 0 0 3px rgba(45, 94, 64, 0.1);
}

.test-credentials {
    border-left: 4px solid #F2C94C;
}
</style>
"""