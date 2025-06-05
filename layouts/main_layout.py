"""
layouts/main_layout.py - Updated main layout with global session management

This file defines the main layout with session store available globally.
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
import datetime

def create_main_layout():
    """
    Create the main application layout with global session management.
    
    Returns:
        dash component: The main layout structure with global session
    """
    # Define color constants
    DARK_GREEN = "#2D5E40"  # Primary green color
    
    layout = html.Div(className="main-app-container", children=[
        # Global components that need to be available everywhere
        dcc.Location(id='url', refresh=False),
        dcc.Store(id="user-session", storage_type="session", data={}),
        dcc.Store(id="current-user-info", storage_type="memory"),
        
        # Header hover trigger area
        html.Div(className="header-hover-area"),
        
        # Header Component - Will be conditionally rendered
        html.Header(id="main-header", className="header", children=[
            html.Div(className="container", children=[
                html.Div(className="header-content", children=[
                    # Logo & Title
                    html.Div(className="header-title", children=[
                        html.H1("Swaccha Andhra Dashboard")
                    ]),
                    
                    # Navigation - will be updated by callback
                    html.Nav(className="header-nav", children=[], id="nav-links"),
                    
                    # Right side actions - will be updated by callback
                    html.Div(className="header-actions", children=[], id="header-actions")
                ])
            ])
        ]),
        
        # Compact Dashboard Title Banner
        html.Div(className="dashboard-title-banner", children=[
            html.Div(className="container", children=[
                html.Div(className="dashboard-title-wrapper", children=[
                    # Status indicators - compact and positioned
                    html.Div(className="dashboard-status-indicators", children=[
                        # Auto-refresh indicator
                        html.Div(className="refresh-indicator", children=[
                            html.I(id="refresh-indicator", className="fas fa-sync-alt fa-spin", 
                                  style={"color": DARK_GREEN, "fontSize": "0.9rem", "marginRight": "0.3rem"}),
                            html.Span("Auto-refresh", className="refresh-text")
                        ]),
                        
                        # Time display
                        html.Div(id="live-time", className="live-time")
                    ]),
                    
                    # Main title content with logos - more compact
                    html.Div(className="dashboard-title-content", children=[
                        # Left Logo
                        html.Img(src="/assets/img/left.png", alt="Left Logo", className="dashboard-logo left-logo"),
                        
                        # Title Container
                        html.Div(className="dashboard-title-container", children=[
                            html.H1("Swaccha Andhra", className="dashboard-main-title"),
                            html.H2("Real-Time Monitoring Dashboard for Legacy Waste Reclamation", className="dashboard-subtitle")
                        ]),
                        
                        # Right Logo
                        html.Img(src="/assets/img/right.png", alt="Right Logo", className="dashboard-logo right-logo")
                    ])
                ])
            ])
        ]),
        
        # Main content - flexible height
        html.Main(className="dashboard-main-content", children=[
            html.Div(id='page-content', className="page-content-wrapper")
        ]),
        
        # Compact Footer
        html.Footer(className="footer", children=[
            html.Div(className="container", children=[
                html.Div(className="footer-content", children=[
                    # Footer Links - more compact
                    html.Div(className="footer-links", children=[
                        html.A("About", href="/about", className="footer-link"),
                        html.A("Help", href="/help", className="footer-link"),
                        html.A("Contact", href="/contact", className="footer-link")
                    ]),
                    
                    # Copyright
                    html.Div(className="footer-copyright", children=[
                        "© 2025 Advitia Labs"
                    ])
                ])
            ])
        ]),
        
        # Clock interval for updating time
        dcc.Interval(
            id='clock-interval',
            interval=1000,  # 1 second
            n_intervals=0
        ),
        
        # Data refresh interval
        dcc.Interval(
            id='refresh-interval',
            interval=60000,  # 1 minute
            n_intervals=0
        ),
        
        # Access check div for callbacks
        html.Div(id="page-access-check", children=[])
    ])
    
    return layout

def create_main_dashboard():
    """Create a clean main authenticated dashboard with filter container"""
    
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
    agencies = ['All Agencies'] + sorted(df['Agency'].dropna().unique().tolist())
    subcontractors = ['All Subcontractors'] + sorted(df['Sub_contractor'].dropna().unique().tolist())
    clusters = ['All Clusters'] + sorted(df['Cluster'].dropna().unique().tolist())
    ulbs = ['All ULBs'] + sorted(df['ULB'].dropna().unique().tolist())
    
    # Get date range from data
    min_date = df['Date'].min().date() if not df['Date'].isna().all() else date.today()
    max_date = df['Date'].max().date() if not df['Date'].isna().all() else date.today()
    
    return html.Div(className="container", children=[
        # Page header
        html.Div(className="page-header", style={"margin": "0.5rem 0"}, children=[
            html.H2("Main Dashboard", style={"margin": "0 0 0.25rem 0"}),
            html.P("Real-time waste management monitoring with advanced analytics.", 
                   style={"margin": "0", "fontSize": "0.9rem"})
        ]),
        
        # Clean Filter Container
        html.Div(className="dashboard-filter-container", style={
            "background": "white",
            "borderRadius": "12px",
            "padding": "1.5rem",
            "boxShadow": "0 4px 12px rgba(0, 0, 0, 0.08)",
            "border": "1px solid #E8E4D0",
            "marginBottom": "2rem"
        }, children=[
            # Filter Header
            html.Div(style={
                "display": "flex",
                "alignItems": "center",
                "marginBottom": "1.5rem"
            }, children=[
                html.I(className="fas fa-filter", style={
                    "fontSize": "1.2rem",
                    "color": "#2D5E40",
                    "marginRight": "0.5rem"
                }),
                html.H3("Filters", style={
                    "margin": "0",
                    "color": "#2D5E40",
                    "fontSize": "1.1rem",
                    "fontWeight": "600"
                })
            ]),
            
            # Filter Controls - Responsive Grid
            html.Div(className="filter-grid", style={
                "display": "grid",
                "gridTemplateColumns": "repeat(auto-fit, minmax(180px, 1fr))",
                "gap": "1rem",
                "marginBottom": "1.5rem"
            }, children=[
                # Agency Filter
                html.Div(className="filter-item", children=[
                    html.Label("Agency", style={
                        "fontWeight": "600",
                        "color": "#2D5E40",
                        "fontSize": "0.9rem",
                        "marginBottom": "0.5rem",
                        "display": "block"
                    }),
                    dcc.Dropdown(
                        id='filter-agency',
                        options=[{'label': agency, 'value': agency} for agency in agencies],
                        value='All Agencies',
                        clearable=False,
                        style={"fontSize": "0.9rem"},
                        className="custom-dropdown"
                    )
                ]),
                
                # Subcontractor Filter
                html.Div(className="filter-item", children=[
                    html.Label("Subcontractor", style={
                        "fontWeight": "600",
                        "color": "#2D5E40",
                        "fontSize": "0.9rem",
                        "marginBottom": "0.5rem",
                        "display": "block"
                    }),
                    dcc.Dropdown(
                        id='filter-subcontractor',
                        options=[{'label': sub, 'value': sub} for sub in subcontractors],
                        value='All Subcontractors',
                        clearable=False,
                        style={"fontSize": "0.9rem"},
                        className="custom-dropdown"
                    )
                ]),
                
                # Cluster Filter
                html.Div(className="filter-item", children=[
                    html.Label("Cluster", style={
                        "fontWeight": "600",
                        "color": "#2D5E40",
                        "fontSize": "0.9rem",
                        "marginBottom": "0.5rem",
                        "display": "block"
                    }),
                    dcc.Dropdown(
                        id='filter-cluster',
                        options=[{'label': cluster, 'value': cluster} for cluster in clusters],
                        value='All Clusters',
                        clearable=False,
                        style={"fontSize": "0.9rem"},
                        className="custom-dropdown"
                    )
                ]),
                
                # ULB Filter
                html.Div(className="filter-item", children=[
                    html.Label("ULB", style={
                        "fontWeight": "600",
                        "color": "#2D5E40",
                        "fontSize": "0.9rem",
                        "marginBottom": "0.5rem",
                        "display": "block"
                    }),
                    dcc.Dropdown(
                        id='filter-ulb',
                        options=[{'label': ulb, 'value': ulb} for ulb in ulbs],
                        value='All ULBs',
                        clearable=False,
                        style={"fontSize": "0.9rem"},
                        className="custom-dropdown"
                    )
                ]),
                
                # Date Range Filter - Spans 2 columns on larger screens
                html.Div(className="filter-item date-filter", style={
                    "gridColumn": "span 2"
                }, children=[
                    html.Label("Date Range", style={
                        "fontWeight": "600",
                        "color": "#2D5E40",
                        "fontSize": "0.9rem",
                        "marginBottom": "0.5rem",
                        "display": "block"
                    }),
                    dcc.DatePickerRange(
                        id='filter-date-range',
                        start_date=min_date,
                        end_date=max_date,
                        display_format='DD/MM/YYYY',
                        style={
                            "width": "100%",
                            "fontSize": "0.9rem"
                        },
                        className="custom-date-picker"
                    )
                ])
            ]),
            
            # Filter Actions
            html.Div(className="filter-actions", style={
                "display": "flex",
                "gap": "1rem",
                "justifyContent": "flex-end",
                "alignItems": "center"
            }, children=[
                # Clear Filters Button
                html.Button(
                    [
                        html.I(className="fas fa-times", style={"marginRight": "0.5rem"}),
                        "Clear"
                    ],
                    id="clear-filters-btn",
                    className="btn btn-outline",
                    n_clicks=0,
                    style={"fontSize": "0.9rem"}
                ),
                
                # Apply Filters Button
                html.Button(
                    [
                        html.I(className="fas fa-search", style={"marginRight": "0.5rem"}),
                        "Apply Filters"
                    ],
                    id="apply-filters-btn",
                    className="btn btn-primary",
                    n_clicks=0,
                    style={"fontSize": "0.9rem"}
                )
            ]),
            
            # Real-time Filter Information Display
            html.Div(id="filter-info-display")
        ]),
        
        # Main content area - blank slate for your components
        html.Div(id="main-content-area", style={
            "background": "white",
            "borderRadius": "12px",
            "padding": "2rem",
            "boxShadow": "0 4px 12px rgba(0, 0, 0, 0.08)",
            "border": "1px solid #E8E4D0",
            "minHeight": "400px",
            "marginBottom": "2rem"
        }, children=[
            html.H3("Dashboard Content", style={"color": "#2D5E40", "marginBottom": "1rem"}),
            html.P("Your filtered dashboard content will appear here.", 
                   style={"color": "#8B4513", "fontSize": "1rem"})
        ])
    ])