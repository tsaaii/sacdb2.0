"""
callbacks/routing_callback.py - Fixed routing with only login alerts

Remove duplicate session outputs that conflict with session_callback.py
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

def create_safe_login_layout():
    """Create a safe login layout"""
    
    return html.Div(className="login-page-container", children=[
        html.Div(className="login-container", children=[
            html.Div(className="login-logo-section", children=[
                html.Img(
                    src="/assets/img/right.png", 
                    alt="Swaccha Andhra Logo",
                    style={"width": "80px", "height": "80px", "objectFit": "contain"}
                ),
                html.H1("Swaccha Andhra", style={"color": "#2D5E40", "marginBottom": "0.5rem"}),
                html.P("Waste Management Dashboard", style={"color": "#8B4513", "marginBottom": "1.5rem"})
            ]),
            
            # Alert for login errors
            html.Div(id="login-alert-container", children=[
                html.Div(
                    "",
                    id="login-alert",
                    style={"display": "none"},
                    className="alert"
                )
            ]),
            
            html.Div(children=[
                # Google OAuth Section (if available)
                html.Div(style={
                    "marginBottom": "1.5rem"
                }, children=[
                    html.A([
                        html.I(className="fab fa-google", style={"fontSize": "1.2rem", "marginRight": "0.75rem", "color": "#4285F4"}),
                        html.Span("Continue with Google", style={"fontSize": "1rem"})
                    ], href="/auth/login", style={
                        "display": "flex",
                        "alignItems": "center",
                        "justifyContent": "center",
                        "width": "100%",
                        "padding": "1rem 1.5rem",
                        "backgroundColor": "white",
                        "color": "#2D5E40",
                        "border": "2px solid #4285F4",
                        "borderRadius": "12px",
                        "textDecoration": "none",
                        "fontWeight": "600"
                    })
                ]) if OAUTH_AVAILABLE else html.Div(),
                
                # Divider
                html.Div(style={
                    "display": "flex",
                    "alignItems": "center",
                    "margin": "1.5rem 0",
                    "color": "#8B4513"
                }, children=[
                    html.Hr(style={"flex": "1", "height": "1px", "backgroundColor": "#E8E4D0", "border": "none", "margin": "0 1rem"}),
                    html.Span("or", style={"fontSize": "0.9rem", "fontWeight": "500", "color": "#A67C52"}),
                    html.Hr(style={"flex": "1", "height": "1px", "backgroundColor": "#E8E4D0", "border": "none", "margin": "0 1rem"})
                ]) if OAUTH_AVAILABLE else html.Div(),
                
                # Traditional login
                html.Div(style={
                    "padding": "1.5rem",
                    "border": "2px solid #E8E4D0",
                    "borderRadius": "12px",
                    "backgroundColor": "#FEFEFE"
                }, children=[
                    html.H4("Username & Password", style={"color": "#2D5E40", "marginBottom": "1.5rem", "textAlign": "center"}),
                    
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
            ])
        ])
    ], style={
        "backgroundColor": "#FFFBF5",
        "minHeight": "100vh",
        "display": "flex",
        "flexDirection": "column",
        "justifyContent": "center",
        "alignItems": "center",
        "padding": "2rem 1rem"
    })

def create_main_dashboard():
    """Create the main authenticated dashboard"""
    return html.Div(className="container", children=[
        html.Div(className="page-header", style={"margin": "1rem 0"}, children=[
            html.H2("Main Dashboard", style={"color": "#2D5E40"}),
            html.P("Real-time waste management monitoring and analytics.", style={"color": "#8B4513"})
        ]),
        
        # Dashboard cards
        html.Div(style={
            "display": "grid",
            "gridTemplateColumns": "repeat(auto-fit, minmax(280px, 1fr))",
            "gap": "1.5rem",
            "margin": "2rem 0"
        }, children=[
            # Sample dashboard cards
            html.Div(style={
                "background": "white",
                "borderRadius": "12px",
                "padding": "1.5rem",
                "boxShadow": "0 4px 12px rgba(0, 0, 0, 0.08)",
                "border": "1px solid #E8E4D0"
            }, children=[
                html.H3("Welcome!", style={"color": "#2D5E40", "marginBottom": "1rem"}),
                html.P("You have successfully logged into the Swaccha Andhra Dashboard.", 
                       style={"color": "#8B4513"})
            ])
        ])
    ])

# ====================== ROUTING CALLBACK (NO SESSION OUTPUTS) ======================

@callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname'),
     Input('url', 'search'),
     Input('user-session', 'data')],  # Add as input to react to session changes
    prevent_initial_call=False
)
def display_page(pathname, search_params, session_data):
    """
    Route to the appropriate page layout.
    NO session management - that's handled in session_callback.py
    """
    
    # Handle error parameters in URL
    if search_params:
        try:
            params = parse_qs(search_params.lstrip('?'))
            error_type = params.get('error', [None])[0]
            
            if error_type == 'unauthorized_email':
                return html.Div(style={
                    "backgroundColor": "#FFFBF5",
                    "minHeight": "100vh",
                    "display": "flex",
                    "justifyContent": "center",
                    "alignItems": "center",
                    "textAlign": "center"
                }, children=[
                    html.Div(style={
                        "background": "white",
                        "padding": "2rem",
                        "borderRadius": "12px",
                        "boxShadow": "0 4px 12px rgba(0, 0, 0, 0.1)"
                    }, children=[
                        html.H2("Access Denied", style={"color": "#2D5E40"}),
                        html.P("Your email is not authorized.", style={"color": "#8B4513"}),
                        html.A("Back to Home", href="/", style={
                            "backgroundColor": "#2D5E40", "color": "white", 
                            "padding": "0.75rem 1.5rem", "textDecoration": "none", 
                            "borderRadius": "8px"
                        })
                    ])
                ])
                
        except Exception as e:
            print(f"Error parsing URL params: {e}")
    
    # Check authentication status
    is_authenticated = session_data and session_data.get('authenticated', False)
    
    # Route based on pathname and authentication
    if pathname == '/' or pathname is None:
        return create_public_dashboard()
    elif pathname == '/login':
        return create_safe_login_layout()
    elif pathname == '/main':
        if is_authenticated:
            return create_main_dashboard()
        else:
            return create_safe_login_layout()
    elif pathname == '/reports':
        if is_authenticated:
            return html.Div(className="container", children=[
                html.H2("Reports"),
                html.P("Comprehensive reporting and data export functionality.")
            ])
        else:
            return create_safe_login_layout()
    elif pathname == '/analytics':
        if is_authenticated:
            return create_analytics_layout()
        else:
            return create_safe_login_layout()
    elif pathname == '/upload':
        if is_authenticated:
            return html.Div(className="container", children=[
                html.H2("Upload Data"),
                html.P("Upload waste collection data and reports.")
            ])
        else:
            return create_safe_login_layout()
    elif pathname == '/settings':
        if is_authenticated:
            return html.Div(className="container", children=[
                html.H2("Settings"),
                html.P("Customize your dashboard experience.")
            ])
        else:
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
     Output('login-alert', 'children')],
    [Input('login-submit-btn', 'n_clicks'),
     Input('url', 'search')],
    [State('login-username', 'value'),
     State('login-password', 'value')],
    prevent_initial_call=True
)
def handle_login_alerts(login_clicks, search_params, username, password):
    """
    Handle ONLY login alert messages.
    NO session management - that's in session_callback.py
    """
    
    ctx = callback_context
    if not ctx.triggered:
        return {"display": "none"}, ""
    
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
            }, "⚠️ Please enter both username and password."
        
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
            }, "❌ Invalid username or password. Please try again."
        
        # Success - hide alert (session callback handles redirect)
        return {"display": "none"}, ""
    
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
                }, "⚠️ Access denied. Your email is not authorized."
            
            elif error_type == 'auth_failed':
                return {
                    "display": "block",
                    "backgroundColor": "#f8d7da",
                    "color": "#721c24",
                    "padding": "0.75rem",
                    "borderRadius": "8px",
                    "marginBottom": "1rem",
                    "border": "1px solid #f5c6cb"
                }, "❌ Authentication failed. Please try again."
                
        except Exception:
            pass
    
    # Default: no alert
    return {"display": "none"}, ""

print("✓ Fixed routing callback loaded - login alerts only")