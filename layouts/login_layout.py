"""
layouts/login_layout.py - Updated login layout with both OAuth and traditional login

This file provides both Google OAuth and username/password login options.
"""

from dash import html, dcc
import dash_bootstrap_components as dbc

def create_login_layout():
    """
    Create the login page layout with both Google OAuth and traditional login options.
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
            # Logo section
            html.Div(className="login-logo-section", children=[
                html.Img(
                    src="/assets/img/right.png", 
                    alt="Swaccha Andhra Logo",
                    className="login-logo"
                ),
                html.H1("Swaccha Andhra", className="login-title"),
                html.P("Waste Management Dashboard", className="login-subtitle")
            ]),
            
            # Alert for login errors
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
            
            # Main login options
            html.Div(id="login-form", children=[
                create_dual_login_options(OAUTH_AVAILABLE)
            ])
        ]),
        
        # Footer section
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

def create_dual_login_options(oauth_available=True):
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
            "gridTemplateColumns": "1fr 1fr" if oauth_available else "1fr",
            "gap": "2rem",
            "marginBottom": "2rem"
        }, children=[
            # Google OAuth Section (if available)
            create_oauth_section() if oauth_available else html.Div(),
            
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
        # OAuth section header
        html.Div(style={"marginBottom": "1.5rem"}, children=[
            html.I(className="fab fa-google", style={
                "fontSize": "2rem",
                "color": "#4285F4",
                "marginBottom": "0.5rem"
            }),
            html.H4("Google OAuth", style={
                "color": "#2D5E40",
                "fontSize": "1rem",
                "fontWeight": "600",
                "margin": "0"
            }),
            html.P("Quick and secure", style={
                "color": "#8B4513",
                "fontSize": "0.8rem",
                "margin": "0.25rem 0 0 0"
            })
        ]),
        
        # Google login button
        html.A([
            html.I(className="fab fa-google", style={
                "fontSize": "1.2rem", 
                "marginRight": "0.75rem",
                "color": "#4285F4"
            }),
            html.Span("Continue with Google", style={"fontSize": "1rem"})
        ], href="/auth/login", style={
            "display": "inline-flex",
            "alignItems": "center",
            "justifyContent": "center",
            "width": "100%",
            "padding": "0.875rem 1.5rem",
            "backgroundColor": "white",
            "color": "#2D5E40",
            "border": "2px solid #4285F4",
            "borderRadius": "8px",
            "textDecoration": "none",
            "fontWeight": "600",
            "transition": "all 0.3s ease",
            "boxShadow": "0 2px 4px rgba(0, 0, 0, 0.1)"
        }, className="oauth-button"),
        
        # OAuth benefits
        html.Div(style={"marginTop": "1rem"}, children=[
            html.Ul(style={
                "textAlign": "left",
                "fontSize": "0.8rem",
                "color": "#8B4513",
                "paddingLeft": "1rem",
                "margin": "0"
            }, children=[
                html.Li("No password required"),
                html.Li("Secure Google authentication"),
                html.Li("Faster login process")
            ])
        ])
    ])

def create_traditional_login_section():
    """Create traditional username/password login section"""
    return html.Div(className="traditional-section", style={
        "padding": "1.5rem",
        "border": "2px solid #E8E4D0",
        "borderRadius": "12px",
        "backgroundColor": "white"
    }, children=[
        # Traditional section header
        html.Div(style={"marginBottom": "1.5rem", "textAlign": "center"}, children=[
            html.I(className="fas fa-user-lock", style={
                "fontSize": "2rem",
                "color": "#2D5E40",
                "marginBottom": "0.5rem"
            }),
            html.H4("Traditional Login", style={
                "color": "#2D5E40",
                "fontSize": "1rem",
                "fontWeight": "600",
                "margin": "0"
            }),
            html.P("Username and password", style={
                "color": "#8B4513",
                "fontSize": "0.8rem",
                "margin": "0.25rem 0 0 0"
            })
        ]),
        
        # Username field
        html.Div(className="form-group", style={"marginBottom": "1rem"}, children=[
            html.Label("Username", style={
                "fontWeight": "600",
                "color": "#2D5E40",
                "fontSize": "0.9rem",
                "marginBottom": "0.5rem",
                "display": "block"
            }),
            html.Div(className="input-group", style={"position": "relative"}, children=[
                html.I(className="fas fa-user", style={
                    "position": "absolute",
                    "left": "0.75rem",
                    "top": "50%",
                    "transform": "translateY(-50%)",
                    "color": "#8B4513",
                    "zIndex": "2"
                }),
                dcc.Input(
                    id="login-username",
                    type="text",
                    placeholder="Enter your username",
                    style={
                        "width": "100%",
                        "padding": "0.75rem 0.75rem 0.75rem 2.5rem",
                        "border": "2px solid #E8E4D0",
                        "borderRadius": "8px",
                        "fontSize": "0.9rem",
                        "transition": "border-color 0.3s ease"
                    },
                    className="login-input"
                )
            ])
        ]),
        
        # Password field
        html.Div(className="form-group", style={"marginBottom": "1.5rem"}, children=[
            html.Label("Password", style={
                "fontWeight": "600",
                "color": "#2D5E40",
                "fontSize": "0.9rem",
                "marginBottom": "0.5rem",
                "display": "block"
            }),
            html.Div(className="input-group", style={"position": "relative"}, children=[
                html.I(className="fas fa-lock", style={
                    "position": "absolute",
                    "left": "0.75rem",
                    "top": "50%",
                    "transform": "translateY(-50%)",
                    "color": "#8B4513",
                    "zIndex": "2"
                }),
                dcc.Input(
                    id="login-password",
                    type="password",
                    placeholder="Enter your password",
                    style={
                        "width": "100%",
                        "padding": "0.75rem 0.75rem 0.75rem 2.5rem",
                        "border": "2px solid #E8E4D0",
                        "borderRadius": "8px",
                        "fontSize": "0.9rem",
                        "transition": "border-color 0.3s ease"
                    },
                    className="login-input"
                )
            ])
        ]),
        
        # Login button
        html.Button([
            html.I(className="fas fa-sign-in-alt", style={"marginRight": "0.5rem"}),
            "Login to Dashboard"
        ], id="login-submit-btn", n_clicks=0, style={
            "width": "100%",
            "padding": "0.875rem 1.5rem",
            "fontSize": "1rem",
            "fontWeight": "600",
            "background": "linear-gradient(135deg, #2D5E40 0%, #4A7E64 100%)",
            "color": "white",
            "border": "none",
            "borderRadius": "8px",
            "cursor": "pointer",
            "transition": "all 0.3s ease",
            "boxShadow": "0 2px 4px rgba(0, 0, 0, 0.1)"
        }, className="traditional-login-button"),
        
        # Test credentials info
        html.Div(style={
            "marginTop": "1rem",
            "padding": "0.75rem",
            "backgroundColor": "#F0F8FF",
            "borderRadius": "6px",
            "border": "1px solid #B0E0E6"
        }, children=[
            html.P("Test Credentials:", style={
                "fontWeight": "600",
                "color": "#2D5E40",
                "fontSize": "0.8rem",
                "margin": "0 0 0.25rem 0"
            }),
            html.P("admin / password123", style={
                "margin": "0",
                "fontSize": "0.75rem",
                "color": "#4A7E64",
                "fontFamily": "monospace"
            }),
            html.P("test / test123", style={
                "margin": "0",
                "fontSize": "0.75rem",
                "color": "#4A7E64",
                "fontFamily": "monospace"
            })
        ])
    ])

def create_login_info_section():
    """Create information section about access and security"""
    return html.Div(className="login-info-section", children=[
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
            html.P("This dashboard requires authorized access. Only approved email addresses can use Google OAuth, and valid credentials are required for traditional login.", 
                   style={"margin": "0", "color": "#8B4513", "fontSize": "0.9rem"})
        ]),
        
        # What you get access to
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
                "Need access or having issues? Contact ",
                html.A("admin@advitialabs.com", href="mailto:admin@advitialabs.com", 
                       style={"color": "#2D5E40", "fontWeight": "600"})
            ], style={"margin": "0", "fontSize": "0.9rem", "color": "#8B4513"})
        ])
    ])

# CSS for hover effects
LOGIN_CSS = """
<style>
.oauth-button:hover {
    background-color: #F0F8FF !important;
    border-color: #2D5E40 !important;
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15) !important;
}

.traditional-login-button:hover {
    background: linear-gradient(135deg, #4A7E64 0%, #2D5E40 100%) !important;
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2) !important;
}

.login-input:focus {
    border-color: #2D5E40 !important;
    box-shadow: 0 0 0 3px rgba(45, 94, 64, 0.1) !important;
    outline: none;
}

.dual-login-container {
    animation: fadeIn 0.5s ease-in;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

@media (max-width: 768px) {
    .login-methods-container {
        grid-template-columns: 1fr !important;
        gap: 1.5rem !important;
    }
}
</style>
"""