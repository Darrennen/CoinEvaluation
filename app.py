import streamlit as st
import plotly.graph_objects as go
import numpy as np
import random

# Set random seed for consistent sparklines per session
if 'seed' not in st.session_state:
    st.session_state.seed = random.randint(0, 10000)
random.seed(st.session_state.seed)
np.random.seed(st.session_state.seed)

# Page config
st.set_page_config(
    page_title="CoinVal - Coin Evaluation Dashboard",
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
    header {visibility: hidden;}

    .main-header {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 1rem 0;
        border-bottom: 1px solid #1a1a1a;
        margin-bottom: 1rem;
    }

    .logo {
        background: linear-gradient(135deg, #8b5cf6, #a855f7);
        padding: 8px 14px;
        border-radius: 12px;
        font-weight: bold;
        font-size: 1.1rem;
        color: white;
    }

    .section-title {
        color: #a855f7;
        font-size: 1.5rem;
        font-weight: 600;
        margin: 1.5rem 0 1rem 0;
    }

    .metric-card {
        background: #141414;
        border-radius: 12px;
        padding: 1rem;
        border: 1px solid #1f1f1f;
        height: 100%;
        min-height: 200px;
    }

    .metric-card-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 0.5rem;
    }

    .metric-label {
        color: #888;
        font-size: 0.8rem;
    }

    .metric-value {
        color: #fff;
        font-size: 1.4rem;
        font-weight: 700;
        margin: 0.25rem 0;
    }

    .metric-value-large {
        color: #fff;
        font-size: 2rem;
        font-weight: 700;
    }

    .change-positive {
        color: #22c55e;
        font-size: 0.8rem;
    }

    .change-negative {
        color: #ef4444;
        font-size: 0.8rem;
    }

    .data-source {
        color: #555;
        font-size: 0.7rem;
        margin-top: 0.5rem;
    }

    .metric-description {
        color: #555;
        font-size: 0.7rem;
        margin-top: 0.25rem;
        line-height: 1.3;
    }

    .time-toggle {
        display: inline-flex;
        gap: 2px;
        background: #1a1a1a;
        padding: 2px;
        border-radius: 6px;
        font-size: 0.65rem;
    }

    .time-btn {
        padding: 2px 8px;
        border-radius: 4px;
        cursor: pointer;
        color: #666;
    }

    .time-btn-active {
        background: #8b5cf6;
        color: white;
    }

    .price-change-badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-left: 10px;
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
        border-radius: 12px;
        padding: 1.25rem;
        border: 1px solid #1f1f1f;
        margin-top: 1.5rem;
    }

    .analysis-header {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 0.75rem;
    }

    .status-indicator {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        margin-left: auto;
    }

    .status-bar {
        display: flex;
        gap: 2px;
        margin-right: 8px;
    }

    .status-bar-segment {
        width: 20px;
        height: 6px;
        border-radius: 2px;
        background: #333;
    }

    .status-bar-segment.active-red { background: #ef4444; }
    .status-bar-segment.active-orange { background: #f97316; }
    .status-bar-segment.active-yellow { background: #eab308; }
    .status-bar-segment.active-green { background: #22c55e; }

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
        color: #888;
        font-size: 0.8rem;
        line-height: 1.5;
    }

    .stat-row {
        display: flex;
        justify-content: space-between;
        padding: 0.4rem 0;
        border-bottom: 1px solid #1f1f1f;
    }

    .stat-row:last-child {
        border-bottom: none;
    }

    .stat-row-label {
        color: #888;
        font-size: 0.85rem;
    }

    .stat-row-value {
        color: #fff;
        font-weight: 600;
        font-size: 0.85rem;
    }

    div[data-testid="stHorizontalBlock"] {
        gap: 0.75rem;
    }

    .stButton > button {
        background: #1a1a1a;
        border: 1px solid #2a2a2a;
        color: #fff;
        border-radius: 8px;
        font-size: 0.85rem;
    }

    .stButton > button:hover {
        background: #2a2a2a;
        border-color: #3a3a3a;
    }

    /* Hide plotly modebar */
    .modebar {
        display: none !important;
    }

    .stPlotlyChart {
        background: transparent !important;
    }

    /* Streamlit chart styling */
    [data-testid="stArrowVegaLiteChart"] {
        background: transparent !important;
    }

    .badge-est {
        background: #3b82f6;
        color: white;
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 0.65rem;
        margin-right: 6px;
    }

    .fear-greed-bar {
        height: 6px;
        background: linear-gradient(to right, #ef4444, #f97316, #eab308, #22c55e);
        border-radius: 3px;
        margin-top: 8px;
        position: relative;
    }

    .fear-greed-marker {
        position: absolute;
        width: 4px;
        height: 12px;
        background: white;
        border-radius: 2px;
        top: -3px;
        transform: translateX(-50%);
    }
</style>
""", unsafe_allow_html=True)

# Extended coin data with comprehensive metrics
COINS = {
    "ETH": {
        "name": "Ethereum",
        "icon": "⟠",
        "color": "#627eea",
        "price": 3113.2,
        "change_24h": -4.3,
        "change_90d": -30.2,
        "market_cap": 376.4,
        "volume_24h": 24.9,
        "ath": 4946.1,
        "ath_change": -37.0,
        "realized_price": 1600,
        "realized_price_change": 3.0,
        "mvrv_ratio": 2.03,
        "mvrv_change": -17.3,
        "fear_greed": 42,
        "funding_rate": 0.4986,
        "open_interest": 19.60,
        "open_interest_change": 3.3,
        "exchange_reserve": 16.42,
        "exchange_reserve_change": -6.6,
        "whale_transactions": 71.0,
        "whale_tx_change": -84.9,
        "btc_ratio": 0.03521,
        "btc_ratio_change": 3.6,
        "dominance": 12.3,
        "dominance_change": 6.1,
        "stablecoin_mcap": 306.8,
        "stablecoin_change": 1.1,
        "volatility": 40.7,
        "nvt_ratio": 105.3,
        "nvt_change": 91.9,
        "staking_yield": 2.54,
        "staking_yield_change": -4.51,
        "staked_amount": 31.58,
        "staked_change": 4.7,
        "burned": 22.4,
        "burned_change": -93.4,
        "issued": 2200,
        "issued_change": -6.0,
        "net_supply": 0.66,
        "effective_float": 49.5,
        "effective_float_change": -1.1,
        "gas_price": 0.7,
        "gas_price_change": -83.8,
        "gas_utilization": 50.7,
        "gas_util_change": 0.5,
        "network_fees": 71.3,
        "network_fees_change": -94.5,
        "blob_fees": 1.1,
        "blob_fees_change": 1452.1,
        "blob_count": 36.1,
        "blob_count_change": -3.8,
        "defi_revenue": 12.8,
        "defi_revenue_change": -51.7,
    },
    "BTC": {
        "name": "Bitcoin",
        "icon": "₿",
        "color": "#f7931a",
        "price": 97245.00,
        "change_24h": 2.45,
        "change_90d": 15.2,
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
        "staked_amount": 0,
        "staked_change": 0,
        "burned": 0,
        "burned_change": 0,
        "issued": 450,
        "issued_change": 0,
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
    },
    "SOL": {
        "name": "Solana",
        "icon": "◎",
        "color": "#00ffa3",
        "price": 187.32,
        "change_24h": 4.15,
        "change_90d": 45.8,
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
        "staked_amount": 385,
        "staked_change": 8.2,
        "burned": 0,
        "burned_change": 0,
        "issued": 0,
        "issued_change": 0,
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
    },
    "HYPE": {
        "name": "Hyperliquid",
        "icon": "⬡",
        "color": "#00d4aa",
        "price": 23.45,
        "change_24h": 8.72,
        "change_90d": 156.3,
        "market_cap": 7.8,
        "volume_24h": 0.542,
        "ath": 35.20,
        "ath_change": -33.4,
        "realized_price": 8.5,
        "realized_price_change": 45.2,
        "mvrv_ratio": 2.76,
        "mvrv_change": 85.3,
        "fear_greed": 78,
        "funding_rate": 0.0350,
        "open_interest": 1.2,
        "open_interest_change": 125.5,
        "exchange_reserve": 85.2,
        "exchange_reserve_change": -15.3,
        "whale_transactions": 45,
        "whale_tx_change": 78.5,
        "btc_ratio": 0.000241,
        "btc_ratio_change": 6.2,
        "dominance": 0.24,
        "dominance_change": 145.2,
        "stablecoin_mcap": 306.8,
        "stablecoin_change": 1.1,
        "volatility": 78.5,
        "nvt_ratio": 28.5,
        "nvt_change": -25.3,
        "staking_yield": 12.5,
        "staking_yield_change": 2.5,
        "staked_amount": 125,
        "staked_change": 45.2,
        "burned": 0,
        "burned_change": 0,
        "issued": 0,
        "issued_change": 0,
        "net_supply": 8.5,
        "effective_float": 35.2,
        "effective_float_change": -5.2,
        "gas_price": 0,
        "gas_price_change": 0,
        "gas_utilization": 92.5,
        "gas_util_change": 25.3,
        "network_fees": 45.2,
        "network_fees_change": 185.2,
        "blob_fees": 0,
        "blob_fees_change": 0,
        "blob_count": 0,
        "blob_count_change": 0,
        "defi_revenue": 5.2,
        "defi_revenue_change": 245.5,
    },
    "LIT": {
        "name": "Litentry",
        "icon": "◈",
        "color": "#18d2d2",
        "price": 1.24,
        "change_24h": -3.21,
        "change_90d": -45.2,
        "market_cap": 0.124,
        "volume_24h": 0.0182,
        "ath": 12.45,
        "ath_change": -90.0,
        "realized_price": 2.85,
        "realized_price_change": -15.2,
        "mvrv_ratio": 0.44,
        "mvrv_change": -35.2,
        "fear_greed": 28,
        "funding_rate": -0.0125,
        "open_interest": 0.025,
        "open_interest_change": -25.2,
        "exchange_reserve": 12.5,
        "exchange_reserve_change": 8.5,
        "whale_transactions": 8,
        "whale_tx_change": -65.2,
        "btc_ratio": 0.0000127,
        "btc_ratio_change": -5.5,
        "dominance": 0.004,
        "dominance_change": -48.2,
        "stablecoin_mcap": 306.8,
        "stablecoin_change": 1.1,
        "volatility": 85.2,
        "nvt_ratio": 185.2,
        "nvt_change": 125.3,
        "staking_yield": 8.5,
        "staking_yield_change": -2.5,
        "staked_amount": 25,
        "staked_change": -5.2,
        "burned": 0,
        "burned_change": 0,
        "issued": 0,
        "issued_change": 0,
        "net_supply": 2.5,
        "effective_float": 72.5,
        "effective_float_change": 2.5,
        "gas_price": 0,
        "gas_price_change": 0,
        "gas_utilization": 0,
        "gas_util_change": 0,
        "network_fees": 2.5,
        "network_fees_change": -65.2,
        "blob_fees": 0,
        "blob_fees_change": 0,
        "blob_count": 0,
        "blob_count_change": 0,
        "defi_revenue": 0.15,
        "defi_revenue_change": -45.5,
    },
}


def generate_sparkline_data(length=90, trend="neutral", volatility=0.02, base=100):
    """Generate mock sparkline data."""
    data = [base]
    for _ in range(length - 1):
        change = np.random.normal(0, volatility * base)
        if trend == "up":
            change += 0.3
        elif trend == "down":
            change -= 0.3
        data.append(max(base * 0.5, data[-1] + change))
    return data


def create_sparkline(data, color="#8b5cf6", height=60, show_area=True):
    """Create a minimal sparkline chart using plotly."""
    fig = go.Figure()

    if show_area:
        fig.add_trace(go.Scatter(
            y=data,
            mode='lines',
            fill='tozeroy',
            fillcolor=f'rgba({int(color[1:3], 16)}, {int(color[3:5], 16)}, {int(color[5:7], 16)}, 0.1)',
            line=dict(color=color, width=1.5),
            hoverinfo='skip'
        ))
    else:
        fig.add_trace(go.Scatter(
            y=data,
            mode='lines',
            line=dict(color=color, width=1.5),
            hoverinfo='skip'
        ))

    fig.update_layout(
        height=height,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        xaxis=dict(visible=False, showgrid=False),
        yaxis=dict(visible=False, showgrid=False),
    )

    return fig


def render_change(value, suffix=" 90D"):
    """Render change value with color."""
    if value >= 0:
        return f'<span class="change-positive">+{value:.1f}%{suffix}</span>'
    else:
        return f'<span class="change-negative">{value:.1f}%{suffix}</span>'


def render_time_toggle(active="90D"):
    """Render time period toggle."""
    periods = ["90D", "1Y", "3Y"]
    html = '<div class="time-toggle">'
    for p in periods:
        cls = "time-btn time-btn-active" if p == active else "time-btn"
        html += f'<span class="{cls}">{p}</span>'
    html += '</div>'
    return html


def render_analysis_section(title, status, level, text):
    """Render analysis section with status bar."""
    # level: 1-5 (1=very bearish, 5=very bullish)
    colors = {
        1: ("red", "#ef4444"),
        2: ("orange", "#f97316"),
        3: ("yellow", "#eab308"),
        4: ("green", "#22c55e"),
        5: ("green", "#22c55e"),
    }
    color_name, color_hex = colors.get(level, ("yellow", "#eab308"))

    bar_html = '<div class="status-bar">'
    for i in range(1, 6):
        active = "active-red" if i <= level and level <= 2 else \
                 "active-orange" if i <= level and level == 2 else \
                 "active-yellow" if i <= level and level == 3 else \
                 "active-green" if i <= level and level >= 4 else ""
        bar_html += f'<span class="status-bar-segment {active if i <= level else ""}"></span>'
    bar_html += '</div>'

    return f"""
    <div style="flex: 1; min-width: 280px;">
        <div class="analysis-header">
            <span style="color: #666;">📊</span>
            <span style="color: #888; font-size: 0.85rem;">{title}</span>
            <span class="status-indicator">
                {bar_html}
                <span style="color: {color_hex}; font-weight: 500;">{status}</span>
            </span>
        </div>
        <p class="analysis-text">{text}</p>
    </div>
    """


# Header
st.markdown("""
<div class="main-header">
    <span class="logo">📊 CoinVal</span>
    <span style="color: #666; font-size: 0.8rem;">v0.7.0</span>
</div>
""", unsafe_allow_html=True)

# Navigation tabs
nav_cols = st.columns([1, 1, 1, 1, 1, 3])
tabs = ["Valuation", "Fundamentals", "Ratings", "Community", "Leaderboard"]
for i, tab in enumerate(tabs):
    with nav_cols[i]:
        style = "color: #fff; border-bottom: 2px solid #8b5cf6;" if i == 0 else "color: #666;"
        st.markdown(f'<span style="{style} padding-bottom: 8px; font-size: 0.9rem;">{tab}</span>', unsafe_allow_html=True)

# Coin selector
st.markdown("<div style='margin: 0.5rem 0;'></div>", unsafe_allow_html=True)
coin_options = list(COINS.keys())

if 'selected_coin' not in st.session_state:
    st.session_state.selected_coin = "ETH"

cols = st.columns(len(coin_options) + 2)  # Extra columns for spacing
for i, coin_key in enumerate(coin_options):
    with cols[i]:
        btn_type = "primary" if st.session_state.selected_coin == coin_key else "secondary"
        if st.button(f"{COINS[coin_key]['icon']} {coin_key}", key=f"btn_{coin_key}", type=btn_type, use_container_width=True):
            st.session_state.selected_coin = coin_key
            st.rerun()

coin = COINS[st.session_state.selected_coin]
coin_key = st.session_state.selected_coin

# =============================================================================
# SECTION 02 - FUNDAMENTALS
# =============================================================================
st.markdown('<h2 class="section-title">02 — Fundamentals</h2>', unsafe_allow_html=True)

fund_col1, fund_col2 = st.columns([1, 2])

with fund_col1:
    st.markdown(f"""
    <div class="metric-card" style="min-height: 280px;">
        <div class="metric-label">{coin_key} / USD</div>
        <div class="metric-value-large">${coin['price']:,.1f}</div>
        <span class="price-change-badge price-change-{'negative' if coin['change_24h'] < 0 else 'positive'}">{coin['change_24h']:+.1f}% (24h)</span>

        <div style="margin-top: 1.25rem;">
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
    trend = "down" if coin['change_90d'] < 0 else "up"
    chart_data = generate_sparkline_data(90, trend=trend, volatility=0.015, base=coin['price'])
    fig = create_sparkline(chart_data, color=coin['color'], height=250)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; color: #666; font-size: 0.75rem; margin-top: -10px;">
        <span>CoinGecko</span>
        <span>{render_change(coin['change_90d'], "")}</span>
    </div>
    """, unsafe_allow_html=True)

# =============================================================================
# SECTION 02.1 - INVESTOR SENTIMENT
# =============================================================================
st.markdown('<h2 class="section-title">02.1 — Investor Sentiment</h2>', unsafe_allow_html=True)

sent_row1 = st.columns(4)

# Realized Price
with sent_row1[0]:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-card-header">
            <span class="metric-label">Realized Price</span>
            {render_time_toggle()}
        </div>
        <div class="metric-value">${coin['realized_price']:,.0f}</div>
        {render_change(coin['realized_price_change'])}
    """, unsafe_allow_html=True)
    trend = "up" if coin['realized_price_change'] > 0 else "down"
    fig = create_sparkline(generate_sparkline_data(30, trend, 0.01), color="#22c55e", height=50)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown(f"""
        <div class="data-source">Dune</div>
        <div class="metric-description">Volume-weighted average price. Represents aggregate cost basis.</div>
    </div>
    """, unsafe_allow_html=True)

# MVRV Ratio
with sent_row1[1]:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-card-header">
            <span class="metric-label">MVRV Ratio</span>
            {render_time_toggle()}
        </div>
        <div class="metric-value">{coin['mvrv_ratio']:.2f}x</div>
        {render_change(coin['mvrv_change'])}
    """, unsafe_allow_html=True)
    mvrv_color = "#ef4444" if coin['mvrv_ratio'] > 3 else "#22c55e" if coin['mvrv_ratio'] < 1 else "#f97316"
    fig = create_sparkline(generate_sparkline_data(30, "neutral", 0.02, coin['mvrv_ratio']), color=mvrv_color, height=50)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown(f"""
        <div class="data-source">Dune</div>
        <div class="metric-description">Market Value to Realized Value. >3x = overheated, <1x = undervalued.</div>
    </div>
    """, unsafe_allow_html=True)

# Fear & Greed
with sent_row1[2]:
    fear_color = "#ef4444" if coin['fear_greed'] < 40 else "#22c55e" if coin['fear_greed'] > 60 else "#eab308"
    fear_label = "Fear" if coin['fear_greed'] < 40 else "Greed" if coin['fear_greed'] > 60 else "Neutral"
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-card-header">
            <span class="metric-label">Fear & Greed</span>
            {render_time_toggle()}
        </div>
        <div class="metric-value" style="color: {fear_color}">{coin['fear_greed']}</div>
        <span style="color: {fear_color}; font-size: 0.8rem;">{fear_label}</span>
    """, unsafe_allow_html=True)
    fig = create_sparkline(generate_sparkline_data(30, "neutral", 0.03, coin['fear_greed']), color=fear_color, height=50, show_area=False)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown(f"""
        <div class="data-source">Alternative.me</div>
        <div class="metric-description">Market sentiment index (0-100). Extreme fear often = buying opportunity.</div>
    </div>
    """, unsafe_allow_html=True)

# Funding Rate
with sent_row1[3]:
    fund_color = "#22c55e" if coin['funding_rate'] > 0 else "#ef4444"
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-card-header">
            <span class="metric-label">Funding Rate</span>
            {render_time_toggle()}
        </div>
        <div class="metric-value">{coin['funding_rate']:.4f}%</div>
        <span style="color: #666; font-size: 0.8rem;">--</span>
    """, unsafe_allow_html=True)
    fig = create_sparkline(generate_sparkline_data(30, "neutral", 0.05, 0), color=fund_color, height=50, show_area=False)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown(f"""
        <div class="data-source">CryptoQuant</div>
        <div class="metric-description">Perpetual futures funding. Positive = longs pay shorts, market bullish.</div>
    </div>
    """, unsafe_allow_html=True)

sent_row2 = st.columns(3)

# Open Interest
with sent_row2[0]:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-card-header">
            <span class="metric-label">Open Interest</span>
            {render_time_toggle()}
        </div>
        <div class="metric-value">${coin['open_interest']:.2f}B</div>
        {render_change(coin['open_interest_change'])}
    """, unsafe_allow_html=True)
    trend = "up" if coin['open_interest_change'] > 0 else "down"
    fig = create_sparkline(generate_sparkline_data(30, trend, 0.02), color="#8b5cf6", height=50)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown(f"""
        <div class="data-source">CryptoQuant</div>
        <div class="metric-description">Total open derivative positions. Rising OI + price = strong trend.</div>
    </div>
    """, unsafe_allow_html=True)

# Exchange Reserve
with sent_row2[1]:
    unit = " " + coin_key
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-card-header">
            <span class="metric-label">Exchange {coin_key} Reserve</span>
            {render_time_toggle()}
        </div>
        <div class="metric-value">{coin['exchange_reserve']:.2f}M{unit}</div>
        {render_change(coin['exchange_reserve_change'])}
    """, unsafe_allow_html=True)
    trend = "down" if coin['exchange_reserve_change'] < 0 else "up"
    reserve_color = "#22c55e" if coin['exchange_reserve_change'] < 0 else "#ef4444"
    fig = create_sparkline(generate_sparkline_data(30, trend, 0.01), color=reserve_color, height=50)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown(f"""
        <div class="data-source">CryptoQuant</div>
        <div class="metric-description">{coin_key} on exchanges. Declining = accumulation, bullish signal.</div>
    </div>
    """, unsafe_allow_html=True)

# Whale Transactions
with sent_row2[2]:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-card-header">
            <span class="metric-label">Whale Transactions</span>
            {render_time_toggle()}
        </div>
        <div class="metric-value">{coin['whale_transactions']:.0f} txs</div>
        {render_change(coin['whale_tx_change'])}
    """, unsafe_allow_html=True)
    trend = "up" if coin['whale_tx_change'] > 0 else "down"
    fig = create_sparkline(generate_sparkline_data(30, trend, 0.04), color="#f97316", height=50, show_area=False)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown(f"""
        <div class="data-source">Dune</div>
        <div class="metric-description">Daily 1000+ {coin_key} transactions. Large player activity indicator.</div>
    </div>
    """, unsafe_allow_html=True)

