"""
app.py - Updated Swaccha Andhra Dashboard with Enhanced Features

This file defines the Dash application with enhanced dashboard functionality including
filters, data tables, and CSV export capabilities.
"""

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import os
import flask

# Create a Flask server
server = flask.Flask(__name__)

# Initialize the Dash app with Bootstrap
app = dash.Dash(
    __name__, 
    server=server,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1, maximum-scale=5, shrink-to-fit=no"},
        {"name": "theme-color", "content": "#F2C94C"},
        {"name": "description", "content": "Waste management monitoring dashboard for Andhra Pradesh state"}
    ]
)

# Set title
app.title = "Swaccha Andhra Dashboard"

# Simple index string with Font Awesome
app.index_string = '''
<!DOCTYPE html>
<html lang="en">
    <head>
        {%metas%}
        <title>{%title%}</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css" integrity="sha512-1ycn6IcaQQ40/MKBW2W4Rhis/DbILU74C1vSrLJxCq57o941Ym01SwNsOMqvEBFlcgUa6xLiPY/NS5R+E6ztJQ==" crossorigin="anonymous" referrerpolicy="no-referrer" />
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
        <!-- Mobile navigation toggle -->
        <button id="mobile-nav-toggle" class="mobile-nav-toggle" style="display:none;">
            <i class="fas fa-bars"></i>
        </button>
    </body>
</html>
'''

# Import layouts and callbacks with error handling
try:
    from layouts.main_layout import create_main_layout
    # Define the overall layout using the main layout
    app.layout = create_main_layout()
except ImportError as e:
    print(f"Warning: Could not import main_layout: {e}")
    # Fallback layout
    app.layout = html.Div([
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content', children=[
            html.Div(className="container", children=[
                html.H1("Swaccha Andhra Dashboard"),
                html.P("Welcome to the simplified dashboard."),
                html.P("Some features may not be available due to missing layout files.")
            ])
        ])
    ])

# Register callbacks with error handling
try:
    import callbacks.clock_callback
    print("Clock callback imported successfully")
except ImportError as e:
    print(f"Warning: Could not import clock_callback: {e}")

try:
    import callbacks.navigation_callback
    print("Navigation callback imported successfully")
except ImportError as e:
    print(f"Warning: Could not import navigation_callback: {e}")

try:
    import callbacks.routing_callback
    print("Routing callback imported successfully")
except ImportError as e:
    print(f"Warning: Could not import routing_callback: {e}")

# Import auth callback
try:
    import callbacks.auth_callback
    print("Auth callback imported successfully")
except ImportError as e:
    print(f"Warning: Could not import auth_callback: {e}")

# NEW: Import enhanced dashboard callbacks
try:
    import callbacks.enhanced_dashboard_callbacks
    print("Enhanced dashboard callbacks imported successfully")
except ImportError as e:
    print(f"Warning: Could not import enhanced_dashboard_callbacks: {e}")
    print("Enhanced dashboard features may not be available.")

# Run the server
if __name__ == '__main__':
    # Get port from environment variable (for cloud deployment)
    port = int(os.environ.get('PORT', 8080))
    # Get host from environment
    host = os.environ.get('HOST', '0.0.0.0')
    # Run in debug mode if not in production
    debug = os.environ.get('DASH_ENV') != 'production'
    
    print("Starting Swaccha Andhra Dashboard...")
    print(f"Running on {host}:{port}")
    print("Features available:")
    print("- Basic dashboard and navigation")
    print("- Authentication system")
    print("- Enhanced dashboard with filters and data export")
    print("- Real-time clock updates")
    print("- Responsive design for multiple screen sizes")
    
    # Start the app
    app.run(debug=debug, port=port, host=host)