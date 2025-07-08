# TradeLab

A high-performance Python package for algorithmic trading and technical analysis. TradeLab provides optimized Cython implementations of popular technical indicators and alternative candlestick patterns for fast market data analysis.

## Features

- **High Performance**: Cython-optimized implementations for maximum speed
- **Technical Indicators**: Popular indicators including EMA, RSI, SuperTrend, ADX, ATR, and more
- **Alternative Candles**: Heikin-Ashi and Renko chart implementations
- **Easy to Use**: Clean, intuitive API with comprehensive documentation
- **Type Safety**: Full type hints and validation support

## Installation

```bash
pip install tradelab
```

### For Development

```bash
git clone https://github.com/husainchhil/TradeLab.git
cd TradeLab
pip install -e .
```

## Quick Start

```python
import pandas as pd
from tradelab.indicators import EMA, RSI, SuperTrend, ATR, ADX
from tradelab.candles import RENKO, HEIKINASHI

# Sample OHLCV data
data = pd.DataFrame({
    'open': [100, 101, 102, 103, 104],
    'high': [105, 106, 107, 108, 109],
    'low': [99, 100, 101, 102, 103],
    'close': [102, 103, 104, 105, 106],
    'volume': [1000, 1100, 1200, 1300, 1400]
})

# Technical Indicators
ema_20 = EMA(data['close'], period=20)
rsi_14 = RSI(data['close'], period=14)
atr_14 = ATR(data['high'], data['low'], data['close'], period=14)
supertrend = SUPERTREND(data['high'], data['low'], data['close'])

# Alternative Candles
heikin_ashi = HEIKINASHI(data)
renko_chart = RENKO(data, brick_size=1.0, mode='wicks')
```

## Available Indicators

### Trend Indicators

- **EMA** - Exponential Moving Average
- **SuperTrend** - Trend-following indicator with dynamic support/resistance
- **Normalized T3** - Triple exponential moving average with volume factor

### Momentum Indicators  

- **RSI** - Relative Strength Index (0-100 oscillator)
- **ADX** - Average Directional Index (trend strength)

### Volatility Indicators

- **ATR** - Average True Range (market volatility)

### Comparative Analysis

- **Relative Strength** - Compare performance between two securities

## Alternative Candle Types

### Heikin-Ashi

Smoothed candlesticks that filter market noise and highlight trends.

```python
from tradelab.candles import HEIKINASHI

ha_candles = HEIKINASHI(ohlcv_data)
```

### Renko Charts

Price-based charts that ignore time and focus on price movements.

```python
from tradelab.candles import RENKO

renko_bricks = RENKO(ohlcv_data, brick_size=1.0, mode='wicks')
```

## Data Utilities

### OHLCV Resampling

TradeLab includes a powerful resampling function for converting OHLCV data to different timeframes.

```python
from tradelab.utils import resample_ohlcv

# Resample to 1-hour bars starting at 9:15 AM
hourly_data = resample_ohlcv(data, freq="1H", anchor="09:15:00")

# Resample to 15-minute bars
intraday_data = resample_ohlcv(data, freq="15T", anchor="09:30:00")

# Resample to weekly bars starting on Monday
weekly_data = resample_ohlcv(data, freq="1W", anchor="MON")
```

**Features:**

- **Flexible Timeframes**: Support for any pandas frequency string (1H, 30T, 15min, 5S, 1W, etc.)
- **Custom Anchoring**: Align bars to specific times (intraday) or days (weekly)
- **Proper OHLCV Aggregation**: Open=first, High=max, Low=min, Close=last, Volume=sum
- **Data Validation**: Automatic column validation and cleaning

## Performance

TradeLab uses Cython for performance-critical calculations, providing significant speed improvements over pure Python implementations:

- **2-10x faster** than equivalent pandas/numpy operations
- **Memory efficient** with optimized data structures
- **Type-safe** with compile-time optimizations

## Package Structure

```
tradelab/
├── indicators/           # Technical indicators
│   ├── ema/             # Exponential Moving Average
│   ├── rsi/             # Relative Strength Index  
│   ├── supertrend/      # SuperTrend indicator
│   ├── adx/             # Average Directional Index
│   ├── normalized_t3/   # Normalized T3 Moving Average
│   ├── volatility/      # Volatility indicators (ATR)
│   └── relative_strength/ # Relative Strength analysis
├── candles/             # Alternative candle types
│   ├── heikinashi/      # Heikin-Ashi candles
│   └── renko/           # Renko charts
└── utils.py             # Utility functions
```

## Development Files

### Build System

- **`setup.py`** - Main build configuration with Cython support
- **`pyproject.toml`** - Modern Python packaging configuration  
- **`MANIFEST.in`** - Package file inclusion rules

### Development Tools

- **`compile_cython.py`** - Development script for compiling Cython extensions
- **`debug.ipynb`** - Jupyter notebook for testing and development
- **`uv.lock`** - Dependency lock file for reproducible builds

### Configuration

- **`.gitignore`** - Git ignore patterns
- **`LICENSE`** - MIT License
- **`.python-version`** - Python version specification

## Building from Source

### Prerequisites

```bash
pip install setuptools wheel Cython numpy pandas
```

### Development Build

```bash
# Compile Cython extensions in-place
python setup.py build_ext --inplace

# Or use the development script
python compile_cython.py
```

### Distribution Build

```bash
# Build wheel and source distribution
python -m build

# Install locally
pip install dist/tradelab-*.whl
```

### Clean Build Artifacts

```bash
python compile_cython.py --clean
```

## Requirements

- **Python**: ≥3.11
- **NumPy**: ≤2.2.0  
- **Pandas**: ≤2.2.3
- **Pydantic**: ≥2.11.7

### Build Requirements

- **Cython**: ≥3.0.0
- **Setuptools**: ≥64
- **Wheel**: Latest

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-indicator`)
3. Commit your changes (`git commit -am 'Add new indicator'`)
4. Push to the branch (`git push origin feature/new-indicator`)
5. Create a Pull Request

## Support

- **Issues**: [GitHub Issues](https://github.com/husainchhil/TradeLab/issues)
- **Documentation**: Available in code docstrings

## Author

**Husain Chhil** - [hychhil@gmail.com](mailto:hychhil@gmail.com)

## Disclaimer

**Important Notice**: TradeLab is provided for educational and research purposes only. This software is not intended to provide financial advice or recommendations for actual trading decisions.

**Risk Warning**: Trading in financial markets involves substantial risk of loss and is not suitable for all investors. Past performance does not guarantee future results. The indicators and tools provided in this package should not be used as the sole basis for trading decisions.

**No Warranty**: This software is provided "as is" without any warranties, express or implied. The authors and contributors are not responsible for any financial losses or damages that may result from the use of this software.

**Professional Advice**: Always consult with qualified financial advisors before making investment decisions. Users are solely responsible for their trading decisions and any resulting profits or losses.

---

*TradeLab - High-performance technical analysis for algorithmic trading*
