"""
callbacks/header_handlers.py - Header & Clock Management

Save this as: callbacks/header_handlers.py
"""

from dash import callback, Output, Input, State, html, no_update, clientside_callback
from datetime import datetime

# Check if OAuth is available
try:
    from auth.google_oauth import get_current_user, is_authenticated
    OAUTH_AVAILABLE = True
except ImportError:
    OAUTH_AVAILABLE = False
    def get_current_user():
        return None
    def is_authenticated():
        return False

def get_current_time():
    """Get current time formatted for display"""
    now = datetime.now()
    date_str = now.strftime("%b %d, %Y")
    time_str = now.strftime("%I:%M:%S %p")
    header_time = now.strftime("%I:%M %p")
    live_time = f"{date_str} {time_str}"
    return live_time, header_time

# ==================== CLOCK UPDATE CALLBACK ====================

@callback(
    Output('live-time', 'children'),
    [Input('clock-interval', 'n_intervals')]
)
def update_live_time(n_intervals):
    """Update the live time display with current date and time"""
    now = datetime.now()
    date_str = now.strftime("%b %d, %Y")
    time_str = now.strftime("%I:%M:%S %p")
    
    return html.Div(f"{date_str} {time_str}", className="live-update-text")

# ==================== HEADER ACTIONS CALLBACK ====================

@callback(
    Output('header-actions', 'children'),
    [Input('url', 'pathname'),
     Input('clock-interval', 'n_intervals')],
    [State('user-session', 'data')],
    prevent_initial_call=False
)
def update_header_actions(pathname, n_intervals, session_data):
    """Update header actions based on authentication state"""
    
    print(f"🔍 HEADER DEBUG - Header actions update triggered:")
    print(f"  - pathname: {pathname}")
    print(f"  - session_data: {session_data}")
    
    # Get current time for header clock
    now = datetime.now()
    header_time = now.strftime("%I:%M %p")
    
    # Check authentication
    oauth_authenticated = is_authenticated() if OAUTH_AVAILABLE else False
    dash_authenticated = session_data and session_data.get('authenticated', False)
    is_auth = oauth_authenticated or dash_authenticated
    
    print(f"🔍 HEADER DEBUG - Authentication status:")
    print(f"  - oauth_authenticated: {oauth_authenticated}")
    print(f"  - dash_authenticated: {dash_authenticated}")
    print(f"  - is_auth: {is_auth}")
    
    # Public routes
    public_routes = ['/', '/login']
    is_public_page = pathname in public_routes
    
    if not is_auth or is_public_page:
        # Public page - show login option
        if pathname == '/login':
            # On login page
            print("✅ HEADER DEBUG - Showing login page header")
            return [
                html.Div(header_time, className="clock-display"),
                html.A("Home", href="/", className="btn btn-outline")
            ]
        else:
            # Regular public page
            print("✅ HEADER DEBUG - Showing public page header")
            return [
                html.Div(header_time, className="clock-display"),
                html.A("Login", href="/login?source=public", className="btn btn-primary")
            ]
    else:
        # Authenticated user - show full header actions
        user_name = "User"
        user_picture = None
        
        # FIXED: Get user info from OAuth first, then fallback to session
        if OAUTH_AVAILABLE and oauth_authenticated:
            try:
                oauth_user = get_current_user()
                if oauth_user:
                    user_name = oauth_user.get('name', oauth_user.get('email', 'User'))
                    user_picture = oauth_user.get('picture')
                    print(f"✅ HEADER DEBUG - OAuth user info: name={user_name}, picture={user_picture}")
            except Exception as e:
                print(f"❌ HEADER DEBUG - Error getting OAuth user: {e}")
        
        # Fallback to session data if OAuth info not available
        if user_name == "User" and session_data:
            user_name = session_data.get('username', session_data.get('name', 'User'))
            user_picture = session_data.get('picture')
            print(f"🔄 HEADER DEBUG - Using session data: name={user_name}, picture={user_picture}")
        
        # Create user profile section
        user_profile = []
        if user_picture:
            user_profile.append(
                html.Img(
                    src=user_picture,
                    style={
                        "width": "28px",
                        "height": "28px", 
                        "borderRadius": "50%",
                        "marginRight": "0.5rem"
                    }
                )
            )
        
        user_profile.append(
            html.Span(
                user_name.split()[0] if user_name else "User",
                style={
                    "color": "#FEFEFE",
                    "fontSize": "0.9rem",
                    "marginRight": "1rem"
                }
            )
        )
        
        header_actions = [
            # Auto-refresh indicator
            html.Div(className="auto-refresh-indicator", children=[
                html.I(className="fas fa-sync-alt"),
                html.Span("Auto-refreshing")
            ]),
            
            # Clock display (dynamically updated)
            html.Div(header_time, className="clock-display"),
            
            # User profile
            html.Div(user_profile, style={"display": "flex", "alignItems": "center"}),
            
            # Logout button with explicit onclick handler
            html.Button("Logout", id="logout-btn", n_clicks=0, className="btn btn-accent", 
                       **{
                           'data-testid': 'logout-button',
                           'style': {
                               "backgroundColor": "#C74A3C",
                               "color": "white", 
                               "border": "none",
                               "padding": "0.35rem 0.85rem",
                               "borderRadius": "8px",
                               "fontWeight": "600",
                               "cursor": "pointer",
                               "fontSize": "0.85rem"
                           }
                       })
        ]
        
        print(f"✅ HEADER DEBUG - Created authenticated header with logout button")
        print(f"  - User name: {user_name}")
        print(f"  - Header actions count: {len(header_actions)}")
        
        return header_actions

