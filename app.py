import streamlit as st

# Page config
st.set_page_config(
    page_title="Coin Evaluation",
    page_icon="📊",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
    .stApp {
        background-color: #0d1117;
    }

    .main-title {
        text-align: center;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }

    .subtitle {
        text-align: center;
        color: #8b949e;
        margin-bottom: 2rem;
    }

    .coin-card {
        background: #161b22;
        border-radius: 20px;
        padding: 2rem;
        border: 1px solid #30363d;
        margin: 1rem 0;
    }

    .price-display {
        font-size: 2.5rem;
        font-weight: bold;
        color: #f0f6fc;
    }

    .change-positive {
        color: #3fb950;
        background: rgba(63, 185, 80, 0.15);
        padding: 0.25rem 0.75rem;
        border-radius: 6px;
        font-weight: 500;
    }

    .change-negative {
        color: #f85149;
        background: rgba(248, 81, 73, 0.15);
        padding: 0.25rem 0.75rem;
        border-radius: 6px;
        font-weight: 500;
    }

    .stat-label {
        color: #8b949e;
        font-size: 0.875rem;
    }

    .stat-value {
        color: #f0f6fc;
        font-size: 1.1rem;
        font-weight: 600;
    }

    .description-text {
        color: #8b949e;
        line-height: 1.7;
    }

    div[data-testid="stHorizontalBlock"] {
        gap: 0.5rem;
    }

    .stButton > button {
        border-radius: 10px;
        padding: 0.75rem 1.25rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
</style>
""", unsafe_allow_html=True)

# Coin data
COINS = {
    "BTC": {
        "name": "Bitcoin",
        "icon": "₿",
        "price": 97245.00,
        "change": 2.45,
        "market_cap": "$1.92T",
        "volume": "$28.5B",
        "supply": "19.8M BTC",
        "ath": "$108,135",
        "description": "Bitcoin is a decentralized digital currency that enables peer-to-peer transactions without intermediaries. Created in 2009 by Satoshi Nakamoto, it uses blockchain technology to maintain a secure and transparent ledger."
    },
    "HYPE": {
        "name": "Hyperliquid",
        "icon": "⬡",
        "price": 23.45,
        "change": 8.72,
        "market_cap": "$7.8B",
        "volume": "$542M",
        "supply": "333M HYPE",
        "ath": "$35.20",
        "description": "Hyperliquid is a high-performance Layer 1 blockchain optimized for decentralized perpetual trading. It features a fully on-chain order book with sub-second finality."
    },
    "LIT": {
        "name": "Litentry",
        "icon": "◈",
        "price": 1.24,
        "change": -3.21,
        "market_cap": "$124M",
        "volume": "$18.2M",
        "supply": "100M LIT",
        "ath": "$12.45",
        "description": "Litentry is a decentralized identity aggregator that enables users to manage their identities across multiple networks. It provides privacy-preserving identity verification."
    },
    "SOL": {
        "name": "Solana",
        "icon": "◎",
        "price": 187.32,
        "change": 4.15,
        "market_cap": "$91.2B",
        "volume": "$3.8B",
        "supply": "486M SOL",
        "ath": "$263.83",
        "description": "Solana is a high-performance blockchain supporting builders creating crypto apps that scale. Known for its speed and low transaction costs using Proof of History consensus."
    },
    "XPL": {
        "name": "Explora",
        "icon": "✦",
        "price": 0.0842,
        "change": 15.67,
        "market_cap": "$42M",
        "volume": "$8.5M",
        "supply": "500M XPL",
        "ath": "$0.15",
        "description": "Explora is an emerging cryptocurrency focused on cross-chain interoperability and decentralized data sharing solutions."
    }
}

def format_price(price):
    if price >= 1000:
        return f"${price:,.2f}"
    elif price >= 1:
        return f"${price:.2f}"
    else:
        return f"${price:.4f}"

# Header
st.markdown('<h1 class="main-title">Coin Evaluation</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Track and evaluate your favorite cryptocurrencies</p>', unsafe_allow_html=True)

# Coin selector
coin_options = list(COINS.keys())

# Initialize session state
if 'selected_coin' not in st.session_state:
    st.session_state.selected_coin = "BTC"

# Create coin selector tabs
cols = st.columns(len(coin_options))
for i, coin in enumerate(coin_options):
    with cols[i]:
        btn_type = "primary" if st.session_state.selected_coin == coin else "secondary"
        if st.button(f"{COINS[coin]['icon']} {coin}", key=f"btn_{coin}", type=btn_type, use_container_width=True):
            st.session_state.selected_coin = coin
            st.rerun()

# Get selected coin data
coin = COINS[st.session_state.selected_coin]

st.markdown("---")

# Coin header
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown(f"### {coin['icon']} {coin['name']}")
    st.caption(st.session_state.selected_coin)

with col2:
    st.markdown(f'<p class="price-display">{format_price(coin["price"])}</p>', unsafe_allow_html=True)
    change_class = "change-positive" if coin["change"] >= 0 else "change-negative"
    change_sign = "+" if coin["change"] >= 0 else ""
    st.markdown(f'<span class="{change_class}">{change_sign}{coin["change"]:.2f}%</span>', unsafe_allow_html=True)

st.markdown("---")

# Stats grid
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<p class="stat-label">Market Cap</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="stat-value">{coin["market_cap"]}</p>', unsafe_allow_html=True)

with col2:
    st.markdown('<p class="stat-label">24h Volume</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="stat-value">{coin["volume"]}</p>', unsafe_allow_html=True)

with col3:
    st.markdown('<p class="stat-label">Circulating Supply</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="stat-value">{coin["supply"]}</p>', unsafe_allow_html=True)

with col4:
    st.markdown('<p class="stat-label">All Time High</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="stat-value">{coin["ath"]}</p>', unsafe_allow_html=True)

st.markdown("---")

# Description
st.markdown("#### About")
st.markdown(f'<p class="description-text">{coin["description"]}</p>', unsafe_allow_html=True)

st.markdown("---")

# Action buttons
col1, col2, col3 = st.columns(3)
with col1:
    st.button(f"Buy {st.session_state.selected_coin}", type="primary", use_container_width=True)
with col2:
    st.button("View Chart", use_container_width=True)
with col3:
    st.button("Set Alert", use_container_width=True)

# Footer
st.markdown("---")
st.caption("Data updates in real-time. Not financial advice.")
