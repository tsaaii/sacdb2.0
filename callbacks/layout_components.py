"""
callbacks/layout_components.py - Layout Creation Functions

Save this as: callbacks/layout_components.py
"""

from dash import html, dcc
from datetime import datetime

# Check if OAuth is available
try:
    from auth.google_oauth import get_current_user
    OAUTH_AVAILABLE = True
except ImportError:
    OAUTH_AVAILABLE = False
    def get_current_user():
        return None

# Import layouts with fallbacks
try:
    from layouts.public_landing import create_public_dashboard as create_public_content
except ImportError:
    def create_public_content():
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

def get_current_time():
    """Get current time formatted for display"""
    now = datetime.now()
    date_str = now.strftime("%b %d, %Y")
    time_str = now.strftime("%I:%M:%S %p")
    header_time = now.strftime("%I:%M %p")
    live_time = f"{date_str} {time_str}"
    return live_time, header_time

# ==================== FOOTER COMPONENT ====================

def create_footer():
    """Create footer component"""
    return html.Footer(className="footer", children=[
        html.Div(className="container", children=[
            html.Div(className="footer-content", children=[
                # Footer logo and links
                html.Div(className="footer-logo", children=[
                    html.Img(src="/assets/img/logo-white.png", alt="Logo", style={"height": "28px", "width": "auto"}),
                    html.Span("Swaccha Andhra", style={"fontWeight": "600", "fontSize": "1rem"})
                ]),
                
                # Footer links
                html.Div(className="footer-links", children=[
                    html.A("About", href="/about", className="footer-link"),
                    html.A("Help", href="/help", className="footer-link"),
                    html.A("Contact", href="/contact", className="footer-link")
                ]),
                
                # Copyright
                html.Div(className="footer-copyright", children=[
                    "© 2025 Advitia Labs • Made in Andhra Pradesh"
                ])
            ])
        ])
    ])

# ==================== TITLE BANNER COMPONENT ====================

def create_title_banner():
    """Create title banner component"""
    live_time, _ = get_current_time()
    
    return html.Div(className="dashboard-title-banner", children=[
        html.Div(className="container", children=[
            html.Div(className="dashboard-title-wrapper", children=[
                # Status indicators
                html.Div(className="dashboard-status-indicators", children=[
                    html.Div(className="refresh-indicator", children=[
                        html.I(className="fas fa-sync-alt fa-spin", style={"color": "#2D5E40", "marginRight": "0.3rem"}),
                        html.Span("Auto-refresh")
                    ]),
                    html.Div(live_time, id="live-time", className="live-time")
                ]),
                html.Div(className="dashboard-title-content", children=[
                    html.Img(src="/assets/img/left.png", alt="Left Logo", className="dashboard-logo"),
                    html.Div(className="dashboard-title-container", children=[
                        html.H1("Swaccha Andhra", className="dashboard-main-title"),
                        html.H2("Real-Time Monitoring Dashboard for Legacy Waste Reclamation", className="dashboard-subtitle")
                    ]),
                    html.Img(src="/assets/img/right.png", alt="Right Logo", className="dashboard-logo")
                ])
            ])
        ])
    ])

# ==================== PUBLIC DASHBOARD ====================

