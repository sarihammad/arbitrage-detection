# Cryptocurrency Arbitrage Detection

A real-time cryptocurrency arbitrage detection system that identifies profitable trading cycles across currency pairs using graph algorithms and live exchange rate data from Binance.

## Live Demo

https://crypto-arbitrage-detection.streamlit.app/

<img width="1440" alt="Screenshot 2025-07-06 at 4 37 17 pm" src="https://github.com/user-attachments/assets/ab9b9645-d433-4b90-ba62-7692d072b3ab" />

## Features

- Fetches **real-time exchange rates** from Binance for selected cryptocurrencies (e.g., BTC, ETH, USDT).
- Builds a **directed weighted graph** where each node is a currency and each edge is `-log(rate)`.
- Applies the **Bellman-Ford algorithm** to detect **negative-weight cycles**, which represent arbitrage opportunities.
- Simulates **slippage** by modeling market depth, price impact, and order book behavior to assess the real-world feasibility of arbitrage trades.
- Presents the results in an interactive **Streamlit web interface**:

    - Choose between **Live Binance Data** or **Manual Input**
    - Display of input rates and arbitrage paths
    - Clear success/failure results

## How It Works

By transforming exchange rates using negative logarithms, arbitrage detection becomes a graph problem. A **negative cycle** implies that a series of trades results in more of the starting currency than initially held. This is a classic arbitrage opportunity.

## Live Data Example

```json
{
  "BTC": {"ETH": 15.0, "USDT": 30000.0},
  "ETH": {"BTC": 0.066, "USDT": 2000.0},
  "USDT": {"BTC": 0.000033, "ETH": 0.0005}
}
```

The system evaluates combinations like `BTC -> ETH -> USDT -> BTC` to find profit loops.

## How to Run

To run the app locally:

1. Clone the repository.
2. Install the required dependencies (see `requirements.txt`).
3. Start the Streamlit app:

  ```bash
  streamlit run app.py
  ```
