import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import requests
from functools import lru_cache
import time

# CoinGecko API Configuration
COINGECKO_API_BASE = "https://api.coingecko.com/api/v3"

# Coin ID mapping for CoinGecko API
COINGECKO_IDS = {
    "ETH": "ethereum",
    "BTC": "bitcoin",
    "SOL": "solana",
    "HYPE": "hyperliquid",
    "XPL": "plasma",
    "LIT": "lighter"
}

@st.cache_data(ttl=300)  # Cache for 5 minutes
def fetch_all_prices():
    """Fetch all coin prices in a single API call"""
    try:
        coin_ids = ",".join(COINGECKO_IDS.values())
        url = f"{COINGECKO_API_BASE}/simple/price"
        params = {
            "ids": coin_ids,
            "vs_currencies": "usd",
            "include_24hr_change": "true",
            "include_market_cap": "true",
            "include_24hr_vol": "true"
        }
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:
            # Rate limited - return None silently
            return None
    except Exception:
        pass
    return None

@st.cache_data(ttl=300)  # Cache for 5 minutes
def fetch_coin_price(coin_id):
    """Fetch current price from CoinGecko"""
    try:
        url = f"{COINGECKO_API_BASE}/simple/price"
        params = {
            "ids": coin_id,
            "vs_currencies": "usd",
            "include_24hr_change": "true",
            "include_market_cap": "true",
            "include_24hr_vol": "true"
        }
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            return response.json().get(coin_id, {})
    except Exception:
        pass
    return None

@st.cache_data(ttl=600)  # Cache for 10 minutes
def fetch_historical_prices(coin_id, days=90):
    """Fetch historical price data from CoinGecko"""
    try:
        url = f"{COINGECKO_API_BASE}/coins/{coin_id}/market_chart"
        params = {
            "vs_currency": "usd",
            "days": days,
            "interval": "daily"
        }
        response = requests.get(url, params=params, timeout=15)
        if response.status_code == 200:
            data = response.json()
            prices = data.get("prices", [])
            if prices:
                df = pd.DataFrame(prices, columns=["timestamp", "price"])
                df["date"] = pd.to_datetime(df["timestamp"], unit="ms")
                return df
    except Exception:
        pass
    return None

@st.cache_data(ttl=600)  # Cache for 10 minutes
def fetch_coin_market_data(coin_id):
    """Fetch detailed market data from CoinGecko"""
    try:
        url = f"{COINGECKO_API_BASE}/coins/{coin_id}"
        params = {
            "localization": "false",
            "tickers": "false",
            "community_data": "false",
            "developer_data": "false"
        }
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass
    return None

@st.cache_data(ttl=1800)  # Cache for 30 minutes
def fetch_defi_tvl():
    """Fetch DeFi TVL data from DefiLlama"""
    try:
        # DefiLlama API for TVL
        url = "https://api.llama.fi/v2/chains"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            chains = response.json()
            tvl_data = {}
            for chain in chains:
                name = chain.get("name", "").lower()
                if name == "ethereum":
                    tvl_data["ETH"] = chain.get("tvl", 0) / 1e9  # Convert to billions
                elif name == "solana":
                    tvl_data["SOL"] = chain.get("tvl", 0) / 1e9
                elif name == "bitcoin":
                    tvl_data["BTC"] = chain.get("tvl", 0) / 1e9
            return tvl_data
    except Exception as e:
        pass
    return {}

def get_live_price(symbol):
    """Get live price for a coin symbol - tries batch fetch first, then individual"""
    coin_id = COINGECKO_IDS.get(symbol)
    if not coin_id:
        return None

    # Try batch fetch first (more efficient)
    all_prices = fetch_all_prices()
    if all_prices and coin_id in all_prices:
        data = all_prices[coin_id]
        return {
            "price": data.get("usd", 0),
            "change_24h": data.get("usd_24h_change", 0),
            "market_cap": data.get("usd_market_cap", 0) / 1e9 if data.get("usd_market_cap") else 0,
            "volume_24h": data.get("usd_24h_vol", 0) / 1e9 if data.get("usd_24h_vol") else 0
        }

    # Fallback to individual fetch
    data = fetch_coin_price(coin_id)
    if data:
        return {
            "price": data.get("usd", 0),
            "change_24h": data.get("usd_24h_change", 0),
            "market_cap": data.get("usd_market_cap", 0) / 1e9 if data.get("usd_market_cap") else 0,
            "volume_24h": data.get("usd_24h_vol", 0) / 1e9 if data.get("usd_24h_vol") else 0
        }
    return None

def get_historical_data(symbol, days=90):
    """Get historical price data for charts"""
    coin_id = COINGECKO_IDS.get(symbol)
    if coin_id:
        df = fetch_historical_prices(coin_id, days)
        if df is not None:
            return df["date"].tolist(), df["price"].tolist()
    return None, None

# Page config
st.set_page_config(
    page_title="CoinVal",
    page_icon="",
    layout="wide"
)