def create_public_dashboard():
    """Create public dashboard with header and footer"""
    live_time, header_time = get_current_time()
    
    return html.Div(className="main-app-container", children=[
        # Header hover trigger area
        html.Div(className="header-hover-area"),
        
        # Public header
        html.Header(className="header", children=[
            html.Div(className="container", children=[
                html.Div(className="header-content", children=[
                    html.Div(className="header-title", children=[
                        html.H1("Swaccha Andhra Dashboard")
                    ]),
                    html.Nav(className="header-nav", children=[]),
                    html.Div(className="header-actions", children=[
                        html.Div(header_time, className="clock-display"),
                        html.A("Login", href="/login?source=public", className="btn btn-primary")
                    ])
                ])
            ])
        ]),
        
        # Title Banner
        create_title_banner(),
        
        # Main content
        html.Main(className="dashboard-main-content", children=[
            html.Div(className="page-content-wrapper", children=[
                # Add login help section for public users
                html.Div(className="container", style={"textAlign": "center", "padding": "2rem 0"}, children=[
                    html.H3("Access the Full Dashboard", style={"color": "#2D5E40", "marginBottom": "1rem"}),
                    html.P("Login to access waste management data, reports, and analytics.", 
                           style={"color": "#8B4513", "marginBottom": "1.5rem"}),
                    html.Div(style={"display": "flex", "gap": "1rem", "justifyContent": "center"}, children=[
                        html.A("Login to Dashboard", href="/login?source=public", 
                               className="btn", style={
                                   "backgroundColor": "#2D5E40", "color": "white", 
                                   "padding": "0.75rem 1.5rem", "textDecoration": "none", 
                                   "borderRadius": "8px", "fontWeight": "600"
                               }),
                        html.A("Force Login", href="/login?force=true", 
                               className="btn", style={
                                   "backgroundColor": "#F2C94C", "color": "#2D5E40", 
                                   "padding": "0.75rem 1.5rem", "textDecoration": "none", 
                                   "borderRadius": "8px", "fontWeight": "600"
                               })
                    ])
                ]),
                create_public_content()
            ])
        ]),
        
        # Footer
        create_footer()
    ])

# ==================== MAIN DASHBOARD ====================

