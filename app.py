"""
app.py - Main application file for Swaccha Andhra Dashboard

This file defines the Dash application with the new earth tones theme.
"""

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from datetime import datetime
import flask
import os

# Create a Flask server
server = flask.Flask(__name__)

# Initialize the Dash app with Bootstrap
app = dash.Dash(
    __name__, 
    server=server,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"},
        {"name": "theme-color", "content": "#2D5E40"},
        {"name": "apple-mobile-web-app-capable", "content": "yes"},
        {"name": "apple-mobile-web-app-status-bar-style", "content": "black-translucent"}
    ]
)

# Set title
app.title = "Swaccha Andhra Dashboard"

# Define the overall layout
app.layout = html.Div([
    # URL Routing
    dcc.Location(id='url', refresh=False),
    
    # Header Component
    html.Header(className="header", children=[
        html.Div(className="container", children=[
            html.Div(className="header-content", children=[
                # Logo & Title
                html.Div(className="header-title", children=[
                    html.Img(src="/assets/img/logo.png", alt="Swaccha Andhra", className="header-logo"),
                    html.H1("Swaccha Andhra Dashboard")
                ]),
                
                # Navigation
                html.Nav(className="header-nav", children=[
                    html.A("Dashboard", href="/", className="header-nav-link active"),
                    html.A("Reports", href="/reports", className="header-nav-link"),
                    html.A("Upload", href="/upload", className="header-nav-link"),
                    html.A("Settings", href="/settings", className="header-nav-link")
                ]),
                
                # Right side actions
                html.Div(className="header-actions", children=[
                    # Clock display
                    html.Div(id="header-clock", className="clock-display"),
                    
                    # Login button
                    html.A("Login", href="/login", className="btn")
                ])
            ])
        ])
    ]),
    
    # Main content
    html.Main(id='page-content'),
    
    # Footer component
    html.Footer(className="footer", children=[
        html.Div(className="container", children=[
            html.Div(className="footer-content", children=[
                # Logo
                html.Div(className="footer-logo", children=[
                    html.Img(src="/assets/img/logo-white.png", alt="Swaccha Andhra"),
                    html.Span("Swaccha Andhra")
                ]),
                
                # Links
                html.Div(className="footer-links", children=[
                    html.A("About", href="#", className="footer-link"),
                    html.A("Help", href="#", className="footer-link"),
                    html.A("Contact", href="#", className="footer-link"),
                    html.A("Policy", href="#", className="footer-link")
                ]),
                
                # Copyright
                html.Div(className="footer-copyright", children=[
                    "© 2025 Advitia Labs • Made in Andhra Pradesh"
                ])
            ])
        ])
    ]),
    
    # Clock interval for updating time
    dcc.Interval(
        id='clock-interval',
        interval=1000,  # 1 second
        n_intervals=0
    )
])

# Create public dashboard layout
def create_public_dashboard():
    """
    Create the public dashboard with 9 square tiles.
    
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
                            letter + ": " + card_titles[i]
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
                        html.Div(className="card-date", children="May 20, 2025")
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

# Define callback for URL routing
@app.callback(
    dash.dependencies.Output('page-content', 'children'),
    [dash.dependencies.Input('url', 'pathname')]
)
def display_page(pathname):
    """
    Route to the appropriate page based on URL.
    """
    if pathname == '/':
        return create_public_dashboard()
    elif pathname == '/login':
        return html.Div("Login Page - Coming Soon", className="container")
    elif pathname == '/reports':
        return html.Div("Reports Page - Coming Soon", className="container")
    elif pathname == '/upload':
        return html.Div("Upload Page - Coming Soon", className="container")
    elif pathname == '/settings':
        return html.Div("Settings Page - Coming Soon", className="container")
    else:
        # 404 page
        return html.Div([
            html.H1('404 - Page Not Found', className='text-center mt-5'),
            html.P('The page you requested does not exist.', className='text-center')
        ], className="container")

# Callback to update the clock display
@app.callback(
    dash.dependencies.Output('header-clock', 'children'),
    [dash.dependencies.Input('clock-interval', 'n_intervals')]
)
def update_clock(n_intervals):
    """
    Update the clock display with current time.
    """
    now = datetime.now()
    return now.strftime("%b %d, %Y • %I:%M:%S %p")

# Run the server
if __name__ == '__main__':
    # Get port from environment variable (for cloud deployment)
    port = int(os.environ.get('PORT', 8080))
    # Get host from environment
    host = os.environ.get('HOST', '0.0.0.0')
    # Run in debug mode if not in production
    debug = os.environ.get('DASH_ENV') != 'production'
    
    # Start the app
    app.run(debug=debug, port=port, host=host)