# Custom CSS for ETHval-style dark theme
st.markdown("""
<style>
    /* Global styles */
    .stApp {
        background-color: #0a0a0f;
        color: #ffffff;
    }

    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Header styles */
    .main-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 1rem 0;
        border-bottom: 1px solid #1a1a2e;
        margin-bottom: 2rem;
    }

    .logo-section {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .logo {
        font-size: 1.5rem;
        font-weight: bold;
        background: linear-gradient(135deg, #00d4aa, #00a8ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .version-badge {
        background: #1a1a2e;
        color: #8b8b9e;
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
        font-size: 0.75rem;
    }

    /* Navigation tabs */
    .nav-tabs {
        display: flex;
        gap: 0.5rem;
        background: #12121a;
        padding: 0.5rem;
        border-radius: 8px;
    }

    .nav-tab {
        padding: 0.5rem 1rem;
        border-radius: 6px;
        color: #8b8b9e;
        text-decoration: none;
        font-size: 0.9rem;
        transition: all 0.2s;
    }

    .nav-tab.active {
        background: #00d4aa;
        color: #0a0a0f;
        font-weight: 600;
    }

    /* Section titles */
    .section-title {
        font-size: 1.75rem;
        font-weight: 600;
        color: #ffffff;
        margin: 2rem 0 1.5rem 0;
    }

    .section-number {
        color: #00d4aa;
    }

    /* Valuation card */
    .valuation-card {
        background: #12121a;
        border: 1px solid #1a1a2e;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }

    .metric-label {
        color: #8b8b9e;
        font-size: 0.85rem;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #ffffff;
    }

    .metric-value-large {
        font-size: 2.5rem;
        font-weight: 700;
        color: #ffffff;
    }

    /* Opportunity badge */
    .opportunity-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        font-weight: 600;
    }

    .undervalued {
        background: rgba(0, 212, 170, 0.15);
        color: #00d4aa;
    }

    .overvalued {
        background: rgba(255, 82, 82, 0.15);
        color: #ff5252;
    }

    /* Model range */
    .model-range {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin: 0.5rem 0;
    }

    .range-label {
        font-size: 0.75rem;
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
        font-weight: 600;
    }

    .range-min {
        background: #00d4aa;
        color: #0a0a0f;
    }

    .range-max {
        background: #a855f7;
        color: #ffffff;
    }

    .range-model {
        color: #8b8b9e;
        font-size: 0.85rem;
    }

    .range-value {
        color: #ffffff;
        font-weight: 600;
        margin-left: auto;
    }

    .range-value.green {
        color: #00d4aa;
    }

    .range-value.red {
        color: #ff5252;
    }

    /* Model cards */
    .model-card {
        background: #12121a;
        border: 1px solid #1a1a2e;
        border-radius: 12px;
        padding: 1.25rem;
        height: 100%;
    }

    .model-name {
        font-size: 1rem;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 0.5rem;
    }

    .model-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 0.75rem;
    }

    .model-progress {
        height: 6px;
        background: #1a1a2e;
        border-radius: 3px;
        overflow: hidden;
        margin-bottom: 0.75rem;
    }

    .model-progress-bar {
        height: 100%;
        border-radius: 3px;
        transition: width 0.3s ease;
    }

    .model-progress-bar.green {
        background: linear-gradient(90deg, #00d4aa, #00ffcc);
    }

    .model-progress-bar.red {
        background: linear-gradient(90deg, #ff5252, #ff7b7b);
    }

    .model-change {
        font-size: 0.9rem;
        font-weight: 600;
    }

    .model-change.positive {
        color: #00d4aa;
    }

    .model-change.negative {
        color: #ff5252;
    }

    .model-status {
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .model-status.undervalued {
        color: #00d4aa;
    }

    .model-status.overvalued {
        color: #ff5252;
    }

    .model-formula {
        background: #0a0a0f;
        color: #8b8b9e;
        padding: 0.4rem 0.75rem;
        border-radius: 4px;
        font-size: 0.75rem;
        font-family: monospace;
        margin-top: 0.75rem;
        display: inline-block;
    }

    .model-toggle {
        display: flex;
        align-items: center;
        justify-content: flex-end;
        margin-top: 0.5rem;
    }

    /* Composite sidebar */
    .composite-card {
        background: #12121a;
        border: 1px solid #1a1a2e;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
    }

    .composite-title {
        font-size: 0.85rem;
        color: #8b8b9e;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
    }

    .composite-subtitle {
        font-size: 0.75rem;
        color: #6b6b7e;
        margin-bottom: 1rem;
    }

    .composite-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 0.5rem;
    }

    .composite-change {
        font-size: 1.1rem;
        font-weight: 600;
        color: #00d4aa;
        margin-bottom: 1.5rem;
    }

    .composite-btn {
        display: inline-block;
        background: rgba(0, 212, 170, 0.15);
        color: #00d4aa;
        padding: 0.5rem 1.5rem;
        border-radius: 6px;
        font-weight: 600;
        margin-bottom: 1.5rem;
    }

    /* Vote counts */
    .vote-section {
        display: flex;
        justify-content: center;
        gap: 2rem;
        padding-top: 1rem;
        border-top: 1px solid #1a1a2e;
    }

    .vote-item {
        text-align: center;
    }

    .vote-count {
        font-size: 1.5rem;
        font-weight: 700;
    }

    .vote-count.buy {
        color: #00d4aa;
    }

    .vote-count.hold {
        color: #8b8b9e;
    }

    .vote-count.sell {
        color: #ff5252;
    }

    .vote-label {
        font-size: 0.7rem;
        color: #6b6b7e;
        text-transform: uppercase;
    }

    /* Stats row */
    .stats-row {
        display: flex;
        justify-content: space-between;
        padding: 0.75rem 0;
        border-bottom: 1px solid #1a1a2e;
    }

    .stats-label {
        color: #8b8b9e;
        font-size: 0.85rem;
    }

    .stats-value {
        color: #ffffff;
        font-weight: 600;
    }

    /* Info box */
    .info-box {
        background: #12121a;
        border: 1px solid #1a1a2e;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }

    .info-icon {
        color: #00d4aa;
        margin-right: 0.5rem;
    }

    .info-text {
        color: #8b8b9e;
        font-size: 0.9rem;
        line-height: 1.6;
    }

    /* Slider section */
    .slider-card {
        background: #12121a;
        border: 1px solid #1a1a2e;
        border-radius: 12px;
        padding: 1.25rem;
        margin-bottom: 1rem;
    }

    .slider-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
    }

    .slider-title {
        font-weight: 600;
        color: #ffffff;
    }

    .slider-values {
        color: #8b8b9e;
        font-size: 0.9rem;
    }

    .slider-description {
        color: #6b6b7e;
        font-size: 0.8rem;
        margin-top: 0.5rem;
        line-height: 1.5;
    }

    /* Simulated values grid */
    .sim-value-item {
        display: flex;
        align-items: center;
        padding: 0.5rem 0;
        border-bottom: 1px solid #1a1a2e;
    }

    .sim-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        margin-right: 0.75rem;
    }

    .sim-name {
        color: #ffffff;
        font-size: 0.85rem;
        flex: 1;
    }

    .sim-value {
        color: #ffffff;
        font-weight: 600;
        margin-right: 0.5rem;
    }

    .sim-change {
        font-size: 0.8rem;
        color: #8b8b9e;
    }

    /* Chart container */
    .chart-container {
        background: #12121a;
        border: 1px solid #1a1a2e;
        border-radius: 12px;
        padding: 1.5rem;
    }

    .chart-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
    }

    .chart-title {
        font-size: 1rem;
        font-weight: 600;
        color: #ffffff;
    }

    .chart-prices {
        display: flex;
        gap: 2rem;
    }

    .chart-price-item {
        text-align: center;
    }

    .chart-price-label {
        font-size: 0.75rem;
        color: #8b8b9e;
    }

    .chart-price-value {
        font-size: 1.25rem;
        font-weight: 700;
        color: #ffffff;
    }

    /* Coin selector */
    .coin-selector {
        display: flex;
        gap: 0.5rem;
        margin-bottom: 2rem;
        flex-wrap: wrap;
    }

    .coin-btn {
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s;
        border: 1px solid #1a1a2e;
        background: #12121a;
        color: #8b8b9e;
    }

    .coin-btn.active {
        background: linear-gradient(135deg, #00d4aa, #00a8ff);
        color: #0a0a0f;
        border-color: transparent;
    }

    /* Streamlit overrides */
    .stSelectbox > div > div {
        background-color: #12121a;
        border-color: #1a1a2e;
    }

    .stSlider > div > div > div {
        background-color: #00d4aa;
    }

    div[data-testid="stMetricValue"] {
        font-size: 1.5rem;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: #12121a;
        border-radius: 8px;
        padding: 0.25rem;
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 6px;
        color: #8b8b9e;
        padding: 0.5rem 1rem;
    }

    .stTabs [aria-selected="true"] {
        background: #00d4aa;
        color: #0a0a0f;
    }

    /* Toggle switch */
    .toggle-on {
        background: #00d4aa;
        color: #0a0a0f;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
    }

    /* Metric cards for Locked Capital / Settlement Volume */
    .metric-card-container {
        background: #12121a;
        border: 1px solid #1a1a2e;
        border-radius: 12px;
        padding: 1.25rem;
        height: 100%;
        display: flex;
        flex-direction: column;
    }

    .metric-card-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 0.5rem;
    }

    .metric-card-title {
        font-size: 0.85rem;
        font-weight: 500;
        color: #ffffff;
    }

    .metric-card-time-selector {
        display: flex;
        gap: 0.25rem;
    }

    .time-btn {
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
        font-size: 0.7rem;
        background: transparent;
        color: #6b6b7e;
        border: none;
        cursor: pointer;
    }

    .time-btn.active {
        background: #00d4aa;
        color: #0a0a0f;
    }

    .metric-card-value {
        font-size: 1.75rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 0.5rem;
    }

    .metric-card-chart {
        flex: 1;
        min-height: 60px;
        margin: 0.5rem 0;
    }

    .metric-card-footer {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-top: 0.5rem;
        border-top: 1px solid #1a1a2e;
    }

    .metric-card-source {
        font-size: 0.75rem;
        color: #6b6b7e;
    }

    .metric-card-change {
        font-size: 0.8rem;
        font-weight: 600;
    }

    .metric-card-change.positive {
        color: #00d4aa;
    }

    .metric-card-change.negative {
        color: #ff5252;
    }

    .metric-card-description {
        font-size: 0.75rem;
        color: #6b6b7e;
        line-height: 1.4;
        margin-top: 0.5rem;
    }

    /* Status indicators */
    .status-section {
        background: #12121a;
        border: 1px solid #1a1a2e;
        border-radius: 12px;
        padding: 1.5rem;
        margin-top: 1.5rem;
    }

    .status-header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 0.5rem;
    }

    .status-icon {
        font-size: 1rem;
    }

    .status-title {
        font-size: 0.9rem;
        font-weight: 600;
        color: #ffffff;
    }

    .status-badge {
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-left: auto;
    }

    .status-badge.hot {
        background: rgba(255, 152, 0, 0.2);
        color: #ff9800;
    }

    .status-badge.down {
        background: rgba(255, 82, 82, 0.2);
        color: #ff5252;
    }

    .status-badge.bullish {
        background: rgba(0, 212, 170, 0.2);
        color: #00d4aa;
    }

    .status-description {
        font-size: 0.85rem;
        color: #8b8b9e;
        line-height: 1.6;
    }

    .status-bar {
        height: 4px;
        background: #1a1a2e;
        border-radius: 2px;
        margin: 0.75rem 0;
        overflow: hidden;
    }

    .status-bar-fill {
        height: 100%;
        border-radius: 2px;
    }

    .status-bar-fill.orange {
        background: linear-gradient(90deg, #ff9800, #ffb74d);
    }

    .status-bar-fill.red {
        background: linear-gradient(90deg, #ff5252, #ff7b7b);
    }

    .status-bar-fill.green {
        background: linear-gradient(90deg, #00d4aa, #00ffcc);
    }
</style>
""", unsafe_allow_html=True)