def create_main_dashboard():
    """Create the main authenticated dashboard"""
    live_time, header_time = get_current_time()
    
    # Get current user name for display
    user_display_name = "User"
    if OAUTH_AVAILABLE:
        try:
            oauth_user = get_current_user()
            if oauth_user:
                user_display_name = oauth_user.get('name', oauth_user.get('email', 'User')).split()[0]
        except Exception:
            pass
    
    return html.Div(className="main-app-container", children=[
        # Header hover trigger area
        html.Div(className="header-hover-area"),
        
        # Header with navigation (authenticated version)
        html.Header(className="header", children=[
            html.Div(className="container", children=[
                html.Div(className="header-content", children=[
                    # Logo & Title
                    html.Div(className="header-title", children=[
                        html.H1("Swaccha Andhra Dashboard")
                    ]),
                    
                    # Navigation
                    html.Nav(className="header-nav", children=[
                        html.A("Dashboard", href="/main", className="header-nav-link active"),
                        html.A("Reports", href="/reports", className="header-nav-link"),
                        html.A("Analytics", href="/analytics", className="header-nav-link"),
                        html.A("Upload", href="/upload", className="header-nav-link"),
                        html.A("Settings", href="/settings", className="header-nav-link")
                    ]),
                    
                    # Right side actions
                    html.Div(className="header-actions", children=[
                        # Auto-refresh indicator
                        html.Div(className="auto-refresh-indicator", children=[
                            html.I(className="fas fa-sync-alt"),
                            html.Span("Auto-refreshing")
                        ]),
                        
                        # Clock display
                        html.Div(header_time, id="header-clock", className="clock-display"),
                        
                        # User info and logout
                        html.Span(user_display_name, style={"color": "#FEFEFE", "marginRight": "1rem"}),
                        html.Button("Logout", id="logout-btn", n_clicks=0, className="btn btn-accent", 
                                   **{
                                       'data-testid': 'logout-button',
                                       'style': {
                                           "backgroundColor": "#C74A3C",
                                           "color": "white", 
                                           "border": "none",
                                           "padding": "0.35rem 0.85rem",
                                           "borderRadius": "8px",
                                           "fontWeight": "600",
                                           "cursor": "pointer",
                                           "fontSize": "0.85rem"
                                       }
                                   })
                    ])
                ])
            ])
        ]),
        
        # Dashboard Title Banner
        create_title_banner(),
        
        # Main Content
        html.Main(className="dashboard-main-content", children=[
            html.Div(className="page-content-wrapper", children=[
                html.Div(className="container", children=[
                    html.Div(className="page-header", style={"margin": "1rem 0"}, children=[
                        html.H2("Main Dashboard", style={"color": "#2D5E40", "marginBottom": "0.5rem"}),
                        html.P("Real-time waste management monitoring dashboard.", style={"color": "#8B4513"})
                    ]),
                    
                    # Dashboard cards
                    html.Div(style={
                        "display": "grid",
                        "gridTemplateColumns": "repeat(auto-fit, minmax(280px, 1fr))",
                        "gap": "1.5rem",
                        "margin": "1.5rem 0"
                    }, children=[
                        # Total Waste Card
                        html.Div(style={
                            "background": "white",
                            "borderRadius": "12px",
                            "padding": "1.5rem",
                            "boxShadow": "0 4px 12px rgba(0, 0, 0, 0.08)",
                            "border": "1px solid #E8E4D0"
                        }, children=[
                            html.Div(style={"display": "flex", "alignItems": "center", "marginBottom": "1rem"}, children=[
                                html.I(className="fas fa-trash-alt", style={"color": "#2D5E40", "marginRight": "0.75rem", "fontSize": "1.5rem"}),
                                html.H3("Total Waste Collected", style={"margin": "0", "fontSize": "1rem", "color": "#2D5E40"})
                            ]),
                            html.P("125,480 MT", style={"margin": "0 0 0.5rem 0", "color": "#8B4513", "fontSize": "2rem", "fontWeight": "700"}),
                            html.P("Cumulative collection", style={"margin": "0", "color": "#A67C52", "fontSize": "0.9rem"})
                        ]),
                        
                        # Active Machines Card
                        html.Div(style={
                            "background": "white",
                            "borderRadius": "12px",
                            "padding": "1.5rem",
                            "boxShadow": "0 4px 12px rgba(0, 0, 0, 0.08)",
                            "border": "1px solid #E8E4D0"
                        }, children=[
                            html.Div(style={"display": "flex", "alignItems": "center", "marginBottom": "1rem"}, children=[
                                html.I(className="fas fa-cogs", style={"color": "#F2C94C", "marginRight": "0.75rem", "fontSize": "1.5rem"}),
                                html.H3("Active Machines", style={"margin": "0", "fontSize": "1rem", "color": "#2D5E40"})
                            ]),
                            html.P("12/15", style={"margin": "0 0 0.5rem 0", "color": "#8B4513", "fontSize": "2rem", "fontWeight": "700"}),
                            html.P("Machines operational", style={"margin": "0", "color": "#A67C52", "fontSize": "0.9rem"})
                        ]),
                        
                        # Efficiency Card
                        html.Div(style={
                            "background": "white",
                            "borderRadius": "12px",
                            "padding": "1.5rem",
                            "boxShadow": "0 4px 12px rgba(0, 0, 0, 0.08)",
                            "border": "1px solid #E8E4D0"
                        }, children=[
                            html.Div(style={"display": "flex", "alignItems": "center", "marginBottom": "1rem"}, children=[
                                html.I(className="fas fa-percent", style={"color": "#C74A3C", "marginRight": "0.75rem", "fontSize": "1.5rem"}),
                                html.H3("Processing Efficiency", style={"margin": "0", "fontSize": "1rem", "color": "#2D5E40"})
                            ]),
                            html.P("94.7%", style={"margin": "0 0 0.5rem 0", "color": "#8B4513", "fontSize": "2rem", "fontWeight": "700"}),
                            html.P("Overall efficiency", style={"margin": "0", "color": "#A67C52", "fontSize": "0.9rem"})
                        ])
                    ])
                ])
            ])
        ]),
        
        # Footer
        create_footer()
    ])

# ==================== LOGIN LAYOUT ====================

