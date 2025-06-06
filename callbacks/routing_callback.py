"""
callbacks/routing_callback.py - Simplified routing with only login alerts

This file handles page routing and login alerts only.
Session management is now handled in session_callback.py
"""

from dash import callback, Output, Input, State, html, dcc, no_update, callback_context
from dash.exceptions import PreventUpdate
import pandas as pd
import plotly.express as px
from datetime import date
from urllib.parse import parse_qs

# Import existing layouts with fallbacks
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

# Check if OAuth is available
try:
    from auth.google_oauth import get_current_user, is_authenticated
    OAUTH_AVAILABLE = True
except ImportError:
    OAUTH_AVAILABLE = False
    def get_current_user():
        return None
    def is_authenticated():
        return False

# [Include all the layout creation functions from the previous version]
# These remain the same...

def create_unauthorized_error_page():
    """Create unauthorized access error page"""
    # ... (same as before)
    return html.Div("Unauthorized Access - Contact Administrator")

def create_main_dashboard():
    """Create the main authenticated dashboard"""
    # ... (same as before - enhanced version)
    return html.Div(className="container", children=[
        html.H2("Main Dashboard"),
        html.P("Welcome to the main dashboard!")
    ])

def create_safe_login_layout():
    """Create a safe login layout with both OAuth and traditional options"""
    
    return html.Div(className="login-page-container", children=[
        html.Div(className="login-container", children=[
            html.Div(className="login-logo-section", children=[
                html.Img(
                    src="/assets/img/right.png", 
                    alt="Swaccha Andhra Logo",
                    className="login-logo",
                    style={"width": "80px", "height": "80px", "objectFit": "contain"}
                ),
                html.H1("Swaccha Andhra", className="login-title", 
                       style={"color": "#2D5E40", "marginBottom": "0.5rem"}),
                html.P("Waste Management Dashboard", className="login-subtitle",
                       style={"color": "#8B4513", "marginBottom": "1.5rem"})
            ]),
            
            # Alert for login errors using dbc.Alert
            html.Div(id="login-alert-container", children=[
                html.Div(
                    "",
                    id="login-alert",
                    style={"display": "none"},
                    className="alert"
                )
            ]),
            
            html.Div(id="login-form", children=[
                create_dual_login_options()
            ])
        ]),
        
        html.Footer(className="login-page-footer", children=[
            html.P("© 2025 Advitia Labs • Made in Andhra Pradesh", 
                   style={"color": "#8B4513", "fontSize": "0.8rem", "textAlign": "center"})
        ])
    ], style={
        "backgroundColor": "#FFFBF5",
        "minHeight": "100vh",
        "display": "flex",
        "flexDirection": "column",
        "justifyContent": "space-between",
        "padding": "2rem 1rem"
    })

def create_dual_login_options():
    """Create login interface with both OAuth and traditional options"""
    
    return html.Div(className="dual-login-container", children=[
        # Login options header
        html.Div(style={"textAlign": "center", "marginBottom": "2rem"}, children=[
            html.H3("Choose your login method", style={
                "color": "#2D5E40",
                "fontSize": "1.2rem",
                "fontWeight": "600",
                "marginBottom": "0.5rem"
            }),
            html.P("Use Google OAuth for quick access or traditional login", style={
                "color": "#8B4513",
                "fontSize": "0.9rem",
                "margin": "0"
            })
        ]),
        
        # Login methods container
        html.Div(className="login-methods-container", style={
            "display": "grid",
            "gridTemplateColumns": "1fr 1fr" if OAUTH_AVAILABLE else "1fr",
            "gap": "2rem",
            "marginBottom": "2rem"
        }, children=[
            # Google OAuth Section (if available)
            create_oauth_section() if OAUTH_AVAILABLE else html.Div(),
            
            # Traditional Login Section
            create_traditional_login_section()
        ]),
        
        # Security and access information
        create_login_info_section()
    ])

