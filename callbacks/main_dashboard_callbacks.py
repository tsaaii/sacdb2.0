"""
callbacks/main_dashboard_callbacks.py - Callbacks for main dashboard filtering

Add this file to enable filtering on the main dashboard.
"""

from dash import callback, Output, Input, State, no_update, html
import pandas as pd
import plotly.express as px

def load_ulb_data():
    """Load the actual ULB data from CSV file"""
    try:
        df = pd.read_csv('Joined_ULB_Data.csv')
        df.columns = df.columns.str.strip()
        df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y', errors='coerce')
        df['Days_since_start'] = pd.to_datetime(df['Days_since_start'], format='%m/%d/%Y', errors='coerce')
        df['percentage_of_completion'] = df['percentage_of_completion'].round(2)
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame()

@callback(
    [Output('main-dashboard-cards', 'children'),
     Output('main-trend-chart', 'figure'),
     Output('main-agency-chart', 'figure')],
    [Input('main-apply-filters-btn', 'n_clicks')],
    [State('main-agency-filter', 'value'),
     State('main-cluster-filter', 'value'),
     State('main-ulb-filter', 'value')]
)
def update_main_dashboard(n_clicks, agency, cluster, ulb):
    """Update the main dashboard based on applied filters"""
    
    # Load the data
    df = load_ulb_data()
    
    if df.empty:
        return [], {}, {}
    
    # Apply filters
    filtered_df = df.copy()
    
    if agency and agency != 'All Agencies':
        filtered_df = filtered_df[filtered_df['Agency'] == agency]
    
    if cluster and cluster != 'All Clusters':
        filtered_df = filtered_df[filtered_df['Cluster'] == cluster]
    
    if ulb and ulb != 'All ULBs':
        filtered_df = filtered_df[filtered_df['ULB'] == ulb]
    
    if filtered_df.empty:
        # Return empty state
        empty_cards = [
            html.Div("No data available for the selected filters.", 
                    style={"textAlign": "center", "padding": "2rem", "color": "#8B4513", "gridColumn": "1 / -1"})
        ]
        empty_fig = px.line(title="No data available")
        empty_fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        return empty_cards, empty_fig, empty_fig
    
    # Recalculate metrics based on filtered data
    total_target = filtered_df['Quantity_to_be_Remediated_x'].sum()
    total_completed = filtered_df['Cumulative_till_date'].sum()
    avg_completion = filtered_df['percentage_of_completion'].mean()
    unique_ulbs = filtered_df['ULB'].nunique()
    
    # For machine capacity calculation
    vendor_capacities = []
    for vendor_name in filtered_df['Sub_contractor'].unique():
        vendor_data = filtered_df[filtered_df['Sub_contractor'] == vendor_name]
        vendor_unique_capacities = vendor_data.drop_duplicates('No_of_machines')['Machine_capacity_per_day']
        vendor_capacities.extend(vendor_unique_capacities.tolist())
    daily_capacity = sum(vendor_capacities)
    
    # Create updated cards
    updated_cards = [
        # Total Target Card
        html.Div(style={
            "background": "linear-gradient(135deg, #2D5E40 0%, #4A7E64 100%)",
            "color": "white",
            "padding": "1.5rem",
            "borderRadius": "12px",
            "textAlign": "center",
            "boxShadow": "0 4px 12px rgba(0, 0, 0, 0.1)"
        }, children=[
            html.I(className="fas fa-target", style={"fontSize": "2rem", "marginBottom": "0.5rem", "opacity": "0.9"}),
            html.Div(f"{total_target:,.0f}", style={"fontSize": "2rem", "fontWeight": "700", "marginBottom": "0.25rem"}),
            html.Div("Total Target (MT)", style={"fontSize": "0.9rem", "opacity": "0.9"})
        ]),
        
        # Total Completed Card  
        html.Div(style={
            "background": "linear-gradient(135deg, #F2C94C 0%, #F2D06B 100%)",
            "color": "#2D5E40",
            "padding": "1.5rem",
            "borderRadius": "12px",
            "textAlign": "center",
            "boxShadow": "0 4px 12px rgba(0, 0, 0, 0.1)"
        }, children=[
            html.I(className="fas fa-check-circle", style={"fontSize": "2rem", "marginBottom": "0.5rem", "opacity": "0.8"}),
            html.Div(f"{total_completed:,.0f}", style={"fontSize": "2rem", "fontWeight": "700", "marginBottom": "0.25rem"}),
            html.Div("Total Completed (MT)", style={"fontSize": "0.9rem", "opacity": "0.8"})
        ]),
        
        # Average Completion Card
        html.Div(style={
            "background": "linear-gradient(135deg, #8B4513 0%, #A67C52 100%)",
            "color": "white",
            "padding": "1.5rem",
            "borderRadius": "12px",
            "textAlign": "center",
            "boxShadow": "0 4px 12px rgba(0, 0, 0, 0.1)"
        }, children=[
            html.I(className="fas fa-percent", style={"fontSize": "2rem", "marginBottom": "0.5rem", "opacity": "0.9"}),
            html.Div(f"{avg_completion:.1f}%", style={"fontSize": "2rem", "fontWeight": "700", "marginBottom": "0.25rem"}),
            html.Div("Avg Completion", style={"fontSize": "0.9rem", "opacity": "0.9"})
        ]),
        
        # Active ULBs Card
        html.Div(style={
            "background": "linear-gradient(135deg, #C74A3C 0%, #E76F51 100%)",
            "color": "white",
            "padding": "1.5rem",
            "borderRadius": "12px",
            "textAlign": "center",
            "boxShadow": "0 4px 12px rgba(0, 0, 0, 0.1)"
        }, children=[
            html.I(className="fas fa-city", style={"fontSize": "2rem", "marginBottom": "0.5rem", "opacity": "0.9"}),
            html.Div(f"{unique_ulbs}", style={"fontSize": "2rem", "fontWeight": "700", "marginBottom": "0.25rem"}),
            html.Div("Active ULBs", style={"fontSize": "0.9rem", "opacity": "0.9"})
        ]),
        
        # Daily Capacity Card
        html.Div(style={
            "background": "linear-gradient(135deg, #4A7E64 0%, #2D5E40 100%)",
            "color": "white",
            "padding": "1.5rem",
            "borderRadius": "12px",
            "textAlign": "center",
            "boxShadow": "0 4px 12px rgba(0, 0, 0, 0.1)"
        }, children=[
            html.I(className="fas fa-cogs", style={"fontSize": "2rem", "marginBottom": "0.5rem", "opacity": "0.9"}),
            html.Div(f"{daily_capacity:,.0f}", style={"fontSize": "2rem", "fontWeight": "700", "marginBottom": "0.25rem"}),
            html.Div("Daily Capacity (MT)", style={"fontSize": "0.9rem", "opacity": "0.9"})
        ])
    ]
    
    # Update trend chart
    df_time = filtered_df.groupby('Date').agg({
        'Cumulative_till_date': 'sum',
        'percentage_of_completion': 'mean'
    }).reset_index().sort_values('Date')
    
    trend_fig = px.line(
        df_time, 
        x='Date', 
        y='Cumulative_till_date',
        title='Cumulative Waste Remediation Trend (Filtered)',
        labels={'Cumulative_till_date': 'Cumulative (MT)', 'Date': ''}
    )
    trend_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=40, b=20),
        height=300,
        showlegend=False,
        title_font_size=16,
        font_family='"Segoe UI", system-ui, -apple-system, sans-serif'
    )
    trend_fig.update_traces(line_color='#2D5E40', line_width=3)
    
    # Update agency chart
    agency_performance = filtered_df.groupby('Agency').agg({
        'Cumulative_till_date': 'sum',
        'percentage_of_completion': 'mean'
    }).reset_index()
    
    agency_fig = px.bar(
        agency_performance,
        x='Agency',
        y='Cumulative_till_date',
        title='Agency Performance Comparison (Filtered)',
        labels={'Cumulative_till_date': 'Total Remediated (MT)', 'Agency': ''}
    )
    agency_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=40, b=20),
        height=300,
        showlegend=False,
        title_font_size=16,
        font_family='"Segoe UI", system-ui, -apple-system, sans-serif'
    )
    agency_fig.update_traces(marker_color='#4A7E64')
    
    return updated_cards, trend_fig, agency_fig

@callback(
    [Output('main-agency-filter', 'value'),
     Output('main-cluster-filter', 'value'),
     Output('main-ulb-filter', 'value')],
    [Input('main-reset-filters-btn', 'n_clicks')],
    prevent_initial_call=True
)
def reset_main_filters(n_clicks):
    """Reset all main dashboard filters"""
    if n_clicks:
        return 'All Agencies', 'All Clusters', 'All ULBs'
    return no_update, no_update, no_update