def create_safe_login_layout():
    """Create login layout with Google OAuth and traditional login"""
    live_time, header_time = get_current_time()
    
    return html.Div(className="main-app-container", children=[
        # Header hover trigger area
        html.Div(className="header-hover-area"),
        
        # Simple header for login page
        html.Header(className="header", children=[
            html.Div(className="container", children=[
                html.Div(className="header-content", children=[
                    html.Div(className="header-title", children=[
                        html.H1("Swaccha Andhra Dashboard")
                    ]),
                    html.Nav(className="header-nav", children=[], id="nav-links"),
                    html.Div(className="header-actions", children=[
                        html.Div(header_time, className="clock-display"),
                        html.A("Home", href="/", className="btn btn-outline")
                    ], id="header-actions")
                ])
            ])
        ]),
        
        # Main login content
        html.Main(className="dashboard-main-content", children=[
            html.Div(className="page-content-wrapper", children=[
                html.Div(className="login-page-container", children=[
                    html.Div(className="login-container", children=[
                        # Logo section
                        html.Div(className="login-logo-section", children=[
                            html.Img(src="/assets/img/right.png", alt="Swaccha Andhra Logo", 
                                     style={"width": "80px", "height": "80px", "marginBottom": "1rem"}),
                            html.H1("Swaccha Andhra", style={"color": "#2D5E40", "marginBottom": "0.5rem"}),
                            html.P("Waste Management Dashboard", style={"color": "#8B4513", "marginBottom": "1.5rem"})
                        ]),
                        
                        # Alert container
                        html.Div(id="login-alert-container", children=[
                            html.Div("", id="login-alert", style={"display": "none"}, className="alert")
                        ]),
                        
                        # Stackable login options
                        html.Div(children=[
                            # Google OAuth Section (Primary option)
                            html.Div(style={
                                "marginBottom": "1.5rem"
                            }, children=[
                                html.A([
                                    html.I(className="fab fa-google", style={
                                        "fontSize": "1.2rem", 
                                        "marginRight": "0.75rem",
                                        "color": "#4285F4"
                                    }),
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
                                    "fontWeight": "600",
                                    "transition": "all 0.3s ease",
                                    "boxShadow": "0 2px 8px rgba(66, 133, 244, 0.1)"
                                })
                            ]) if OAUTH_AVAILABLE else html.Div(),
                            
                            # Divider (only show if OAuth is available)
                            html.Div(style={
                                "display": "flex",
                                "alignItems": "center",
                                "margin": "1.5rem 0",
                                "color": "#8B4513"
                            }, children=[
                                html.Hr(style={
                                    "flex": "1",
                                    "height": "1px",
                                    "backgroundColor": "#E8E4D0",
                                    "border": "none",
                                    "margin": "0 1rem"
                                }),
                                html.Span("or", style={
                                    "fontSize": "0.9rem",
                                    "fontWeight": "500",
                                    "color": "#A67C52"
                                }),
                                html.Hr(style={
                                    "flex": "1",
                                    "height": "1px",
                                    "backgroundColor": "#E8E4D0",
                                    "border": "none",
                                    "margin": "0 1rem"
                                })
                            ]) if OAUTH_AVAILABLE else html.Div(),
                            
                            # Traditional login section (Secondary option)
                            html.Div(style={
                                "padding": "1.5rem",
                                "border": "2px solid #E8E4D0",
                                "borderRadius": "12px",
                                "backgroundColor": "#FEFEFE"
                            }, children=[
                                html.H4("Sign in with Username & Password", style={
                                    "color": "#2D5E40", 
                                    "marginBottom": "1.5rem",
                                    "textAlign": "center",
                                    "fontSize": "1.1rem",
                                    "fontWeight": "600"
                                }),
                                
                                # Username field
                                html.Div(style={"marginBottom": "1rem"}, children=[
                                    html.Label("Username", style={
                                        "fontWeight": "600", 
                                        "color": "#2D5E40", 
                                        "display": "block",
                                        "marginBottom": "0.5rem",
                                        "fontSize": "0.9rem"
                                    }),
                                    html.Div(className="input-group", style={"position": "relative"}, children=[
                                        html.I(className="fas fa-user", style={
                                            "position": "absolute",
                                            "left": "1rem",
                                            "top": "50%",
                                            "transform": "translateY(-50%)",
                                            "color": "#A67C52",
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
                                                "fontSize": "1rem",
                                                "transition": "border-color 0.3s ease"
                                            }
                                        )
                                    ])
                                ]),
                                
                                # Password field
                                html.Div(style={"marginBottom": "1.5rem"}, children=[
                                    html.Label("Password", style={
                                        "fontWeight": "600", 
                                        "color": "#2D5E40", 
                                        "display": "block",
                                        "marginBottom": "0.5rem",
                                        "fontSize": "0.9rem"
                                    }),
                                    html.Div(className="input-group", style={"position": "relative"}, children=[
                                        html.I(className="fas fa-lock", style={
                                            "position": "absolute",
                                            "left": "1rem",
                                            "top": "50%",
                                            "transform": "translateY(-50%)",
                                            "color": "#A67C52",
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
                                                "fontSize": "1rem",
                                                "transition": "border-color 0.3s ease"
                                            }
                                        )
                                    ])
                                ]),
                                
                                # Login button
                                html.Button([
                                    html.I(className="fas fa-sign-in-alt", style={"marginRight": "0.5rem"}),
                                    "Sign In to Dashboard"
                                ], id="login-submit-btn", n_clicks=0, style={
                                    "width": "100%", 
                                    "padding": "0.875rem", 
                                    "backgroundColor": "#F2C94C",
                                    "color": "#2D5E40", 
                                    "border": "none", 
                                    "borderRadius": "8px", 
                                    "fontWeight": "600", 
                                    "cursor": "pointer",
                                    "fontSize": "1rem",
                                    "transition": "all 0.3s ease",
                                    "display": "flex",
                                    "alignItems": "center",
                                    "justifyContent": "center"
                                })
                            ]),
                            
                            # Security notice
                            html.Div(style={
                                "marginTop": "1.5rem",
                                "padding": "1rem",
                                "backgroundColor": "rgba(45, 94, 64, 0.05)",
                                "borderRadius": "8px",
                                "border": "1px solid rgba(45, 94, 64, 0.1)",
                                "textAlign": "center"
                            }, children=[
                                html.I(className="fas fa-shield-alt", style={
                                    "color": "#2D5E40",
                                    "marginRight": "0.5rem",
                                    "fontSize": "1rem"
                                }),
                                html.Span("Authorized access only. Contact administrator for account access.", style={
                                    "color": "#2D5E40",
                                    "fontSize": "0.9rem",
                                    "fontWeight": "500"
                                })
                            ])
                        ])
                    ])
                ])
            ])
        ]),
        
        # Footer
        create_footer()
    ])

