"""
layouts/public_landing.py - Public dashboard layout

This file defines the public dashboard with data cards and summary statistics.
"""

from dash import html, dcc
import dash_bootstrap_components as dbc

def create_public_dashboard():
    """
    Create the public dashboard with 9 compact square tiles.
    
    Returns:
        dash component: The dashboard layout
    """
    # Create cards A through I
    card_titles = ["Waste Collected", "Progress", "Vendors", "Clusters", 
                 "Completion Rate", "Sites", "Recent Activity", "Forecast", "Efficiency"]
    card_values = ["12,450 MT", "76.5%", "4", "12", "81.2%", "123", "24h", "Oct 2025", "94.7%"]
    card_icons = ["fa-trash", "fa-chart-line", "fa-building", "fa-layer-group", 
                "fa-check-circle", "fa-map-marker-alt", "fa-history", "fa-calendar", "fa-bolt"]
    card_changes = ["+2.5%", "+1.2%", "+0", "-1", "+4.3%", "+2", "↑", "-2 weeks", "+0.8%"]
    
    # Create all 9 cards with corresponding letters A-I
    cards = []
    letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
    
    for i in range(9):
        letter = letters[i]
        cards.append(
            html.Div(className=f"card card-theme-{letter.lower()}", children=[
                html.Div(className="card-content", children=[
                    # Card header
                    html.Div(className="card-header", children=[
                        html.H3(className="card-title", children=[
                            f"{card_titles[i]}"
                        ]),
                        html.I(className=f"card-icon fas {card_icons[i]}")
                    ]),
                    
                    # Card body
                    html.Div(className="card-body", children=[
                        html.Div(className="card-value", children=card_values[i]),
                        html.Div(className="card-label", children="Updated today")
                    ]),
                    
                    # Card footer
                    html.Div(className="card-footer", children=[
                        html.Div(className="card-change card-change-positive", children=[
                            html.I(className="fas fa-arrow-up"),
                            card_changes[i]
                        ]),
                        html.Div(className="card-date", children="May 20")
                    ])
                ])
            ])
        )
    
    # Overall dashboard layout
    return html.Div(className="container", children=[
        # Summary statistics
        html.Div(className="stats-summary", children=[
            # Header with title and time period selector
            html.Div(className="stats-header", children=[
                html.H2("Overall Progress"),
                html.Div(className="stats-filters", children=[
                    dcc.Dropdown(
                        id='time-period-selector',
                        options=[
                            {'label': 'Today', 'value': 'today'},
                            {'label': 'This Week', 'value': 'week'},
                            {'label': 'This Month', 'value': 'month'},
                            {'label': 'This Year', 'value': 'year'}
                        ],
                        value='month',
                        clearable=False,
                        searchable=False,
                        className="time-period-selector"
                    )
                ])
            ]),
            
            # Stats grid
            html.Div(className="stats-grid", children=[
                # Total collected
                html.Div(className="stat-item", children=[
                    html.Div(className="stat-value", children="268,450"),
                    html.Div(className="stat-label", children="Total MT Collected")
                ]),
                
                # Total remaining
                html.Div(className="stat-item", children=[
                    html.Div(className="stat-value", children="82,550"),
                    html.Div(className="stat-label", children="MT Remaining")
                ]),
                
                # Overall completion
                html.Div(className="stat-item", children=[
                    html.Div(className="stat-value", children="76.5%"),
                    html.Div(className="stat-label", children="Completion Rate")
                ]),
                
                # Active vendors
                html.Div(className="stat-item", children=[
                    html.Div(className="stat-value", children="4"),
                    html.Div(className="stat-label", children="Active Vendors")
                ])
            ])
        ]),
        
        # Main dashboard grid with 9 square cards
        html.Div(className="dashboard-grid", children=cards)
    ])