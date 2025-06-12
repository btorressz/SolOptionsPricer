import streamlit as st
import requests
import numpy as np
import pandas as pd
from scipy.stats import norm
import time
import math
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="SOL Options Pricing Engine",
    page_icon="📊",
    layout="wide"
)

# API configurations
JUPITER_API_BASE = "https://price.jup.ag/v4"
SOL_MINT = "So11111111111111111111111111111111111111112"

# Alternative price sources
COINGECKO_API = "https://api.coingecko.com/api/v3/simple/price"
BINANCE_API = "https://api.binance.com/api/v3/ticker/price"
KRAKEN_API = "https://api.kraken.com/0/public/Ticker"

class BlackScholes:
    """Black-Scholes option pricing model implementation"""
    
    @staticmethod
    def d1(S, K, T, r, sigma):
        """Calculate d1 parameter"""
        if T <= 0:
            return 0
        return (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    
    @staticmethod
    def d2(S, K, T, r, sigma):
        """Calculate d2 parameter"""
        if T <= 0:
            return 0
        return BlackScholes.d1(S, K, T, r, sigma) - sigma * np.sqrt(T)
    
    @staticmethod
    def call_price(S, K, T, r, sigma):
        """Calculate call option price"""
        if T <= 0:
            return max(S - K, 0)
        
        d1 = BlackScholes.d1(S, K, T, r, sigma)
        d2 = BlackScholes.d2(S, K, T, r, sigma)
        
        call = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
        return max(call, 0)
    
    @staticmethod
    def put_price(S, K, T, r, sigma):
        """Calculate put option price"""
        if T <= 0:
            return max(K - S, 0)
        
        d1 = BlackScholes.d1(S, K, T, r, sigma)
        d2 = BlackScholes.d2(S, K, T, r, sigma)
        
        put = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
        return max(put, 0)
    
    @staticmethod
    def delta_call(S, K, T, r, sigma):
        """Calculate call delta"""
        if T <= 0:
            return 1.0 if S > K else 0.0
        d1 = BlackScholes.d1(S, K, T, r, sigma)
        return norm.cdf(d1)
    
    @staticmethod
    def delta_put(S, K, T, r, sigma):
        """Calculate put delta"""
        if T <= 0:
            return -1.0 if S < K else 0.0
        d1 = BlackScholes.d1(S, K, T, r, sigma)
        return norm.cdf(d1) - 1
    
    @staticmethod
    def gamma(S, K, T, r, sigma):
        """Calculate gamma (same for calls and puts)"""
        if T <= 0:
            return 0
        d1 = BlackScholes.d1(S, K, T, r, sigma)
        return norm.pdf(d1) / (S * sigma * np.sqrt(T))
    
    @staticmethod
    def theta_call(S, K, T, r, sigma):
        """Calculate call theta"""
        if T <= 0:
            return 0
        d1 = BlackScholes.d1(S, K, T, r, sigma)
        d2 = BlackScholes.d2(S, K, T, r, sigma)
        
        theta = (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) 
                - r * K * np.exp(-r * T) * norm.cdf(d2))
        return theta / 365  # Convert to daily theta
    
    @staticmethod
    def theta_put(S, K, T, r, sigma):
        """Calculate put theta"""
        if T <= 0:
            return 0
        d1 = BlackScholes.d1(S, K, T, r, sigma)
        d2 = BlackScholes.d2(S, K, T, r, sigma)
        
        theta = (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) 
                + r * K * np.exp(-r * T) * norm.cdf(-d2))
        return theta / 365  # Convert to daily theta
    
    @staticmethod
    def vega(S, K, T, r, sigma):
        """Calculate vega (same for calls and puts)"""
        if T <= 0:
            return 0
        d1 = BlackScholes.d1(S, K, T, r, sigma)
        return S * norm.pdf(d1) * np.sqrt(T) / 100  # Convert to percentage point

def fetch_sol_price_jupiter():
    """Fetch SOL price from Jupiter API"""
    try:
        url = f"{JUPITER_API_BASE}/price?ids={SOL_MINT}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        if 'data' in data and SOL_MINT in data['data']:
            price = float(data['data'][SOL_MINT]['price'])
            return price, None
        else:
            return None, "Invalid response format from Jupiter API"
            
    except Exception as e:
        return None, f"Jupiter API error: {str(e)}"

def fetch_sol_price_coingecko():
    """Fetch SOL price from CoinGecko API"""
    try:
        url = f"{COINGECKO_API}?ids=solana&vs_currencies=usd"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        if 'solana' in data and 'usd' in data['solana']:
            price = float(data['solana']['usd'])
            return price, None
        else:
            return None, "Invalid response format from CoinGecko API"
            
    except Exception as e:
        return None, f"CoinGecko API error: {str(e)}"

def fetch_sol_price_binance():
    """Fetch SOL price from Binance API"""
    try:
        url = f"{BINANCE_API}?symbol=SOLUSDT"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        if 'price' in data:
            price = float(data['price'])
            return price, None
        else:
            return None, "Invalid response format from Binance API"
            
    except Exception as e:
        return None, f"Binance API error: {str(e)}"