# ==================== PAGE WITH NAVIGATION ====================

def create_page_with_nav(page_name, content, active_nav_item):
    """Create a page with proper navigation"""
    live_time, header_time = get_current_time()
    
    # Get current user name for display
    user_display_name = "User"
    if OAUTH_AVAILABLE:
        try:
            oauth_user = get_current_user()
            if oauth_user:
                user_display_name = oauth_user.get('name', oauth_user.get('email', 'User')).split()[0]
        except Exception:
            pass
    
    nav_items = [
        {"title": "Dashboard", "path": "/main"},
        {"title": "Reports", "path": "/reports"},
        {"title": "Analytics", "path": "/analytics"},
        {"title": "Upload", "path": "/upload"},
        {"title": "Settings", "path": "/settings"}
    ]
    
    nav_elements = []
    for item in nav_items:
        is_active = item["title"] == active_nav_item
        nav_elements.append(
            html.A(
                item["title"], 
                href=item["path"], 
                className=f"header-nav-link {'active' if is_active else ''}"
            )
        )
    
    return html.Div(className="main-app-container", children=[
        # Header hover trigger area
        html.Div(className="header-hover-area"),
        
        # Header with navigation
        html.Header(className="header", children=[
            html.Div(className="container", children=[
                html.Div(className="header-content", children=[
                    html.Div(className="header-title", children=[
                        html.H1("Swaccha Andhra Dashboard")
                    ]),
                    html.Nav(className="header-nav", children=nav_elements),
                    html.Div(className="header-actions", children=[
                        html.Div(className="auto-refresh-indicator", children=[
                            html.I(className="fas fa-sync-alt"),
                            html.Span("Auto-refreshing")
                        ]),
                        html.Div(header_time, id="header-clock", className="clock-display"),
                        html.Span(user_display_name, style={"color": "#FEFEFE", "marginRight": "1rem"}),
                        html.Button("Logout", id="logout-btn", n_clicks=0, className="btn btn-accent", 
                                   **{
                                       'data-testid': 'logout-button',
                                       'style': {
                                           "backgroundColor": "#C74A3C",
                                           "color": "white", 
                                           "border": "none",
                                           "padding": "0.35rem 0.85rem",
                                           "borderRadius": "8px",
                                           "fontWeight": "600",
                                           "cursor": "pointer",
                                           "fontSize": "0.85rem"
                                       }
                                   })
                    ])
                ])
            ])
        ]),
        
        # Title Banner
        create_title_banner(),
        
        # Main content
        html.Main(className="dashboard-main-content", children=[
            html.Div(className="page-content-wrapper", children=[
                html.Div(className="container", children=content)
            ])
        ]),
        
        # Footer
        create_footer()
    ])

