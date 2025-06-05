"""
layouts/error_layouts.py - Error page layouts for the dashboard

This file defines error page layouts that match the dashboard design.
"""

from dash import html, dcc

def create_unauthorized_error_layout():
    """
    Create an unauthorized access error page with contact information.
    
    Returns:
        dash component: The unauthorized error page layout
    """
    
    return html.Div(className="error-page-container", children=[
        # Error page content
        html.Div(className="error-container", children=[
            # Logo section
            html.Div(className="error-logo-section", children=[
                html.Img(
                    src="/assets/img/right.png", 
                    alt="Swaccha Andhra Logo",
                    className="error-logo",
                    style={"width": "100px", "height": "100px", "objectFit": "contain"}
                ),
                html.H1("Swaccha Andhra", style={"color": "#2D5E40", "marginBottom": "0.5rem"}),
                html.P("Waste Management Dashboard", style={"color": "#8B4513", "marginBottom": "2rem"})
            ]),
            
            # Error icon and message
            html.Div(className="error-content", children=[
                # Error icon
                html.Div(className="error-icon", children=[
                    html.I(className="fas fa-user-slash", style={
                        "fontSize": "4rem",
                        "color": "#C74A3C",
                        "marginBottom": "1.5rem"
                    })
                ]),
                
                # Error title
                html.H2("Oops! You don't have access", style={
                    "color": "#2D5E40",
                    "fontSize": "2rem",
                    "fontWeight": "700",
                    "marginBottom": "1rem"
                }),
                
                # Error description
                html.P("Your email address is not authorized to access this dashboard.", style={
                    "color": "#8B4513",
                    "fontSize": "1.1rem",
                    "marginBottom": "2rem",
                    "maxWidth": "600px",
                    "lineHeight": "1.6"
                }),
                
                # Contact information card
                html.Div(className="contact-card", style={
                    "background": "white",
                    "padding": "2rem",
                    "borderRadius": "12px",
                    "boxShadow": "0 4px 12px rgba(0, 0, 0, 0.1)",
                    "border": "1px solid #E8E4D0",
                    "marginBottom": "2rem",
                    "maxWidth": "500px"
                }, children=[
                    html.Div(style={"display": "flex", "alignItems": "center", "marginBottom": "1.5rem"}, children=[
                        html.I(className="fas fa-key", style={
                            "fontSize": "1.5rem",
                            "color": "#F2C94C",
                            "marginRight": "1rem",
                            "background": "rgba(242, 201, 76, 0.1)",
                            "padding": "0.75rem",
                            "borderRadius": "50%"
                        }),
                        html.H3("Request Access", style={"margin": "0", "color": "#2D5E40"})
                    ]),
                    
                    html.P("To get access to this dashboard, please send a text message with your email ID to:", style={
                        "color": "#8B4513",
                        "marginBottom": "1.5rem",
                        "lineHeight": "1.6"
                    }),
                    
                    # Phone number section
                    html.Div(className="phone-section", style={
                        "background": "linear-gradient(135deg, #2D5E40 0%, #4A7E64 100%)",
                        "color": "white",
                        "padding": "1.5rem",
                        "borderRadius": "8px",
                        "textAlign": "center",
                        "marginBottom": "1.5rem"
                    }, children=[
                        html.I(className="fas fa-mobile-alt", style={
                            "fontSize": "1.5rem",
                            "marginBottom": "0.5rem"
                        }),
                        html.Div("+91-6303-640-757", style={
                            "fontSize": "1.8rem",
                            "fontWeight": "700",
                            "letterSpacing": "1px"
                        }),
                        html.P("WhatsApp / SMS", style={
                            "margin": "0.5rem 0 0 0",
                            "fontSize": "0.9rem",
                            "opacity": "0.9"
                        })
                    ]),
                    
                    # Message template
                    html.Div(className="message-template", style={
                        "background": "#F8F4E6",
                        "padding": "1rem",
                        "borderRadius": "8px",
                        "border": "1px solid #E8E4D0"
                    }, children=[
                        html.P("Message template:", style={
                            "color": "#2D5E40",
                            "fontWeight": "600",
                            "marginBottom": "0.5rem"
                        }),
                        html.P('"Hi, I need access to Swaccha Andhra Dashboard. My email: [your-email@domain.com]"', style={
                            "color": "#8B4513",
                            "fontStyle": "italic",
                            "margin": "0",
                            "fontSize": "0.9rem"
                        })
                    ])
                ]),
                
                # Additional information
                html.Div(className="additional-info", style={
                    "background": "rgba(45, 94, 64, 0.05)",
                    "padding": "1.5rem",
                    "borderRadius": "8px",
                    "border": "1px solid rgba(45, 94, 64, 0.1)",
                    "marginBottom": "2rem",
                    "maxWidth": "500px"
                }, children=[
                    html.H4("What happens next?", style={"color": "#2D5E40", "marginBottom": "1rem"}),
                    html.Ul(style={"paddingLeft": "1.5rem", "color": "#8B4513"}, children=[
                        html.Li("Send your email ID via text to the number above"),
                        html.Li("Our admin will verify and add your email to the authorized list"),
                        html.Li("You'll receive confirmation within 24 hours"),
                        html.Li("Try logging in again with your Google account")
                    ])
                ]),
                
                # Action buttons
                html.Div(className="error-actions", style={
                    "display": "flex",
                    "gap": "1rem",
                    "justifyContent": "center",
                    "flexWrap": "wrap"
                }, children=[
                    html.A("Try Login Again", href="/", style={
                        "display": "inline-flex",
                        "alignItems": "center",
                        "padding": "0.75rem 1.5rem",
                        "backgroundColor": "#2D5E40",
                        "color": "white",
                        "textDecoration": "none",
                        "borderRadius": "8px",
                        "fontWeight": "600",
                        "transition": "all 0.3s ease"
                    }, children=[
                        html.I(className="fas fa-redo-alt", style={"marginRight": "0.5rem"}),
                        "Try Again"
                    ]),
                    
                    html.A("tel:+916303640757", style={
                        "display": "inline-flex",
                        "alignItems": "center",
                        "padding": "0.75rem 1.5rem",
                        "backgroundColor": "#F2C94C",
                        "color": "#2D5E40",
                        "textDecoration": "none",
                        "borderRadius": "8px",
                        "fontWeight": "600",
                        "transition": "all 0.3s ease"
                    }, children=[
                        html.I(className="fas fa-phone", style={"marginRight": "0.5rem"}),
                        "Call Now"
                    ])
                ])
            ])
        ]),
        
        # Footer
        html.Footer(className="error-footer", style={
            "marginTop": "3rem",
            "textAlign": "center",
            "color": "#A67C52",
            "fontSize": "0.9rem"
        }, children=[
            html.P("© 2025 Advitia Labs • Made in Andhra Pradesh", style={"margin": "0"})
        ])
    ], style={
        "backgroundColor": "#FFFBF5",
        "minHeight": "100vh",
        "display": "flex",
        "flexDirection": "column",
        "justifyContent": "center",
        "alignItems": "center",
        "padding": "2rem 1rem",
        "textAlign": "center"
    })

