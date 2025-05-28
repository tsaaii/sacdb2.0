"""
layouts/analytics_layout.py - Simplified analytics page layout

This file defines the analytics page with basic charts.
"""

from dash import html, dcc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def create_analytics_layout():
    """
    Create the analytics page layout with basic visualizations.
    
    Returns:
        dash component: The analytics page layout
    """
    # Generate sample data for charts
    dates = pd.date_range(start='2025-01-01', end='2025-05-20')
    waste_collected = np.cumsum(np.random.uniform(200, 320, size=len(dates)))
    
    # Sample data for pie chart
    waste_types = ['Plastic', 'Organic', 'Paper', 'Metal', 'Glass', 'Other']
    waste_percentages = [35, 25, 20, 10, 5, 5]
    
    # Sample data for area performance
    areas = ['North Guntur', 'East Guntur', 'South Guntur', 'West Guntur', 'Central Guntur']
    targets = [100, 100, 100, 100, 100]
    actuals = [92, 87, 105, 95, 101]
    
    # Create line chart for waste collection over time
    waste_fig = px.line(
        x=dates, 
        y=waste_collected,
        labels={'x': 'Date', 'y': 'Cumulative Waste Collected (MT)'},
        title='Waste Collection Trend (YTD 2025)'
    )
    waste_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=40, b=20),
        hovermode='x',
        xaxis_title='',
        yaxis_title='',
        title_font_size=16,
        font_family='"Segoe UI", system-ui, -apple-system, sans-serif'
    )
    
    # Create pie chart for waste composition
    waste_types_fig = px.pie(
        values=waste_percentages,
        names=waste_types,
        title='Waste Composition by Type',
        color_discrete_sequence=px.colors.sequential.Greens
    )
    waste_types_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=40, b=20),
        title_font_size=16,
        font_family='"Segoe UI", system-ui, -apple-system, sans-serif'
    )
    
    # Create bar chart for area performance
    area_fig = go.Figure()
    area_fig.add_trace(go.Bar(
        x=areas,
        y=targets,
        name='Target',
        marker_color='#F2D06B'
    ))
    area_fig.add_trace(go.Bar(
        x=areas,
        y=actuals,
        name='Actual',
        marker_color='#2D5E40'
    ))
    area_fig.update_layout(
        barmode='group',
        title='Area Performance vs Target',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=40, b=20),
        title_font_size=16,
        font_family='"Segoe UI", system-ui, -apple-system, sans-serif',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    # Layout for analytics page
    layout = html.Div(className="container", children=[
        # Page title
        html.Div(className="page-header", children=[
            html.H2("Analytics"),
            html.P("Data trends and visual insights for waste management progress.")
        ]),
        
        # Top row with filters
        html.Div(className="content-section", children=[
            html.H3("Filters"),
            html.Div(style={"display": "flex", "gap": "1rem", "flexWrap": "wrap", "marginBottom": "1rem"}, children=[
                # Time period selector
                html.Div(style={"flex": "1", "minWidth": "180px"}, children=[
                    html.Label("Time Period"),
                    dcc.Dropdown(
                        id='analytics-time-period',
                        options=[
                            {'label': 'Last 30 Days', 'value': '30d'},
                            {'label': 'Last 90 Days', 'value': '90d'},
                            {'label': 'Year to Date', 'value': 'ytd'},
                            {'label': 'Last 12 Months', 'value': '12m'}
                        ],
                        value='ytd',
                        clearable=False
                    )
                ]),
                
                # Area selector
                html.Div(style={"flex": "1", "minWidth": "180px"}, children=[
                    html.Label("Area"),
                    dcc.Dropdown(
                        id='analytics-area',
                        options=[
                            {'label': 'All Areas', 'value': 'all'},
                            {'label': 'North Guntur', 'value': 'north'},
                            {'label': 'East Guntur', 'value': 'east'},
                            {'label': 'South Guntur', 'value': 'south'},
                            {'label': 'West Guntur', 'value': 'west'},
                            {'label': 'Central Guntur', 'value': 'central'}
                        ],
                        value='all',
                        clearable=False
                    )
                ])
            ])
        ]),
        
        # Charts section
        html.Div(className="content-section", children=[
            html.H3("Charts"),
            
            # Main trend chart
            html.Div(style={"marginBottom": "2rem"}, children=[
                dcc.Graph(
                    id='waste-trend-chart',
                    figure=waste_fig
                )
            ]),
            
            # Row with two charts
            html.Div(style={"display": "grid", "gridTemplateColumns": "repeat(auto-fit, minmax(400px, 1fr))", "gap": "1rem", "marginBottom": "2rem"}, children=[
                # Waste type composition
                html.Div(children=[
                    dcc.Graph(
                        id='waste-composition-chart',
                        figure=waste_types_fig
                    )
                ]),
                
                # Area performance
                html.Div(children=[
                    dcc.Graph(
                        id='area-performance-chart',
                        figure=area_fig
                    )
                ])
            ]),
            
            # Key metrics
            html.Div(children=[
                html.H3("Key Performance Metrics"),
                html.Div(style={"display": "grid", "gridTemplateColumns": "repeat(auto-fit, minmax(200px, 1fr))", "gap": "1rem", "marginTop": "1rem"}, children=[
                    html.Div(children=[
                        html.Div("268,450", style={"fontSize": "1.5rem", "fontWeight": "700", "color": "#8B4513"}),
                        html.Div("Total MT Collected", style={"fontSize": "0.75rem", "color": "#A67C52"})
                    ]),
                    html.Div(children=[
                        html.Div("12,450", style={"fontSize": "1.5rem", "fontWeight": "700", "color": "#8B4513"}),
                        html.Div("This Month (MT)", style={"fontSize": "0.75rem", "color": "#A67C52"})
                    ]),
                    html.Div(children=[
                        html.Div("+15.3%", style={"fontSize": "1.5rem", "fontWeight": "700", "color": "#8B4513"}),
                        html.Div("YoY Growth", style={"fontSize": "0.75rem", "color": "#A67C52"})
                    ]),
                    html.Div(children=[
                        html.Div("94.7%", style={"fontSize": "1.5rem", "fontWeight": "700", "color": "#8B4513"}),
                        html.Div("Processing Efficiency", style={"fontSize": "0.75rem", "color": "#A67C52"})
                    ])
                ])
            ])
        ])
    ])
    
    return layout