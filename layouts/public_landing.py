"""
layouts/public_landing.py - Updated public dashboard layout with login only

This file defines a public dashboard that only shows login option.
"""

from dash import html, dcc
import dash_bootstrap_components as dbc

def create_public_dashboard():
    """
    Create a public dashboard that shows only basic info and login option.
    
    Returns:
        dash component: The public dashboard layout
    """
    
    # Overall dashboard layout - compact and efficient
    return html.Div(className="container", children=[
        # Compact page header
        html.Div(className="page-header", style={"margin": "0.5rem 0"}, children=[
            html.H2("Welcome to Swaccha Andhra Dashboard", style={"margin": "0 0 0.25rem 0"}),
            html.P("Real-Time Monitoring Dashboard for Legacy Waste Reclamation in Andhra Pradesh.", style={"margin": "0", "fontSize": "0.9rem"})
        ]),
        
        # Main content in a grid layout for efficient space usage
        html.Div(style={
            "display": "grid",
            "gridTemplateColumns": "repeat(auto-fit, minmax(250px, 1fr))",
            "gap": "1rem",
            "margin": "1rem 0"
        }, children=[
            # System Status Card
            html.Div(style={
                "background": "white",
                "borderRadius": "10px",
                "padding": "1rem",
                "boxShadow": "0 2px 8px rgba(0, 0, 0, 0.06)",
                "border": "1px solid #E8E4D0"
            }, children=[
                html.Div(style={"display": "flex", "alignItems": "center", "marginBottom": "0.5rem"}, children=[
                    html.I(className="fas fa-check-circle", style={"color": "#4A7E64", "marginRight": "0.5rem"}),
                    html.H3("System Status", style={"margin": "0", "fontSize": "1rem", "color": "#2D5E40"})
                ]),
                html.P("All systems operational", style={"margin": "0", "color": "#8B4513", "fontSize": "0.9rem"}),
                html.Div(style={"marginTop": "0.5rem"}, children=[
                    html.Div("✓ Data Processing", style={"fontSize": "0.8rem", "color": "#4A7E64"}),
                    html.Div("✓ Real-time Updates", style={"fontSize": "0.8rem", "color": "#4A7E64"}),
                    html.Div("✓ Network Connection", style={"fontSize": "0.8rem", "color": "#4A7E64"})
                ])
            ]),
            
            # Recent Updates Card
            html.Div(style={
                "background": "white",
                "borderRadius": "10px",
                "padding": "1rem",
                "boxShadow": "0 2px 8px rgba(0, 0, 0, 0.06)",
                "border": "1px solid #E8E4D0"
            }, children=[
                html.Div(style={"display": "flex", "alignItems": "center", "marginBottom": "0.5rem"}, children=[
                    html.I(className="fas fa-clock", style={"color": "#F2C94C", "marginRight": "0.5rem"}),
                    html.H3("Recent Updates", style={"margin": "0", "fontSize": "1rem", "color": "#2D5E40"})
                ]),
                html.P("Data last updated: May 27, 2025", style={"margin": "0", "color": "#8B4513", "fontSize": "0.9rem"}),
                html.Div(style={"marginTop": "0.5rem"}, children=[
                    html.Div("• Collection routes optimized", style={"fontSize": "0.8rem", "color": "#A67C52"}),
                    html.Div("• Processing efficiency: 94.7%", style={"fontSize": "0.8rem", "color": "#A67C52"}),
                    html.Div("• Monthly targets on track", style={"fontSize": "0.8rem", "color": "#A67C52"})
                ])
            ]),
            
            # Quick Stats Card
            html.Div(style={
                "background": "white",
                "borderRadius": "10px",
                "padding": "1rem",
                "boxShadow": "0 2px 8px rgba(0, 0, 0, 0.06)",
                "border": "1px solid #E8E4D0"
            }, children=[
                html.Div(style={"display": "flex", "alignItems": "center", "marginBottom": "0.5rem"}, children=[
                    html.I(className="fas fa-chart-bar", style={"color": "#C74A3C", "marginRight": "0.5rem"}),
                    html.H3("Quick Stats", style={"margin": "0", "fontSize": "1rem", "color": "#2D5E40"})
                ]),
                html.Div(style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "0.5rem"}, children=[
                    html.Div(children=[
                        html.Div("12,450", style={"fontSize": "1.2rem", "fontWeight": "700", "color": "#8B4513"}),
                        html.Div("MT This Month", style={"fontSize": "0.7rem", "color": "#A67C52"})
                    ]),
                    html.Div(children=[
                        html.Div("268K", style={"fontSize": "1.2rem", "fontWeight": "700", "color": "#8B4513"}),
                        html.Div("Total MT", style={"fontSize": "0.7rem", "color": "#A67C52"})
                    ]),
                    html.Div(children=[
                        html.Div("+15.3%", style={"fontSize": "1.2rem", "fontWeight": "700", "color": "#4A7E64"}),
                        html.Div("YoY Growth", style={"fontSize": "0.7rem", "color": "#A67C52"})
                    ]),
                    html.Div(children=[
                        html.Div("5", style={"fontSize": "1.2rem", "fontWeight": "700", "color": "#8B4513"}),
                        html.Div("Active Areas", style={"fontSize": "0.7rem", "color": "#A67C52"})
                    ])
                ])
            ])
        ]),
    ])