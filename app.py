import streamlit as st
import json
from src.arbitrage_finder import find_arbitrage
from src.price_fetcher import fetch_coingecko_rates
from src.slippage_model import apply_slippage


st.title("Crypto Arbitrage Detector")

mode = st.radio("Select input mode", ["Live from Binance", "Manual JSON input"])

if mode == "Live from Binance":
    with st.spinner("Fetching live rates..."):
        try:
            rates = fetch_coingecko_rates(["BTC", "ETH", "USDT"])
        except Exception as e:
            st.error(f"Failed to fetch live rates: {e}")
            st.stop()
    slippage_pct = st.slider("Slippage Percentage", 0.0, 5.0, 1.0, step=0.1) / 100.0
    for base in rates:
        for quote in list(rates[base]):
            try:
                rates[base][quote] = apply_slippage(rates[base][quote], slippage_pct)
            except Exception:
                del rates[base][quote]
    st.write("Exchange Rates", rates)
    if st.button("Detect Arbitrage"):
        cycle = find_arbitrage(rates)
        if cycle:
            st.success("Arbitrage opportunity found!")
            st.write(" -> ".join(cycle))
        else:
            st.info("No arbitrage opportunity detected.")

else:
    user_input = st.text_area("Enter exchange rates as JSON", height=300)
    if st.button("Detect Arbitrage"):
        try:
            rates = json.loads(user_input)
            slippage_pct = st.slider("Slippage Percentage", 0.0, 5.0, 1.0, step=0.1) / 100.0
            for base in rates:
                for quote in rates[base]:
                    rates[base][quote] = apply_slippage(rates[base][quote], slippage_pct)
            cycle = find_arbitrage(rates)
            if cycle:
                st.success("Arbitrage opportunity found!")
                st.write(" -> ".join(cycle))
            else:
                st.info("No arbitrage opportunity detected.")
        except Exception as e:
            st.error(f"Error parsing input: {e}")