


import networkx as nx
from src.graph_builder import build_exchange_graph
import math

def test_build_exchange_graph():
    rates = {
        "BTC": {"ETH": 15.0, "USDT": 30000.0},
        "ETH": {"BTC": 0.066},
    }

    graph = build_exchange_graph(rates)

    # check nodes
    assert set(graph.nodes()) == {"BTC", "ETH", "USDT"}

    # check edge weights
    expected_weight_btc_eth = -math.log(15.0)
    expected_weight_btc_usdt = -math.log(30000.0)
    expected_weight_eth_btc = -math.log(0.066)

    assert math.isclose(graph["BTC"]["ETH"]["weight"], expected_weight_btc_eth, rel_tol=1e-9)
    assert math.isclose(graph["BTC"]["USDT"]["weight"], expected_weight_btc_usdt, rel_tol=1e-9)
    assert math.isclose(graph["ETH"]["BTC"]["weight"], expected_weight_eth_btc, rel_tol=1e-9)

    # check no edge for missing ETH -> USDT
    assert not graph.has_edge("ETH", "USDT")