# Sentiment Analysis Summary
sentiment_level = 2 if coin['fear_greed'] < 40 else 4 if coin['fear_greed'] > 60 else 3
st.markdown(f"""
<div class="analysis-section">
    <div style="display: flex; flex-wrap: wrap; gap: 1.5rem;">
        {render_analysis_section(
            "Current Status",
            "Cool" if coin['fear_greed'] < 50 else "Warm",
            sentiment_level,
            f"{coin['name']}'s current investor sentiment reveals cautious introspection. Market participants are navigating uncertainty with heightened apprehension."
        )}
        {render_analysis_section(
            "90-Day Trend",
            "Down" if coin['change_90d'] < 0 else "Up",
            2 if coin['change_90d'] < -20 else 3 if coin['change_90d'] < 10 else 4,
            f"The ecosystem is witnessing transformation in participant behavior. Fundamental shifts indicate potential recalibration of investment strategies."
        )}
        {render_analysis_section(
            "Valuation Insight",
            "Undervalued" if coin['mvrv_ratio'] < 1.5 else "Fair" if coin['mvrv_ratio'] < 2.5 else "Overheated",
            4 if coin['mvrv_ratio'] < 1.5 else 3 if coin['mvrv_ratio'] < 2.5 else 2,
            f"{coin['name']}'s ecosystem demonstrates resilience amidst market conditions. Technical fundamentals suggest potential growth."
        )}
    </div>
</div>
""", unsafe_allow_html=True)

