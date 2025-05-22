"""
callbacks/live_time_callback.py - Real-time clock display with date and AM/PM

This file defines the callback that updates the live time display with date and time.
"""

from dash import callback, Output, Input, html
from datetime import datetime

@callback(
    Output('live-time', 'children'),
    [Input('clock-interval', 'n_intervals')]
)
def update_live_time(n_intervals):
    """
    Update the live time display with current date and time including AM/PM.
    
    Args:
        n_intervals: Number of intervals elapsed
        
    Returns:
        html components: Formatted date and time with styling
    """
    now = datetime.now()
    date_str = now.strftime("%b %d, %Y")
    time_str = now.strftime("%I:%M:%S %p")
    
    return [html.Div(f"{date_str} {time_str}", className="live-update-text")]