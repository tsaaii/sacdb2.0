"""
callbacks/routing_callback.py - Updated routing callback with enhanced dashboard

This file defines routing for both public and authenticated pages including the enhanced dashboard.
"""

from dash import callback, Output, Input, html, dcc
import pandas as pd
import plotly.express as px
from datetime import date

# Import existing layouts
try:
    from layouts.public_landing import create_public_dashboard
except ImportError:
    def create_public_dashboard():
        return html.Div(className="container", children=[
            html.H2("Welcome to Swaccha Andhra Dashboard"),
            html.P("Please login to access the full dashboard.")
        ])

try:
    from layouts.analytics_layout import create_analytics_layout
except ImportError:
    def create_analytics_layout():
        return html.Div(className="container", children=[
            html.H2("Analytics"),
            html.P("Analytics functionality will be available soon.")
        ])

try:
    from layouts.enhanced_main_layout import create_enhanced_main_dashboard
except ImportError:
    def create_enhanced_main_dashboard():
        return html.Div(className="container", children=[
            html.H2("Enhanced Dashboard"),
            html.P("Enhanced dashboard with filters not available. Using basic dashboard.")
        ])

def create_main_dashboard():
    """Create the enhanced main authenticated dashboard with filters and 4 responsive cards"""
    
    # Load the actual data
    try:
        df = pd.read_csv('Joined_ULB_Data.csv')
        df.columns = df.columns.str.strip()
        df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y', errors='coerce')
        df['Days_since_start'] = pd.to_datetime(df['Days_since_start'], format='%m/%d/%Y', errors='coerce')
        df['percentage_of_completion'] = df['percentage_of_completion'].round(2)
    except Exception as e:
        print(f"Error loading data: {e}")
        df = pd.DataFrame()
    
    if df.empty:
        return html.Div(className="container", children=[
            html.Div(className="alert alert-warning", children=[
                html.H4("Data Loading Error"),
                html.P("Could not load the ULB data file. Please ensure 'Joined_ULB_Data.csv' is available.")
            ])
        ])
    
    # Get unique values for filters
    agencies = ['All Vendors'] + sorted(df['Sub_contractor'].dropna().unique().tolist())
    clusters = ['All Clusters'] + sorted(df['Cluster'].dropna().unique().tolist())
    ulbs = ['All ULBs'] + sorted(df['ULB'].dropna().unique().tolist())
    
    # Get date range from data
    min_date = df['Date'].min().date() if not df['Date'].isna().all() else date.today()
    max_date = df['Date'].max().date() if not df['Date'].isna().all() else date.today()
    
    # Prepare data for line chart (% waste processed over time)
    df_time = df.groupby('Date').agg({
        'percentage_of_completion': 'mean',
        'Cumulative_till_date': 'sum',
        'Quantity_to_be_Remediated_x': 'sum'
    }).reset_index().sort_values('Date')
    
    # Create line chart for waste processing percentage over time
    line_fig = px.line(
        df_time, 
        x='Date', 
        y='percentage_of_completion',
        title='Waste Processing Progress (%)',
        labels={'percentage_of_completion': 'Completion %', 'Date': 'Date'}
    )
    line_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=30, b=20),
        height=200,
        showlegend=False,
        title_font_size=14,
        font_family='"Segoe UI", system-ui, -apple-system, sans-serif',
        xaxis_title='',
        yaxis_title='',
        xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)'),
        yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)')
    )
    line_fig.update_traces(line_color='#2D5E40', line_width=3)
    
    # Calculate metrics
    unique_machines = len(df['No_of_machines'].unique())
    # Get distinct machine capacities (not sum of all entries)
    unique_capacities = df.drop_duplicates('No_of_machines')['Machine_capacity_per_day']
    total_capacity = unique_capacities.sum()
    total_target = df['Quantity_to_be_Remediated_x'].sum()
    total_completed = df['Cumulative_till_date'].sum()
    avg_completion = df['percentage_of_completion'].mean()
    
    # Calculate expected vs actual progress
    days_elapsed = (max_date - min_date).days + 1 if max_date > min_date else 1
    expected_daily_processing = total_target / (days_elapsed * 2)  # Assuming reasonable timeline
    expected_completed = expected_daily_processing * days_elapsed
    progress_lag = ((expected_completed - total_completed) / expected_completed * 100) if expected_completed > 0 else 0
    
    # Calculate project completion timeline
    remaining_waste = total_target - total_completed
    daily_avg_processing = total_completed / days_elapsed if days_elapsed > 0 else 1
    days_to_complete = remaining_waste / daily_avg_processing if daily_avg_processing > 0 else 365
    completion_date = pd.Timestamp.now() + pd.Timedelta(days=int(days_to_complete))
    
    return html.Div(className="container", children=[
        # Page header
        html.Div(className="page-header", style={"margin": "0.5rem 0"}, children=[
            html.H2("Main Dashboard", style={"margin": "0 0 0.25rem 0"}),
            html.P("Real-time waste management monitoring with advanced analytics.", 
                   style={"margin": "0", "fontSize": "0.9rem"})
        ]),
        
        # Filter Section
        html.Div(className="filter-section", style={
            "background": "white",
            "borderRadius": "10px",
            "padding": "1.5rem",
            "boxShadow": "0 2px 8px rgba(0, 0, 0, 0.06)",
            "border": "1px solid #E8E4D0",
            "marginBottom": "1.5rem"
        }, children=[
            html.H3("Dashboard Filters", style={"color": "#2D5E40", "marginBottom": "1rem", "fontSize": "1.1rem"}),
            
            # Filter controls
            html.Div(style={
                "display": "grid",
                "gridTemplateColumns": "repeat(auto-fit, minmax(200px, 1fr))",
                "gap": "1rem",
                "marginBottom": "1rem"
            }, children=[
                # Vendor filter
                html.Div(children=[
                    html.Label("Vendor", style={"fontWeight": "600", "color": "#2D5E40", "marginBottom": "0.5rem", "display": "block"}),
                    dcc.Dropdown(
                        id='main-vendor-filter',
                        options=[{'label': vendor, 'value': vendor} for vendor in agencies],
                        value='All Vendors',
                        clearable=False,
                        style={"fontSize": "0.9rem"}
                    )
                ]),
                
                # Cluster filter
                html.Div(children=[
                    html.Label("Cluster", style={"fontWeight": "600", "color": "#2D5E40", "marginBottom": "0.5rem", "display": "block"}),
                    dcc.Dropdown(
                        id='main-cluster-filter',
                        options=[{'label': cluster, 'value': cluster} for cluster in clusters],
                        value='All Clusters',
                        clearable=False,
                        style={"fontSize": "0.9rem"}
                    )
                ]),
                
                # ULB filter
                html.Div(children=[
                    html.Label("ULB", style={"fontWeight": "600", "color": "#2D5E40", "marginBottom": "0.5rem", "display": "block"}),
                    dcc.Dropdown(
                        id='main-ulb-filter',
                        options=[{'label': ulb, 'value': ulb} for ulb in ulbs],
                        value='All ULBs',
                        clearable=False,
                        style={"fontSize": "0.9rem"}
                    )
                ]),
                
                # Date range filter
                html.Div(children=[
                    html.Label("Date Range", style={"fontWeight": "600", "color": "#2D5E40", "marginBottom": "0.5rem", "display": "block"}),
                    dcc.DatePickerRange(
                        id='main-date-filter',
                        start_date=min_date,
                        end_date=max_date,
                        display_format='YYYY-MM-DD',
                        style={"width": "100%"}
                    )
                ])
            ]),
            
            # Apply filters button
            html.Div(style={"marginTop": "1rem"}, children=[
                html.Button(
                    [html.I(className="fas fa-filter", style={"marginRight": "0.5rem"}), "Apply Filters"],
                    id="main-apply-filters-btn",
                    className="btn btn-primary",
                    n_clicks=0,
                    style={"fontSize": "0.9rem"}
                )
            ])
        ]),
        
        # Four Responsive Cards
        html.Div(id="main-dashboard-cards", style={
            "display": "grid",
            "gridTemplateColumns": "repeat(auto-fit, minmax(300px, 1fr))",
            "gap": "1.5rem",
            "marginBottom": "2rem"
        }, children=[
            # Card 1: Machine Count & Capacity
            html.Div(style={
                "background": "white",
                "borderRadius": "12px",
                "padding": "1.5rem",
                "boxShadow": "0 4px 12px rgba(0, 0, 0, 0.08)",
                "border": "1px solid #E8E4D0",
                "minHeight": "200px"
            }, children=[
                html.Div(style={"display": "flex", "alignItems": "center", "marginBottom": "1rem"}, children=[
                    html.I(className="fas fa-cogs", style={
                        "fontSize": "2rem", 
                        "color": "#2D5E40", 
                        "marginRight": "1rem",
                        "background": "rgba(45, 94, 64, 0.1)",
                        "padding": "0.5rem",
                        "borderRadius": "8px"
                    }),
                    html.H3("Machinery Overview", style={"margin": "0", "color": "#2D5E40"})
                ]),
                html.Div(style={"display": "flex", "justifyContent": "space-between", "alignItems": "center"}, children=[
                    html.Div(children=[
                        html.Div(f"{unique_machines}", style={"fontSize": "2.5rem", "fontWeight": "700", "color": "#8B4513"}),
                        html.Div("Unique Machines", style={"fontSize": "0.9rem", "color": "#A67C52", "marginBottom": "1rem"})
                    ]),
                    html.Div(children=[
                        html.Div(f"{total_capacity:,.0f}", style={"fontSize": "2.5rem", "fontWeight": "700", "color": "#4A7E64"}),
                        html.Div("MT/Day Capacity", style={"fontSize": "0.9rem", "color": "#A67C52"})
                    ])
                ])
            ]),
            
            # Card 2: Waste Processing Progress Chart
            html.Div(style={
                "background": "white",
                "borderRadius": "12px",
                "padding": "1.5rem",
                "boxShadow": "0 4px 12px rgba(0, 0, 0, 0.08)",
                "border": "1px solid #E8E4D0",
                "minHeight": "200px"
            }, children=[
                html.H3("Processing Progress", style={"margin": "0 0 1rem 0", "color": "#2D5E40"}),
                dcc.Graph(
                    id='main-progress-chart',
                    figure=line_fig,
                    config={'displayModeBar': False}
                )
            ]),
            
            # Card 3: Progress Analysis
            html.Div(style={
                "background": "white",
                "borderRadius": "12px",
                "padding": "1.5rem",
                "boxShadow": "0 4px 12px rgba(0, 0, 0, 0.08)",
                "border": "1px solid #E8E4D0",
                "minHeight": "200px"
            }, children=[
                html.Div(style={"display": "flex", "alignItems": "center", "marginBottom": "1rem"}, children=[
                    html.I(className="fas fa-chart-line", style={
                        "fontSize": "2rem", 
                        "color": "#F2C94C", 
                        "marginRight": "1rem",
                        "background": "rgba(242, 201, 76, 0.1)",
                        "padding": "0.5rem",
                        "borderRadius": "8px"
                    }),
                    html.H3("Progress Analysis", style={"margin": "0", "color": "#2D5E40"})
                ]),
                html.Div(children=[
                    html.Div(style={"marginBottom": "1rem"}, children=[
                        html.Div("Expected Progress", style={"fontSize": "0.9rem", "color": "#A67C52"}),
                        html.Div(f"{expected_completed:,.0f} MT", style={"fontSize": "1.2rem", "fontWeight": "600", "color": "#8B4513"})
                    ]),
                    html.Div(style={"marginBottom": "1rem"}, children=[
                        html.Div("Actual Progress", style={"fontSize": "0.9rem", "color": "#A67C52"}),
                        html.Div(f"{total_completed:,.0f} MT", style={"fontSize": "1.2rem", "fontWeight": "600", "color": "#8B4513"})
                    ]),
                    html.Div(children=[
                        html.Div("Performance Gap", style={"fontSize": "0.9rem", "color": "#A67C52"}),
                        html.Div(f"{abs(progress_lag):.1f}% {'Behind' if progress_lag > 0 else 'Ahead'}", 
                                style={"fontSize": "1.5rem", "fontWeight": "700", 
                                      "color": "#C74A3C" if progress_lag > 0 else "#4A7E64"})
                    ])
                ])
            ]),
            
            # Card 4: Project Timeline
            html.Div(style={
                "background": "white",
                "borderRadius": "12px",
                "padding": "1.5rem",
                "boxShadow": "0 4px 12px rgba(0, 0, 0, 0.08)",
                "border": "1px solid #E8E4D0",
                "minHeight": "200px"
            }, children=[
                html.Div(style={"display": "flex", "alignItems": "center", "marginBottom": "1rem"}, children=[
                    html.I(className="fas fa-calendar-alt", style={
                        "fontSize": "2rem", 
                        "color": "#C74A3C", 
                        "marginRight": "1rem",
                        "background": "rgba(199, 74, 60, 0.1)",
                        "padding": "0.5rem",
                        "borderRadius": "8px"
                    }),
                    html.H3("Project Timeline", style={"margin": "0", "color": "#2D5E40"})
                ]),
                html.Div(children=[
                    html.Div(style={"marginBottom": "1rem"}, children=[
                        html.Div("Remaining Work", style={"fontSize": "0.9rem", "color": "#A67C52"}),
                        html.Div(f"{remaining_waste:,.0f} MT", style={"fontSize": "1.2rem", "fontWeight": "600", "color": "#8B4513"})
                    ]),
                    html.Div(style={"marginBottom": "1rem"}, children=[
                        html.Div("Days to Complete", style={"fontSize": "0.9rem", "color": "#A67C52"}),
                        html.Div(f"{int(days_to_complete)} days", style={"fontSize": "1.5rem", "fontWeight": "700", "color": "#C74A3C"})
                    ]),
                    html.Div(children=[
                        html.Div("Expected Completion", style={"fontSize": "0.9rem", "color": "#A67C52"}),
                        html.Div(completion_date.strftime("%B %d, %Y"), 
                                style={"fontSize": "1.1rem", "fontWeight": "600", "color": "#2D5E40"})
                    ])
                ])
            ])
        ]),
        
        # Quick Actions Section
        html.Div(style={
            "background": "white",
            "borderRadius": "10px",
            "padding": "1.5rem",
            "boxShadow": "0 2px 8px rgba(0, 0, 0, 0.06)",
            "border": "1px solid #E8E4D0"
        }, children=[
            html.H3("Quick Actions", style={"color": "#2D5E40", "marginBottom": "1rem"}),
            html.Div(style={"display": "flex", "gap": "1rem", "flexWrap": "wrap"}, children=[
                html.A("Enhanced Dashboard", href="/enhanced", className="btn btn-primary", 
                       style={"fontSize": "0.9rem"}),
                html.A("View Analytics", href="/analytics", className="btn btn-outline", 
                       style={"fontSize": "0.9rem"}),
                html.A("Generate Reports", href="/reports", className="btn", 
                       style={"fontSize": "0.9rem"}),
                html.A("Upload Data", href="/upload", className="btn btn-accent", 
                       style={"fontSize": "0.9rem"})
            ])
        ])
    ])

