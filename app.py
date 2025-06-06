"""
app.py - Ultra Simple Version with Master Callback Only

This version has no conflicting callbacks at all.
"""

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import os
import flask

# Create a Flask server
server = flask.Flask(__name__)

# Initialize Google OAuth (optional)
try:
    from auth.google_oauth import init_oauth
    oauth = init_oauth(server)
    OAUTH_ENABLED = True
    print("✓ Google OAuth authentication enabled")
except ImportError as e:
    print(f"⚠️  Google OAuth not available: {e}")
    OAUTH_ENABLED = False

# Initialize the Dash app
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

app.index_string = '''
<!DOCTYPE html>
<html lang="en">
    <head>
        {%metas%}
        <title>{%title%}</title>
        <!-- PWA Manifest -->
        <link rel="manifest" href="/assets/manifest.json">
        <!-- Font Awesome -->
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css" integrity="sha512-1ycn6IcaQQ40/MKBW2W4Rhis/DbILU74C1vSrLJxCq57o941Ym01SwNsOMqvEBFlcgUa6xLiPY/NS5R+E6ztJQ==" crossorigin="anonymous" referrerpolicy="no-referrer" />
        {%favicon%}
        {%css%}
        <!-- PWA Scripts -->
        <script src="/assets/js/pwa-register.js"></script>
        <script src="/assets/js/nav-control.js" defer></script>
        <script src="/assets/js/splash-screen.js" defer></script>
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
        <!-- PWA Install Button -->
        <div id="install-container" style="display: none;">
            <button id="install-button" class="pwa-install-button">
                <i class="fas fa-download"></i>
                Install App
            </button>
        </div>
    </body>
</html>
'''

# Create the main layout
def create_main_layout():
    """Create the main application layout"""
    return html.Div(className="main-app-container", children=[
        # Global components
        dcc.Location(id='url', refresh=False),
        dcc.Store(id="user-session", storage_type="session", data={}),
        dcc.Store(id="current-user-info", storage_type="memory"),
        dcc.Store(id="page-navigation-status", storage_type="memory"),
        
        # Header hover trigger area
        html.Div(className="header-hover-area"),
        
        # Main content (master callback will handle everything including header/footer)
        html.Div(id='page-content', className="page-content-wrapper"),
        
        # Intervals for real-time updates
        dcc.Interval(id='clock-interval', interval=1000, n_intervals=0),
        dcc.Interval(id='refresh-interval', interval=60000, n_intervals=0),
        
        # Helper divs for callbacks (hidden but needed for callback compatibility)
        html.Div(id="page-access-check", children=[], style={"display": "none"}),
        html.Div(id="nav-links", children=[], style={"display": "none"}),
        html.Div(id="header-actions", children=[], style={"display": "none"}),
        html.Div(id="live-time", children=[], style={"display": "none"}),
        html.Div(id="header-clock", children=[], style={"display": "none"})
    ])

# Set the layout
app.layout = create_main_layout()

# Import ONLY the master callback
try:
    import callbacks.master_callback
    print("✓ Master callback imported successfully")
except ImportError as e:
    print(f"❌ Could not import master callback: {e}")

# Serve PWA files
@server.route('/service-worker.js')
def service_worker():
    try:
        return server.send_static_file('js/service-worker.js')
    except:
        return "// Service worker not available", 200, {'Content-Type': 'application/javascript'}

@server.route('/offline.html')
def offline():
    try:
        return server.send_static_file('offline.html')
    except:
        return "<html><body><h1>Offline</h1></body></html>"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    host = os.environ.get('HOST', '0.0.0.0')
    debug = os.environ.get('DASH_ENV') != 'production'
    
    print("=" * 60)
    print("🌱 Starting Swaccha Andhra Dashboard...")
    print(f"🌐 Running on {host}:{port}")
    print(f"🔐 OAuth: {'✓ Enabled' if OAUTH_ENABLED else '✗ Disabled'}")
    print("📋 Using Master Callback - Zero Conflicts!")
    print("=" * 60)
    
    try:
        app.run(debug=debug, port=port, host=host)
    except AttributeError:
        app.run_server(debug=debug, port=port, host=host)