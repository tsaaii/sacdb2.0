"""
callbacks/routing_callback.py - Fixed routing with proper error page handling

This fixes the children argument conflict in the error page.
"""

from dash import callback, Output, Input, State, html, dcc, no_update
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

def create_unauthorized_error_page():
    logo_div = html.Div()

    error_icon = html.I(
        className="fas fa-user-slash", style={
        "fontSize": "3rem",
        "color": "#8B0000",
        "marginBottom": "1rem"
    })

    error_message = html.Div([
        html.H2("Access Denied", style={
            "color": "#2D5E40",
            "fontSize": "1.6rem",
            "marginBottom": "0.75rem"
        }),
        html.P("You do not have permission to access this dashboard.", style={
            "color": "#5A5A5A",
            "marginBottom": "1.5rem",
            "fontSize": "1rem"
        })
    ])

    phone_section = html.Div([
        html.I(className="fas fa-mobile-alt", style={"fontSize": "1.2rem", "marginBottom": "0.25rem", "color": "#2D5E40"}),
        html.Div("+91-6303-640-757", style={
            "fontSize": "1.3rem",
            "fontWeight": "bold",
            "letterSpacing": "1px",
            "margin": "0.5rem 0",
            "color": "#2D5E40"
        }),
        html.P("WhatsApp / SMS", style={"margin": "0", "fontSize": "0.85rem", "color": "#888"})
    ], style={"textAlign": "center", "margin": "1rem 0"})

    message_template = html.Div([
        html.P("Message template:", style={"fontWeight": "bold", "marginBottom": "0.3rem", "color": "#333"}),
        html.P('"Hi, I need access to Swaccha Andhra Dashboard. My email: [your-email@domain.com]"', style={"color": "#555"})
    ], style={
        "background": "#F9F9F9",
        "padding": "1rem",
        "borderRadius": "6px",
        "fontStyle": "italic",
        "color": "#333",
        "border": "1px solid #DDD"
    })

    contact_card = html.Div([
        html.H3([
            html.I(className="fas fa-key", style={"marginRight": "0.5rem", "color": "#2D5E40"}),
            "Request Access"
        ], style={"marginBottom": "0.75rem", "color": "#2D5E40"}),
        html.P("To get access to this dashboard, please send a message with your email ID to:", style={"color": "#555"}),
        phone_section,
        message_template
    ], style={
        "background": "#FFFFFF",
        "padding": "1.5rem",
        "borderRadius": "8px",
        "marginBottom": "1.5rem",
        "boxShadow": "0 2px 6px rgba(0, 0, 0, 0.05)",
        "border": "1px solid #E0E0E0"
    })

    instructions = html.Div()

    action_buttons = html.Div([
        html.A([
            html.I(className="fas fa-redo-alt", style={"marginRight": "0.5rem"}),
            "Try Again"
        ], href="/", style={
            "display": "inline-flex",
            "alignItems": "center",
            "padding": "0.6rem 1.2rem",
            "margin": "0.4rem",
            "backgroundColor": "#2D5E40",
            "color": "white",
            "textDecoration": "none",
            "borderRadius": "6px",
            "fontWeight": "600"
        }),
        html.A([
            html.I(className="fas fa-phone", style={"marginRight": "0.5rem"}),
            "Call Now"
        ], href="tel:+916303640757", style={
            "display": "inline-flex",
            "alignItems": "center",
            "padding": "0.6rem 1.2rem",
            "margin": "0.4rem",
            "backgroundColor": "#E6B800",
            "color": "#2D5E40",
            "textDecoration": "none",
            "borderRadius": "6px",
            "fontWeight": "600"
        })
    ])

    footer = html.P("© 2025 Advitia Labs • Made in Andhra Pradesh", style={
        "marginTop": "2rem",
        "fontSize": "0.85rem",
        "color": "#999"
    })

    content_card = html.Div([
        logo_div,
        error_icon,
        error_message,
        contact_card,
        instructions,
        action_buttons,
        footer
    ], style={
        "background": "#FFFFFF",
        "padding": "2rem 1.5rem",
        "borderRadius": "10px",
        "boxShadow": "0 4px 12px rgba(0, 0, 0, 0.08)",
        "border": "1px solid #E8E4D0",
        "maxWidth": "600px",
        "width": "100%"
    })

    return html.Div(
        content_card,
        style={
            "backgroundColor": "#F9F9F9",
            "minHeight": "100vh",
            "display": "flex",
            "flexDirection": "column",
            "justifyContent": "center",
            "alignItems": "center",
            "padding": "1.5rem",
            "textAlign": "center"
        }
    )



