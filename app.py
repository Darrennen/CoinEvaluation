import streamlit as st
import numpy as np
import random

# Page config
st.set_page_config(
    page_title="Coin Evaluation",
    page_icon="📊",
    layout="wide"
)

# Custom CSS matching ETHval dark theme
st.markdown("""
<style>
    .stApp {
        background-color: #0d0d0d;
    }

    /* Hide default streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    .main-header {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 1rem 0;
        border-bottom: 1px solid #1a1a1a;
        margin-bottom: 2rem;
    }

    .logo {
        background: linear-gradient(135deg, #8b5cf6, #a855f7);
        padding: 8px 12px;
        border-radius: 12px;
        font-weight: bold;
        color: white;
    }

    .section-title {
        color: #a855f7;
        font-size: 1.75rem;
        font-weight: 600;
        margin: 2rem 0 1.5rem 0;
    }

    .metric-card {
        background: #141414;
        border-radius: 16px;
        padding: 1.25rem;
        border: 1px solid #1f1f1f;
        height: 100%;
    }

    .metric-label {
        color: #888;
        font-size: 0.85rem;
        margin-bottom: 0.5rem;
    }

    .metric-value {
        color: #fff;
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
    }

    .metric-value-large {
        color: #fff;
        font-size: 2.25rem;
        font-weight: 700;
    }

    .change-positive {
        color: #22c55e;
        font-size: 0.875rem;
    }

    .change-negative {
        color: #ef4444;
        font-size: 0.875rem;
    }

    .data-source {
        color: #666;
        font-size: 0.75rem;
        margin-top: 0.5rem;
    }

    .metric-description {
        color: #666;
        font-size: 0.75rem;
        margin-top: 0.5rem;
        line-height: 1.4;
    }

    .time-toggle {
        display: inline-flex;
        gap: 4px;
        background: #1a1a1a;
        padding: 4px;
        border-radius: 8px;
    }

    .time-btn {
        padding: 4px 12px;
        border-radius: 6px;
        font-size: 0.75rem;
        cursor: pointer;
    }

    .time-btn-active {
        background: #8b5cf6;
        color: white;
    }

    .time-btn-inactive {
        color: #888;
    }

    .price-display {
        font-size: 2.5rem;
        font-weight: 700;
        color: #fff;
    }

    .price-change-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 6px;
        font-size: 0.875rem;
        font-weight: 600;
        margin-left: 12px;
    }

    .price-change-negative {
        background: rgba(239, 68, 68, 0.2);
        color: #ef4444;
    }

    .price-change-positive {
        background: rgba(34, 197, 94, 0.2);
        color: #22c55e;
    }

    .analysis-section {
        background: #141414;
        border-radius: 16px;
        padding: 1.5rem;
        border: 1px solid #1f1f1f;
        margin-top: 2rem;
    }

    .analysis-header {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 1rem;
    }

    .status-indicator {
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }

    .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
    }

    .status-cool { background: #f97316; }
    .status-weak { background: #ef4444; }
    .status-bullish { background: #22c55e; }
    .status-neutral { background: #eab308; }

    .analysis-text {
        color: #999;
        font-size: 0.875rem;
        line-height: 1.6;
    }

    .coin-selector-btn {
        background: #1a1a1a;
        border: 1px solid #2a2a2a;
        padding: 8px 16px;
        border-radius: 8px;
        color: #fff;
        cursor: pointer;
        transition: all 0.2s;
    }

    .coin-selector-btn:hover {
        background: #2a2a2a;
    }

    .coin-selector-btn.active {
        background: #8b5cf6;
        border-color: #8b5cf6;
    }

    /* Sparkline placeholder */
    .sparkline {
        height: 60px;
        margin-top: 0.5rem;
    }

    .nav-tabs {
        display: flex;
        gap: 2rem;
        margin-bottom: 2rem;
    }

    .nav-tab {
        color: #888;
        text-decoration: none;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid transparent;
    }

    .nav-tab.active {
        color: #fff;
        border-bottom-color: #8b5cf6;
    }

    .stat-row {
        display: flex;
        justify-content: space-between;
        padding: 0.5rem 0;
        border-bottom: 1px solid #1f1f1f;
    }

    .stat-row:last-child {
        border-bottom: none;
    }

    .stat-row-label {
        color: #888;
    }

    .stat-row-value {
        color: #fff;
        font-weight: 600;
    }

    div[data-testid="stHorizontalBlock"] {
        gap: 1rem;
    }

    .stButton > button {
        background: #1a1a1a;
        border: 1px solid #2a2a2a;
        color: #fff;
        border-radius: 8px;
    }

    .stButton > button:hover {
        background: #2a2a2a;
        border-color: #3a3a3a;
    }

    .stSelectbox > div > div {
        background: #1a1a1a;
        border-color: #2a2a2a;
    }
</style>
""", unsafe_allow_html=True)

