// Coin data with valuation metrics
const coinData = {
    BTC: {
        name: 'Bitcoin',
        symbol: 'BTC',
        icon: '₿',
        price: 97245.00,
        change: 2.45,
        marketCap: '$1.92T',
        volume: '$28.5B',
        supply: '19.8M BTC',
        ath: '$108,135',
        description: 'Bitcoin is a decentralized digital currency that enables peer-to-peer transactions without intermediaries. Created in 2009 by Satoshi Nakamoto, it uses blockchain technology to maintain a secure and transparent ledger. As the first cryptocurrency, it pioneered the concept of digital scarcity.'
    },
    HYPE: {
        name: 'Hyperliquid',
        symbol: 'HYPE',
        icon: '⬡',
        price: 23.45,
        change: 8.72,
        marketCap: '$7.8B',
        volume: '$542M',
        supply: '333M HYPE',
        ath: '$35.20',
        description: 'Hyperliquid is a high-performance Layer 1 blockchain optimized for decentralized perpetual trading. It features a fully on-chain order book with sub-second finality, offering institutional-grade trading infrastructure in a decentralized environment.'
    },
    LIT: {
        name: 'Litentry',
        symbol: 'LIT',
        icon: '◈',
        price: 1.24,
        change: -3.21,
        marketCap: '$124M',
        volume: '$18.2M',
        supply: '100M LIT',
        ath: '$12.45',
        description: 'Litentry is a decentralized identity aggregator that enables users to manage their identities across multiple networks. It provides privacy-preserving identity verification and reputation systems for Web3 applications.'
    },
    SOL: {
        name: 'Solana',
        symbol: 'SOL',
        icon: '◎',
        price: 187.32,
        change: 4.15,
        marketCap: '$91.2B',
        volume: '$3.8B',
        supply: '486M SOL',
        ath: '$263.83',
        description: 'Solana is a high-performance blockchain supporting builders around the world creating crypto apps that scale. Known for its speed and low transaction costs, Solana uses a unique Proof of History consensus combined with Proof of Stake.'
    },
    XPL: {
        name: 'Explora',
        symbol: 'XPL',
        icon: '✦',
        price: 0.0842,
        change: 15.67,
        marketCap: '$42M',
        volume: '$8.5M',
        supply: '500M XPL',
        ath: '$0.15',
        description: 'Explora is an emerging cryptocurrency focused on exploration and discovery in the decentralized space. It aims to provide innovative solutions for cross-chain interoperability and decentralized data sharing.'
    }
};

// DOM Elements
const coinTabs = document.querySelectorAll('.coin-tab');
const selectedCoinIcon = document.getElementById('selected-coin-icon');
const selectedCoinName = document.getElementById('selected-coin-name');
const selectedCoinSymbol = document.getElementById('selected-coin-symbol');
const coinPrice = document.getElementById('coin-price');
const coinChange = document.getElementById('coin-change');
const marketCap = document.getElementById('market-cap');
const volume = document.getElementById('volume');
const supply = document.getElementById('supply');
const ath = document.getElementById('ath');
const coinDescription = document.getElementById('coin-description');
const actionCoin = document.getElementById('action-coin');

// Format price with commas and decimals
function formatPrice(price) {
    if (price >= 1000) {
        return '$' + price.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    } else if (price >= 1) {
        return '$' + price.toFixed(2);
    } else {
        return '$' + price.toFixed(4);
    }
}

// Update display with selected coin data
function updateCoinDisplay(coinSymbol) {
    const coin = coinData[coinSymbol];
    if (!coin) return;

    // Update icon and basic info
    selectedCoinIcon.textContent = coin.icon;
    selectedCoinName.textContent = coin.name;
    selectedCoinSymbol.textContent = coin.symbol;

    // Update price with animation
    coinPrice.style.opacity = '0';
    setTimeout(() => {
        coinPrice.textContent = formatPrice(coin.price);
        coinPrice.style.opacity = '1';
    }, 150);

    // Update change percentage
    const changeValue = coin.change;
    const isPositive = changeValue >= 0;
    coinChange.textContent = (isPositive ? '+' : '') + changeValue.toFixed(2) + '%';
    coinChange.className = 'change ' + (isPositive ? 'positive' : 'negative');

    // Update stats
    marketCap.textContent = coin.marketCap;
    volume.textContent = coin.volume;
    supply.textContent = coin.supply;
    ath.textContent = coin.ath;

    // Update description
    coinDescription.textContent = coin.description;

    // Update action button
    actionCoin.textContent = coin.symbol;
}

// Handle tab click
function handleTabClick(event) {
    const clickedTab = event.currentTarget;
    const coinSymbol = clickedTab.dataset.coin;

    // Update active tab
    coinTabs.forEach(tab => tab.classList.remove('active'));
    clickedTab.classList.add('active');

    // Update display
    updateCoinDisplay(coinSymbol);

    // Save selection to localStorage
    localStorage.setItem('selectedCoin', coinSymbol);
}

// Add click listeners to all tabs
coinTabs.forEach(tab => {
    tab.addEventListener('click', handleTabClick);
});

// Add keyboard navigation
document.addEventListener('keydown', (e) => {
    const coins = Object.keys(coinData);
    const activeTab = document.querySelector('.coin-tab.active');
    const currentIndex = coins.indexOf(activeTab.dataset.coin);

    let newIndex = currentIndex;

    if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
        newIndex = (currentIndex + 1) % coins.length;
    } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
        newIndex = (currentIndex - 1 + coins.length) % coins.length;
    } else if (e.key >= '1' && e.key <= '5') {
        newIndex = parseInt(e.key) - 1;
    }

    if (newIndex !== currentIndex) {
        const newCoin = coins[newIndex];
        const newTab = document.querySelector(`[data-coin="${newCoin}"]`);
        if (newTab) {
            newTab.click();
        }
    }
});

// Initialize with saved coin or default to BTC
document.addEventListener('DOMContentLoaded', () => {
    const savedCoin = localStorage.getItem('selectedCoin') || 'BTC';
    const savedTab = document.querySelector(`[data-coin="${savedCoin}"]`);

    if (savedTab) {
        coinTabs.forEach(tab => tab.classList.remove('active'));
        savedTab.classList.add('active');
        updateCoinDisplay(savedCoin);
    }

    // Add smooth transition to price
    coinPrice.style.transition = 'opacity 0.15s ease';
});

// Simulate price updates (demo feature)
function simulatePriceUpdate() {
    Object.keys(coinData).forEach(symbol => {
        const coin = coinData[symbol];
        const changePercent = (Math.random() - 0.5) * 0.5; // -0.25% to +0.25%
        coin.price *= (1 + changePercent / 100);
        coin.change += changePercent * 0.1;
    });

    // Update current display
    const activeTab = document.querySelector('.coin-tab.active');
    if (activeTab) {
        updateCoinDisplay(activeTab.dataset.coin);
    }
}

// Update prices every 10 seconds (demo)
setInterval(simulatePriceUpdate, 10000);
