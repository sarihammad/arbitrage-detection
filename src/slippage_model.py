"""
Slippage Model Module

This module provides functionality to estimate slippage in cryptocurrency trading.
"""

def apply_slippage(rate, slippage_pct):
    """
    Adjusts the exchange rate to account for slippage.

    Args:
        rate (float): The original exchange rate.
        slippage_pct (float): Slippage percentage (e.g., 0.01 for 1%).

    Returns:
        float: The adjusted exchange rate after slippage.
    """
    return rate * (1 - slippage_pct)