# Coin valuation data with 12 models (ETHval-style)
COINS = {
    "ETH": {
        "name": "Ethereum",
        "icon": "",
        "current_price": 3118.0,
        "models": {
            "TVL Multiple": {"value": 4340.5, "formula": "TVL * Multiple / Supply", "weight": 1},
            "Staking Scarcity": {"value": 3628.7, "formula": "Price * sqrt(Supply / (Supply - Staked))", "weight": 1},
            "Metcalfe's Law": {"value": 10728.3, "formula": "Coef * TVL^Exp / Supply", "weight": 1},
            "DCF (Staking)": {"value": 9353.9, "formula": "Price * (1+APR) / (Discount - Growth)", "weight": 1},
            "L2 Ecosystem": {"value": 4593.3, "formula": "(TVL + L2*Weight) * Multiple / Supply", "weight": 1},
            "P/S Ratio (25x)": {"value": 83.2, "formula": "(L1Fees + BlobFees) * 365 * PSRatio / Supply", "weight": 1},
            "Fee Yield": {"value": 131.0, "formula": "(L1Fees + BlobFees) * 365 / APR / Supply", "weight": 1},
            "Liquidity Premium": {"value": 4430.1, "formula": "Price * sqrt(Supply / Liquid Float)", "weight": 1},
            "App Capital": {"value": 4889.8, "formula": "AppCapital / Supply", "weight": 1},
            "Validator Economics": {"value": 7365.3, "formula": "Price * (Target / APR)", "weight": 1},
            "ETH Monetary (MV=PQ)": {"value": 5210.0, "formula": "Velocity * GDP / Supply", "weight": 1},
            "Ecosystem Settlement": {"value": 14153.1, "formula": "Settlement Volume * Multiple / Supply", "weight": 1},
        },
        "metrics": {
            "tvl": 74.5,  # billions
            "daily_fees": 30.9,  # thousands
            "staking_ratio": 26,  # percent
            "stablecoins": 164.9,  # billions
            "daily_addresses": 620,  # thousands
            "l2_tvl": 45.2,  # billions
        },
        "locked_capital": {
            "l1_tvl": {"value": 74.8, "change": -9.7, "source": "DefiLlama", "desc": "Total USD value locked in Ethereum L1 DeFi protocols (Aave, Lido, MakerDAO, etc). Key measure of DeFi adoption."},
            "l2_tvl": {"value": 8.8, "change": -16.8, "source": "DefiLlama", "desc": "Total USD value locked in L2 rollups (Arbitrum, Optimism, Base, zkSync, etc). Growing L2 TVL indicates scaling adoption."},
            "defi_lending_tvl": {"value": 37.42, "change": -9.7, "source": "DefiLlama", "desc": "Assets in L1 DeFi lending protocols (Aave, Compound, etc). Indicates mainnet DeFi capital."},
            "l1_stablecoin": {"value": 165.2, "change": 3.3, "source": "DefiLlama", "desc": "Stablecoin value on Ethereum. Shows ETH dominance as settlement layer."},
            "l2_stablecoin": {"value": 15.26, "change": -8.8, "source": "Dune", "desc": "Total stablecoin supply on L2s (USDC, USDT, DAI, USDe). Indicates L2 capital inflow."},
            "app_capital": {"value": 590, "change": 3.3, "source": "Calculated", "desc": "Capital deployed in Ethereum apps (DeFi, stables, etc)."},
        },
        "settlement_volume": {
            "l1_total_volume": {"value": 256.8, "change": 13.6, "source": "Dune", "desc": "Total on-chain volume (ETH + all ERC-20 tokens). Complete L1 settlement."},
            "l1_eth_transfer": {"value": 1.1, "change": -98.1, "source": "Dune", "desc": "Daily ETH transfers on mainnet. Native token settlement only."},
            "l1_stablecoin_volume": {"value": 59.05, "change": -44.7, "source": "Dune", "desc": "Daily stablecoin transfer volume on Ethereum (USDT, USDC, DAI, USDe, FDUSD)."},
            "l1_dex_volume": {"value": 1.9, "change": -62.4, "source": "DefiLlama", "desc": "Weekly DEX trading volume on L1 Ethereum. Key indicator of mainnet DeFi activity."},
            "l2_total_volume": {"value": 443.4, "change": 165.4, "source": "Dune", "desc": "Total on-chain volume across 8 L2s (Native + all tokens). Complete L2 settlement."},
            "l2_eth_transfer": {"value": 0.1037, "change": -92.7, "source": "Dune", "desc": "ETH transfers on L2s (excludes Mantle MNT). For ETH Monetary calculation."},
            "l2_stablecoin_volume": {"value": 77.84, "change": 19.8, "source": "Dune", "desc": "Daily stablecoin transfer volume on L2s (Arbitrum, Base, Optimism, Polygon, zkSync, Linea, Scroll)."},
            "l2_dex_volume": {"value": 0.1896, "change": -94.5, "source": "Dune", "desc": "Daily DEX trading volume on L2s (Arbitrum, Optimism, Base, etc). DeFi activity indicator."},
            "bridge_total_volume": {"value": 0.1618, "change": -50.7, "source": "Dune", "desc": "All assets bridged to L2s (ETH + ERC-20 tokens). Total cross-chain capital flow."},
            "bridge_eth_volume": {"value": 0.0034, "change": -93.5, "source": "Dune", "desc": "Daily ETH bridged to L2s. Cross-chain ETH flow indicator."},
        },
    },
    "BTC": {
        "name": "Bitcoin",
        "icon": "",
        "current_price": 97245.0,
        "models": {
            "Stock-to-Flow": {"value": 125000.0, "formula": "Coef * (Stock/Flow)^Exp", "weight": 1},
            "Metcalfe's Law": {"value": 145000.0, "formula": "Coef * ActiveAddr^Exp", "weight": 1},
            "Production Cost": {"value": 85000.0, "formula": "Mining Cost * Multiplier", "weight": 1},
            "NVT Ratio": {"value": 92000.0, "formula": "TxVolume * NVT / Supply", "weight": 1},
            "MVRV Ratio": {"value": 78000.0, "formula": "RealizedCap * MVRV / Supply", "weight": 1},
            "Thermocap Multiple": {"value": 110000.0, "formula": "Thermocap * Multiple / Supply", "weight": 1},
            "Hash Rate Value": {"value": 88000.0, "formula": "HashRate * Coef / Supply", "weight": 1},
            "Lightning Capacity": {"value": 105000.0, "formula": "LN_Capacity * Multiple / Supply", "weight": 1},
            "Realized Price": {"value": 72000.0, "formula": "AvgPurchasePrice * Multiple", "weight": 1},
            "Power Law": {"value": 135000.0, "formula": "Days^Exp * Coef", "weight": 1},
            "Global M2 Ratio": {"value": 155000.0, "formula": "GlobalM2 * Allocation / Supply", "weight": 1},
            "Digital Gold": {"value": 180000.0, "formula": "GoldMarketCap * Penetration / Supply", "weight": 1},
        },
        "metrics": {
            "tvl": 1.2,
            "daily_fees": 850.0,
            "staking_ratio": 0,
            "stablecoins": 0,
            "daily_addresses": 950,
            "l2_tvl": 2.5,
        },
        "locked_capital": {
            "l1_tvl": {"value": 1.2, "change": 15.2, "source": "DefiLlama", "desc": "Total USD value locked in Bitcoin DeFi protocols. Emerging BTC DeFi ecosystem."},
            "l2_tvl": {"value": 2.5, "change": 45.3, "source": "DefiLlama", "desc": "Total USD value locked in Bitcoin L2s (Lightning, Stacks, etc)."},
            "lightning_capacity": {"value": 0.52, "change": 8.2, "source": "mempool.space", "desc": "Total BTC capacity in Lightning Network channels."},
            "wrapped_btc": {"value": 12.5, "change": -5.4, "source": "DefiLlama", "desc": "WBTC and other wrapped BTC on Ethereum and other chains."},
            "ordinals_tvl": {"value": 0.85, "change": 125.0, "source": "Dune", "desc": "Value locked in Ordinals and BRC-20 tokens."},
            "runes_tvl": {"value": 0.32, "change": 85.0, "source": "Dune", "desc": "Value in Runes protocol tokens."},
        },
        "settlement_volume": {
            "l1_total_volume": {"value": 15.2, "change": 5.2, "source": "blockchain.com", "desc": "Total on-chain BTC transfer volume."},
            "lightning_volume": {"value": 0.125, "change": 22.5, "source": "mempool.space", "desc": "Daily Lightning Network payment volume."},
            "exchange_inflow": {"value": 2.8, "change": -15.3, "source": "Glassnode", "desc": "BTC flowing into exchanges."},
            "exchange_outflow": {"value": 3.2, "change": 8.5, "source": "Glassnode", "desc": "BTC flowing out of exchanges."},
            "miner_revenue": {"value": 0.045, "change": -12.5, "source": "blockchain.com", "desc": "Daily miner revenue from fees and block rewards."},
            "whale_transactions": {"value": 8.5, "change": 25.0, "source": "Glassnode", "desc": "Large transactions (>$100K)."},
        },
    },
    "SOL": {
        "name": "Solana",
        "icon": "",
        "current_price": 187.32,
        "models": {
            "TVL Multiple": {"value": 245.0, "formula": "TVL * Multiple / Supply", "weight": 1},
            "Staking Yield": {"value": 198.5, "formula": "Price * (1 + StakingAPR)", "weight": 1},
            "Fee Revenue": {"value": 165.0, "formula": "DailyFees * 365 * Multiple / Supply", "weight": 1},
            "DEX Volume": {"value": 285.0, "formula": "DEXVolume * Multiple / Supply", "weight": 1},
            "NFT Market": {"value": 210.0, "formula": "NFTVolume * Multiple / Supply", "weight": 1},
            "Active Addresses": {"value": 312.0, "formula": "Coef * ActiveAddr^Exp / Supply", "weight": 1},
            "TPS Valuation": {"value": 225.0, "formula": "AvgTPS * ValuePerTx * 365 / Supply", "weight": 1},
            "DeFi TVL": {"value": 195.0, "formula": "DeFiTVL * Multiple / Supply", "weight": 1},
            "Validator Economics": {"value": 178.0, "formula": "ValidatorRewards / (Discount - Growth)", "weight": 1},
            "Network Revenue": {"value": 205.0, "formula": "NetworkRev * Multiple / Supply", "weight": 1},
            "Ecosystem Growth": {"value": 268.0, "formula": "Projects * AvgValue / Supply", "weight": 1},
            "Meme Coin Premium": {"value": 155.0, "formula": "MemeTVL * Sentiment / Supply", "weight": 1},
        },
        "metrics": {
            "tvl": 8.5,
            "daily_fees": 125.0,
            "staking_ratio": 65,
            "stablecoins": 5.2,
            "daily_addresses": 2100,
            "l2_tvl": 0,
        },
        "locked_capital": {
            "defi_tvl": {"value": 8.5, "change": 45.2, "source": "DefiLlama", "desc": "Total USD value locked in Solana DeFi protocols (Marinade, Jito, Raydium, etc)."},
            "staking_tvl": {"value": 78.5, "change": 12.3, "source": "Solana Beach", "desc": "Total SOL staked with validators. Core network security."},
            "liquid_staking": {"value": 5.2, "change": 65.0, "source": "DefiLlama", "desc": "SOL in liquid staking protocols (Marinade mSOL, Jito jitoSOL)."},
            "stablecoin_supply": {"value": 5.2, "change": 85.0, "source": "DefiLlama", "desc": "Stablecoin value on Solana (USDC, USDT). Growing payments adoption."},
            "nft_tvl": {"value": 0.85, "change": -25.0, "source": "Magic Eden", "desc": "Value in NFT collections and marketplaces."},
            "meme_tvl": {"value": 2.5, "change": 250.0, "source": "Dune", "desc": "Capital in meme coins and speculation."},
        },
        "settlement_volume": {
            "total_volume": {"value": 125.5, "change": 85.0, "source": "Dune", "desc": "Total on-chain transfer volume (SOL + SPL tokens)."},
            "dex_volume": {"value": 3.5, "change": 120.0, "source": "DefiLlama", "desc": "Daily DEX trading volume (Raydium, Orca, Jupiter)."},
            "stablecoin_volume": {"value": 8.5, "change": 95.0, "source": "Dune", "desc": "Daily stablecoin transfer volume on Solana."},
            "nft_volume": {"value": 0.025, "change": -45.0, "source": "Magic Eden", "desc": "Daily NFT trading volume."},
            "perp_volume": {"value": 1.2, "change": 150.0, "source": "DefiLlama", "desc": "Perpetual futures trading volume."},
            "payment_volume": {"value": 0.15, "change": 200.0, "source": "Solana Pay", "desc": "Solana Pay merchant payment volume."},
        },
    },
    "HYPE": {
        "name": "Hyperliquid",
        "icon": "🔷",
        "current_price": 25.0,
        "models": {
            "Trading Volume": {"value": 35.0, "formula": "DailyVolume * Multiple / Supply", "weight": 1},
            "Fee Revenue": {"value": 28.0, "formula": "Fees * 365 * Multiple / Supply", "weight": 1},
            "TVL Multiple": {"value": 32.0, "formula": "TVL * Multiple / Supply", "weight": 1},
            "User Growth": {"value": 40.0, "formula": "ActiveUsers * ValuePerUser / Supply", "weight": 1},
            "Perp Dominance": {"value": 45.0, "formula": "PerpMarketShare * TotalMarket / Supply", "weight": 1},
            "L1 Premium": {"value": 38.0, "formula": "L1Value * BlockchainMultiple / Supply", "weight": 1},
            "Token Utility": {"value": 30.0, "formula": "StakedTokens * UtilityMultiple / Supply", "weight": 1},
            "DEX Comparison": {"value": 42.0, "formula": "dYdX_Ratio * dYdX_Price", "weight": 1},
            "Growth Rate": {"value": 50.0, "formula": "Price * (1 + GrowthRate)^Years", "weight": 1},
            "Ecosystem Value": {"value": 35.0, "formula": "EcosystemTVL / Supply", "weight": 1},
            "Network Effects": {"value": 48.0, "formula": "Coef * Users^Exp / Supply", "weight": 1},
            "Liquidity Premium": {"value": 33.0, "formula": "OrderBookDepth * Multiple / Supply", "weight": 1},
        },
        "metrics": {
            "tvl": 2.5,
            "daily_fees": 500.0,
            "staking_ratio": 45,
            "stablecoins": 1.2,
            "daily_addresses": 150,
            "l2_tvl": 0,
        },
        "locked_capital": {
            "perp_tvl": {"value": 2.5, "change": 120.0, "source": "DefiLlama", "desc": "Total value locked in Hyperliquid perpetual contracts."},
            "spot_tvl": {"value": 0.8, "change": 85.0, "source": "DefiLlama", "desc": "Value in spot trading pools."},
            "staked_hype": {"value": 1.2, "change": 150.0, "source": "Hyperliquid", "desc": "HYPE tokens staked for rewards and governance."},
            "vault_deposits": {"value": 0.5, "change": 200.0, "source": "Hyperliquid", "desc": "Assets in Hyperliquid vaults."},
        },
        "settlement_volume": {
            "perp_volume": {"value": 8.5, "change": 95.0, "source": "DefiLlama", "desc": "Daily perpetual trading volume."},
            "spot_volume": {"value": 0.5, "change": 120.0, "source": "DefiLlama", "desc": "Daily spot trading volume."},
            "liquidations": {"value": 0.025, "change": -15.0, "source": "Hyperliquid", "desc": "Daily liquidation volume."},
        },
    },
    "XPL": {
        "name": "Plasma",
        "icon": "⚡",
        "current_price": 0.50,
        "models": {
            "Stablecoin Volume": {"value": 0.85, "formula": "USDTVolume * Multiple / Supply", "weight": 1},
            "TVL Multiple": {"value": 0.65, "formula": "TVL * Multiple / Supply", "weight": 1},
            "Fee Revenue": {"value": 0.45, "formula": "Fees * 365 * PSRatio / Supply", "weight": 1},
            "Network Effects": {"value": 0.95, "formula": "Coef * Users^Exp / Supply", "weight": 1},
            "BTC Bridge": {"value": 0.75, "formula": "BridgedBTC * Multiple / Supply", "weight": 1},
            "Validator Economics": {"value": 0.55, "formula": "StakingRewards / (Discount - Growth)", "weight": 1},
            "Payment Adoption": {"value": 1.10, "formula": "TxCount * AvgValue / Supply", "weight": 1},
            "L1 Comparison": {"value": 0.80, "formula": "L1_Benchmark * PlasmaTPS / BenchmarkTPS", "weight": 1},
            "Staking Scarcity": {"value": 0.70, "formula": "Price * sqrt(Supply / Float)", "weight": 1},
            "DeFi TVL": {"value": 0.60, "formula": "DeFiTVL * Multiple / Supply", "weight": 1},
            "Zero-Fee Premium": {"value": 1.20, "formula": "CompetitorFees * MarketShare / Supply", "weight": 1},
            "Growth DCF": {"value": 0.90, "formula": "FutureRevenue / (Discount - Growth)", "weight": 1},
        },
        "metrics": {
            "tvl": 32.0,
            "daily_fees": 0,
            "staking_ratio": 35,
            "stablecoins": 28.5,
            "daily_addresses": 450,
            "l2_tvl": 0,
        },
        "locked_capital": {
            "total_tvl": {"value": 32.0, "change": -50.0, "source": "DefiLlama", "desc": "Total value locked on Plasma chain."},
            "usdt_supply": {"value": 28.5, "change": 15.0, "source": "Plasma", "desc": "USDT supply on Plasma (zero-fee transfers)."},
            "staked_xpl": {"value": 3.5, "change": 25.0, "source": "Plasma", "desc": "XPL staked with validators."},
            "btc_bridged": {"value": 0.8, "change": 45.0, "source": "Plasma", "desc": "BTC bridged via trust-minimized bridge."},
        },
        "settlement_volume": {
            "usdt_volume": {"value": 5.2, "change": 85.0, "source": "Plasma", "desc": "Daily zero-fee USDT transfer volume."},
            "total_volume": {"value": 8.5, "change": 65.0, "source": "Plasma", "desc": "Total on-chain transfer volume."},
            "smart_contract": {"value": 0.3, "change": 120.0, "source": "Plasma", "desc": "Smart contract interaction volume."},
        },
    },
    "LIT": {
        "name": "Lighter",
        "icon": "🔥",
        "current_price": 3.50,
        "models": {
            "Trading Volume": {"value": 5.20, "formula": "DailyVolume * Multiple / Supply", "weight": 1},
            "Fee Revenue": {"value": 4.50, "formula": "Fees * 365 * Multiple / Supply", "weight": 1},
            "TVL Multiple": {"value": 4.80, "formula": "TVL * Multiple / Supply", "weight": 1},
            "User Acquisition": {"value": 5.50, "formula": "NewUsers * LTV / Supply", "weight": 1},
            "DEX Comparison": {"value": 6.00, "formula": "Uniswap_Ratio * Volume_Ratio", "weight": 1},
            "Verifiable Premium": {"value": 5.80, "formula": "SecurityPremium * MarketShare", "weight": 1},
            "Order Book Depth": {"value": 4.20, "formula": "Liquidity * Multiple / Supply", "weight": 1},
            "Token Burns": {"value": 4.00, "formula": "BurnRate * Price * Multiple", "weight": 1},
            "Growth Rate": {"value": 6.50, "formula": "Price * (1 + GrowthRate)^Years", "weight": 1},
            "Market Share": {"value": 5.00, "formula": "DEXMarket * SharePercent / Supply", "weight": 1},
            "Airdrop Impact": {"value": 3.80, "formula": "CirculatingSupply * Velocity", "weight": 1},
            "Network Effects": {"value": 5.50, "formula": "Coef * Traders^Exp / Supply", "weight": 1},
        },
        "metrics": {
            "tvl": 0.15,
            "daily_fees": 85.0,
            "staking_ratio": 0,
            "stablecoins": 0.08,
            "daily_addresses": 25,
            "l2_tvl": 0,
        },
        "locked_capital": {
            "trading_tvl": {"value": 0.15, "change": 200.0, "source": "DefiLlama", "desc": "Total value in Lighter trading pools."},
            "liquidity": {"value": 0.08, "change": 150.0, "source": "Lighter", "desc": "Liquidity provider deposits."},
        },
        "settlement_volume": {
            "trading_volume": {"value": 0.025, "change": 300.0, "source": "Lighter", "desc": "Daily trading volume on Lighter DEX."},
            "unique_traders": {"value": 0.005, "change": 250.0, "source": "Lighter", "desc": "Daily unique traders value."},
        },
    }
}