# Extended coin data with comprehensive metrics
COINS = {
    "ETH": {
        "name": "Ethereum",
        "icon": "⟠",
        "price": 3113.2,
        "change_24h": -4.3,
        "market_cap": 376.4,  # billions
        "volume_24h": 24.9,  # billions
        "ath": 4946.1,
        "ath_change": -37.0,
        # Investor Sentiment
        "realized_price": 1600,
        "realized_price_change": 3.0,
        "mvrv_ratio": 2.03,
        "mvrv_change": -17.3,
        "fear_greed": 42,
        "funding_rate": 0.4986,
        "open_interest": 19.60,  # billions
        "open_interest_change": 3.3,
        "exchange_reserve": 16.42,  # millions ETH
        "exchange_reserve_change": -6.6,
        "whale_transactions": 71.0,
        "whale_tx_change": -84.9,
        # Market Position
        "btc_ratio": 0.03521,
        "btc_ratio_change": 3.6,
        "dominance": 12.3,
        "dominance_change": 6.1,
        "stablecoin_mcap": 306.8,  # billions
        "stablecoin_change": 1.1,
        "volatility": 40.7,
        "nvt_ratio": 105.3,
        "nvt_change": 91.9,
        # Supply Dynamics
        "staking_yield": 2.54,
        "staking_yield_change": -4.51,
        "staked_eth": 31.58,  # millions
        "staked_eth_change": 4.7,
        "eth_burned": 22.4,
        "eth_burned_change": -93.4,
        "eth_issued": 2200,
        "eth_issued_change": -6.0,
        "net_supply": 0.66,
        "effective_float": 49.5,
        "effective_float_change": -1.1,
        # Network Demand
        "gas_price": 0.7,
        "gas_price_change": -83.8,
        "gas_utilization": 50.7,
        "gas_util_change": 0.5,
        "network_fees": 71.3,  # thousands
        "network_fees_change": -94.5,
        "blob_fees": 1.1,  # millions
        "blob_fees_change": 1452.1,
        "blob_count": 36.1,  # thousands
        "blob_count_change": -3.8,
        "defi_revenue": 12.8,  # millions
        "defi_revenue_change": -51.7,
        "description": "Ethereum is a decentralized platform that enables smart contracts and dApps. The network transitioned to Proof of Stake with The Merge in 2022."
    },
    "BTC": {
        "name": "Bitcoin",
        "icon": "₿",
        "price": 97245.00,
        "change_24h": 2.45,
        "market_cap": 1920,
        "volume_24h": 28.5,
        "ath": 108135,
        "ath_change": -10.1,
        "realized_price": 35000,
        "realized_price_change": 2.1,
        "mvrv_ratio": 2.78,
        "mvrv_change": 5.2,
        "fear_greed": 65,
        "funding_rate": 0.0125,
        "open_interest": 45.2,
        "open_interest_change": 8.5,
        "exchange_reserve": 2.1,
        "exchange_reserve_change": -3.2,
        "whale_transactions": 245,
        "whale_tx_change": 12.3,
        "btc_ratio": 1.0,
        "btc_ratio_change": 0,
        "dominance": 54.2,
        "dominance_change": 2.1,
        "stablecoin_mcap": 306.8,
        "stablecoin_change": 1.1,
        "volatility": 32.5,
        "nvt_ratio": 78.2,
        "nvt_change": 15.3,
        "staking_yield": 0,
        "staking_yield_change": 0,
        "staked_eth": 0,
        "staked_eth_change": 0,
        "eth_burned": 0,
        "eth_burned_change": 0,
        "eth_issued": 450,
        "eth_issued_change": 0,
        "net_supply": 1.7,
        "effective_float": 78.5,
        "effective_float_change": -0.5,
        "gas_price": 0,
        "gas_price_change": 0,
        "gas_utilization": 0,
        "gas_util_change": 0,
        "network_fees": 850,
        "network_fees_change": 25.3,
        "blob_fees": 0,
        "blob_fees_change": 0,
        "blob_count": 0,
        "blob_count_change": 0,
        "defi_revenue": 2.1,
        "defi_revenue_change": 45.2,
        "description": "Bitcoin is a decentralized digital currency created in 2009. It uses blockchain technology and Proof of Work consensus."
    },
    "SOL": {
        "name": "Solana",
        "icon": "◎",
        "price": 187.32,
        "change_24h": 4.15,
        "market_cap": 91.2,
        "volume_24h": 3.8,
        "ath": 263.83,
        "ath_change": -29.0,
        "realized_price": 45.0,
        "realized_price_change": 12.5,
        "mvrv_ratio": 4.16,
        "mvrv_change": 25.3,
        "fear_greed": 72,
        "funding_rate": 0.0285,
        "open_interest": 5.2,
        "open_interest_change": 15.2,
        "exchange_reserve": 42.5,
        "exchange_reserve_change": -8.5,
        "whale_transactions": 125,
        "whale_tx_change": 32.5,
        "btc_ratio": 0.00193,
        "btc_ratio_change": 1.8,
        "dominance": 2.8,
        "dominance_change": 12.5,
        "stablecoin_mcap": 306.8,
        "stablecoin_change": 1.1,
        "volatility": 55.2,
        "nvt_ratio": 42.5,
        "nvt_change": -15.2,
        "staking_yield": 6.8,
        "staking_yield_change": 0.5,
        "staked_eth": 385,
        "staked_eth_change": 8.2,
        "eth_burned": 0,
        "eth_burned_change": 0,
        "eth_issued": 0,
        "eth_issued_change": 0,
        "net_supply": 5.2,
        "effective_float": 62.5,
        "effective_float_change": -2.5,
        "gas_price": 0.00025,
        "gas_price_change": -5.2,
        "gas_utilization": 85.2,
        "gas_util_change": 12.5,
        "network_fees": 125,
        "network_fees_change": 85.2,
        "blob_fees": 0,
        "blob_fees_change": 0,
        "blob_count": 0,
        "blob_count_change": 0,
        "defi_revenue": 8.5,
        "defi_revenue_change": 125.5,
        "description": "Solana is a high-performance blockchain supporting builders creating crypto apps that scale. Known for its speed and low transaction costs."
    }
}