# ==================== LOGOUT BUTTON DETECTION CALLBACK ====================

@callback(
    Output('current-pathname-store', 'data', allow_duplicate=True),
    [Input('header-actions', 'children')],
    [State('user-session', 'data')],
    prevent_initial_call=True
)
def handle_logout_button_attachment(header_actions, session_data):
    """Attach logout handler when button is created"""
    
    print(f"🔍 LOGOUT DEBUG - Header actions updated: {len(header_actions) if header_actions else 0} items")
    
    # Check if logout button exists
    logout_btn_found = False
    if header_actions:
        for item in header_actions:
            if hasattr(item, 'id') and item.id == 'logout-btn':
                logout_btn_found = True
                print(f"✅ LOGOUT DEBUG - Logout button found in header actions")
                break
    
    if not logout_btn_found:
        print(f"❌ LOGOUT DEBUG - Logout button NOT found in header actions")
    
    return no_update

# ==================== CLIENT-SIDE LOGOUT HANDLER ====================

clientside_callback(
    """
    function(header_actions, session_data) {
        console.log('🔍 LOGOUT SIMPLE - Attaching logout handler');
        
        if (!header_actions || !Array.isArray(header_actions)) {
            console.log('❌ LOGOUT SIMPLE - No header actions array');
            return window.dash_clientside.no_update;
        }
        
        // Wait for DOM update then find and attach handler
        setTimeout(function() {
            const logoutBtn = document.getElementById('logout-btn');
            console.log('🔍 LOGOUT SIMPLE - Found logout button:', !!logoutBtn);
            
            if (logoutBtn && !logoutBtn.dataset.simpleHandler) {
                console.log('✅ LOGOUT SIMPLE - Attaching simple handler');
                logoutBtn.dataset.simpleHandler = 'true';
                
                // Add visual feedback
                logoutBtn.style.transition = 'all 0.2s ease';
                
                logoutBtn.onclick = function(e) {
                    console.log('🚀 SIMPLE LOGOUT CLICKED!');
                    e.preventDefault();
                    e.stopPropagation();
                    
                    // Visual feedback
                    logoutBtn.style.backgroundColor = '#a73228';
                    logoutBtn.textContent = 'Logging out...';
                    logoutBtn.disabled = true;
                    
                    // Get auth method from session
                    const auth_method = session_data && session_data.auth_method;
                    console.log('🔍 LOGOUT SIMPLE - Auth method:', auth_method);
                    
                    // Force immediate redirect
                    setTimeout(function() {
                        if (auth_method === 'google_oauth') {
                            console.log('🔐 SIMPLE - OAuth logout redirect');
                            window.location.href = '/auth/logout';
                        } else {
                            console.log('🔐 SIMPLE - Traditional logout redirect');
                            window.location.href = '/?logout=true&timestamp=' + Date.now();
                        }
                    }, 500); // Small delay to show visual feedback
                };
                
                console.log('✅ LOGOUT SIMPLE - Handler attached successfully');
            }
        }, 200);
        
        return window.dash_clientside.no_update;
    }
    """,
    Output('page-navigation-status', 'data', allow_duplicate=True),
    [Input('header-actions', 'children')],
    [State('user-session', 'data')],
    prevent_initial_call=True
)

# ==================== CLIENT-SIDE NAVIGATION CALLBACK ====================

# Client-side callback for smooth navigation without page reloads
clientside_callback(
    """
    function(pathname) {
        // Add any client-side navigation logic here
        // For example, smooth scrolling or page transitions
        if (pathname && pathname !== window.location.pathname) {
            // Smooth transition effect
            document.body.style.opacity = '0.95';
            setTimeout(function() {
                document.body.style.opacity = '1';
            }, 100);
        }
        return pathname;
    }
    """,
    Output('current-pathname-store', 'data', allow_duplicate=True),
    [Input('url', 'pathname')],
    prevent_initial_call=True
)

print("✓ Header handlers module loaded successfully")