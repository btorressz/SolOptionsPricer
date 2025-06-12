
# 📊 SolOptionsPricer - SOL Options Pricing Engine

A real-time Solana options pricing engine built with Streamlit that calculates theoretical call and put option prices using the Black-Scholes model with live SOL price feeds.

## 🌟 Features

- **Real-time SOL Price Feed**: Fetches live SOL prices from multiple reliable APIs
- **Black-Scholes Option Pricing**: Calculates theoretical call and put option prices
- **Option Greeks**: Displays Delta, Gamma, Theta, and Vega for risk management
- **Interactive Interface**: User-friendly sliders for volatility and risk-free rate
- **Multiple Price Sources**: Robust fallback system with Jupiter, Kraken, CoinGecko, and Binance APIs
- **Auto-refresh**: Automatic price updates every 30 seconds
- **Light Theme**: Clean, professional interface optimized for trading

  ## 📋 Dependencies

```
streamlit
requests
numpy
pandas
scipy
```

## 🔧 Configuration

The application uses multiple price sources with automatic fallback:

1. **Jupiter API** - Primary (Solana ecosystem)
2. **Kraken API** - Secondary (traditional exchange)
3. **CoinGecko API** - Third fallback
4. **Binance API** - Final fallback

No API keys required - all sources use public endpoints.

## 📊 Usage

### Input Parameters

- **Strike Price**: The exercise price of the option (auto-populated with current SOL price)
- **Expiry Date**: Option expiration date (1-365 days from current date)
- **Implied Volatility**: Expected price volatility (1-200%)
- **Risk-free Rate**: Risk-free interest rate (0-10%)

### Output

- **Call Option Price**: Theoretical call option value
- **Put Option Price**: Theoretical put option value
- **Option Greeks**: Risk sensitivities (Delta, Gamma, Theta, Vega)
- **Option Status**: Moneyness and intrinsic values

  ## 🧮 Black-Scholes Model

The application implements the complete Black-Scholes formula for European options:


### Call Option Price
```
C = S₀ × N(d₁) - K × e^(-r×T) × N(d₂)
```

### Put Option Price
```
P = K × e^(-r×T) × N(-d₂) - S₀ × N(-d₁)
```

Where:
- `S₀` = Current SOL price
- `K` = Strike price
- `r` = Risk-free rate
- `T` = Time to expiry
- `N()` = Cumulative standard normal distribution

### Greeks Calculations

- **Delta**: Price sensitivity to underlying price changes
- **Gamma**: Delta sensitivity to underlying price changes
- **Theta**: Time decay (price change per day)
- **Vega**: Volatility sensitivity (per percentage point)

  ## 🌐 API Integration

### Price Source Priority

1. **Jupiter API**: `https://price.jup.ag/v4/price`
   - Optimized for Solana ecosystem pricing
   - Most accurate for DeFi applications

2. **Kraken API**: `https://api.kraken.com/0/public/Ticker`
   - Reliable traditional exchange
   - High uptime and stability

3. **CoinGecko API**: `https://api.coingecko.com/api/v3/simple/price`
   - Comprehensive crypto data
   - Rate-limited for free tier

4. **Binance API**: `https://api.binance.com/api/v3/ticker/price`
   - Large volume exchange
   - May be geo-restricted
  
     
## 🔄 Auto-refresh Feature

- Automatic price updates every 30 seconds when enabled
- Manual refresh button for immediate updates
- Displays last update timestamp and data source
- Graceful error handling with user notifications

## 🎨 User Interface

- **Light Theme**: Professional trading interface
- **Responsive Design**: Works on desktop and mobile
- **Interactive Elements**: Smooth sliders and buttons
- **Real-time Updates**: Live price and calculation updates
- **Error Handling**: Clear error messages and fallback options

## 📈 Use Cases

- **Options Trading**: Calculate theoretical option prices for SOL
- **Risk Management**: Analyze option Greeks for portfolio hedging
- **Education**: Learn options pricing and sensitivity analysis
- **DeFi Research**: Study Solana ecosystem option strategies
- **Volatility Analysis**: Test different volatility scenarios

- ## ⚠️ Disclaimers

- This tool is for educational and research purposes only
- Not financial advice - consult professionals before trading
- Theoretical prices may differ from actual market prices
- The Black-Scholes model assumes constant volatility and rates
- Past performance does not guarantee future results

  
### Core Components

- **Price Fetching**: Multi-source API integration with fallbacks
- **Mathematical Engine**: Black-Scholes implementation with scipy
- **User Interface**: Streamlit-based interactive dashboard
- **Data Validation**: Input validation and error handling
- **State Management**: Session state for auto-refresh functionality