def generate_sparkline_data(length=30, trend="neutral", volatility=0.1):
    """Generate mock sparkline data."""
    base = 100
    data = [base]
    for _ in range(length - 1):
        change = random.gauss(0, volatility * base)
        if trend == "up":
            change += 0.5
        elif trend == "down":
            change -= 0.5
        data.append(max(0, data[-1] + change))
    return data


def format_number(value, prefix="", suffix="", decimals=2):
    """Format number with optional prefix/suffix."""
    if value >= 1e9:
        return f"{prefix}{value/1e9:.{decimals}f}B{suffix}"
    elif value >= 1e6:
        return f"{prefix}{value/1e6:.{decimals}f}M{suffix}"
    elif value >= 1e3:
        return f"{prefix}{value/1e3:.{decimals}f}K{suffix}"
    else:
        return f"{prefix}{value:.{decimals}f}{suffix}"


def render_change(value, suffix="%"):
    """Render change value with color."""
    if value >= 0:
        return f'<span class="change-positive">+{value:.1f}{suffix} 90D</span>'
    else:
        return f'<span class="change-negative">{value:.1f}{suffix} 90D</span>'


def render_metric_card(label, value, change=None, source=None, description=None, unit=""):
    """Render a metric card."""
    change_html = render_change(change) if change is not None else ""
    source_html = f'<div class="data-source">{source}</div>' if source else ""
    desc_html = f'<div class="metric-description">{description}</div>' if description else ""

    return f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}{unit}</div>
        {change_html}
        {source_html}
        {desc_html}
    </div>
    """


def render_analysis_section(title, status, status_color, text):
    """Render analysis section."""
    return f"""
    <div style="flex: 1;">
        <div class="analysis-header">
            <span style="color: #888;">📊</span>
            <span style="color: #888;">{title}</span>
            <span class="status-indicator">
                <span class="status-dot status-{status_color}"></span>
                <span style="color: {'#22c55e' if status_color == 'bullish' else '#f97316' if status_color == 'cool' else '#ef4444'}">{status}</span>
            </span>
        </div>
        <p class="analysis-text">{text}</p>
    </div>
    """


# Header
st.markdown("""
<div class="main-header">
    <span class="logo">📊 CoinVal</span>
    <span style="color: #666; font-size: 0.875rem;">v0.6.1</span>
