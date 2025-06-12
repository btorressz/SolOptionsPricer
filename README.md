
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