# =============================================================================
# SECTION 02.2 - MARKET POSITION
# =============================================================================
st.markdown('<h2 class="section-title">02.2 — Market Position</h2>', unsafe_allow_html=True)

mkt_row1 = st.columns(4)

# BTC Ratio
with mkt_row1[0]:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-card-header">
            <span class="metric-label">{coin_key}/BTC Ratio</span>
            {render_time_toggle()}
        </div>
        <div class="metric-value">{coin['btc_ratio']:.5f}</div>
        {render_change(coin['btc_ratio_change'])}
    """, unsafe_allow_html=True)
    trend = "up" if coin['btc_ratio_change'] > 0 else "down"
    fig = create_sparkline(generate_sparkline_data(30, trend, 0.015), color="#f7931a", height=50)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown(f"""
        <div class="data-source">CoinGecko</div>
        <div class="metric-description">{coin_key} price relative to BTC. Rising ratio = {coin_key} strength vs Bitcoin.</div>
    </div>
    """, unsafe_allow_html=True)

# Dominance
with mkt_row1[1]:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-card-header">
            <span class="metric-label">{coin_key} Dominance</span>
            {render_time_toggle()}
        </div>
        <div class="metric-value">{coin['dominance']:.1f}%</div>
        {render_change(coin['dominance_change'])}
    """, unsafe_allow_html=True)
    trend = "up" if coin['dominance_change'] > 0 else "down"
    fig = create_sparkline(generate_sparkline_data(30, trend, 0.01), color="#8b5cf6", height=50)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown(f"""
        <div class="data-source">CoinGecko</div>
        <div class="metric-description">{coin_key}'s share of total crypto market cap. Higher = outperforming alts.</div>
    </div>
    """, unsafe_allow_html=True)

