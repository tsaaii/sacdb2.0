"""
layouts/analytics_layout.py - Analytics page layout using real CSV data

This file defines the analytics page with charts based on actual ULB data.
"""

from dash import html, dcc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def load_ulb_data():
    """Load the actual ULB data from CSV file"""
    try:
        # Load the CSV data
        df = pd.read_csv('Joined_ULB_Data.csv')
        
        # Clean column names
        df.columns = df.columns.str.strip()
        
        # Convert date column to proper datetime format
        df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y', errors='coerce')
        df['Days_since_start'] = pd.to_datetime(df['Days_since_start'], format='%m/%d/%Y', errors='coerce')
        
        # Round percentage to 2 decimal places
        df['percentage_of_completion'] = df['percentage_of_completion'].round(2)
        
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        # Return empty dataframe if file not found
        return pd.DataFrame()

def create_analytics_layout():
    """
    Create the analytics page layout with visualizations based on real ULB data.
    
    Returns:
        dash component: The analytics page layout
    """
    # Load the actual data
    df = load_ulb_data()
    
    if df.empty:
        return html.Div(className="container", children=[
            html.Div(className="alert alert-warning", children=[
                html.H4("Data Loading Error"),
                html.P("Could not load the ULB data file. Please ensure 'Joined_ULB_Data.csv' is available.")
            ])
        ])
    
    # Prepare data for charts
    
    # 1. Cumulative waste remediation over time (grouped by date)
    df_time = df.groupby('Date').agg({
        'Quantity_remediated_today': 'sum',
        'Cumulative_till_date': 'sum'
    }).reset_index().sort_values('Date')
    
    # 2. Agency performance comparison
    agency_performance = df.groupby('Agency').agg({
        'Cumulative_till_date': 'sum',
        'Quantity_to_be_Remediated_x': 'sum',
        'percentage_of_completion': 'mean',
        'No_of_machines': 'sum'
    }).reset_index()
    agency_performance['completion_rate'] = (agency_performance['Cumulative_till_date'] / 
                                           agency_performance['Quantity_to_be_Remediated_x'] * 100).round(2)
    
    # 3. ULB-wise completion status
    ulb_performance = df.groupby('ULB').agg({
        'percentage_of_completion': 'mean',
        'Cumulative_till_date': 'sum',
        'Balance_Quantity': 'sum'
    }).reset_index().sort_values('percentage_of_completion', ascending=False)
    
    # 4. Cluster distribution
    cluster_data = df.groupby('Cluster').agg({
        'Cumulative_till_date': 'sum',
        'ULB': 'nunique'
    }).reset_index()
    
    # Create charts
    
    # 1. Time series chart for cumulative remediation
    time_fig = px.line(
        df_time, 
        x='Date', 
        y='Cumulative_till_date',
        title='Cumulative Waste Remediation Over Time',
        labels={'Cumulative_till_date': 'Cumulative Remediated (MT)', 'Date': 'Date'}
    )
    time_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=40, b=20),
        hovermode='x unified',
        xaxis_title='',
        yaxis_title='',
        title_font_size=16,
        font_family='"Segoe UI", system-ui, -apple-system, sans-serif'
    )
    
    # 2. Agency performance comparison
    agency_fig = go.Figure()
    agency_fig.add_trace(go.Bar(
        x=agency_performance['Agency'],
        y=agency_performance['Cumulative_till_date'],
        name='Cumulative Remediated (MT)',
        marker_color='#2D5E40',
        yaxis='y'
    ))
    agency_fig.add_trace(go.Scatter(
        x=agency_performance['Agency'],
        y=agency_performance['completion_rate'],
        mode='lines+markers',
        name='Completion Rate (%)',
        line=dict(color='#F2C94C', width=3),
        marker=dict(size=8),
        yaxis='y2'
    ))
    agency_fig.update_layout(
        title='Agency Performance Comparison',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=40, b=20),
        title_font_size=16,
        font_family='"Segoe UI", system-ui, -apple-system, sans-serif',
        yaxis=dict(title='Cumulative Remediated (MT)', side='left'),
        yaxis2=dict(title='Completion Rate (%)', side='right', overlaying='y'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    # 3. ULB completion status pie chart
    # Categorize ULBs by completion status
    completion_categories = []
    for _, row in ulb_performance.iterrows():
        if row['percentage_of_completion'] >= 80:
            completion_categories.append('High Progress (≥80%)')
        elif row['percentage_of_completion'] >= 50:
            completion_categories.append('Medium Progress (50-79%)')
        elif row['percentage_of_completion'] >= 20:
            completion_categories.append('Low Progress (20-49%)')
        else:
            completion_categories.append('Very Low Progress (<20%)')
    
    completion_counts = pd.Series(completion_categories).value_counts()
    
    completion_fig = px.pie(
        values=completion_counts.values,
        names=completion_counts.index,
        title='ULB Completion Status Distribution',
        color_discrete_sequence=['#2D5E40', '#4A7E64', '#F2C94C', '#C74A3C']
    )
    completion_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=40, b=20),
        title_font_size=16,
        font_family='"Segoe UI", system-ui, -apple-system, sans-serif'
    )
    
    # 4. Cluster performance bar chart
    cluster_fig = px.bar(
        cluster_data.sort_values('Cumulative_till_date', ascending=True),
        x='Cumulative_till_date',
        y='Cluster',
        orientation='h',
        title='Cluster-wise Remediation Progress',
        labels={'Cumulative_till_date': 'Cumulative Remediated (MT)', 'Cluster': 'Cluster'},
        color='Cumulative_till_date',
        color_continuous_scale='Greens'
    )
    cluster_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=40, b=20),
        title_font_size=16,
        font_family='"Segoe UI", system-ui, -apple-system, sans-serif',
        showlegend=False
    )
    
    # Calculate real metrics from data
    total_target = df['Quantity_to_be_Remediated_x'].sum()
    total_remediated = df['Cumulative_till_date'].sum()
    avg_completion = df['percentage_of_completion'].mean()
    unique_machines = len(df['No_of_machines'].unique())
    
    # For machine capacity: sum distinct max machines across all vendors
    vendor_capacities = []
    for vendor_name in df['Sub_contractor'].unique():
        vendor_data = df[df['Sub_contractor'] == vendor_name]
        vendor_unique_capacities = vendor_data.drop_duplicates('No_of_machines')['Machine_capacity_per_day']
        vendor_capacities.extend(vendor_unique_capacities.tolist())
    daily_capacity = sum(vendor_capacities)
    
    # Layout for analytics page
    layout = html.Div(className="container", children=[
        # Page title
        html.Div(className="page-header", children=[
            html.H2("Analytics Dashboard"),
            html.P("Data trends and visual insights for waste management progress based on real-time data.")
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
                            {'label': 'All Time', 'value': 'all'}
                        ],
                        value='all',
                        clearable=False
                    )
                ]),
                
                # Agency selector
                html.Div(style={"flex": "1", "minWidth": "180px"}, children=[
                    html.Label("Agency"),
                    dcc.Dropdown(
                        id='analytics-agency',
                        options=[{'label': 'All Agencies', 'value': 'all'}] + 
                               [{'label': agency, 'value': agency} for agency in sorted(df['Agency'].unique())],
                        value='all',
                        clearable=False
                    )
                ])
            ])
        ]),
        
        # Charts section
        html.Div(className="content-section", children=[
            html.H3("Visual Analytics"),
            
            # Main trend chart
            html.Div(style={"marginBottom": "2rem"}, children=[
                dcc.Graph(
                    id='waste-trend-chart',
                    figure=time_fig
                )
            ]),
            
            # Row with two charts
            html.Div(style={"display": "grid", "gridTemplateColumns": "repeat(auto-fit, minmax(400px, 1fr))", "gap": "1rem", "marginBottom": "2rem"}, children=[
                # Agency performance
                html.Div(children=[
                    dcc.Graph(
                        id='agency-performance-chart',
                        figure=agency_fig
                    )
                ]),
                
                # ULB completion status
                html.Div(children=[
                    dcc.Graph(
                        id='completion-status-chart',
                        figure=completion_fig
                    )
                ])
            ]),
            
            # Cluster performance chart
            html.Div(style={"marginBottom": "2rem"}, children=[
                dcc.Graph(
                    id='cluster-performance-chart',
                    figure=cluster_fig
                )
            ]),
            
            # Key metrics based on real data
            html.Div(children=[
                html.H3("Key Performance Metrics"),
                html.Div(style={"display": "grid", "gridTemplateColumns": "repeat(auto-fit, minmax(200px, 1fr))", "gap": "1rem", "marginTop": "1rem"}, children=[
                    html.Div(children=[
                        html.Div(f"{total_target:,.0f}", style={"fontSize": "1.5rem", "fontWeight": "700", "color": "#8B4513"}),
                        html.Div("Total Target (MT)", style={"fontSize": "0.75rem", "color": "#A67C52"})
                    ]),
                    html.Div(children=[
                        html.Div(f"{total_remediated:,.0f}", style={"fontSize": "1.5rem", "fontWeight": "700", "color": "#8B4513"}),
                        html.Div("Total Remediated (MT)", style={"fontSize": "0.75rem", "color": "#A67C52"})
                    ]),
                    html.Div(children=[
                        html.Div(f"{avg_completion:.1f}%", style={"fontSize": "1.5rem", "fontWeight": "700", "color": "#4A7E64"}),
                        html.Div("Average Completion", style={"fontSize": "0.75rem", "color": "#A67C52"})
                    ]),
                    html.Div(children=[
                        html.Div(f"{unique_machines}", style={"fontSize": "1.5rem", "fontWeight": "700", "color": "#8B4513"}),
                        html.Div("Unique Machines", style={"fontSize": "0.75rem", "color": "#A67C52"})
                    ]),
                    html.Div(children=[
                        html.Div(f"{daily_capacity:,.0f}", style={"fontSize": "1.5rem", "fontWeight": "700", "color": "#8B4513"}),
                        html.Div("Daily Capacity (MT)", style={"fontSize": "0.75rem", "color": "#A67C52"})
                    ])
                ])
            ])
        ])
    ])
    
    return layout