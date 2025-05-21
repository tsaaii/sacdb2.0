"""
callbacks/clock_callback.py - Clock display callback

This file defines the callback that updates the clock display.
"""

from dash import callback, Output, Input
from datetime import datetime

@callback(
    Output('header-clock', 'children'),
    [Input('clock-interval', 'n_intervals')]
)
def update_clock(n_intervals):
    """
    Update the clock display with current time.
    
    Args:
        n_intervals: Number of intervals elapsed
        
    Returns:
        str: Formatted date and time string
    """
    now = datetime.now()
    return now.strftime("%b %d, %Y • %I:%M:%S %p")