def create_main_dashboard():
    """Create the main authenticated dashboard"""
    return html.Div(className="container", children=[
        html.Div(className="page-header", style={"margin": "0.5rem 0"}, children=[
            html.H2("Main Dashboard", style={"margin": "0 0 0.25rem 0"}),
            html.P("Real-time waste management monitoring dashboard.", 
                   style={"margin": "0", "fontSize": "0.9rem"})
        ]),
        
        # Dashboard cards
        html.Div(style={
            "display": "grid",
            "gridTemplateColumns": "repeat(auto-fit, minmax(250px, 1fr))",
            "gap": "1rem",
            "margin": "1rem 0"
        }, children=[
            # Sample dashboard cards
            html.Div(style={
                "background": "white",
                "borderRadius": "10px",
                "padding": "1rem",
                "boxShadow": "0 2px 8px rgba(0, 0, 0, 0.06)",
                "border": "1px solid #E8E4D0"
            }, children=[
                html.Div(style={"display": "flex", "alignItems": "center", "marginBottom": "0.5rem"}, children=[
                    html.I(className="fas fa-trash-alt", style={"color": "#2D5E40", "marginRight": "0.5rem"}),
                    html.H3("Total Waste Collected", style={"margin": "0", "fontSize": "1rem", "color": "#2D5E40"})
                ]),
                html.P("125,480 MT", style={"margin": "0", "color": "#8B4513", "fontSize": "1.5rem", "fontWeight": "700"}),
                html.P("Cumulative collection", style={"margin": "0", "color": "#A67C52", "fontSize": "0.8rem"})
            ]),
            
            html.Div(style={
                "background": "white",
                "borderRadius": "10px",
                "padding": "1rem",
                "boxShadow": "0 2px 8px rgba(0, 0, 0, 0.06)",
                "border": "1px solid #E8E4D0"
            }, children=[
                html.Div(style={"display": "flex", "alignItems": "center", "marginBottom": "0.5rem"}, children=[
                    html.I(className="fas fa-cogs", style={"color": "#F2C94C", "marginRight": "0.5rem"}),
                    html.H3("Active Machines", style={"margin": "0", "fontSize": "1rem", "color": "#2D5E40"})
                ]),
                html.P("12/15", style={"margin": "0", "color": "#8B4513", "fontSize": "1.5rem", "fontWeight": "700"}),
                html.P("Machines operational", style={"margin": "0", "color": "#A67C52", "fontSize": "0.8rem"})
            ]),
            
            html.Div(style={
                "background": "white",
                "borderRadius": "10px",
                "padding": "1rem",
                "boxShadow": "0 2px 8px rgba(0, 0, 0, 0.06)",
                "border": "1px solid #E8E4D0"
            }, children=[
                html.Div(style={"display": "flex", "alignItems": "center", "marginBottom": "0.5rem"}, children=[
                    html.I(className="fas fa-percent", style={"color": "#C74A3C", "marginRight": "0.5rem"}),
                    html.H3("Processing Efficiency", style={"margin": "0", "fontSize": "1rem", "color": "#2D5E40"})
                ]),
                html.P("94.7%", style={"margin": "0", "color": "#8B4513", "fontSize": "1.5rem", "fontWeight": "700"}),
                html.P("Overall efficiency", style={"margin": "0", "color": "#A67C52", "fontSize": "0.8rem"})
            ])
        ])
    ])