def create_reports_layout():
    """Create reports layout"""
    return html.Div(className="container", children=[
        html.H2("Reports"),
        html.P("Comprehensive reporting and data export functionality."),
        html.Div(className="content-section", children=[
            html.H3("Available Reports"),
            html.Ul(children=[
                html.Li("Daily Collection Summary"),
                html.Li("Weekly Performance Report"),
                html.Li("Monthly Analytics"),
                html.Li("Equipment Utilization"),
                html.Li("Area-wise Progress")
            ])
        ])
    ])

@callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    """
    Route to the appropriate page layout based on URL.
    
    Args:
        pathname: Current URL pathname
        
    Returns:
        dash.components: The page layout for the requested route
    """
    # Route to appropriate layout based on pathname
    if pathname == '/' or pathname is None:
        # Public landing page
        return create_public_dashboard()
    elif pathname == '/main':
        # Main authenticated dashboard
        return create_main_dashboard()
    elif pathname == '/enhanced':
        # NEW: Enhanced dashboard with filters and data table
        return create_enhanced_main_dashboard()
    elif pathname == '/reports':
        return create_reports_layout()
    elif pathname == '/analytics':
        return create_analytics_layout()
    elif pathname == '/upload':
        return html.Div(className="container", children=[
            html.H2("Upload Data"),
            html.P("Upload waste collection data and reports."),
            html.Div(className="upload-section", children=[
                html.Div(className="upload-container", children=[
                    html.I(className="fas fa-cloud-upload-alt upload-icon"),
                    html.P("Drag and drop files here or click to browse"),
                    html.Button("Browse Files", className="btn btn-primary"),
                    html.P("Accepted formats: CSV, Excel, PDF", className="upload-formats")
                ])
            ])
        ])
    elif pathname == '/settings':
        return html.Div(className="container", children=[
            html.H2("Settings"),
            html.P("Customize your dashboard experience."),
            html.Div(className="settings-section", children=[
                html.H3("Display Settings"),
                html.Div(className="settings-option", children=[
                    html.Label("Theme Mode"),
                    html.Div(className="settings-controls", children=[
                        html.Button("Light", id="light-theme", className="btn btn-primary", n_clicks=0),
                        html.Button("Dark", id="dark-theme", className="btn btn-outline", n_clicks=0),
                        html.Button("Auto", id="auto-theme", className="btn btn-outline", n_clicks=0)
                    ])
                ]),
                html.Div(className="settings-option", children=[
                    html.Label("Navigation Bar"),
                    html.Div(className="settings-controls", children=[
                        html.Button("Show on Hover", id="nav-hover", className="btn btn-primary", n_clicks=0),
                        html.Button("Always Show", id="nav-show", className="btn btn-outline", n_clicks=0)
                    ])
                ])
            ])
        ])
    elif pathname == '/login':
        # Import login layout
        try:
            from layouts.login_layout import create_login_layout
            return create_login_layout()
        except ImportError:
            # Fallback login page if login_layout.py is not available
            return html.Div(className="container", children=[
                html.H2("Login"),
                html.P("Please log in to access the full dashboard features."),
                html.Div(className="form-container", children=[
                    html.Div(className="form-group", children=[
                        html.Label("Username"),
                        html.Input(type="text", className="form-control", placeholder="Enter username")
                    ]),
                    html.Div(className="form-group", children=[
                        html.Label("Password"),
                        html.Input(type="password", className="form-control", placeholder="Enter password")
                    ]),
                    html.A("Login to Dashboard", href="/main", className="btn btn-primary", 
                           style={"width": "100%", "textAlign": "center", "display": "block"}),
                    html.A("Forgot Password?", href="#", className="form-link")
                ])
            ])
    else:
        # 404 page
        return html.Div(className="container", children=[
            html.Div(className="error-container", children=[
                html.H1("404", className="error-code"),
                html.H2("Page Not Found", className="error-title"),
                html.P("The page you requested does not exist."),
                html.A("Go to Home", href="/", className="btn btn-primary")
            ])
        ])