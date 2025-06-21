# TradeLab

A simple and powerful Python package for algorithmic trading and technical analysis. Calculate technical indicators, create alternative candle charts, and analyze market data with ease.

## What Does It Do?

TradeLab helps you:

- Calculate technical indicators (moving averages, RSI, SuperTrend, etc.)
- Create alternative candle charts (Heikin Ashi, Renko)
- Compare different stocks or assets
- Analyze market data without complex coding

## Quick Start

### Installation

```bash

pip install tradelab

```

### Basic Usage

```python

import pandas as pd

from tradelab.indicators import rsi, ema, supertrend


# Load your stock data (CSV file with columns: date, open, high, low, close, volume)

data = pd.read_csv('your_stock_data.csv')


# Calculate indicators

rsi_values =rsi(data,period=14)

moving_average =ema(data,period=20)

trend_data =supertrend(data,period=10,multiplier=3.0)


print(f"Current RSI: {rsi_values.iloc[-1]:.2f}")

print(f"Current EMA: {moving_average.iloc[-1]:.2f}")

```

## Available Indicators

### Trend Indicators

- **EMA** - Exponential Moving Average

- **SuperTrend** - Trend following indicator

- **Normalized T3** - Smoothed trend oscillator

### Momentum Indicators

- **RSI** - Relative Strength Index (0-100 scale)

- **ADX** - Average Directional Index

### Volatility Indicators

- **ATR** - Average True Range

### Comparative Indicators

- **Relative Strength** - Compare two stocks or assets

## Available Candles

### Alternative Chart Types

- **Heikin Ashi** - Smoothed candlesticks for clearer trend visualization
- **Renko** - Price movement based boxes that filter out time and minor price movements

## Examples

### Calculate Heikin Ashi candles

```python
from tradelab.candles import heikin_ashi

# Transform regular OHLC data to Heikin Ashi
ha_data = heikin_ashi(data)
print("Heikin Ashi data:")
print(ha_data.tail())
```

### Calculate Renko charts

```python
from tradelab.candles import renko

# Create Renko bricks with fixed brick size
renko_data = renko(data, brick_size=25, mode='normal')
print("Renko bricks:")
print(renko_data.tail())
```

### Calculate RSI values

```python

from tradelab.indicators import rsi


# Calculate RSI

rsi_values =rsi(data,period=14)

print(f"Current RSI: {rsi_values.iloc[-1]:.2f}")


# Check if overbought (>70) or oversold (<30)

if rsi_values.iloc[-1]>70:

    print("Potentially overbought")

elif rsi_values.iloc[-1]<30:

    print("Potentially oversold")

```

### Compare two stocks

```python

from tradelab.indicators import relative_strength


# Compare Apple vs S&P 500

apple_data = pd.read_csv('AAPL.csv')

spy_data = pd.read_csv('SPY.csv')


comparison =relative_strength(apple_data, spy_data)

print(f"Apple vs S&P 500 strength: {comparison['relative_strength'].iloc[-1]:.4f}")

```

### Calculate multiple indicators

```python

from tradelab.indicators import rsi, ema, atr


# Calculate multiple indicators at once

rsi_14 =rsi(data,period=14)

ema_20 =ema(data,period=20)

volatility =atr(data,period=14)


print(f"RSI(14): {rsi_14.iloc[-1]:.2f}")

print(f"EMA(20): {ema_20.iloc[-1]:.2f}")

print(f"ATR(14): {volatility.iloc[-1]:.2f}")

```

## Data Format

Your data should be a pandas DataFrame with these columns:

-`date` (optional, can be index)

-`open` - Opening price

-`high` - Highest price

-`low` - Lowest price

-`close` - Closing price

-`volume` - Trading volume

Example:

```csv

date,open,high,low,close,volume

2024-01-01,150.00,152.50,149.00,151.25,1000000

2024-01-02,151.30,153.00,150.50,152.75,1200000

```

## Import Options

You can import indicators in different ways:

```python

# Import everything

from tradelab.indicators import*


# Import specific indicators

from tradelab.indicators import rsi, ema


# Import candles

from tradelab.candles import renko, heikin_ashi

from tradelab.candles import *

```

## Requirements

- Python 3.8+
- pandas
- numpy
- ta-lib
- fixedta

## Contributing

We welcome contributions! Feel free to:

- Report bugs
- Suggest new indicators
- Submit pull requests
- Improve documentation

## License

MIT License - feel free to use in your projects.

## Support

If you find this package helpful, please give it a star ⭐ on GitHub!

---

**Disclaimer**: This package is for educational and research purposes. Always do your own research before making investment decisions.
