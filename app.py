"""
app.py - Simplified Swaccha Andhra Dashboard with Fixed OAuth Integration

This file removes the duplicate callback that was causing the error.
"""

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import os
import flask

# Create a Flask server
server = flask.Flask(__name__)

# Initialize Google OAuth (optional - will work without it)
try:
    from auth.google_oauth import init_oauth
    oauth = init_oauth(server)
    OAUTH_ENABLED = True
    print("✓ Google OAuth authentication enabled")
except ImportError as e:
    print(f"⚠️  Google OAuth not available: {e}")
    print("   Dashboard will work without OAuth authentication")
    OAUTH_ENABLED = False

# Initialize the Dash app with Bootstrap
app = dash.Dash(
    __name__, 
    server=server,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1, maximum-scale=5, shrink-to-fit=no"},
        {"name": "theme-color", "content": "#F2C94C"},
        {"name": "description", "content": "Waste management monitoring dashboard for Andhra Pradesh state"},
        # PWA support
        {"name": "apple-mobile-web-app-capable", "content": "yes"},
        {"name": "mobile-web-app-capable", "content": "yes"}
    ]
)

# Set title
app.title = "Swaccha Andhra Dashboard"

# Enhanced index string with PWA support
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

# Import your existing layouts and callbacks
try:
    from layouts.main_layout import create_main_layout
    app.layout = create_main_layout()
    print("✓ Main layout loaded successfully")
except ImportError as e:
    print(f"Warning: Could not import main_layout: {e}")
    # Your existing fallback layout
    app.layout = html.Div([
        dcc.Location(id='url', refresh=False),
        dcc.Store(id="user-session", storage_type="session", data={}),
        html.Div(id='page-content', children=[
            html.Div(className="container", children=[
                html.H1("Swaccha Andhra Dashboard"),
                html.P("Welcome to the simplified dashboard."),
                html.P("Some features may not be available due to missing layout files.")
            ])
        ])
    ])

# Import your existing callbacks
callback_modules = [
    'callbacks.clock_callback',
    'callbacks.navigation_callback', 
    'callbacks.routing_callback',
    'callbacks.auth_callback'  # This now contains the consolidated OAuth logic
]

for module in callback_modules:
    try:
        __import__(module)
        print(f"✓ {module} imported successfully")
    except ImportError as e:
        print(f"⚠️  Could not import {module}: {e}")

# REMOVED: The duplicate OAuth callback that was causing the error
# The OAuth logic is now handled entirely in callbacks/auth_callback.py

# Serve PWA files
@server.route('/service-worker.js')
def service_worker():
    """Serve service worker for PWA"""
    try:
        return server.send_static_file('js/service-worker.js')
    except:
        return "// Service worker not available", 200, {'Content-Type': 'application/javascript'}

@server.route('/offline.html')
def offline():
    """Serve offline page for PWA"""
    try:
        return server.send_static_file('offline.html')
    except:
        return "<html><body><h1>Offline</h1><p>You are offline.</p></body></html>"

# API endpoints for authentication status
@server.route('/api/auth/status')
def api_auth_status():
    """API to check authentication status"""
    if OAUTH_ENABLED:
        try:
            from auth.google_oauth import get_current_user
            user = get_current_user()
            if user:
                return flask.jsonify({
                    'authenticated': True,
                    'user': {
                        'email': user.get('email'),
                        'name': user.get('name'),
                        'picture': user.get('picture')
                    }
                })
        except Exception as e:
            print(f"Error checking auth status: {e}")
    return flask.jsonify({'authenticated': False})

# Helper functions for your existing callbacks
def require_auth_check():
    """Helper function to check authentication in your existing callbacks"""
    if OAUTH_ENABLED:
        try:
            from auth.google_oauth import is_authenticated
            return is_authenticated()
        except:
            pass
    return True  # Allow access if OAuth is disabled

def get_user_info():
    """Helper function to get user info in your existing callbacks"""
    if OAUTH_ENABLED:
        try:
            from auth.google_oauth import get_current_user
            return get_current_user()
        except:
            pass
    return {'email': 'test@example.com', 'name': 'Test User', 'authenticated': True}

# Make helper functions available to callbacks
app.server.require_auth_check = require_auth_check
app.server.get_user_info = get_user_info

if __name__ == '__main__':
    # Get configuration from environment
    port = int(os.environ.get('PORT', 8080))
    host = os.environ.get('HOST', '0.0.0.0')
    debug = os.environ.get('DASH_ENV') != 'production'
    
    print("=" * 60)
    print("🌱 Starting Swaccha Andhra Dashboard...")
    print(f"🌐 Running on {host}:{port}")
    print("📱 PWA Features:")
    print("   ✓ Service Worker for offline support")
    print("   ✓ App installation prompts") 
    print("   ✓ Responsive design for mobile and TV")
    print("🔐 Authentication:")
    print(f"   {'✓' if OAUTH_ENABLED else '✗'} Google OAuth integration")
    if OAUTH_ENABLED:
        print("   ✓ Email-based access control")
        print("   ✓ Session management")
    print("🎨 UI Features:")
    print("   ✓ Earth tones color palette")
    print("   ✓ Auto-hiding navigation")
    print("   ✓ Live clock and status indicators")
    print("="*60)
    
    if not OAUTH_ENABLED:
        print("💡 To enable Google OAuth:")
        print("   1. Install dependencies: pip install google-auth google-auth-oauthlib")
        print("   2. Create client_secrets.json with your Google OAuth credentials")
        print("   3. Add auth/google_oauth.py to your project")
        print("   4. Configure config/allowed_emails.json")
    
    print("\n🚀 Starting application...")
    
    # Fixed: Use app.run() instead of app.run_server() for newer Dash versions
    try:
        # Try the new method first (Dash 3.0+)
        app.run(debug=debug, port=port, host=host)
    except AttributeError:
        # Fallback to old method for older Dash versions
        app.run_server(debug=debug, port=port, host=host)