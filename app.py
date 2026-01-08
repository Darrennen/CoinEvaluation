import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

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
        }
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
        }
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
        }
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

def generate_historical_data(coin_data, days=90):
    """Generate historical price and fair value data"""
    np.random.seed(42)
    dates = pd.date_range(end=datetime.now(), periods=days, freq='D')

    current_price = coin_data["current_price"]
    fair_value = calculate_composite_fair_value(coin_data)

    # Generate price data with some volatility
    price_returns = np.random.normal(0.001, 0.03, days)
    prices = [current_price]
    for r in price_returns[:-1]:
        prices.append(prices[-1] * (1 + r))
    prices = prices[::-1]  # Reverse so current is last

    # Generate fair value data (less volatile)
    fv_returns = np.random.normal(0.0005, 0.015, days)
    fair_values = [fair_value]
    for r in fv_returns[:-1]:
        fair_values.append(fair_values[-1] * (1 + r))
    fair_values = fair_values[::-1]

    # Generate individual model values
    model_data = {}
    for model_name, model_info in coin_data["models"].items():
        model_returns = np.random.normal(0.0005, 0.025, days)
        values = [model_info["value"]]
        for r in model_returns[:-1]:
            values.append(values[-1] * (1 + r))
        model_data[model_name] = values[::-1]

    return dates, prices, fair_values, model_data

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
    current_price = coin["current_price"]
    composite_fv = calculate_composite_fair_value(coin)
    status, diff_pct = get_opportunity_status(current_price, composite_fv)

    # Section 01 - Valuation
    st.markdown('<h2 class="section-title"><span class="section-number">01</span> — Valuation</h2>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown(f"""
        <div class="valuation-card">
            <div class="metric-label">CURRENT PRICE</div>
            <div class="metric-value-large">${current_price:,.1f}</div>
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

    # Generate historical data
    dates, prices, fair_values, model_historical = generate_historical_data(coin)

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