def calculate_composite_fair_value(coin_data):
    """Calculate composite fair value from all models"""
    models = coin_data["models"]
    total_value = sum(m["value"] * m["weight"] for m in models.values())
    total_weight = sum(m["weight"] for m in models.values())
    return total_value / total_weight if total_weight > 0 else 0

def get_opportunity_status(current_price, fair_value):
    """Determine if undervalued or overvalued"""
    diff_pct = ((fair_value - current_price) / current_price) * 100
    if diff_pct > 0:
        return "Undervalued", diff_pct
    else:
        return "Overvalued", diff_pct

def generate_historical_data(coin_data, days=90, symbol="ETH"):
    """Generate historical price and fair value data - uses real CoinGecko data"""
    fair_value = calculate_composite_fair_value(coin_data)

    # Try to fetch real historical data from CoinGecko
    real_dates, real_prices = get_historical_data(symbol, days)

    if real_dates and real_prices:
        # Use real data
        dates = real_dates
        prices = real_prices
        current_price = prices[-1] if prices else coin_data["current_price"]
    else:
        # Fallback to generated data if API fails
        np.random.seed(42)
        dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
        current_price = coin_data["current_price"]

        price_returns = np.random.normal(0.001, 0.03, days)
        prices = [current_price]
        for r in price_returns[:-1]:
            prices.append(prices[-1] * (1 + r))
        prices = prices[::-1]

    # Generate fair value data based on actual price movements
    # Fair value tracks price with some smoothing
    if len(prices) > 0:
        price_array = np.array(prices)
        # Calculate fair value as smoothed price adjusted by model ratio
        ratio = fair_value / prices[-1] if prices[-1] > 0 else 1
        fair_values = (price_array * ratio).tolist()
    else:
        fair_values = [fair_value] * len(dates)

    # Generate individual model values based on price movement
    model_data = {}
    for model_name, model_info in coin_data["models"].items():
        base_value = model_info["value"]
        if len(prices) > 0:
            # Scale model values based on price movement
            price_ratio = np.array(prices) / prices[-1]
            model_values = (base_value * price_ratio * np.random.uniform(0.95, 1.05, len(prices))).tolist()
        else:
            model_returns = np.random.normal(0.0005, 0.025, days)
            values = [base_value]
            for r in model_returns[:-1]:
                values.append(values[-1] * (1 + r))
            model_values = values[::-1]
        model_data[model_name] = model_values

    return dates, prices, fair_values, model_data

