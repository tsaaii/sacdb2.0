"""
layouts/report_layout.py - Reports page layout

This file defines the reports page layout.
"""

from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
import pandas as pd

def create_reports_layout():
    """
    Create the reports page layout with filters and tables.
    
    Returns:
        dash component: The reports page layout
    """
    # Example data for reports
    sample_data = {
        'Date': ['2025-05-15', '2025-05-16', '2025-05-17', '2025-05-18', '2025-05-19', '2025-05-20'],
        'Waste Collected (MT)': [245, 280, 210, 310, 260, 290],
        'Area': ['North Guntur', 'East Guntur', 'South Guntur', 'West Guntur', 'Central Guntur', 'North Guntur'],
        'Vendor': ['Vendor A', 'Vendor B', 'Vendor C', 'Vendor B', 'Vendor A', 'Vendor C'],
        'Completion (%)': [94, 87, 91, 89, 95, 92]
    }
    
    # Create example dataframe
    df = pd.DataFrame(sample_data)
    
    # Layout for reports page
    layout = html.Div(className="container", children=[
        # Page title
        html.Div(className="page-header", children=[
            html.H2("Reports"),
            html.P("View, filter and export waste collection reports.")
        ]),
        
        # Filters section
        html.Div(className="filter-section", children=[
            html.Div(className="filter-row", children=[
                # Date range filter
                html.Div(className="filter-item", children=[
                    html.Label("Date Range"),
                    dcc.DatePickerRange(
                        id='date-range',
                        start_date_placeholder_text="Start Date",
                        end_date_placeholder_text="End Date",
                        calendar_orientation='horizontal',
                        className="date-picker"
                    )
                ]),
                
                # Area filter
                html.Div(className="filter-item", children=[
                    html.Label("Area"),
                    dcc.Dropdown(
                        id='area-filter',
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
                ]),
                
                # Vendor filter
                html.Div(className="filter-item", children=[
                    html.Label("Vendor"),
                    dcc.Dropdown(
                        id='vendor-filter',
                        options=[
                            {'label': 'All Vendors', 'value': 'all'},
                            {'label': 'Vendor A', 'value': 'a'},
                            {'label': 'Vendor B', 'value': 'b'},
                            {'label': 'Vendor C', 'value': 'c'},
                            {'label': 'Vendor D', 'value': 'd'}
                        ],
                        value='all',
                        clearable=False,
                        className="filter-dropdown"
                    )
                ])
            ]),
            
            # Action buttons
            html.Div(className="filter-actions", children=[
                html.Button("Apply Filters", id="apply-filters", className="btn btn-primary"),
                html.Button("Reset", id="reset-filters", className="btn btn-outline"),
                html.Button("Export CSV", id="export-csv", className="btn")
            ])
        ]),
        
        # Reports data table
        html.Div(className="report-table-container", children=[
            dash_table.DataTable(
                id='reports-table',
                columns=[{"name": i, "id": i} for i in df.columns],
                data=df.to_dict('records'),
                page_size=10,
                style_table={'overflowX': 'auto'},
                style_cell={
                    'textAlign': 'left',
                    'padding': '12px',
                    'fontFamily': '"Segoe UI", system-ui, -apple-system, sans-serif'
                },
                style_header={
                    'backgroundColor': 'var(--primary-green)',
                    'color': 'white',
                    'fontWeight': 'bold',
                    'textAlign': 'left'
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'var(--background-light)'
                    }
                ],
                sort_action='native',
                filter_action='native'
            )
        ]),
        
        # Summary metrics
        html.Div(className="report-summary", children=[
            html.Div(className="summary-item", children=[
                html.Span("Total Records:"),
                html.Strong("6")
            ]),
            html.Div(className="summary-item", children=[
                html.Span("Average Collection:"),
                html.Strong("265.8 MT")
            ]),
            html.Div(className="summary-item", children=[
                html.Span("Average Completion:"),
                html.Strong("91.3%")
            ])
        ])
    ])
    
    return layout