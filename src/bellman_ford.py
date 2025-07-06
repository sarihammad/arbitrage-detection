"""
Bellman-Ford Arbitrage Detection Module

This module provides functionality to detect arbitrage opportunities 
using the Bellman-Ford algorithm. A negative-weight cycle in the 
transformed graph corresponds to an arbitrage loop.
"""

import networkx as nx

def detect_arbitrage(graph):
    """
    Detects arbitrage opportunities in a currency exchange graph using the Bellman-Ford algorithm.

    Args:
        graph (networkx.DiGraph): Directed graph with edge weights as -log(exchange_rate).

    Returns:
        list: A list of currencies forming an arbitrage cycle, or None if no arbitrage exists.
    """
    nodes = list(graph.nodes)
    
    for source in nodes:
        # initialize distances and predecessors
        distance = {node: float('inf') for node in nodes}
        predecessor = {node: None for node in nodes}
        distance[source] = 0

        # relax edges |V| - 1 times
        for _ in range(len(nodes) - 1):
            for u, v, data in graph.edges(data=True):
                if distance[u] + data["weight"] < distance[v]:
                    distance[v] = distance[u] + data["weight"]
                    predecessor[v] = u

        # check for negative-weight cycles
        for u, v, data in graph.edges(data=True):
            if distance[u] + data["weight"] < distance[v]:
                # negative cycle found: reconstruct path
                cycle = [v]
                while True:
                    v = predecessor[v]
                    if v in cycle or v is None:
                        break
                    cycle.append(v)
                cycle.reverse()
                # trim to loop
                if cycle and cycle[0] != cycle[-1]:
                    cycle.append(cycle[0])
                return cycle

    return None