def fetch_sol_price_kraken():
    """Fetch SOL price from Kraken API"""
    try:
        url = f"{KRAKEN_API}?pair=SOLUSD"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        if 'error' in data and len(data['error']) == 0 and 'result' in data:
            if 'SOLUSD' in data['result']:
                # Kraken returns current price in the 'c' field [price, volume]
                price = float(data['result']['SOLUSD']['c'][0])
                return price, None
        
        return None, "Invalid response format from Kraken API"
            
    except Exception as e:
        return None, f"Kraken API error: {str(e)}"

def fetch_sol_price():
    """Fetch current SOL price with fallback sources"""
    # Try Jupiter first (most accurate for Solana/DeFi ecosystem)
    price, error = fetch_sol_price_jupiter()
    if price is not None:
        return price, None, "Jupiter"
    
    # Fallback to Kraken (reliable traditional exchange)
    price, error = fetch_sol_price_kraken()
    if price is not None:
        return price, None, "Kraken"
    
    # Fallback to CoinGecko
    price, error = fetch_sol_price_coingecko()
    if price is not None:
        return price, None, "CoinGecko"
    
    # Final fallback to Binance
    price, error = fetch_sol_price_binance()
    if price is not None:
        return price, None, "Binance"
    
    # All sources failed
    return None, "All price sources unavailable. Please check your internet connection.", None

def calculate_time_to_expiry(expiry_date):
    """Calculate time to expiry in years"""
    now = datetime.now()
    if expiry_date <= now.date():
        return 0
    
    time_diff = datetime.combine(expiry_date, datetime.min.time()) - now
    return time_diff.total_seconds() / (365.25 * 24 * 3600)

