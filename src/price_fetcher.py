"""
Binance Price Fetcher Module

This module provides functionality to fetch and organize exchange rates 
from the Binance API. It returns a nested dictionary of rates between 
specified crypto assets, suitable for use in arbitrage detection or 
other financial analysis.
"""

import requests
from collections import defaultdict

def fetch_binance_rates(assets=None):
    """
    Fetches exchange rates from Binance and returns a nested dictionary format.

    Args:
        assets (list): Optional list of assets (e.g., ["BTC", "ETH", "USDT"]).
                       If None, defaults to top crypto symbols.

    Returns:
        dict: Nested dictionary like { "BTC": {"ETH": rate, "USDT": rate}, ... }
    """
    if assets is None:
        assets = ["BTC", "ETH", "USDT"]

    response = requests.get("https://api.binance.com/api/v3/ticker/price")
    tickers = response.json()

    rates = defaultdict(dict)
    for item in tickers:
        symbol = item["symbol"]
        price = float(item["price"])

        for base in assets:
            for quote in assets:
                if base == quote:
                    continue
                if symbol == f"{base}{quote}":
                    rates[base][quote] = price
                elif symbol == f"{quote}{base}":
                    rates[quote][base] = 1 / price

    return dict(rates)