def generate_mini_chart_data(current_value, change_pct, days=90):
    """Generate mini chart data for metric cards"""
    np.random.seed(hash(str(current_value)) % 2**32)

    # Calculate starting value based on change percentage
    start_value = current_value / (1 + change_pct / 100)

    # Generate data with trend
    trend = np.linspace(start_value, current_value, days)
    noise = np.random.normal(0, abs(current_value - start_value) * 0.1, days)
    values = trend + noise

    return values.tolist()

def create_mini_chart(values, color, height=60):
    """Create a mini sparkline chart"""
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        y=values,
        mode='lines',
        line=dict(color=color, width=2),
        fill='tozeroy',
        fillcolor=f'rgba({int(color[1:3], 16)}, {int(color[3:5], 16)}, {int(color[5:7], 16)}, 0.1)',
        showlegend=False,
        hoverinfo='skip'
    ))

    fig.update_layout(
        height=height,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(visible=False, showgrid=False),
        yaxis=dict(visible=False, showgrid=False),
    )

    return fig

def format_value(value, prefix="$", suffix="B"):
    """Format value with appropriate suffix"""
    if value >= 1000:
        return f"{prefix}{value/1000:.1f}T"
    elif value >= 1:
        return f"{prefix}{value:.2f}{suffix}"
    elif value >= 0.001:
        return f"{prefix}{value*1000:.1f}M"
    else:
        return f"{prefix}{value*1000000:.1f}K"

def render_metric_card(title, data, chart_color):
    """Render a metric card with mini chart"""
    value = data["value"]
    change = data["change"]
    source = data["source"]
    desc = data["desc"]

    # Generate chart data
    chart_data = generate_mini_chart_data(value, change)

    # Determine color based on change
    change_class = "positive" if change >= 0 else "negative"
    change_color = "#00d4aa" if change >= 0 else "#ff5252"

    # Format value
    formatted_value = format_value(value)

    st.markdown(f"""
    <div class="metric-card-container">
        <div class="metric-card-header">
            <span class="metric-card-title">{title}</span>
            <div class="metric-card-time-selector">
                <span class="time-btn active">90D</span>
                <span class="time-btn">1Y</span>
                <span class="time-btn">3Y</span>
            </div>
        </div>
        <div class="metric-card-value">{formatted_value}</div>
    </div>
    """, unsafe_allow_html=True)

    # Mini chart
    fig = create_mini_chart(chart_data, chart_color)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    st.markdown(f"""
    <div class="metric-card-footer">
        <span class="metric-card-source">{source}</span>
        <span class="metric-card-change {change_class}">{change:+.1f}% 90D</span>
    </div>
    <div class="metric-card-description">{desc}</div>
    """, unsafe_allow_html=True)

# Initialize session state
if 'selected_coin' not in st.session_state:
    st.session_state.selected_coin = "ETH"

# Header
col1, col2 = st.columns([1, 3])
with col1:
    st.markdown("""
    <div class="logo-section">
        <span class="logo">CoinVal</span>
        <span class="version-badge">v0.6.1</span>
    </div>
    """, unsafe_allow_html=True)

# Navigation tabs
tabs = st.tabs(["Valuation", "Fundamentals", "Ratings", "Community", "Leaderboard"])