# Stablecoin Mcap
with mkt_row1[2]:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-card-header">
            <span class="metric-label">Stablecoin Mcap</span>
            {render_time_toggle()}
        </div>
        <div class="metric-value">${coin['stablecoin_mcap']:.1f}B</div>
        {render_change(coin['stablecoin_change'])}
    """, unsafe_allow_html=True)
    fig = create_sparkline(generate_sparkline_data(30, "up", 0.005), color="#22c55e", height=50)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown(f"""
        <div class="data-source">DefiLlama</div>
        <div class="metric-description">Total stablecoin market cap. Growth indicates capital inflow to crypto.</div>
    </div>
    """, unsafe_allow_html=True)

# Volatility
with mkt_row1[3]:
    vol_status = "Moderate" if 30 < coin['volatility'] < 60 else "High" if coin['volatility'] >= 60 else "Low"
    vol_color = "#eab308" if 30 < coin['volatility'] < 60 else "#ef4444" if coin['volatility'] >= 60 else "#22c55e"
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-card-header">
            <span class="metric-label">Volatility</span>
            {render_time_toggle()}
        </div>
        <div class="metric-value">{coin['volatility']:.1f}%</div>
        <span style="color: {vol_color}; font-size: 0.8rem;">{vol_status}</span>
    """, unsafe_allow_html=True)
    fig = create_sparkline(generate_sparkline_data(30, "neutral", 0.03), color=vol_color, height=50, show_area=False)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown(f"""
        <div class="data-source">CoinGecko</div>
        <div class="metric-description">30-day price volatility. Lower volatility often precedes big moves.</div>
    </div>
    """, unsafe_allow_html=True)