</div>
""", unsafe_allow_html=True)

# Navigation tabs
tab_col1, tab_col2, tab_col3, tab_col4, tab_col5 = st.columns(5)
with tab_col1:
    st.markdown('<span style="color: #fff; border-bottom: 2px solid #8b5cf6; padding-bottom: 8px;">Valuation</span>', unsafe_allow_html=True)
with tab_col2:
    st.markdown('<span style="color: #888;">Fundamentals</span>', unsafe_allow_html=True)
with tab_col3:
    st.markdown('<span style="color: #888;">Ratings</span>', unsafe_allow_html=True)
with tab_col4:
    st.markdown('<span style="color: #888;">Community</span>', unsafe_allow_html=True)
with tab_col5:
    st.markdown('<span style="color: #888;">Leaderboard</span>', unsafe_allow_html=True)

# Coin selector
st.markdown("---")
coin_options = list(COINS.keys())

if 'selected_coin' not in st.session_state:
    st.session_state.selected_coin = "ETH"

cols = st.columns(len(coin_options))
for i, coin_key in enumerate(coin_options):
    with cols[i]:
        btn_type = "primary" if st.session_state.selected_coin == coin_key else "secondary"
        if st.button(f"{COINS[coin_key]['icon']} {coin_key}", key=f"btn_{coin_key}", type=btn_type, use_container_width=True):
            st.session_state.selected_coin = coin_key
            st.rerun()

coin = COINS[st.session_state.selected_coin]

# =============================================================================
# SECTION 02 - FUNDAMENTALS
# =============================================================================
st.markdown('<h2 class="section-title">02 — Fundamentals</h2>', unsafe_allow_html=True)

fund_col1, fund_col2 = st.columns([1, 2])

with fund_col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{st.session_state.selected_coin} / USD</div>
        <div class="metric-value-large">${coin['price']:,.1f}</div>
        <span class="price-change-badge price-change-{'negative' if coin['change_24h'] < 0 else 'positive'}">{coin['change_24h']:+.1f}% (24h)</span>

        <div style="margin-top: 1.5rem;">
            <div class="stat-row">
                <span class="stat-row-label">Market Cap</span>
                <span class="stat-row-value">${coin['market_cap']:.1f}B</span>
            </div>
            <div class="stat-row">
                <span class="stat-row-label">24h Volume</span>
                <span class="stat-row-value">${coin['volume_24h']:.1f}B</span>
            </div>
            <div class="stat-row">
                <span class="stat-row-label">ATH</span>
                <span class="stat-row-value">${coin['ath']:,.1f} <span class="change-negative">{coin['ath_change']:.1f}%</span></span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with fund_col2:
    # Price chart placeholder
    chart_data = generate_sparkline_data(90, trend="down" if coin['change_24h'] < 0 else "up", volatility=0.02)
    st.line_chart(chart_data, height=250, use_container_width=True)
    st.caption("CoinGecko | -30.2% 90D")

# =============================================================================
# SECTION 02.1 - INVESTOR SENTIMENT
# =============================================================================
st.markdown('<h2 class="section-title">02.1 — Investor Sentiment</h2>', unsafe_allow_html=True)

sent_row1 = st.columns(4)

with sent_row1[0]:
    st.markdown(render_metric_card(
        "Realized Price",
        f"${coin['realized_price']:,.0f}" if coin['realized_price'] >= 1000 else f"${coin['realized_price']:.2f}",
        coin['realized_price_change'],
        "Dune",
        "Volume-weighted average price of all transfers since 2016. Represents aggregate cost basis of all holders."
    ), unsafe_allow_html=True)

with sent_row1[1]:
    st.markdown(render_metric_card(
        "MVRV Ratio",
        f"{coin['mvrv_ratio']:.2f}x",
        coin['mvrv_change'],
        "Dune",
        "Market Value to Realized Value. >3x = overheated, <1x = undervalued."
    ), unsafe_allow_html=True)

with sent_row1[2]:
    fear_color = "#ef4444" if coin['fear_greed'] < 40 else "#22c55e" if coin['fear_greed'] > 60 else "#eab308"
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Fear & Greed</div>
        <div class="metric-value" style="color: {fear_color}">{coin['fear_greed']}</div>
        <span style="color: {fear_color}; font-size: 0.875rem;">{'Fear' if coin['fear_greed'] < 40 else 'Greed' if coin['fear_greed'] > 60 else 'Neutral'}</span>
        <div class="data-source">Alternative.me</div>
        <div class="metric-description">Market sentiment index (0-100). Extreme fear often = buying opportunity.</div>
    </div>
    """, unsafe_allow_html=True)

