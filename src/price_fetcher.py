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

    url = "https://api.binance.com/api/v3/ticker/price"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        tickers = response.json()

        if not isinstance(tickers, list) or not all(isinstance(item, dict) for item in tickers):
            raise ValueError("Unexpected API response format")

    except Exception as e:
        raise RuntimeError(f"Binance API error: {e}")

    rates = defaultdict(dict)
    for item in tickers:
        symbol = item.get("symbol")
        price_str = item.get("price")

        if not symbol or not price_str:
            continue

        try:
            price = float(price_str)
        except ValueError:
            continue

        for base in assets:
            for quote in assets:
                if base == quote:
                    continue
                if symbol == f"{base}{quote}":
                    rates[base][quote] = price
                elif symbol == f"{quote}{base}":
                    rates[quote][base] = 1 / price

    return dict(rates)