mkt_row2 = st.columns(4)

# NVT Ratio
with mkt_row2[0]:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-card-header">
            <span class="metric-label">NVT Ratio</span>
            {render_time_toggle()}
        </div>
        <div class="metric-value">{coin['nvt_ratio']:.1f}</div>
        {render_change(coin['nvt_change'])}
    """, unsafe_allow_html=True)
    trend = "up" if coin['nvt_change'] > 0 else "down"
    nvt_color = "#ef4444" if coin['nvt_ratio'] > 100 else "#22c55e" if coin['nvt_ratio'] < 50 else "#eab308"
    fig = create_sparkline(generate_sparkline_data(30, trend, 0.02), color=nvt_color, height=50)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown(f"""
        <div class="data-source">Calculated</div>
        <div class="metric-description">Market cap ÷ on-chain volume (7-day avg). Lower = undervalued.</div>
    </div>
    """, unsafe_allow_html=True)

# Market Position Analysis
mkt_level = 3 if coin['dominance_change'] > 0 else 2
st.markdown(f"""
<div class="analysis-section">
    <div style="display: flex; flex-wrap: wrap; gap: 1.5rem;">
        {render_analysis_section(
            "Current Status",
            "Cold" if coin['volatility'] > 50 else "Neutral",
            mkt_level,
            f"The {coin['name']} ecosystem reveals cautious market dynamics where investors are experiencing recalibration and strategic repositioning."
        )}
        {render_analysis_section(
            "90-Day Trend",
            "Weak" if coin['change_90d'] < 0 else "Strong",
            2 if coin['change_90d'] < 0 else 4,
            f"{coin['name']}'s market positioning reflects sophisticated interplay of technological and economic factors."
        )}
        {render_analysis_section(
            "Valuation Insight",
            "Bullish" if coin['nvt_ratio'] < 80 else "Cautious",
            4 if coin['nvt_ratio'] < 80 else 2,
            f"Advanced market analysis unveils technological potential and economic recalibration within the {coin['name']} ecosystem."
        )}
    </div>
