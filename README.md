
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

