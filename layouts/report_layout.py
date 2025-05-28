"""
app.py - Simplified Swaccha Andhra Dashboard

This file defines the Dash application with basic functionality.
All panels and complex styling have been removed.
"""

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import os
import flask

# Import layouts and callbacks
from layouts.main_layout import create_main_layout

# Register callbacks (must import to ensure they are registered)
import callbacks.clock_callback
import callbacks.navigation_callback
import callbacks.routing_callback

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
        <script src="/assets/js/nav-control.js" defer></script>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
        <!-- Mobile navigation toggle -->
        <button id="mobile-nav-toggle" class="mobile-nav-toggle">
            <i class="fas fa-bars"></i>
        </button>
    </body>
</html>
'''

# Define the overall layout using the main layout
app.layout = create_main_layout()

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