</div>
""", unsafe_allow_html=True)

# =============================================================================
# SECTION 02.3 - SUPPLY DYNAMICS
# =============================================================================
st.markdown('<h2 class="section-title">02.3 — Supply Dynamics</h2>', unsafe_allow_html=True)

sup_row1 = st.columns(4)

# Staking Yield
with sup_row1[0]:
    if coin['staking_yield'] > 0:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-card-header">
                <span class="metric-label">Staking Yield (APR)</span>
                {render_time_toggle()}
            </div>
            <div class="metric-value">{coin['staking_yield']:.2f}%</div>
            {render_change(coin['staking_yield_change'], "pp 90D")}
        """, unsafe_allow_html=True)
        trend = "down" if coin['staking_yield_change'] < 0 else "up"
        fig = create_sparkline(generate_sparkline_data(30, trend, 0.01, coin['staking_yield']), color="#22c55e", height=50)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        source = "Lido" if coin_key == "ETH" else "Marinade" if coin_key == "SOL" else "Protocol"
        st.markdown(f"""
            <div class="data-source">{source}</div>
            <div class="metric-description">Annual L1 staking return. Benchmark yield for {coin_key} investment.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Staking Yield (APR)</div>
            <div class="metric-value" style="color: #666;">N/A</div>
            <div class="metric-description" style="margin-top: 80px;">{coin_key} does not support native staking.</div>
        </div>
        """, unsafe_allow_html=True)

# Staked Amount
with sup_row1[1]:
    if coin['staked_amount'] > 0:
        unit = " " + coin_key
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-card-header">
                <span class="metric-label">Staked {coin_key}</span>
                {render_time_toggle()}
            </div>
            <div class="metric-value">{coin['staked_amount']:.2f}M{unit}</div>
            {render_change(coin['staked_change'])}
        """, unsafe_allow_html=True)
        fig = create_sparkline(generate_sparkline_data(30, "up", 0.008), color="#8b5cf6", height=50)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.markdown(f"""
            <div class="data-source">Dune</div>
            <div class="metric-description">{coin_key} locked in staking. Higher = more network security.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Staked {coin_key}</div>
            <div class="metric-value" style="color: #666;">N/A</div>
            <div class="metric-description" style="margin-top: 80px;">{coin_key} uses Proof of Work.</div>
        </div>
        """, unsafe_allow_html=True)

# Burned
with sup_row1[2]:
    if coin_key == "ETH" and coin['burned'] > 0:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-card-header">
                <span class="metric-label">ETH Burned</span>
                {render_time_toggle()}
            </div>
            <div class="metric-value" style="color: #ef4444;">{coin['burned']:.1f} ETH</div>
            {render_change(coin['burned_change'])}
        """, unsafe_allow_html=True)
        fig = create_sparkline(generate_sparkline_data(30, "down", 0.03), color="#ef4444", height=50)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.markdown(f"""
            <div class="data-source">Dune</div>
            <div class="metric-description">ETH burned via EIP-1559 on L1. Higher burn = more mainnet activity.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{coin_key} Burned</div>
            <div class="metric-value" style="color: #666;">N/A</div>
            <div class="metric-description" style="margin-top: 80px;">{coin_key} does not have burn mechanism.</div>
        </div>
        """, unsafe_allow_html=True)

# Issued
with sup_row1[3]:
    if coin_key == "ETH":
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-card-header">
                <span class="metric-label">ETH Issued</span>
                {render_time_toggle()}
            </div>
            <div class="metric-value" style="color: #22c55e;">{coin['issued']:,.0f} ETH</div>
            {render_change(coin['issued_change'])}
        """, unsafe_allow_html=True)
        fig = create_sparkline(generate_sparkline_data(30, "neutral", 0.01), color="#22c55e", height=50, show_area=False)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.markdown(f"""
            <div class="data-source">Beaconcha.in</div>
            <div class="metric-description">New ETH issued to L1 validators. ~930 ETH/day post-merge.</div>
        </div>
        """, unsafe_allow_html=True)
    elif coin['issued'] > 0:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{coin_key} Issued</div>
            <div class="metric-value">{coin['issued']:.0f}/day</div>
            <div class="metric-description" style="margin-top: 80px;">New {coin_key} issued daily via mining.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{coin_key} Issued</div>
            <div class="metric-value" style="color: #666;">N/A</div>
            <div class="metric-description" style="margin-top: 80px;">Issuance data not available.</div>
        </div>
        """, unsafe_allow_html=True)

sup_row2 = st.columns(2)