def create_generic_error_layout(error_type="unknown", error_message="An error occurred"):
    """
    Create a generic error page layout.
    
    Args:
        error_type: Type of error (auth_failed, oauth_not_configured, etc.)
        error_message: Custom error message
        
    Returns:
        dash component: Generic error page layout
    """
    
    # Error type specific configurations
    error_configs = {
        "auth_failed": {
            "icon": "fas fa-times-circle",
            "color": "#C74A3C",
            "title": "Authentication Failed",
            "message": "There was a problem logging you in. Please try again."
        },
        "oauth_not_configured": {
            "icon": "fas fa-cog",
            "color": "#F2C94C",
            "title": "System Configuration Error",
            "message": "The authentication system is not properly configured. Please contact the administrator."
        },
        "invalid_state": {
            "icon": "fas fa-shield-alt",
            "color": "#C74A3C",
            "title": "Security Error",
            "message": "Invalid security token. Please try logging in again."
        }
    }
    
    config = error_configs.get(error_type, {
        "icon": "fas fa-exclamation-triangle",
        "color": "#F2C94C",
        "title": "Error",
        "message": error_message
    })
    
    return html.Div(className="error-page-container", children=[
        html.Div(className="error-container", children=[
            # Logo
            html.Img(src="/assets/img/right.png", alt="Swaccha Andhra", 
                    style={"width": "80px", "height": "80px", "marginBottom": "1rem"}),
            
            # Error icon
            html.I(className=config["icon"], style={
                "fontSize": "3rem",
                "color": config["color"],
                "marginBottom": "1rem"
            }),
            
            # Error title
            html.H2(config["title"], style={
                "color": "#2D5E40",
                "marginBottom": "1rem"
            }),
            
            # Error message
            html.P(config["message"], style={
                "color": "#8B4513",
                "marginBottom": "2rem",
                "maxWidth": "500px"
            }),
            
            # Back button
            html.A("Back to Home", href="/", style={
                "display": "inline-flex",
                "alignItems": "center",
                "padding": "0.75rem 1.5rem",
                "backgroundColor": "#2D5E40",
                "color": "white",
                "textDecoration": "none",
                "borderRadius": "8px",
                "fontWeight": "600"
            }, children=[
                html.I(className="fas fa-home", style={"marginRight": "0.5rem"}),
                "Home"
            ])
        ])
    ], style={
        "backgroundColor": "#FFFBF5",
        "minHeight": "100vh",
        "display": "flex",
        "justifyContent": "center",
        "alignItems": "center",
        "textAlign": "center",
        "padding": "2rem"
    })