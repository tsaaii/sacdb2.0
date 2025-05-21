"""
callbacks/timestamp_callback.py - Update time display callback

This file defines the callback that updates the timestamp display.
"""

from dash import callback, Output, Input
from datetime import datetime

@callback(
    Output('update-time', 'children'),
    [Input('refresh-interval', 'n_intervals')]
)
def update_timestamp(n_intervals):
    """
    Update the timestamp display with current time.
    
    Args:
        n_intervals: Number of intervals elapsed
        
    Returns:
        str: Formatted date and time string
    """
    now = datetime.now()
    return now.strftime("%b %d, %Y • %I:%M:%S %p")