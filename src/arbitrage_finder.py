"""
Arbitrage Finder Module

This module integrates the graph builder and Bellman-Ford algorithm to detect arbitrage opportunities
in a set of currency exchange rates.
"""

from src.graph_builder import build_exchange_graph
from src.bellman_ford import detect_arbitrage

def find_arbitrage(rates):
    """
    Detects arbitrage opportunities given a dictionary of exchange rates.

    Args:
        rates (dict): A nested dictionary where rates[A][B] is the exchange rate from currency A to B.

    Returns:
        list: A list of currencies representing an arbitrage cycle, or None if none found.
    """
    graph = build_exchange_graph(rates)
    cycle = detect_arbitrage(graph)
    return cycle