def apply_custom_css():
    """Apply light theme styling with blue interactive elements"""
    st.markdown("""
    <style>
    /* Force light background */
    .stApp {
        background-color: #ffffff;
        color: #000000;
    }
    
    /* Ensure sidebar is light */
    .css-1d391kg {
        background-color: #f8f9fa;
    }
    
    /* Remove custom slider styling to use defaults */
    
    /* Style other interactive elements in blue */
    .stButton > button {
        background-color: #1f77b4;
        color: white;
        border: none;
        border-radius: 4px;
    }
    
    .stButton > button:hover {
        background-color: #1565c0;
    }
    
    /* Input field styling */
    .stNumberInput > div > div > input {
        border: 1px solid #1f77b4;
    }
    
    .stSelectbox > div > div {
        border: 1px solid #1f77b4;
    }
    
    /* Date input styling */
    .stDateInput > div > div > input {
        border: 1px solid #1f77b4;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    apply_custom_css()
    
    st.title("📊 SOL Options Pricing Engine")
    st.markdown("Real-time Solana options pricing using Black-Scholes model with live price feeds")
    
    # Initialize session state for auto-refresh
    if 'last_refresh' not in st.session_state:
        st.session_state.last_refresh = 0
    if 'auto_refresh' not in st.session_state:
        st.session_state.auto_refresh = True
    
    # Sidebar for controls
    st.sidebar.header("Option Parameters")
    
    # Auto-refresh toggle
    auto_refresh = st.sidebar.checkbox("Auto-refresh price", value=st.session_state.auto_refresh)
    st.session_state.auto_refresh = auto_refresh
    
    # Manual refresh button
    if st.sidebar.button("🔄 Refresh Price Now"):
        st.session_state.last_refresh = 0
    
    # Fetch SOL price
    current_time = time.time()
    if (auto_refresh and current_time - st.session_state.last_refresh > 30) or st.session_state.last_refresh == 0:
        with st.spinner("Fetching SOL price..."):
            sol_price, error, source = fetch_sol_price()
            st.session_state.last_refresh = current_time
            
            if error:
                st.error(f"Failed to fetch SOL price: {error}")
                st.info("Please check your internet connection or try again later.")
                return
            else:
                st.session_state.sol_price = sol_price
                st.session_state.price_source = source
    
    # Use cached price if available
    if 'sol_price' not in st.session_state:
        st.warning("Unable to fetch SOL price. Please refresh the page or check your connection.")
        return
    
    sol_price = st.session_state.sol_price
    
    # Display current SOL price prominently
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.metric(
            label="Current SOL Price",
            value=f"${sol_price:.4f}",
            delta=None
        )
    
    st.markdown("---")
    
    # Option parameters input
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Option Parameters")
        
        # Strike price
        default_strike = float(sol_price) if sol_price is not None else 100.0
        strike_price = st.number_input(
            "Strike Price ($)",
            min_value=0.01,
            value=default_strike,
            step=0.01,
            format="%.4f",
            help="The strike price of the option"
        )
        
        # Expiry date
        min_date = datetime.now().date() + timedelta(days=1)
        max_date = datetime.now().date() + timedelta(days=365)
        
        expiry_date = st.date_input(
            "Expiry Date",
            value=min_date + timedelta(days=30),
            min_value=min_date,
            max_value=max_date,
            help="The expiration date of the option"
        )
        
        # Calculate time to expiry
        time_to_expiry = calculate_time_to_expiry(expiry_date)
        st.info(f"Time to expiry: {time_to_expiry:.4f} years ({time_to_expiry * 365:.1f} days)")
        
    with col2:
        st.subheader("Market Parameters")
        
        # Volatility
        volatility = st.slider(
            "Implied Volatility (%)",
            min_value=1.0,
            max_value=200.0,
            value=80.0,
            step=1.0,
            format="%.1f%%",
            help="The implied volatility of the underlying asset"
        ) / 100
        
        # Risk-free rate
        risk_free_rate = st.slider(
            "Risk-free Rate (%)",
            min_value=0.0,
            max_value=10.0,
            value=5.0,
            step=0.1,
            format="%.1f%%",
            help="The risk-free interest rate"
        ) / 100
    
    # Validate inputs
    if time_to_expiry <= 0:
        st.error("Expiry date must be in the future")
        return
    
    if strike_price <= 0:
        st.error("Strike price must be positive")
        return
    
    # Calculate option prices and Greeks
    try:
        call_price = BlackScholes.call_price(sol_price, strike_price, time_to_expiry, risk_free_rate, volatility)
        put_price = BlackScholes.put_price(sol_price, strike_price, time_to_expiry, risk_free_rate, volatility)
        
        # Calculate Greeks
        delta_call = BlackScholes.delta_call(sol_price, strike_price, time_to_expiry, risk_free_rate, volatility)
        delta_put = BlackScholes.delta_put(sol_price, strike_price, time_to_expiry, risk_free_rate, volatility)
        gamma = BlackScholes.gamma(sol_price, strike_price, time_to_expiry, risk_free_rate, volatility)
        theta_call = BlackScholes.theta_call(sol_price, strike_price, time_to_expiry, risk_free_rate, volatility)
        theta_put = BlackScholes.theta_put(sol_price, strike_price, time_to_expiry, risk_free_rate, volatility)
        vega = BlackScholes.vega(sol_price, strike_price, time_to_expiry, risk_free_rate, volatility)
        
    except Exception as e:
        st.error(f"Error calculating option prices: {str(e)}")
        return
    
    # Display results
    st.markdown("---")
    st.subheader("Option Prices & Greeks")
    
    # Option prices
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            label="📈 Call Option Price",
            value=f"${call_price:.4f}",
            help="Theoretical call option price using Black-Scholes model"
        )
        
    with col2:
        st.metric(
            label="📉 Put Option Price",
            value=f"${put_price:.4f}",
            help="Theoretical put option price using Black-Scholes model"
        )
    
    # Greeks table
    st.subheader("Option Greeks")
    
    greeks_data = {
        'Greek': ['Delta', 'Gamma', 'Theta', 'Vega'],
        'Call': [f"{delta_call:.4f}", f"{gamma:.4f}", f"{theta_call:.4f}", f"{vega:.4f}"],
        'Put': [f"{delta_put:.4f}", f"{gamma:.4f}", f"{theta_put:.4f}", f"{vega:.4f}"],
        'Description': [
            'Price sensitivity to underlying price change',
            'Delta sensitivity to underlying price change',
            'Price decay per day',
            'Price sensitivity to volatility change (%)'
        ]
    }
    
    greeks_df = pd.DataFrame(greeks_data)
    st.table(greeks_df)
    
    # Additional information
    st.markdown("---")
    st.subheader("Model Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        **Black-Scholes Assumptions:**
        - Constant volatility and risk-free rate
        - European-style options (exercise only at expiry)
        - No dividends
        - Efficient markets with no transaction costs
        """)
    
    with col2:
        sol_price_val = sol_price if sol_price is not None else 0.0
        strike_price_val = strike_price if strike_price is not None else 0.0
        
        moneyness = sol_price_val / strike_price_val if strike_price_val != 0 else 0
        if moneyness > 1.05:
            status = "In-the-Money (ITM)"
            status_class = "itm-status"
        elif moneyness < 0.95:
            status = "Out-of-the-Money (OTM)"
            status_class = "otm-status"
        else:
            status = "At-the-Money (ATM)"
            status_class = "atm-status"
        
        call_intrinsic = max(sol_price_val - strike_price_val, 0)
        put_intrinsic = max(strike_price_val - sol_price_val, 0)
        
        st.markdown(f"""
        **Option Status:**
        - Moneyness: {moneyness:.4f}
        - Status: {status}
        - Intrinsic Value (Call): ${call_intrinsic:.4f}
        - Intrinsic Value (Put): ${put_intrinsic:.4f}
        """)
    
    # Footer with last update time
    st.markdown("---")
    last_update = datetime.fromtimestamp(st.session_state.last_refresh)
    price_source = st.session_state.get('price_source', 'API')
    st.caption(f"Last price update: {last_update.strftime('%Y-%m-%d %H:%M:%S')} | Data provided by {price_source} API")
    
    # Auto-refresh mechanism
    if auto_refresh:
        time.sleep(1)
        st.rerun()

if __name__ == "__main__":
    main()