def create_safe_login_layout():
    """Create a safe login layout"""
    try:
        from auth.google_oauth import oauth
        OAUTH_AVAILABLE = True
    except ImportError:
        OAUTH_AVAILABLE = False
    
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
            
            html.Div(id="login-alert-container", children=[
                html.Div(
                    id="login-alert",
                    style={"display": "none"},
                    className="alert alert-danger"
                )
            ]),
            
            html.Div(id="login-form", children=[
                create_oauth_login() if OAUTH_AVAILABLE else create_fallback_login()
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

def create_oauth_login():
    """Create Google OAuth login interface"""
    return html.Div(className="oauth-login-form", children=[
        html.Div(style={"textAlign": "center", "marginBottom": "2rem"}, children=[
            html.A([
                html.I(className="fab fa-google", style={
                    "fontSize": "1.5rem", 
                    "marginRight": "1rem",
                    "color": "#4285F4"
                }),
                html.Span("Continue with Google", style={"fontSize": "1.1rem"})
            ], href="/auth/login", style={
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
            })
        ])
    ])

def create_fallback_login():
    """Create fallback login form"""
    return html.Div(className="fallback-login-form", children=[
        html.Div(style={
            "backgroundColor": "#E3F2FD",
            "padding": "1rem",
            "borderRadius": "8px",
            "marginBottom": "1.5rem",
            "border": "1px solid #BBDEFB"
        }, children=[
            html.I(className="fas fa-info-circle", style={"marginRight": "0.5rem", "color": "#1976D2"}),
            html.Span("Google OAuth is not configured.", style={"color": "#1976D2"})
        ]),
        
        html.Div(style={"marginBottom": "1rem"}, children=[
            html.Label("Username", style={"fontWeight": "600", "color": "#2D5E40", "marginBottom": "0.5rem", "display": "block"}),
            dcc.Input(
                id="login-username",
                type="text",
                placeholder="Enter your username",
                style={
                    "width": "100%",
                    "padding": "0.75rem",
                    "border": "1px solid #E8E4D0",
                    "borderRadius": "8px",
                    "fontSize": "1rem"
                }
            )
        ]),
        
        html.Div(style={"marginBottom": "1.5rem"}, children=[
            html.Label("Password", style={"fontWeight": "600", "color": "#2D5E40", "marginBottom": "0.5rem", "display": "block"}),
            dcc.Input(
                id="login-password",
                type="password",
                placeholder="Enter your password",
                style={
                    "width": "100%",
                    "padding": "0.75rem",
                    "border": "1px solid #E8E4D0",
                    "borderRadius": "8px",
                    "fontSize": "1rem"
                }
            )
        ]),
        
        html.Button([
            html.I(className="fas fa-sign-in-alt", style={"marginRight": "0.5rem"}),
            "Log In to Dashboard"
        ], id="login-submit-btn", n_clicks=0, style={
            "width": "100%",
            "padding": "0.875rem",
            "backgroundColor": "#2D5E40",
            "color": "white",
            "border": "none",
            "borderRadius": "8px",
            "fontSize": "1rem",
            "fontWeight": "600",
            "cursor": "pointer"
        })
    ])

@callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname'),
     Input('url', 'search')]
)
def display_page_with_error_handling(pathname, search_params):
    """
    Route to the appropriate page layout with error handling.
    Fixed to avoid children argument conflicts.
    """
    
    # Handle error parameters in URL
    if search_params:
        try:
            params = parse_qs(search_params.lstrip('?'))
            error_type = params.get('error', [None])[0]
            
            if error_type == 'unauthorized_email':
                return create_unauthorized_error_page()
                
        except Exception as e:
            # If error parsing fails, continue with normal routing
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
                html.H1("404", style={"fontSize": "6rem", "fontWeight": "700", "color": "#F2C94C", "margin": "0"}),
                html.H2("Page Not Found", style={"color": "#2D5E40"}),
                html.P("The page you requested does not exist."),
                html.A("Go to Home", href="/", style={
                    "backgroundColor": "#2D5E40", 
                    "color": "white", 
                    "padding": "0.75rem 1.5rem", 
                    "textDecoration": "none", 
                    "borderRadius": "8px"
                })
            ])
        ])

# Safe login callback (only registers when login elements exist)
@callback(
    [Output('login-alert', 'style'),
     Output('login-alert', 'children'),
     Output('user-session', 'data', allow_duplicate=True),
     Output('url', 'pathname', allow_duplicate=True)],
    [Input('login-submit-btn', 'n_clicks')],
    [State('login-username', 'value'),
     State('login-password', 'value'),
     State('user-session', 'data')],
    prevent_initial_call=True
)
def handle_safe_login(login_clicks, username, password, session_data):
    """Safe login handler for fallback authentication"""
    
    if not login_clicks or login_clicks == 0:
        return {"display": "none"}, "", no_update, no_update
    
    # Check if OAuth is available
    try:
        from auth.google_oauth import oauth
        OAUTH_AVAILABLE = True
    except ImportError:
        OAUTH_AVAILABLE = False
    
    if OAUTH_AVAILABLE:
        return {"display": "none"}, "", no_update, '/auth/login'
    
    if not username or not password:
        return {
            "display": "block",
            "backgroundColor": "#f8d7da",
            "color": "#721c24",
            "padding": "0.75rem",
            "borderRadius": "8px",
            "border": "1px solid #f5c6cb"
        }, "Please enter both username and password.", no_update, no_update
    
    # Simple validation
    valid_users = {
        'admin': 'password123',
        'user': 'password456', 
        'test': 'test123'
    }
    
    if username in valid_users and valid_users[username] == password:
        user_data = {
            'user_id': username,
            'username': username,
            'role': 'user',
            'authenticated': True,
            'auth_method': 'fallback'
        }
        return {"display": "none"}, "", user_data, '/main'
    else:
        return {
            "display": "block",
            "backgroundColor": "#f8d7da",
            "color": "#721c24",
            "padding": "0.75rem",
            "borderRadius": "8px",
            "border": "1px solid #f5c6cb"
        }, "Invalid username or password. Please try again.", no_update, no_update