# Net Supply
with sup_row2[0]:
    net_supply_status = "Inflationary" if coin['net_supply'] > 0 else "Deflationary"
    supply_color = "#ef4444" if coin['net_supply'] > 0 else "#22c55e"
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-card-header">
            <span class="metric-label">Net Supply</span>
            {render_time_toggle()}
        </div>
        <div class="metric-value">{'+' if coin['net_supply'] > 0 else ''}{coin['net_supply']:.2f}%/yr</div>
        <span style="color: {supply_color}; font-size: 0.8rem;">{net_supply_status}</span>
    """, unsafe_allow_html=True)
    fig = create_sparkline(generate_sparkline_data(30, "neutral", 0.02), color=supply_color, height=50, show_area=False)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown(f"""
        <div class="data-source">Calculated</div>
        <div class="metric-description">L1 burn minus issuance. Negative = deflationary, bullish for {coin_key} value.</div>
    </div>
    """, unsafe_allow_html=True)

# Effective Float
with sup_row2[1]:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-card-header">
            <span class="metric-label">Effective Float</span>
            {render_time_toggle()}
        </div>
        <div class="metric-value">{coin['effective_float']:.1f}%</div>
        {render_change(coin['effective_float_change'], "pp 90D")}
    """, unsafe_allow_html=True)
    # Stacked bar visualization
    st.markdown(f"""
    <div style="display: flex; height: 20px; border-radius: 4px; overflow: hidden; margin: 10px 0;">
        <div style="background: #8b5cf6; width: {coin['effective_float']}%;" title="Float"></div>
        <div style="background: #22c55e; width: {(100 - coin['effective_float']) * 0.6}%;" title="Staking"></div>
        <div style="background: #3b82f6; width: {(100 - coin['effective_float']) * 0.3}%;" title="DeFi"></div>
        <div style="background: #666; width: {(100 - coin['effective_float']) * 0.1}%;" title="Others"></div>
    </div>
    <div style="display: flex; gap: 12px; font-size: 0.65rem; color: #888; margin-bottom: 8px;">
        <span>● Float</span><span style="color: #22c55e;">● Staking</span><span style="color: #3b82f6;">● DeFi</span><span style="color: #666;">● Others</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f"""
        <div class="data-source">DefiLlama</div>
        <div class="metric-description">Liquid {coin_key} available for trading. Others = L2 bridges, lost coins.</div>
    </div>
    """, unsafe_allow_html=True)

# Supply Dynamics Analysis
supply_level = 4 if coin['net_supply'] < 0 else 2 if coin['net_supply'] > 3 else 3
st.markdown(f"""
<div class="analysis-section">
    <div style="display: flex; flex-wrap: wrap; gap: 1.5rem;">
        {render_analysis_section(
            "Current Status",
            "Cool" if coin['staking_yield'] < 5 else "Warm",
            supply_level,
            f"{coin['name']}'s supply landscape reveals subtle yet significant shifts in network economics. Staking participation demonstrates cautious expansion."
        )}
        {render_analysis_section(
            "90-Day Trend",
            "Weak" if coin['burned_change'] < -50 else "Stable",
            2 if coin['burned_change'] < -50 else 3,
            f"Deflationary pressures are experiencing recalibration within {coin['name']}'s tokenomic framework. Network burn mechanisms have contracted."
        )}
        {render_analysis_section(
            "Valuation Insight",
            "Slightly Bullish" if coin['net_supply'] < 2 else "Neutral",
            4 if coin['net_supply'] < 2 else 3,
            f"{coin['name']}'s supply dynamics represent sophisticated intersection between technological innovation and economic engineering."
        )}
    </div>
</div>
""", unsafe_allow_html=True)

# =============================================================================
# SECTION 02.4 - NETWORK DEMAND
# =============================================================================
st.markdown('<h2 class="section-title">02.4 — Network Demand</h2>', unsafe_allow_html=True)

net_row1 = st.columns(4)

# Gas Price
with net_row1[0]:
    if coin_key == "ETH":
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-card-header">
                <span class="metric-label">Gas Price</span>
                {render_time_toggle()}
            </div>
            <div class="metric-value">{coin['gas_price']:.1f} Gwei</div>
            {render_change(coin['gas_price_change'])}
        """, unsafe_allow_html=True)
        fig = create_sparkline(generate_sparkline_data(30, "down", 0.04), color="#8b5cf6", height=50, show_area=False)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.markdown(f"""
            <div class="data-source">Dune</div>
            <div class="metric-description">Average L1 gas price in Gwei. Reflects mainnet transaction costs.</div>
        </div>
        """, unsafe_allow_html=True)
    elif coin['gas_price'] > 0:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-card-header">
                <span class="metric-label">Avg Fee</span>
                {render_time_toggle()}
            </div>
            <div class="metric-value">${coin['gas_price']:.5f}</div>
            {render_change(coin['gas_price_change'])}
        """, unsafe_allow_html=True)
        fig = create_sparkline(generate_sparkline_data(30, "neutral", 0.02), color="#8b5cf6", height=50)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.markdown(f"""
            <div class="data-source">Explorer</div>
            <div class="metric-description">Average transaction fee on {coin_key} network.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Gas/Fee</div>
            <div class="metric-value" style="color: #666;">N/A</div>
            <div class="metric-description" style="margin-top: 80px;">Fee data not available for {coin_key}.</div>
        </div>
        """, unsafe_allow_html=True)

# Gas Utilization
with net_row1[1]:
    if coin['gas_utilization'] > 0:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-card-header">
                <span class="metric-label">Gas Utilization</span>
                {render_time_toggle()}
            </div>
            <div class="metric-value">{coin['gas_utilization']:.1f}%</div>
            {render_change(coin['gas_util_change'])}
        """, unsafe_allow_html=True)
        fig = create_sparkline(generate_sparkline_data(30, "neutral", 0.01, coin['gas_utilization']), color="#22c55e", height=50)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.markdown(f"""
            <div class="data-source">Dune</div>
            <div class="metric-description">% of L1 block gas limit used. High utilization = strong network demand.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Block Utilization</div>
            <div class="metric-value" style="color: #666;">N/A</div>
            <div class="metric-description" style="margin-top: 80px;">Block utilization metric not applicable for {coin_key}.</div>
        </div>
        """, unsafe_allow_html=True)