def create_oauth_section():
    """Create Google OAuth login section"""
    return html.Div(className="oauth-section", style={
        "padding": "1.5rem",
        "border": "2px solid #E8E4D0",
        "borderRadius": "12px",
        "backgroundColor": "#F8F4E6",
        "textAlign": "center"
    }, children=[
        html.H4("Google OAuth", style={"color": "#2D5E40", "marginBottom": "1rem"}),
        html.A("Continue with Google", href="/auth/login", style={
            "display": "inline-block",
            "padding": "0.875rem 1.5rem",
            "backgroundColor": "white",
            "color": "#2D5E40",
            "textDecoration": "none",
            "borderRadius": "8px",
            "fontWeight": "600"
        })
    ])

def create_traditional_login_section():
    """Create traditional username/password login section"""
    return html.Div(className="traditional-section", style={
        "padding": "1.5rem",
        "border": "2px solid #E8E4D0",
        "borderRadius": "12px",
        "backgroundColor": "white"
    }, children=[
        html.H4("Traditional Login", style={"color": "#2D5E40", "marginBottom": "1rem"}),
        
        # Username field
        html.Div(style={"marginBottom": "1rem"}, children=[
            html.Label("Username", style={"fontWeight": "600", "color": "#2D5E40", "display": "block"}),
            dcc.Input(
                id="login-username",
                type="text",
                placeholder="Enter your username",
                style={
                    "width": "100%",
                    "padding": "0.75rem",
                    "border": "2px solid #E8E4D0",
                    "borderRadius": "8px",
                    "marginTop": "0.5rem"
                }
            )
        ]),
        
        # Password field
        html.Div(style={"marginBottom": "1.5rem"}, children=[
            html.Label("Password", style={"fontWeight": "600", "color": "#2D5E40", "display": "block"}),
            dcc.Input(
                id="login-password",
                type="password",
                placeholder="Enter your password",
                style={
                    "width": "100%",
                    "padding": "0.75rem",
                    "border": "2px solid #E8E4D0",
                    "borderRadius": "8px",
                    "marginTop": "0.5rem"
                }
            )
        ]),
        
        # Login button
        html.Button("Login to Dashboard", id="login-submit-btn", n_clicks=0, style={
            "width": "100%",
            "padding": "0.875rem",
            "backgroundColor": "#2D5E40",
            "color": "white",
            "border": "none",
            "borderRadius": "8px",
            "fontWeight": "600",
            "cursor": "pointer"
        }),
        
        # Test credentials
        html.Div(style={
            "marginTop": "1rem",
            "padding": "0.75rem",
            "backgroundColor": "#F0F8FF",
            "borderRadius": "6px"
        }, children=[
            html.P("Test: admin / password123", style={"margin": "0", "fontSize": "0.8rem"}),
            html.P("Test: test / test123", style={"margin": "0", "fontSize": "0.8rem"})
        ])
    ])

def create_login_info_section():
    """Create information section"""
    return html.Div(style={
        "backgroundColor": "#F8F4E6",
        "padding": "1.5rem",
        "borderRadius": "8px",
        "marginTop": "1rem"
    }, children=[
        html.H4("Authorized Access Only", style={"color": "#2D5E40", "marginBottom": "1rem"}),
        html.P("Contact admin@advitialabs.com for access.", style={"margin": "0", "color": "#8B4513"})
    ])

# ====================== MAIN ROUTING CALLBACK ======================

@callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname'),
     Input('url', 'search')]
)
def display_page(pathname, search_params):
    """
    Route to the appropriate page layout.
    Session management is handled separately.
    """
    
    # Handle error parameters in URL
    if search_params:
        try:
            params = parse_qs(search_params.lstrip('?'))
            error_type = params.get('error', [None])[0]
            
            if error_type == 'unauthorized_email':
                return create_unauthorized_error_page()
                
        except Exception as e:
            print(f"Error parsing URL params: {e}")
    
    # Normal page routing
    if pathname == '/' or pathname is None:
        return create_public_dashboard()
    elif pathname == '/main':
        return create_main_dashboard()
    elif pathname == '/reports':
        return html.Div(className="container", children=[
            html.H2("Reports"),
            html.P("Comprehensive reporting and data export functionality.")
        ])
    elif pathname == '/analytics':
        return create_analytics_layout()
    elif pathname == '/upload':
        return html.Div(className="container", children=[
            html.H2("Upload Data"),
            html.P("Upload waste collection data and reports.")
        ])
    elif pathname == '/settings':
        return html.Div(className="container", children=[
            html.H2("Settings"),
            html.P("Customize your dashboard experience.")
        ])
    elif pathname == '/login':
        return create_safe_login_layout()
    else:
        # 404 page
        return html.Div(className="container", children=[
            html.Div(style={"textAlign": "center", "padding": "3rem 0"}, children=[
                html.H1("404", style={"fontSize": "6rem", "color": "#F2C94C"}),
                html.H2("Page Not Found", style={"color": "#2D5E40"}),
                html.A("Go to Home", href="/", style={
                    "backgroundColor": "#2D5E40", 
                    "color": "white", 
                    "padding": "0.75rem 1.5rem", 
                    "textDecoration": "none", 
                    "borderRadius": "8px"
                })
            ])
        ])

# ====================== LOGIN ALERTS ONLY ======================

@callback(
    [Output('login-alert', 'style'),
     Output('login-alert', 'children'),
     Output('login-alert', 'className')],
    [Input('login-submit-btn', 'n_clicks'),
     Input('url', 'search')],
    [State('login-username', 'value'),
     State('login-password', 'value')],
    prevent_initial_call=True
)
def handle_login_alerts(login_clicks, search_params, username, password):
    """
    Handle ONLY login alert messages.
    Session management is handled in session_callback.py
    """
    
    ctx = callback_context
    if not ctx.triggered:
        return {"display": "none"}, "", "alert"
    
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    # Handle login form validation
    if trigger_id == 'login-submit-btn' and login_clicks and login_clicks > 0:
        if not username or not password:
            return {
                "display": "block",
                "backgroundColor": "#fff3cd",
                "color": "#856404",
                "padding": "0.75rem",
                "borderRadius": "8px",
                "marginBottom": "1rem",
                "border": "1px solid #ffeaa7"
            }, "⚠️ Please enter both username and password.", "alert alert-warning"
        
        # Check credentials
        valid_users = {'admin': 'password123', 'user': 'password456', 'test': 'test123'}
        
        if username.strip() not in valid_users or valid_users[username.strip()] != password:
            return {
                "display": "block",
                "backgroundColor": "#f8d7da",
                "color": "#721c24",
                "padding": "0.75rem",
                "borderRadius": "8px",
                "marginBottom": "1rem",
                "border": "1px solid #f5c6cb"
            }, "❌ Invalid username or password. Please try again.", "alert alert-danger"
        
        # Success - hide alert (session callback handles redirect)
        return {"display": "none"}, "", "alert"
    
    # Handle URL error parameters
    elif trigger_id == 'url' and search_params:
        try:
            params = parse_qs(search_params.lstrip('?'))
            error_type = params.get('error', [None])[0]
            
            if error_type == 'unauthorized_email':
                return {
                    "display": "block",
                    "backgroundColor": "#fff3cd",
                    "color": "#856404",
                    "padding": "0.75rem",
                    "borderRadius": "8px",
                    "marginBottom": "1rem",
                    "border": "1px solid #ffeaa7"
                }, "⚠️ Access denied. Your email is not authorized.", "alert alert-warning"
            
            elif error_type == 'auth_failed':
                return {
                    "display": "block",
                    "backgroundColor": "#f8d7da",
                    "color": "#721c24",
                    "padding": "0.75rem",
                    "borderRadius": "8px",
                    "marginBottom": "1rem",
                    "border": "1px solid #f5c6cb"
                }, "❌ Authentication failed. Please try again.", "alert alert-danger"
                
        except Exception:
            pass
    
    # Default: no alert
    return {"display": "none"}, "", "alert"

print("✓ Simplified routing callback loaded - login alerts only")