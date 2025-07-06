

import pytest
import networkx as nx
from src.bellman_ford import detect_arbitrage

def test_no_arbitrage_cycle():
    graph = nx.DiGraph()
    graph.add_edge("USD", "EUR", weight=-0.1)
    graph.add_edge("EUR", "GBP", weight=-0.2)
    graph.add_edge("GBP", "USD", weight=0.3)  # Total weight: 0.0 (no arbitrage)
    assert detect_arbitrage(graph) is None

def test_arbitrage_cycle_exists():
    graph = nx.DiGraph()
    graph.add_edge("USD", "EUR", weight=-0.1)
    graph.add_edge("EUR", "GBP", weight=-0.2)
    graph.add_edge("GBP", "USD", weight=-0.1)  # Total weight: -0.4 (arbitrage)
    cycle = detect_arbitrage(graph)
    assert cycle is not None
    assert isinstance(cycle, list)
    assert len(cycle) > 1
    assert cycle[0] == cycle[-1]  # Ensure it's a cycle

def test_disconnected_graph():
    graph = nx.DiGraph()
    graph.add_edge("BTC", "ETH", weight=-0.05)
    graph.add_node("USDT")  # Disconnected node
    assert detect_arbitrage(graph) is None