with sent_row1[3]:
    st.markdown(render_metric_card(
        "Funding Rate",
        f"{coin['funding_rate']:.4f}%",
        None,
        "CryptoQuant",
        "Perpetual futures funding. Positive = longs pay shorts, market bullish."
    ), unsafe_allow_html=True)

sent_row2 = st.columns(3)

with sent_row2[0]:
    st.markdown(render_metric_card(
        "Open Interest",
        f"${coin['open_interest']:.2f}B",
        coin['open_interest_change'],
        "CryptoQuant",
        "Total open derivative positions. Rising OI + price = strong trend confirmation."
    ), unsafe_allow_html=True)

with sent_row2[1]:
    unit = " ETH" if st.session_state.selected_coin == "ETH" else f" {st.session_state.selected_coin}"
    st.markdown(render_metric_card(
        f"Exchange {st.session_state.selected_coin} Reserve",
        f"{coin['exchange_reserve']:.2f}M{unit}",
        coin['exchange_reserve_change'],
        "CryptoQuant",
        f"{st.session_state.selected_coin} held on exchanges. Declining reserve = accumulation, bullish signal."
    ), unsafe_allow_html=True)

with sent_row2[2]:
    st.markdown(render_metric_card(
        "Whale Transactions",
        f"{coin['whale_transactions']:.0f} txs",
        coin['whale_tx_change'],
        "Dune",
        f"Daily 1000+ {st.session_state.selected_coin} transactions. Large player activity indicator."
    ), unsafe_allow_html=True)

# Sentiment Analysis Summary
st.markdown("""
<div class="analysis-section">
    <div style="display: flex; gap: 2rem;">
""", unsafe_allow_html=True)

st.markdown(render_analysis_section(
    "Current Status", "Cool", "cool",
    f"{coin['name']}'s current investor sentiment reveals a landscape of profound uncertainty and cautious introspection. Market participants are navigating through turbulent waters characterized by heightened apprehension and reduced confidence."
), unsafe_allow_html=True)

st.markdown(render_analysis_section(
    "90-Day Trend", "Down", "weak",
    f"The broader cryptocurrency ecosystem is witnessing a remarkable transformation in participant behavior and market dynamics. Fundamental shifts are occurring beneath the surface, indicating a potential recalibration of investment strategies."
), unsafe_allow_html=True)

st.markdown(render_analysis_section(
    "Valuation Insight", "Slight", "neutral",
    f"{coin['name']}'s ecosystem continues to demonstrate remarkable resilience amidst challenging market conditions. Technical fundamentals remain robust, suggesting potential future growth."
), unsafe_allow_html=True)

st.markdown("</div></div>", unsafe_allow_html=True)

# =============================================================================
# SECTION 02.2 - MARKET POSITION
# =============================================================================
st.markdown('<h2 class="section-title">02.2 — Market Position</h2>', unsafe_allow_html=True)

mkt_row1 = st.columns(4)

with mkt_row1[0]:
    st.markdown(render_metric_card(
        f"{st.session_state.selected_coin}/BTC Ratio",
        f"{coin['btc_ratio']:.5f}",
        coin['btc_ratio_change'],
        "CoinGecko",
        f"{st.session_state.selected_coin} price relative to BTC. Rising ratio signals {st.session_state.selected_coin} strength vs Bitcoin."
    ), unsafe_allow_html=True)

