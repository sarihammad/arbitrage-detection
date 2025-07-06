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

def fetch_coingecko_rates(assets=None):
    """
    Fetches exchange rates from CoinGecko and returns a nested dictionary format.

    Args:
        assets (list): Optional list of assets (e.g., ["BTC", "ETH", "USDT"]).
                       If None, defaults to top crypto symbols.

    Returns:
        dict: Nested dictionary like { "BTC": {"ETH": rate, "USDT": rate}, ... }
    """

    if assets is None:
        assets = ["BTC", "ETH", "USDT"]

    coingecko_ids = {
        "BTC": "bitcoin",
        "ETH": "ethereum",
        "USDT": "tether"
    }

    ids = [coingecko_ids[a] for a in assets if a in coingecko_ids]
    vs_currencies = ",".join([a.lower() for a in assets])

    url = (
        "https://api.coingecko.com/api/v3/simple/price"
        f"?ids={','.join(ids)}&vs_currencies={vs_currencies}"
    )

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        prices = response.json()
    except Exception as e:
        raise RuntimeError(f"CoinGecko API error: {e}")

    rates = defaultdict(dict)
    for base_symbol, base_id in coingecko_ids.items():
        if base_symbol not in assets:
            continue
        base_prices = prices.get(base_id, {})
        for quote_symbol in assets:
            if base_symbol == quote_symbol:
                continue
            quote_lower = quote_symbol.lower()
            rate = base_prices.get(quote_lower)
            if rate:
                rates[base_symbol][quote_symbol] = rate

    return dict(rates)