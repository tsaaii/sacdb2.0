"""
layouts/public_landing.py - Public dashboard layout

This file defines the public dashboard with futuristic data cards and summary statistics.
Updated with futuristic card designs and light color hues.
"""

from dash import html, dcc
import dash_bootstrap_components as dbc

def create_public_dashboard():
    """
    Create the public dashboard with 9 futuristic square tiles and stats.
    
    Returns:
        dash component: The dashboard layout
    """
    # Enhanced card data with futuristic styling
    card_data = [
        {
            "title": "Waste Collected",
            "value": "12,450",
            "unit": "MT",
            "icon": "fa-trash-alt",
            "change": "+2.5%",
            "status": "ACTIVE",
            "theme": "yellow",
            "glow": "amber"
        },
        {
            "title": "Progress",
            "value": "76.5",
            "unit": "%",
            "icon": "fa-chart-line",
            "change": "+1.2%",
            "status": "RISING",
            "theme": "green",
            "glow": "emerald"
        },
        {
            "title": "Vendors",
            "value": "4",
            "unit": "UNITS",
            "icon": "fa-building",
            "change": "+0",
            "status": "STABLE",
            "theme": "red",
            "glow": "coral"
        },
        {
            "title": "Clusters",
            "value": "12",
            "unit": "ZONES",
            "icon": "fa-layer-group",
            "change": "-1",
            "status": "OPTIMAL",
            "theme": "yellow",
            "glow": "gold"
        },
        {
            "title": "Completion Rate",
            "value": "81.2",
            "unit": "%",
            "icon": "fa-check-circle",
            "change": "+4.3%",
            "status": "TARGET",
            "theme": "green",
            "glow": "mint"
        },
        {
            "title": "Sites",
            "value": "123",
            "unit": "LOC",
            "icon": "fa-map-marker-alt",
            "change": "+2",
            "status": "ONLINE",
            "theme": "red",
            "glow": "rose"
        },
        {
            "title": "Recent Activity",
            "value": "24",
            "unit": "HRS",
            "icon": "fa-history",
            "change": "↑",
            "status": "LIVE",
            "theme": "yellow",
            "glow": "sunshine"
        },
        {
            "title": "Forecast",
            "value": "Oct",
            "unit": "2025",
            "icon": "fa-calendar-alt",
            "change": "-2W",
            "status": "PRED",
            "theme": "green",
            "glow": "forest"
        },
        {
            "title": "Efficiency",
            "value": "94.7",
            "unit": "%",
            "icon": "fa-bolt",
            "change": "+0.8%",
            "status": "PEAK",
            "theme": "red",
            "glow": "crimson"
        }
    ]
    
    # Create futuristic cards
    cards = []
    for i, card in enumerate(card_data):
        letter = chr(ord('A') + i)  # A, B, C, etc.
        
        cards.append(
            html.Div(className=f"card-futuristic card-theme-{card['theme']} card-glow-{card['glow']}", children=[
                # Background effects
                html.Div(className="card-bg-effect"),
                html.Div(className="card-scan-line"),
                
                html.Div(className="card-content-futuristic", children=[
                    # Card header with floating icon
                    html.Div(className="card-header-futuristic", children=[
                        html.Div(className="card-title-container", children=[
                            html.H3(className="card-title-futuristic", children=card['title']),
                            html.Div(className="card-id", children=letter)
                        ]),
                        html.Div(className="card-icon-container", children=[
                            html.I(className=f"card-icon-futuristic fas {card['icon']}")
                        ])
                    ]),
                    
                    # Card body with enhanced values
                    html.Div(className="card-body-futuristic", children=[
                        html.Div(className="card-value-container", children=[
                            html.Div(className="card-value-futuristic", children=card['value']),
                            html.Div(className="card-unit", children=card['unit'])
                        ]),
                        html.Div(className="card-status-indicator", children=[
                            html.Span(className="status-dot"),
                            html.Span(className="status-text", children=card['status'])
                        ])
                    ]),
                    
                    # Card footer with metrics
                    html.Div(className="card-footer-futuristic", children=[
                        html.Div(className="card-change-futuristic", children=[
                            html.I(className="fas fa-chevron-up change-icon"),
                            html.Span(card['change'])
                        ]),
                        html.Div(className="card-timestamp", children="LIVE")
                    ])
                ])
            ])
        )
    
    # Overall dashboard layout
    return html.Div(className="container", children=[
        # Futuristic Summary statistics - smaller and more compact
        html.Div(className="stats-summary-futuristic", children=[
            # Header with title only (no calendar filter)
            html.Div(className="stats-header-futuristic", children=[
                html.Div(className="stats-title-container", children=[
                    html.I(className="fas fa-chart-pulse stats-title-icon"),
                    html.H3("System Overview", className="stats-title-futuristic")
                ])
            ]),
            
            # Compact stats grid with futuristic design
            html.Div(className="stats-grid-futuristic", children=[
                # Total collected with progress ring
                html.Div(className="stat-item-futuristic", children=[
                    html.Div(className="stat-icon-container", children=[
                        html.I(className="fas fa-database stat-icon")
                    ]),
                    html.Div(className="stat-content", children=[
                        html.Div(className="stat-value-futuristic", children="268.45k"),
                        html.Div(className="stat-label-futuristic", children="MT Collected"),
                        html.Div(className="stat-progress", children=[
                            html.Div(className="progress-bar", style={"width": "76.5%"})
                        ])
                    ])
                ]),
                
                # Completion rate with circular progress
                html.Div(className="stat-item-futuristic", children=[
                    html.Div(className="stat-icon-container", children=[
                        html.I(className="fas fa-bullseye stat-icon")
                    ]),
                    html.Div(className="stat-content", children=[
                        html.Div(className="stat-value-futuristic", children="76.5%"),
                        html.Div(className="stat-label-futuristic", children="Completion"),
                        html.Div(className="stat-indicator success", children="ON TARGET")
                    ])
                ]),
                
                # Active systems
                html.Div(className="stat-item-futuristic", children=[
                    html.Div(className="stat-icon-container", children=[
                        html.I(className="fas fa-network-wired stat-icon")
                    ]),
                    html.Div(className="stat-content", children=[
                        html.Div(className="stat-value-futuristic", children="4"),
                        html.Div(className="stat-label-futuristic", children="Active Systems"),
                        html.Div(className="stat-indicator online", children="ONLINE")
                    ])
                ]),
                
                # Efficiency meter
                html.Div(className="stat-item-futuristic", children=[
                    html.Div(className="stat-icon-container", children=[
                        html.I(className="fas fa-tachometer-alt stat-icon")
                    ]),
                    html.Div(className="stat-content", children=[
                        html.Div(className="stat-value-futuristic", children="94.7%"),
                        html.Div(className="stat-label-futuristic", children="Efficiency"),
                        html.Div(className="stat-indicator optimal", children="OPTIMAL")
                    ])
                ])
            ])
        ]),
        
        # Main dashboard grid with 9 futuristic cards
        html.Div(className="dashboard-grid", children=cards)
    ])