with mkt_row1[1]:
    st.markdown(render_metric_card(
        f"{st.session_state.selected_coin} Dominance",
        f"{coin['dominance']:.1f}%",
        coin['dominance_change'],
        "CoinGecko",
        f"{st.session_state.selected_coin}'s share of total crypto market cap. Higher = {st.session_state.selected_coin} outperforming alts."
    ), unsafe_allow_html=True)

with mkt_row1[2]:
    st.markdown(render_metric_card(
        "Stablecoin Mcap",
        f"${coin['stablecoin_mcap']:.1f}B",
        coin['stablecoin_change'],
        "DefiLlama",
        "Total stablecoin market cap. Growth indicates capital inflow to crypto."
    ), unsafe_allow_html=True)

with mkt_row1[3]:
    vol_status = "Moderate" if 30 < coin['volatility'] < 60 else "High" if coin['volatility'] >= 60 else "Low"
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Volatility</div>
        <div class="metric-value">{coin['volatility']:.1f}%</div>
        <span style="color: #888; font-size: 0.875rem;">{vol_status}</span>
        <div class="data-source">CoinGecko</div>
        <div class="metric-description">30-day price volatility. Lower volatility often precedes big moves.</div>
    </div>
    """, unsafe_allow_html=True)

mkt_row2 = st.columns(4)

with mkt_row2[0]:
    st.markdown(render_metric_card(
        "NVT Ratio",
        f"{coin['nvt_ratio']:.1f}",
        coin['nvt_change'],
        "Calculated",
        "Market cap ÷ on-chain volume (7-day avg). Lower = undervalued."
    ), unsafe_allow_html=True)

# Market Position Analysis
st.markdown("""
<div class="analysis-section">
    <div style="display: flex; gap: 2rem;">
""", unsafe_allow_html=True)

st.markdown(render_analysis_section(
    "Current Status", "Cold", "cool",
    f"The {coin['name']} ecosystem reveals a nuanced landscape of cautious market dynamics where investors are experiencing a period of recalibration and strategic repositioning."
), unsafe_allow_html=True)

st.markdown(render_analysis_section(
    "90-Day Trend", "Weak", "weak",
    f"{coin['name']}'s market positioning reflects a sophisticated interplay of complex technological and economic factors that transcend simplistic interpretations of market movements."
), unsafe_allow_html=True)

st.markdown(render_analysis_section(
    "Valuation Insight", "Bullish", "bullish",
    f"Advanced market analysis unveils a sophisticated narrative of technological potential and economic recalibration within the {coin['name']} ecosystem."
), unsafe_allow_html=True)

st.markdown("</div></div>", unsafe_allow_html=True)

# =============================================================================
# SECTION 02.3 - SUPPLY DYNAMICS
# =============================================================================
st.markdown('<h2 class="section-title">02.3 — Supply Dynamics</h2>', unsafe_allow_html=True)

sup_row1 = st.columns(4)

with sup_row1[0]:
    if coin['staking_yield'] > 0:
        st.markdown(render_metric_card(
            "Staking Yield (APR)",
            f"{coin['staking_yield']:.2f}%",
            coin['staking_yield_change'],
            "Lido" if st.session_state.selected_coin == "ETH" else "Marinade",
            f"Annual L1 staking return. Benchmark yield for {st.session_state.selected_coin} investment."
        ), unsafe_allow_html=True)
    else:
        st.markdown(render_metric_card(
            "Staking Yield (APR)",
            "N/A",
            None,
            None,
            f"{st.session_state.selected_coin} does not support native staking."
        ), unsafe_allow_html=True)

with sup_row1[1]:
    if coin['staked_eth'] > 0:
        unit = " ETH" if st.session_state.selected_coin == "ETH" else f" {st.session_state.selected_coin}"
        st.markdown(render_metric_card(
            f"Staked {st.session_state.selected_coin}",
            f"{coin['staked_eth']:.2f}M{unit}",
            coin['staked_eth_change'],
            "Dune",
            f"{st.session_state.selected_coin} locked in staking. Higher = more network security."
        ), unsafe_allow_html=True)
    else:
        st.markdown(render_metric_card(
            f"Staked {st.session_state.selected_coin}",
            "N/A",
            None,
            None,
            f"{st.session_state.selected_coin} uses Proof of Work."
        ), unsafe_allow_html=True)

with sup_row1[2]:
    if st.session_state.selected_coin == "ETH":
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">ETH Burned</div>
            <div class="metric-value" style="color: #ef4444;">{coin['eth_burned']:.1f} ETH</div>
            {render_change(coin['eth_burned_change'])}
            <div class="data-source">Dune</div>
            <div class="metric-description">ETH burned via EIP-1559 on L1. Higher burn = more mainnet activity.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(render_metric_card(
            f"{st.session_state.selected_coin} Burned",
            "N/A",
            None,
            None,
            f"{st.session_state.selected_coin} does not have burn mechanism."
        ), unsafe_allow_html=True)

with sup_row1[3]:
    if st.session_state.selected_coin == "ETH":
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">ETH Issued</div>
            <div class="metric-value" style="color: #22c55e;">{coin['eth_issued']:,.0f} ETH</div>
            {render_change(coin['eth_issued_change'])}
            <div class="data-source">Beaconcha.in</div>
            <div class="metric-description">New ETH issued to L1 validators. ~930 ETH/day post-merge.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(render_metric_card(
            f"{st.session_state.selected_coin} Issued",
            f"{coin['eth_issued']:.0f}/day",
            None,
            None,
            f"New {st.session_state.selected_coin} issued daily."
        ), unsafe_allow_html=True)

sup_row2 = st.columns(2)

with sup_row2[0]:
    net_supply_status = "Inflationary" if coin['net_supply'] > 0 else "Deflationary"
    supply_color = "#ef4444" if coin['net_supply'] > 0 else "#22c55e"
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Net Supply</div>
        <div class="metric-value">{'+' if coin['net_supply'] > 0 else ''}{coin['net_supply']:.2f}%/yr</div>
        <span style="color: {supply_color}; font-size: 0.875rem;">{net_supply_status}</span>
        <div class="data-source">Calculated</div>
        <div class="metric-description">L1 burn minus issuance. Negative = deflationary, bullish for {st.session_state.selected_coin} value.</div>
    </div>
    """, unsafe_allow_html=True)

