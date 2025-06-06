"""
callbacks/utility_functions.py - Utility Functions & Helpers

Save this as: callbacks/utility_functions.py
"""

from dash import html, dcc
from datetime import datetime, date

# ==================== TIME UTILITY FUNCTIONS ====================

def get_current_time():
    """Get current time formatted for display"""
    now = datetime.now()
    date_str = now.strftime("%b %d, %Y")
    time_str = now.strftime("%I:%M:%S %p")
    header_time = now.strftime("%I:%M %p")
    live_time = f"{date_str} {time_str}"
    return live_time, header_time

def format_timestamp(timestamp_format="%Y-%m-%d %H:%M:%S"):
    """Get current timestamp in specified format"""
    return datetime.now().strftime(timestamp_format)

def get_time_components():
    """Get individual time components"""
    now = datetime.now()
    return {
        'date': now.strftime("%b %d, %Y"),
        'time': now.strftime("%I:%M:%S %p"),
        'header_time': now.strftime("%I:%M %p"),
        'iso': now.isoformat(),
        'timestamp': now.timestamp()
    }

# ==================== LAYOUT UTILITY FUNCTIONS ====================

def get_required_layout_components():
    """Get components that must be included in the main layout"""
    return [
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
        
        # Store for current pathname (used by client-side callback)
        dcc.Store(id='current-pathname-store', storage_type='memory'),
        
        # Store for navigation status
        dcc.Store(id='page-navigation-status', storage_type='memory'),
    ]

# ==================== AUTHENTICATION UTILITY FUNCTIONS ====================

def create_auth_alert(alert_type, message):
    """Create standardized authentication alert components"""
    
    alert_styles = {
        'warning': {
            "display": "block",
            "backgroundColor": "#fff3cd",
            "color": "#856404",
            "padding": "0.75rem",
            "borderRadius": "8px",
            "border": "1px solid #ffeaa7"
        },
        'error': {
            "display": "block",
            "backgroundColor": "#f8d7da",
            "color": "#721c24",
            "padding": "0.75rem",
            "borderRadius": "8px",
            "border": "1px solid #f5c6cb"
        },
        'success': {
            "display": "block",
            "backgroundColor": "#d4edda",
            "color": "#155724",
            "padding": "0.75rem",
            "borderRadius": "8px",
            "border": "1px solid #c3e6cb"
        }
    }
    
    icons = {
        'warning': "fas fa-exclamation-triangle",
        'error': "fas fa-times-circle",
        'success': "fas fa-check-circle"
    }
    
    return alert_styles.get(alert_type, alert_styles['warning']), [
        html.I(className=icons.get(alert_type, icons['warning']), 
               style={"marginRight": "0.5rem"}),
        message
    ]

# ==================== DATA VALIDATION FUNCTIONS ====================

def validate_session_data(session_data):
    """Validate session data structure"""
    if not session_data or not isinstance(session_data, dict):
        return False, "Invalid session data structure"
    
    required_fields = ['authenticated']
    for field in required_fields:
        if field not in session_data:
            return False, f"Missing required field: {field}"
    
    if session_data.get('authenticated') and not session_data.get('username'):
        return False, "Authenticated session missing username"
    
    return True, "Session data valid"

def sanitize_user_input(input_string, max_length=100):
    """Sanitize user input for security"""
    if not input_string:
        return ""
    
    # Strip whitespace and limit length
    sanitized = str(input_string).strip()[:max_length]
    
    # Remove potentially dangerous characters
    dangerous_chars = ['<', '>', '"', "'", '&', '\n', '\r', '\t']
    for char in dangerous_chars:
        sanitized = sanitized.replace(char, '')
    
    return sanitized

# ==================== URL UTILITY FUNCTIONS ====================

def parse_url_params(search_params):
    """Parse URL search parameters safely"""
    if not search_params:
        return {}
    
    try:
        from urllib.parse import parse_qs
        return parse_qs(search_params.lstrip('?'))
    except Exception as e:
        print(f"Error parsing URL params: {e}")
        return {}

def build_url_with_params(base_url, params):
    """Build URL with parameters"""
    if not params:
        return base_url
    
    try:
        from urllib.parse import urlencode
        param_string = urlencode(params)
        separator = '&' if '?' in base_url else '?'
        return f"{base_url}{separator}{param_string}"
    except Exception as e:
        print(f"Error building URL: {e}")
        return base_url

# ==================== DEBUGGING UTILITY FUNCTIONS ====================

def create_debug_info(context, data=None):
    """Create standardized debug information"""
    timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
    debug_msg = f"🔍 DEBUG [{timestamp}] - {context}"
    
    if data:
        debug_msg += f": {data}"
    
    return debug_msg