# ==================== ERROR PAGES ====================

def create_404_page():
    """Create 404 page"""
    return html.Div(className="container", style={"textAlign": "center", "padding": "3rem 0"}, children=[
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

def create_unauthorized_error_page():
    """Create unauthorized access error page"""
    return html.Div(style={
        "backgroundColor": "#FFFBF5",
        "minHeight": "100vh",
        "display": "flex",
        "flexDirection": "column",
        "justifyContent": "center",
        "alignItems": "center",
        "padding": "2rem",
        "textAlign": "center"
    }, children=[
        html.Div(style={
            "background": "white",
            "padding": "2rem",
            "borderRadius": "12px",
            "boxShadow": "0 4px 12px rgba(0, 0, 0, 0.1)",
            "maxWidth": "500px"
        }, children=[
            html.Img(src="/assets/img/right.png", alt="Logo", style={"width": "80px", "height": "80px", "marginBottom": "1rem"}),
            html.I(className="fas fa-user-slash", style={"fontSize": "3rem", "color": "#C74A3C", "marginBottom": "1rem"}),
            html.H2("Access Denied", style={"color": "#2D5E40", "marginBottom": "1rem"}),
            html.P("Your email address is not authorized to access this dashboard.", style={"color": "#8B4513", "marginBottom": "2rem"}),
            html.A("Back to Home", href="/", style={
                "backgroundColor": "#2D5E40", "color": "white", "padding": "0.75rem 1.5rem",
                "textDecoration": "none", "borderRadius": "8px", "fontWeight": "600"
            })
        ])
    ])

# ==================== ERROR BOUNDARY ====================

def create_error_boundary(error_message="An error occurred", show_debug=False):
    """Create an error boundary component for graceful error handling"""
    return html.Div(className="error-boundary", style={
        "backgroundColor": "#fff3cd",
        "border": "1px solid #ffeaa7",
        "borderRadius": "8px",
        "padding": "1rem",
        "margin": "1rem 0",
        "textAlign": "center"
    }, children=[
        html.I(className="fas fa-exclamation-triangle", style={
            "color": "#856404",
            "fontSize": "2rem",
            "marginBottom": "0.5rem"
        }),
        html.H3("Something went wrong", style={"color": "#856404", "margin": "0.5rem 0"}),
        html.P(error_message, style={"color": "#856404", "margin": "0.5rem 0"}),
        html.Button("Refresh Page", onClick="window.location.reload()", style={
            "backgroundColor": "#856404",
            "color": "white",
            "border": "none",
            "borderRadius": "4px",
            "padding": "0.5rem 1rem",
            "cursor": "pointer"
        })
    ])

print("✓ Layout components module loaded successfully")