with sup_row2[1]:
    st.markdown(render_metric_card(
        "Effective Float",
        f"{coin['effective_float']:.1f}%",
        coin['effective_float_change'],
        "DefiLlama",
        f"Liquid {st.session_state.selected_coin} available for trading. Others = L2 bridges, lost coins."
    ), unsafe_allow_html=True)

# Supply Dynamics Analysis
st.markdown("""
<div class="analysis-section">
    <div style="display: flex; gap: 2rem;">
""", unsafe_allow_html=True)

st.markdown(render_analysis_section(
    "Current Status", "Cool", "cool",
    f"{coin['name']}'s supply landscape reveals a nuanced and transformative period characterized by subtle yet significant shifts in network economics. Staking participation demonstrates cautious expansion."
), unsafe_allow_html=True)

st.markdown(render_analysis_section(
    "90-Day Trend", "Weak", "weak",
    f"Deflationary pressures are experiencing a remarkable recalibration within {coin['name']}'s tokenomic framework. Network burn mechanisms have substantially contracted."
), unsafe_allow_html=True)

st.markdown(render_analysis_section(
    "Valuation Insight", "Slightly Bullish", "bullish",
    f"{coin['name']}'s supply dynamics represent a sophisticated intersection between technological innovation and economic engineering."
), unsafe_allow_html=True)

st.markdown("</div></div>", unsafe_allow_html=True)

# =============================================================================
# SECTION 02.4 - NETWORK DEMAND
# =============================================================================
st.markdown('<h2 class="section-title">02.4 — Network Demand</h2>', unsafe_allow_html=True)

net_row1 = st.columns(4)

with net_row1[0]:
    if st.session_state.selected_coin == "ETH":
        st.markdown(render_metric_card(
            "Gas Price",
            f"{coin['gas_price']:.1f} Gwei",
            coin['gas_price_change'],
            "Dune",
            "Average L1 gas price in Gwei. Reflects mainnet transaction costs."
        ), unsafe_allow_html=True)
    else:
        st.markdown(render_metric_card(
            "Avg Fee",
            f"${coin['gas_price']:.5f}" if coin['gas_price'] > 0 else "N/A",
            coin['gas_price_change'] if coin['gas_price'] > 0 else None,
            "Explorer",
            f"Average transaction fee on {st.session_state.selected_coin} network."
        ), unsafe_allow_html=True)

