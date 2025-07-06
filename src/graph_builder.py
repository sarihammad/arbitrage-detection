"""
Graph Builder Module for Arbitrage Detection

This module defines functions to construct a directed weighted graph 
from cryptocurrency exchange rates. Each node represents a currency/asset, 
and each directed edge weight is computed as the negative logarithm of the exchange rate.

This transformation allows detection of arbitrage opportunities using the 
Bellman-Ford algorithm, where a negative-weight cycle corresponds to an arbitrage path.

Functions:
- build_exchange_graph: Converts exchange rates to a directed graph with -log weights.
"""

import networkx as nx
import math


def build_exchange_graph(rates):
    """
    Build a directed graph from exchange rate data.

    Args:
        rates (dict): A nested dictionary where rates[A][B] is the exchange rate from currency A to currency B.

    Returns:
        networkx.DiGraph: A directed graph where each edge weight is -log(rate), suitable for arbitrage detection.
    """
    graph = nx.DiGraph()

    for base_currency in rates:
        for quote_currency, rate in rates[base_currency].items():
            if rate <= 0:
                continue  # skip invalid rates
            weight = -math.log(rate)
            graph.add_edge(base_currency, quote_currency, weight=weight)

    return graph