def log_callback_info(callback_name, inputs=None, outputs=None, triggered=None):
    """Log callback information for debugging"""
    timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
    
    print(f"🔄 CALLBACK [{timestamp}] - {callback_name}")
    
    if inputs:
        print(f"  📥 Inputs: {inputs}")
    
    if outputs:
        print(f"  📤 Outputs: {outputs}")
    
    if triggered:
        print(f"  🎯 Triggered by: {triggered}")

# ==================== COMPONENT STYLING FUNCTIONS ====================

def get_button_style(button_type='primary'):
    """Get standardized button styles"""
    styles = {
        'primary': {
            "backgroundColor": "#2D5E40",
            "color": "white",
            "border": "none",
            "padding": "0.75rem 1.5rem",
            "borderRadius": "8px",
            "fontWeight": "600",
            "cursor": "pointer",
            "textDecoration": "none",
            "fontSize": "1rem"
        },
        'secondary': {
            "backgroundColor": "#F2C94C",
            "color": "#2D5E40",
            "border": "none",
            "padding": "0.75rem 1.5rem",
            "borderRadius": "8px",
            "fontWeight": "600",
            "cursor": "pointer",
            "textDecoration": "none",
            "fontSize": "1rem"
        },
        'danger': {
            "backgroundColor": "#C74A3C",
            "color": "white",
            "border": "none",
            "padding": "0.35rem 0.85rem",
            "borderRadius": "8px",
            "fontWeight": "600",
            "cursor": "pointer",
            "fontSize": "0.85rem"
        },
        'outline': {
            "backgroundColor": "transparent",
            "color": "#2D5E40",
            "border": "2px solid #2D5E40",
            "padding": "0.75rem 1.5rem",
            "borderRadius": "8px",
            "fontWeight": "600",
            "cursor": "pointer",
            "textDecoration": "none",
            "fontSize": "1rem"
        }
    }
    
    return styles.get(button_type, styles['primary'])

def get_card_style():
    """Get standardized card styles"""
    return {
        "background": "white",
        "borderRadius": "12px",
        "padding": "1.5rem",
        "boxShadow": "0 4px 12px rgba(0, 0, 0, 0.08)",
        "border": "1px solid #E8E4D0"
    }

def get_container_style():
    """Get standardized container styles"""
    return {
        "maxWidth": "1200px",
        "margin": "0 auto",
        "padding": "0 1rem"
    }

# ==================== COLOR CONSTANTS ====================

COLORS = {
    'primary': '#2D5E40',
    'secondary': '#F2C94C',
    'accent': '#C74A3C',
    'text_primary': '#8B4513',
    'text_secondary': '#A67C52',
    'border': '#E8E4D0',
    'background': '#FFFBF5',
    'white': '#FEFEFE',
    'success': '#28a745',
    'warning': '#ffc107',
    'danger': '#dc3545',
    'info': '#17a2b8'
}

# ==================== RESPONSIVE BREAKPOINTS ====================

BREAKPOINTS = {
    'mobile': '576px',
    'tablet': '768px',
    'desktop': '992px',
    'large': '1200px'
}

# ==================== UTILITY CLASSES ====================

def create_responsive_grid(columns=3, gap="1.5rem", min_width="280px"):
    """Create responsive grid styles"""
    return {
        "display": "grid",
        "gridTemplateColumns": f"repeat(auto-fit, minmax({min_width}, 1fr))",
        "gap": gap
    }

def create_flex_container(direction="row", justify="center", align="center", gap="1rem"):
    """Create flex container styles"""
    return {
        "display": "flex",
        "flexDirection": direction,
        "justifyContent": justify,
        "alignItems": align,
        "gap": gap
    }

# ==================== ERROR HANDLING FUNCTIONS ====================

def handle_callback_error(error, callback_name):
    """Handle callback errors gracefully"""
    error_msg = f"Error in {callback_name}: {str(error)}"
    print(f"❌ {error_msg}")
    
    # You could log to a file or external service here
    # For now, just print to console
    
    return error_msg

def create_fallback_content(error_message="Something went wrong"):
    """Create fallback content for errors"""
    return html.Div(
        style={
            "textAlign": "center",
            "padding": "2rem",
            "color": COLORS['text_secondary']
        },
        children=[
            html.I(className="fas fa-exclamation-triangle", style={
                "fontSize": "2rem",
                "marginBottom": "1rem",
                "color": COLORS['warning']
            }),
            html.H3(error_message),
            html.P("Please refresh the page or contact support if the problem persists.")
        ]
    )

print("✓ Utility functions module loaded successfully")