with tabs[0]:  # Valuation tab
    # Coin selector
    st.markdown("### Select Coin")
    coin_cols = st.columns(len(COINS))
    for i, (symbol, data) in enumerate(COINS.items()):
        with coin_cols[i]:
            btn_type = "primary" if st.session_state.selected_coin == symbol else "secondary"
            if st.button(f"{data['icon']} {symbol}", key=f"coin_{symbol}", type=btn_type, use_container_width=True):
                st.session_state.selected_coin = symbol
                st.rerun()

    # Get selected coin data
    coin = COINS[st.session_state.selected_coin]

    # Fetch live price from CoinGecko
    live_data = get_live_price(st.session_state.selected_coin)
    if live_data:
        current_price = live_data["price"]
        price_change_24h = live_data["change_24h"]
        market_cap = live_data["market_cap"]
        volume_24h = live_data["volume_24h"]
        # Update coin data with live price for calculations
        coin["current_price"] = current_price
    else:
        current_price = coin["current_price"]
        price_change_24h = 0
        market_cap = 0
        volume_24h = 0

    composite_fv = calculate_composite_fair_value(coin)
    status, diff_pct = get_opportunity_status(current_price, composite_fv)

    # Section 01 - Valuation
    st.markdown('<h2 class="section-title"><span class="section-number">01</span> — Valuation</h2>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])

    with col1:
        # Show live price with 24h change
        change_class = "positive" if price_change_24h >= 0 else "negative"
        change_color = "#00d4aa" if price_change_24h >= 0 else "#ff5252"
        live_badge = '<span style="background: #00d4aa; color: #0a0a0f; padding: 2px 6px; border-radius: 4px; font-size: 0.65rem; margin-left: 8px;">LIVE</span>' if live_data else ''

        st.markdown(f"""
        <div class="valuation-card">
            <div class="metric-label">CURRENT PRICE {live_badge}</div>
            <div class="metric-value-large">${current_price:,.2f}</div>
            <div style="color: {change_color}; font-size: 0.9rem; font-weight: 600;">{price_change_24h:+.2f}% (24h)</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="valuation-card">
            <div class="metric-label">COMPOSITE FAIR VALUE</div>
            <div style="font-size: 0.75rem; color: #6b6b7e;">(12 / 12 models)</div>
            <div class="metric-value-large">${composite_fv:,.1f}</div>
        </div>
        """, unsafe_allow_html=True)

        badge_class = "undervalued" if status == "Undervalued" else "overvalued"
        st.markdown(f"""
        <div class="valuation-card">
            <div class="metric-label">OPPORTUNITY</div>
            <div class="opportunity-badge {badge_class}">
                {status} <strong>{diff_pct:+.1f}%</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Model range
        models = coin["models"]
        min_model = min(models.items(), key=lambda x: x[1]["value"])
        max_model = max(models.items(), key=lambda x: x[1]["value"])

        st.markdown(f"""
        <div class="valuation-card">
            <div class="metric-label">MODEL RANGE</div>
            <div class="model-range">
                <span class="range-label range-min">Min</span>
                <span class="range-model">{min_model[0]}</span>
                <span class="range-value {'green' if min_model[1]['value'] > current_price else 'red'}">${min_model[1]['value']:,.1f}</span>
            </div>
            <div class="model-range">
                <span class="range-label range-max">Max</span>
                <span class="range-model">{max_model[0]}</span>
                <span class="range-value green">${max_model[1]['value']:,.1f}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="info-box">
            <span class="info-icon">ℹ</span>
            <span class="info-text">
                CoinVal derives {coin['name']}'s intrinsic value using 12 valuation models across four methodological categories:
                Traditional Finance (Staking DCF, P/S Ratio, Fee Yield, Validator Economics), On-chain Asset Value (TVL Multiple, App Capital),
                Network Effects (Metcalfe's Law, Ecosystem Settlement, L2 Ecosystem), and Supply Scarcity (Staking Scarcity, Liquidity Premium).
            </span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="info-box">
            <span class="info-icon">🔓</span>
            <span class="info-text">
                Proof of Rating: CoinVal is completely free — no subscriptions, no hidden fees. Rate just 2 models to unlock 3Y historical data
                & the What-If Simulator. Your ratings help refine the valuation framework — think of it as staking your opinion to earn access.
                Let's build better data together!
            </span>
        </div>
        """, unsafe_allow_html=True)

    # Section 01.1 - Models & Fair Value
    st.markdown('<h2 class="section-title"><span class="section-number">01.1</span> — Models & Fair Value</h2>', unsafe_allow_html=True)

    # Create model cards grid with sidebar
    model_col, sidebar_col = st.columns([3, 1])

    with model_col:
        # Grid of model cards (2 columns)
        model_items = list(coin["models"].items())
        for i in range(0, len(model_items), 2):
            cols = st.columns(2)
            for j, col in enumerate(cols):
                if i + j < len(model_items):
                    model_name, model_info = model_items[i + j]
                    model_value = model_info["value"]
                    diff = ((model_value - current_price) / current_price) * 100
                    is_undervalued = diff > 0

                    # Calculate progress bar width (relative to max model value)
                    max_val = max(m["value"] for m in models.values())
                    progress_pct = min((model_value / max_val) * 100, 100)

                    bar_class = "green" if is_undervalued else "red"
                    change_class = "positive" if is_undervalued else "negative"
                    status_class = "undervalued" if is_undervalued else "overvalued"
                    status_text = "UNDERVALUED" if is_undervalued else "OVERVALUED"

                    with col:
                        st.markdown(f"""
                        <div class="model-card">
                            <div class="model-name">{model_name}</div>
                            <div class="model-value">${model_value:,.1f}</div>
                            <div class="model-progress">
                                <div class="model-progress-bar {bar_class}" style="width: {progress_pct}%"></div>
                            </div>
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <span class="model-change {change_class}">{diff:+.1f}%</span>
                                <span class="model-status {status_class}">{status_text}</span>
                            </div>
                            <div class="model-formula">{model_info['formula']}</div>
                            <div class="model-toggle">
                                <span class="toggle-on">On</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        st.markdown("")

    with sidebar_col:
        st.markdown(f"""
        <div class="composite-card">
            <div class="composite-title">COMPOSITE FAIR VALUE</div>
            <div class="composite-subtitle">(12 / 12 models)</div>
            <div class="composite-value">${composite_fv:,.1f}</div>
            <div class="composite-change">{diff_pct:+.1f}% vs Current</div>
            <div class="composite-btn">▲ UNDERVALUED</div>
            <div class="vote-section">
                <div class="vote-item">
                    <div class="vote-count buy">10</div>
                    <div class="vote-label">BUY</div>
                </div>
                <div class="vote-item">
                    <div class="vote-count hold">0</div>
                    <div class="vote-label">HOLD</div>
                </div>
                <div class="vote-item">
                    <div class="vote-count sell">2</div>
                    <div class="vote-label">SELL</div>
                </div>
            </div>
            <div style="margin-top: 1.5rem; text-align: left;">
                <div class="stats-row">
                    <span class="stats-label">Current Price</span>
                    <span class="stats-value">${current_price:,.1f}</span>
                </div>
                <div class="stats-row">
                    <span class="stats-label">Median</span>
                    <span class="stats-value">${np.median([m['value'] for m in models.values()]):,.1f} ({((np.median([m['value'] for m in models.values()]) - current_price) / current_price * 100):+.1f}%)</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Section 01.2 - Historical Trends
    st.markdown('<h2 class="section-title"><span class="section-number">01.2</span> — Historical Trends</h2>', unsafe_allow_html=True)

    # Generate historical data with real CoinGecko data
    dates, prices, fair_values, model_historical = generate_historical_data(coin, days=90, symbol=st.session_state.selected_coin)

    # Chart controls
    chart_col1, chart_col2 = st.columns([3, 1])
    with chart_col1:
        st.markdown(f"""
        <div class="chart-header">
            <div class="chart-title">COMPOSITE FAIR VALUE OVER TIME <span style="color: #6b6b7e;">(12 / 12 models)</span></div>
        </div>
        <div class="chart-prices">
            <div class="chart-price-item">
                <div class="chart-price-label">Market Price</div>
                <div class="chart-price-value">${prices[-1]:,.1f}</div>
            </div>
            <div class="chart-price-item">
                <div class="chart-price-label">Composite Fair Value</div>
                <div class="chart-price-value" style="color: #00d4aa;">${fair_values[-1]:,.1f} <span style="font-size: 0.9rem;">{diff_pct:+.1f}%</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with chart_col2:
        time_range = st.radio("Time Range", ["90D", "1Y", "3Y"], horizontal=True, label_visibility="collapsed")

    # Create the chart
    fig = go.Figure()

    # Add market price line (dashed white)
    fig.add_trace(go.Scatter(
        x=dates,
        y=prices,
        mode='lines',
        name='Market Price',
        line=dict(color='#ffffff', width=2, dash='dash'),
    ))

    # Add composite fair value line (solid white)
    fig.add_trace(go.Scatter(
        x=dates,
        y=fair_values,
        mode='lines',
        name='Composite Fair Value',
        line=dict(color='#ffffff', width=3),
    ))

    # Add individual model lines with different colors
    colors = ['#ff6b6b', '#ffd93d', '#6bcb77', '#4d96ff', '#a855f7', '#f472b6',
              '#fb923c', '#22d3ee', '#a3e635', '#e879f9', '#38bdf8', '#facc15']

    for idx, (model_name, values) in enumerate(model_historical.items()):
        fig.add_trace(go.Scatter(
            x=dates,
            y=values,
            mode='lines',
            name=model_name,
            line=dict(color=colors[idx % len(colors)], width=1.5),
            visible='legendonly'
        ))

    fig.update_layout(
        plot_bgcolor='#0a0a0f',
        paper_bgcolor='#12121a',
        font=dict(color='#8b8b9e'),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.15,
            xanchor="center",
            x=0.5,
            bgcolor='rgba(0,0,0,0)'
        ),
        margin=dict(l=50, r=50, t=30, b=100),
        xaxis=dict(
            gridcolor='#1a1a2e',
            showgrid=True,
        ),
        yaxis=dict(
            gridcolor='#1a1a2e',
            showgrid=True,
            tickprefix='$',
        ),
        hovermode='x unified',
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)

    # Section 01.3 - Scenario Simulator
    st.markdown('<h2 class="section-title"><span class="section-number">01.3</span> — Scenario Simulator</h2>', unsafe_allow_html=True)

    sim_col1, sim_col2 = st.columns([1, 1])

    metrics = coin["metrics"]

    # Store slider values for simulation
    if 'sim_tvl' not in st.session_state:
        st.session_state.sim_tvl = 1.0
    if 'sim_fees' not in st.session_state:
        st.session_state.sim_fees = 1.0
    if 'sim_staking' not in st.session_state:
        st.session_state.sim_staking = metrics["staking_ratio"]
    if 'sim_stablecoins' not in st.session_state:
        st.session_state.sim_stablecoins = 1.0

    with sim_col1:
        st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
            <div>
                <div style="font-size: 1.1rem; font-weight: 600; color: #ffffff;">WHAT-IF SCENARIO SIMULATOR</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Display current values
        st.markdown(f"""
        <div class="chart-prices" style="margin-bottom: 1.5rem;">
            <div class="chart-price-item">
                <div class="chart-price-label">Market Price</div>
                <div class="chart-price-value">${current_price:,.1f}</div>
            </div>
            <div class="chart-price-item">
                <div class="chart-price-label">Current Fair Value</div>
                <div class="chart-price-value">${composite_fv:,.1f} <span style="color: #00d4aa; font-size: 0.9rem;">{diff_pct:+.1f}%</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**Scenario Variables** *(drag to adjust)*")

        # TVL Slider
        st.markdown(f"""
        <div class="slider-card">
            <div class="slider-header">
                <span class="slider-title">Total Value Locked (TVL)</span>
                <span class="slider-values">${metrics['tvl']:.1f}B → ${metrics['tvl'] * st.session_state.sim_tvl:.1f}B</span>
            </div>
        """, unsafe_allow_html=True)
        tvl_mult = st.slider("TVL Multiplier", 0.1, 10.0, 1.0, 0.1, key="tvl_slider", label_visibility="collapsed")
        st.session_state.sim_tvl = tvl_mult
        st.markdown("""
            <div class="slider-description">More capital locked in DeFi = greater network utility. Drives Network Fees (+50%), Ecosystem Settlement (+50%), and Liquidity Premium. Impacts TVL Multiple, Metcalfe, and L2 Ecosystem models.</div>
        </div>
        """, unsafe_allow_html=True)

        # Daily Fees Slider
        st.markdown(f"""
        <div class="slider-card">
            <div class="slider-header">
                <span class="slider-title">Daily Network Fees (L1 + Blob)</span>
                <span class="slider-values">${metrics['daily_fees']:.1f}K → ${metrics['daily_fees'] * st.session_state.sim_fees:.1f}K</span>
            </div>
        """, unsafe_allow_html=True)
        fees_mult = st.slider("Fees Multiplier", 0.1, 10.0, 1.0, 0.1, key="fees_slider", label_visibility="collapsed")
        st.session_state.sim_fees = fees_mult
        st.markdown("""
            <div class="slider-description">Higher fees = more economic activity. Also affected by TVL changes. Drives P/S ratio and yield valuations.</div>
        </div>
        """, unsafe_allow_html=True)

        # Staking Ratio Slider
        st.markdown(f"""
        <div class="slider-card">
            <div class="slider-header">
                <span class="slider-title">Staking Ratio</span>
                <span class="slider-values">{metrics['staking_ratio']}% → {st.session_state.sim_staking}%</span>
            </div>
        """, unsafe_allow_html=True)
        staking = st.slider("Staking %", 10, 70, metrics["staking_ratio"], 1, key="staking_slider", label_visibility="collapsed")
        st.session_state.sim_staking = staking
        st.markdown("""
            <div class="slider-description">More staked = reduced liquid supply. Impacts Staking Scarcity, Liquidity Premium, and validator APR (affects DCF and Validator Economics).</div>
        </div>
        """, unsafe_allow_html=True)

        # Stablecoins Slider
        st.markdown(f"""
        <div class="slider-card">
            <div class="slider-header">
                <span class="slider-title">Stablecoins on {st.session_state.selected_coin}</span>
                <span class="slider-values">${metrics['stablecoins']:.1f}B → ${metrics['stablecoins'] * st.session_state.sim_stablecoins:.1f}B</span>
            </div>
        """, unsafe_allow_html=True)
        stable_mult = st.slider("Stablecoins Multiplier", 0.1, 10.0, 1.0, 0.1, key="stable_slider", label_visibility="collapsed")
        st.session_state.sim_stablecoins = stable_mult
        st.markdown("""
            <div class="slider-description">Real-world capital on chain. Directly drives App Capital model. Indirectly boosts TVL (+30%) and Network Fees (+30%) through DeFi activity.</div>
        </div>
        """, unsafe_allow_html=True)

    with sim_col2:
        # Calculate simulated values
        sim_factor = (tvl_mult + fees_mult + (staking / metrics["staking_ratio"]) + stable_mult) / 4

        st.markdown("**Simulated Values**")

        # Display simulated model values
        st.markdown('<div style="background: #12121a; border: 1px solid #1a1a2e; border-radius: 12px; padding: 1rem;">', unsafe_allow_html=True)

        sim_colors = ['#ff6b6b', '#ffd93d', '#6bcb77', '#4d96ff', '#a855f7', '#f472b6',
                      '#fb923c', '#22d3ee', '#a3e635', '#e879f9', '#38bdf8', '#facc15']

        for idx, (model_name, model_info) in enumerate(coin["models"].items()):
            base_value = model_info["value"]

            # Apply different simulation factors based on model type
            if "TVL" in model_name or "Ecosystem" in model_name:
                sim_value = base_value * tvl_mult
            elif "Fee" in model_name or "P/S" in model_name:
                sim_value = base_value * fees_mult
            elif "Staking" in model_name or "Liquidity" in model_name:
                sim_value = base_value * (staking / metrics["staking_ratio"])
            elif "App Capital" in model_name:
                sim_value = base_value * stable_mult
            else:
                sim_value = base_value * sim_factor

            change_pct = ((sim_value - base_value) / base_value) * 100 if base_value > 0 else 0

            st.markdown(f"""
            <div class="sim-value-item">
                <div class="sim-dot" style="background: {sim_colors[idx % len(sim_colors)]};"></div>
                <span class="sim-name">{model_name}</span>
                <span class="sim-value">${sim_value:,.1f}</span>
                <span class="sim-change">{change_pct:+.0f}%</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # Simulated composite fair value
        sim_composite = composite_fv * sim_factor
        sim_diff = ((sim_composite - current_price) / current_price) * 100

        st.markdown(f"""
        <div class="composite-card" style="margin-top: 1rem;">
            <div class="composite-title">SIMULATED FAIR VALUE</div>
            <div class="composite-value">${sim_composite:,.1f}</div>
            <div class="composite-change">{sim_diff:+.1f}% vs Current</div>
        </div>
        """, unsafe_allow_html=True)

    # Section 02.6 - Locked Capital
    st.markdown('<h2 class="section-title"><span class="section-number">02.6</span> — Locked Capital</h2>', unsafe_allow_html=True)

    # Get locked capital data
    locked_capital = coin.get("locked_capital", {})

    # Chart colors for different metrics
    lc_colors = ['#00d4aa', '#f472b6', '#ffd93d', '#4d96ff', '#a855f7', '#fb923c']

    # Define display names for locked capital metrics
    lc_display_names = {
        # ETH metrics
        "l1_tvl": "L1 Total Value Locked",
        "l2_tvl": "L2 Total Value Locked",
        "defi_lending_tvl": "DeFi Lending TVL",
        "l1_stablecoin": "L1 Stablecoin Supply",
        "l2_stablecoin": "L2 Stablecoin Supply",
        "app_capital": "App Capital",
        # BTC metrics
        "lightning_capacity": "Lightning Capacity",
        "wrapped_btc": "Wrapped BTC",
        "ordinals_tvl": "Ordinals TVL",
        "runes_tvl": "Runes TVL",
        # SOL metrics
        "defi_tvl": "DeFi TVL",
        "staking_tvl": "Staking TVL",
        "liquid_staking": "Liquid Staking",
        "stablecoin_supply": "Stablecoin Supply",
        "nft_tvl": "NFT TVL",
        "meme_tvl": "Meme Coin TVL",
    }

    # Create grid for locked capital metrics
    lc_items = list(locked_capital.items())

    # First row (4 columns for ETH, 3 for others)
    if len(lc_items) >= 4:
        row1_cols = st.columns(4)
        for i in range(min(4, len(lc_items))):
            key, data = lc_items[i]
            display_name = lc_display_names.get(key, key.replace("_", " ").title())
            chart_color = lc_colors[i % len(lc_colors)]
            change_class = "positive" if data["change"] >= 0 else "negative"

            with row1_cols[i]:
                chart_data = generate_mini_chart_data(data["value"], data["change"])
                formatted_value = format_value(data["value"])

                st.markdown(f"""
                <div class="metric-card-container">
                    <div class="metric-card-header">
                        <span class="metric-card-title">{display_name}</span>
                        <div class="metric-card-time-selector">
                            <span class="time-btn active">90D</span>
                            <span class="time-btn">1Y</span>
                            <span class="time-btn">3Y</span>
                        </div>
                    </div>
                    <div class="metric-card-value">{formatted_value}</div>
                </div>
                """, unsafe_allow_html=True)

                fig = create_mini_chart(chart_data, chart_color)
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

                st.markdown(f"""
                <div class="metric-card-footer">
                    <span class="metric-card-source">{data["source"]}</span>
                    <span class="metric-card-change {change_class}">{data["change"]:+.1f}% 90D</span>
                </div>
                <div class="metric-card-description">{data["desc"]}</div>
                """, unsafe_allow_html=True)

    # Second row (remaining items)
    if len(lc_items) > 4:
        row2_cols = st.columns(min(4, len(lc_items) - 4))
        for i in range(4, len(lc_items)):
            key, data = lc_items[i]
            display_name = lc_display_names.get(key, key.replace("_", " ").title())
            chart_color = lc_colors[i % len(lc_colors)]
            change_class = "positive" if data["change"] >= 0 else "negative"

            with row2_cols[i - 4]:
                chart_data = generate_mini_chart_data(data["value"], data["change"])
                formatted_value = format_value(data["value"])

                st.markdown(f"""
                <div class="metric-card-container">
                    <div class="metric-card-header">
                        <span class="metric-card-title">{display_name}</span>
                        <div class="metric-card-time-selector">
                            <span class="time-btn active">90D</span>
                            <span class="time-btn">1Y</span>
                            <span class="time-btn">3Y</span>
                        </div>
                    </div>
                    <div class="metric-card-value">{formatted_value}</div>
                </div>
                """, unsafe_allow_html=True)

                fig = create_mini_chart(chart_data, chart_color)
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

                st.markdown(f"""
                <div class="metric-card-footer">
                    <span class="metric-card-source">{data["source"]}</span>
                    <span class="metric-card-change {change_class}">{data["change"]:+.1f}% 90D</span>
                </div>
                <div class="metric-card-description">{data["desc"]}</div>
                """, unsafe_allow_html=True)

    # Status indicators for Locked Capital
    st.markdown("""
    <div style="display: flex; gap: 1rem; margin-top: 1.5rem;">
        <div class="status-section" style="flex: 1;">
            <div class="status-header">
                <span class="status-icon">📊</span>
                <span class="status-title">Current Status</span>
                <span class="status-badge hot">Hot</span>
            </div>
            <div class="status-bar"><div class="status-bar-fill orange" style="width: 75%;"></div></div>
            <div class="status-description">
                Locked capital landscape reveals a complex and dynamic ecosystem characterized by substantial capital concentration and strategic positioning across multiple layers of blockchain infrastructure.
            </div>
        </div>
        <div class="status-section" style="flex: 1;">
            <div class="status-header">
                <span class="status-icon">📈</span>
                <span class="status-title">90-Day Trend</span>
                <span class="status-badge down">Down</span>
            </div>
            <div class="status-bar"><div class="status-bar-fill red" style="width: 40%;"></div></div>
            <div class="status-description">
                Layers of blockchain capital demonstrate intricate interconnectedness through multiple channels of value transmission and storage mechanisms.
            </div>
        </div>
        <div class="status-section" style="flex: 1;">
            <div class="status-header">
                <span class="status-icon">💡</span>
                <span class="status-title">Valuation Insight</span>
                <span class="status-badge bullish">Slightly Bullish</span>
            </div>
            <div class="status-bar"><div class="status-bar-fill green" style="width: 60%;"></div></div>
            <div class="status-description">
                Ecosystem exhibits remarkable adaptability with complex capital allocation mechanisms that transcend traditional financial boundaries.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Section 02.7 - Settlement Volume
    st.markdown('<h2 class="section-title"><span class="section-number">02.7</span> — Settlement Volume</h2>', unsafe_allow_html=True)

    # Get settlement volume data
    settlement_volume = coin.get("settlement_volume", {})

    # Chart colors for settlement volume
    sv_colors = ['#4d96ff', '#ffd93d', '#a855f7', '#00d4aa', '#fb923c', '#f472b6', '#22d3ee', '#a3e635', '#e879f9', '#ff6b6b']

    # Define display names for settlement volume metrics
    sv_display_names = {
        # ETH metrics
        "l1_total_volume": "L1 Total Volume",
        "l1_eth_transfer": "L1 ETH Transfer",
        "l1_stablecoin_volume": "L1 Stablecoin Volume",
        "l1_dex_volume": "L1 DEX Volume",
        "l2_total_volume": "L2 Total Volume",
        "l2_eth_transfer": "L2 ETH Transfer",
        "l2_stablecoin_volume": "L2 Stablecoin Volume",
        "l2_dex_volume": "L2 DEX Volume",
        "bridge_total_volume": "Bridge Total Volume",
        "bridge_eth_volume": "Bridge ETH Volume",
        # BTC metrics
        "lightning_volume": "Lightning Volume",
        "exchange_inflow": "Exchange Inflow",
        "exchange_outflow": "Exchange Outflow",
        "miner_revenue": "Miner Revenue",
        "whale_transactions": "Whale Transactions",
        # SOL metrics
        "total_volume": "Total Volume",
        "dex_volume": "DEX Volume",
        "stablecoin_volume": "Stablecoin Volume",
        "nft_volume": "NFT Volume",
        "perp_volume": "Perp Volume",
        "payment_volume": "Payment Volume",
    }

    sv_items = list(settlement_volume.items())

    # Create rows of 4 columns each
    for row_start in range(0, len(sv_items), 4):
        row_end = min(row_start + 4, len(sv_items))
        row_cols = st.columns(4)

        for i in range(row_start, row_end):
            key, data = sv_items[i]
            display_name = sv_display_names.get(key, key.replace("_", " ").title())
            chart_color = sv_colors[i % len(sv_colors)]
            change_class = "positive" if data["change"] >= 0 else "negative"

            with row_cols[i - row_start]:
                chart_data = generate_mini_chart_data(data["value"], data["change"])
                formatted_value = format_value(data["value"])

                st.markdown(f"""
                <div class="metric-card-container">
                    <div class="metric-card-header">
                        <span class="metric-card-title">{display_name}</span>
                        <div class="metric-card-time-selector">
                            <span class="time-btn active">90D</span>
                            <span class="time-btn">1Y</span>
                            <span class="time-btn">3Y</span>
                        </div>
                    </div>
                    <div class="metric-card-value">{formatted_value}</div>
                </div>
                """, unsafe_allow_html=True)

                fig = create_mini_chart(chart_data, chart_color)
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

                st.markdown(f"""
                <div class="metric-card-footer">
                    <span class="metric-card-source">{data["source"]}</span>
                    <span class="metric-card-change {change_class}">{data["change"]:+.1f}% 90D</span>
                </div>
                <div class="metric-card-description">{data["desc"]}</div>
                """, unsafe_allow_html=True)

with tabs[1]:  # Fundamentals tab
    st.markdown("### Fundamentals")
    st.info("Fundamentals analysis coming soon...")

with tabs[2]:  # Ratings tab
    st.markdown("### Community Ratings")
    st.info("User ratings coming soon...")

with tabs[3]:  # Community tab
    st.markdown("### Community")
    st.info("Community features coming soon...")

with tabs[4]:  # Leaderboard tab
    st.markdown("### Leaderboard")
    st.info("Leaderboard coming soon...")

# Footer
st.markdown("---")
st.caption("Data for demonstration purposes. Not financial advice.")
