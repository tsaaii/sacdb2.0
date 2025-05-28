"""
callbacks/clock_callback.py - Fixed real-time clock display

This file defines the callback that updates the live time display.
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
    
    return html.Div(f"{date_str} {time_str}", className="live-update-text")

@callback(
    Output('header-clock', 'children'),
    [Input('clock-interval', 'n_intervals')]
)
def update_header_clock(n_intervals):
    """
    Update the header clock display.
    
    Args:
        n_intervals: Number of intervals elapsed
        
    Returns:
        str: Formatted time for header
    """
    now = datetime.now()
    time_str = now.strftime("%I:%M %p")
    return time_str