with net_row1[1]:
    if st.session_state.selected_coin in ["ETH", "SOL"]:
        st.markdown(render_metric_card(
            "Gas Utilization",
            f"{coin['gas_utilization']:.1f}%",
            coin['gas_util_change'],
            "Dune",
            "% of L1 block gas limit used. High utilization = strong network demand."
        ), unsafe_allow_html=True)
    else:
        st.markdown(render_metric_card(
            "Block Utilization",
            "N/A",
            None,
            None,
            f"Block utilization metric not applicable for {st.session_state.selected_coin}."
        ), unsafe_allow_html=True)

with net_row1[2]:
    st.markdown(render_metric_card(
        "Network Fees",
        f"${coin['network_fees']:.1f}K",
        coin['network_fees_change'],
        "DefiLlama",
        f"Total fees paid to L1 network. Revenue proxy for {coin['name']} mainnet."
    ), unsafe_allow_html=True)

with net_row1[3]:
    if st.session_state.selected_coin == "ETH":
        st.markdown(render_metric_card(
            "Blob Fees",
            f"${coin['blob_fees']:.1f}M",
            coin['blob_fees_change'],
            "Etherscan",
            "L2 data posting fees since Dencun upgrade (Mar 2024). Blob fees are burned like gas."
        ), unsafe_allow_html=True)
    else:
        st.markdown(render_metric_card(
            "L2 Fees",
            "N/A",
            None,
            None,
            f"{st.session_state.selected_coin} doesn't have blob-style L2 fees."
        ), unsafe_allow_html=True)

net_row2 = st.columns(2)

with net_row2[0]:
    if st.session_state.selected_coin == "ETH":
        st.markdown(render_metric_card(
            "Blob Count",
            f"{coin['blob_count']:.1f}K",
            coin['blob_count_change'],
            "Etherscan",
            "Data blobs posted by L2s since Dencun (Mar 2024). More blobs = growing L2 adoption."
        ), unsafe_allow_html=True)
    else:
        st.markdown(render_metric_card(
            "Daily Transactions",
            f"{random.randint(1, 50):.0f}M",
            random.uniform(-20, 40),
            "Explorer",
            f"Total daily transactions on {st.session_state.selected_coin} network."
        ), unsafe_allow_html=True)

with net_row2[1]:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">DeFi Protocol Revenue</div>
        <div class="metric-value">${coin['defi_revenue']:.1f}M</div>
        <span style="background: #3b82f6; color: white; padding: 2px 8px; border-radius: 4px; font-size: 0.7rem; margin-right: 8px;">Est.</span>
        {render_change(coin['defi_revenue_change'])}
        <div class="data-source">DefiLlama</div>
        <div class="metric-description">Daily fee revenue from DeFi protocols (Uniswap, Aave, Lido, etc). Shows ecosystem economic activity.</div>
    </div>
    """, unsafe_allow_html=True)

# Network Demand Analysis
st.markdown("""
<div class="analysis-section">
    <div style="display: flex; gap: 2rem;">
""", unsafe_allow_html=True)

st.markdown(render_analysis_section(
    "Current Status", "Cold", "cool",
    f"{coin['name']}'s network demand currently presents a nuanced landscape of profound transformation and strategic recalibration. The blockchain ecosystem is experiencing a remarkable compression of transactional costs."
), unsafe_allow_html=True)

st.markdown(render_analysis_section(
    "90-Day Trend", "Weak", "weak",
    f"The network's utilization metrics reveal intriguing patterns of resilience amidst widespread contraction. Gas utilization remains remarkably stable despite significant price compressions."
), unsafe_allow_html=True)

st.markdown(render_analysis_section(
    "Valuation Insight", "Bullish", "bullish",
    f"{coin['name']}'s ecosystem is navigating a complex transition characterized by significant metric volatilities and structural recalibrations."
), unsafe_allow_html=True)

st.markdown("</div></div>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.caption("Data updates periodically. Not financial advice. Sources: CoinGecko, Dune, DefiLlama, CryptoQuant, Alternative.me")
