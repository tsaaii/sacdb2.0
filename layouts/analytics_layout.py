"""
layouts/analytics_layout.py - Analytics page layout

This file defines the analytics page with charts and trend analysis.
"""

from dash import html, dcc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def create_analytics_layout():
    """
    Create the analytics page layout with visualizations.
    
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
        font_family='"Segoe UI", system-ui, -apple-system, sans-serif',
        font_color='var(--text-dark)',
    )
    waste_fig.update_traces(line_color='var(--primary-green)')
    
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
        font_family='"Segoe UI", system-ui, -apple-system, sans-serif',
        font_color='var(--text-dark)',
    )
    
    # Create bar chart for area performance
    area_fig = go.Figure()
    area_fig.add_trace(go.Bar(
        x=areas,
        y=targets,
        name='Target',
        marker_color='var(--secondary-yellow)'
    ))
    area_fig.add_trace(go.Bar(
        x=areas,
        y=actuals,
        name='Actual',
        marker_color='var(--primary-green)'
    ))
    area_fig.update_layout(
        barmode='group',
        title='Area Performance vs Target',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=40, b=20),
        title_font_size=16,
        font_family='"Segoe UI", system-ui, -apple-system, sans-serif',
        font_color='var(--text-dark)',
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
        html.Div(className="filter-row", children=[
            # Time period selector
            html.Div(className="filter-item", children=[
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
                    clearable=False,
                    className="filter-dropdown"
                )
            ]),
            
            # Area selector
            html.Div(className="filter-item", children=[
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
                    clearable=False,
                    className="filter-dropdown"
                )
            ])
        ]),
        
        # Charts section
        html.Div(className="analytics-grid", children=[
            # Main trend chart
            html.Div(className="chart-card wide", children=[
                dcc.Graph(
                    id='waste-trend-chart',
                    figure=waste_fig,
                    className="chart"
                )
            ]),
            
            # Waste type composition
            html.Div(className="chart-card", children=[
                dcc.Graph(
                    id='waste-composition-chart',
                    figure=waste_types_fig,
                    className="chart"
                )
            ]),
            
            # Area performance
            html.Div(className="chart-card", children=[
                dcc.Graph(
                    id='area-performance-chart',
                    figure=area_fig,
                    className="chart"
                )
            ]),
            
            # Key metrics card
            html.Div(className="metrics-card", children=[
                html.H3("Key Performance Metrics"),
                html.Div(className="metrics-grid", children=[
                    html.Div(className="metric-item", children=[
                        html.Div(className="metric-value", children="268,450"),
                        html.Div(className="metric-label", children="Total MT Collected")
                    ]),
                    html.Div(className="metric-item", children=[
                        html.Div(className="metric-value", children="12,450"),
                        html.Div(className="metric-label", children="This Month (MT)")
                    ]),
                    html.Div(className="metric-item", children=[
                        html.Div(className="metric-value", children="+15.3%"),
                        html.Div(className="metric-label", children="YoY Growth")
                    ]),
                    html.Div(className="metric-item", children=[
                        html.Div(className="metric-value", children="94.7%"),
                        html.Div(className="metric-label", children="Processing Efficiency")
                    ])
                ])
            ])
        ])
    ])
    
    return layout