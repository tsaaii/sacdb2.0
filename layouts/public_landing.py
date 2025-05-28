"""
layouts/public_landing.py - Simplified public dashboard layout

This file defines a basic public dashboard without panels.
"""

from dash import html, dcc
import dash_bootstrap_components as dbc

def create_public_dashboard():
    """
    Create a simple public dashboard with basic content.
    
    Returns:
        dash component: The basic dashboard layout
    """
    
    # Overall dashboard layout
    return html.Div(className="container", children=[
        # Page title
        html.Div(className="page-header", children=[
            html.H2("Dashboard"),
            html.P("Welcome to the Swaccha Andhra Dashboard.")
        ]),
        
        # Basic content
        html.Div(className="content-section", children=[
            html.H3("System Status"),
            html.P("All systems are operational."),
            
            html.H3("Recent Updates"),
            html.P("Data last updated: May 27, 2025")
        ])
    ])