# Network Fees
with net_row1[2]:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-card-header">
            <span class="metric-label">Network Fees</span>
            {render_time_toggle()}
        </div>
        <div class="metric-value">${coin['network_fees']:.1f}K</div>
        {render_change(coin['network_fees_change'])}
    """, unsafe_allow_html=True)
    trend = "up" if coin['network_fees_change'] > 0 else "down"
    fig = create_sparkline(generate_sparkline_data(30, trend, 0.03), color="#f97316", height=50)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown(f"""
        <div class="data-source">DefiLlama</div>
        <div class="metric-description">Total fees paid to L1 network. Revenue proxy for {coin['name']} mainnet.</div>
    </div>
    """, unsafe_allow_html=True)

# Blob Fees (ETH only)
with net_row1[3]:
    if coin_key == "ETH":
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-card-header">
                <span class="metric-label">Blob Fees</span>
                <div class="time-toggle">
                    <span class="time-btn time-btn-active">90D</span>
                    <span class="time-btn">1Y</span>
                    <span class="time-btn">All</span>
                </div>
            </div>
            <div class="metric-value">${coin['blob_fees']:.1f}M</div>
            {render_change(coin['blob_fees_change'])}
        """, unsafe_allow_html=True)
        fig = create_sparkline(generate_sparkline_data(30, "up", 0.05), color="#3b82f6", height=50)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.markdown(f"""
            <div class="data-source">Etherscan</div>
            <div class="metric-description">L2 data posting fees since Dencun upgrade (Mar 2024). Blob fees are burned.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">L2 Fees</div>
            <div class="metric-value" style="color: #666;">N/A</div>
            <div class="metric-description" style="margin-top: 80px;">{coin_key} doesn't have blob-style L2 fees.</div>
        </div>
        """, unsafe_allow_html=True)

net_row2 = st.columns(2)

# Blob Count / Daily Txs
with net_row2[0]:
    if coin_key == "ETH":
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-card-header">
                <span class="metric-label">Blob Count</span>
                <div class="time-toggle">
                    <span class="time-btn time-btn-active">90D</span>
                    <span class="time-btn">1Y</span>
                    <span class="time-btn">All</span>
                </div>
            </div>
            <div class="metric-value">{coin['blob_count']:.1f}K</div>
            {render_change(coin['blob_count_change'])}
        """, unsafe_allow_html=True)
        fig = create_sparkline(generate_sparkline_data(30, "neutral", 0.02), color="#8b5cf6", height=50, show_area=False)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.markdown(f"""
            <div class="data-source">Etherscan</div>
            <div class="metric-description">Data blobs posted by L2s since Dencun (Mar 2024). More blobs = growing L2 adoption.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        daily_tx = random.randint(5, 50)
        tx_change = random.uniform(-20, 40)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-card-header">
                <span class="metric-label">Daily Transactions</span>
                {render_time_toggle()}
            </div>
            <div class="metric-value">{daily_tx}M</div>
            {render_change(tx_change)}
        """, unsafe_allow_html=True)
        fig = create_sparkline(generate_sparkline_data(30, "up", 0.02), color="#22c55e", height=50)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.markdown(f"""
            <div class="data-source">Explorer</div>
            <div class="metric-description">Total daily transactions on {coin_key} network.</div>
        </div>
        """, unsafe_allow_html=True)

# DeFi Revenue
with net_row2[1]:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-card-header">
            <span class="metric-label">DeFi Protocol Revenue</span>
            {render_time_toggle()}
        </div>
        <div class="metric-value">${coin['defi_revenue']:.1f}M</div>
        <span class="badge-est">Est.</span>
        {render_change(coin['defi_revenue_change'])}
    """, unsafe_allow_html=True)
    trend = "up" if coin['defi_revenue_change'] > 0 else "down"
    fig = create_sparkline(generate_sparkline_data(30, trend, 0.03), color="#a855f7", height=50)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown(f"""
        <div class="data-source">DefiLlama</div>
        <div class="metric-description">Daily fee revenue from DeFi protocols (Uniswap, Aave, Lido, etc). Shows ecosystem activity.</div>
    </div>
    """, unsafe_allow_html=True)

# Network Demand Analysis
demand_level = 4 if coin['defi_revenue_change'] > 50 else 2 if coin['network_fees_change'] < -50 else 3
st.markdown(f"""
<div class="analysis-section">
    <div style="display: flex; flex-wrap: wrap; gap: 1.5rem;">
        {render_analysis_section(
            "Current Status",
            "Cold" if coin['gas_price'] < 5 else "Hot",
            demand_level,
            f"{coin['name']}'s network demand presents transformation and strategic recalibration. The ecosystem is experiencing compression of transactional costs."
        )}
        {render_analysis_section(
            "90-Day Trend",
            "Weak" if coin['network_fees_change'] < 0 else "Strong",
            2 if coin['network_fees_change'] < 0 else 4,
            f"The network's utilization metrics reveal intriguing patterns of resilience. Gas utilization remains stable despite price compressions."
        )}
        {render_analysis_section(
            "Valuation Insight",
            "Bullish" if coin['defi_revenue_change'] > 20 else "Neutral",
            4 if coin['defi_revenue_change'] > 20 else 3,
            f"{coin['name']}'s ecosystem is navigating complex transition with significant metric volatilities and structural recalibrations."
        )}
    </div>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="display: flex; justify-content: space-between; align-items: center; color: #666; font-size: 0.75rem;">
    <span>Data updates periodically. Not financial advice.</span>
    <span>Sources: CoinGecko, Dune, DefiLlama, CryptoQuant, Alternative.me, Etherscan</span>
</div>
""", unsafe_allow_html=True)
