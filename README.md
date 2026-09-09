# Stock Analyzer

A command-line tool for pulling stock price history and computing common technical indicators.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
python main.py AAPL
python main.py TSLA --period 6mo --interval 1d --plot
python main.py MSFT --period 5y --save-chart msft.png --csv msft.csv
```

### Options

- `ticker` — ticker symbol (e.g. `AAPL`)
- `--period` — history window: `1mo`, `6mo`, `1y`, `5y`, `max` (default `1y`)
- `--interval` — bar size: `1d`, `1wk`, `1mo` (default `1d`)
- `--plot` — display a chart (price + moving averages + Bollinger Bands, RSI, MACD)
- `--save-chart PATH` — save the chart to a file instead of displaying it
- `--csv PATH` — write the full indicator table to a CSV file

## What it computes

- Simple & exponential moving averages (20/50/200)
- RSI (14)
- MACD (12/26/9) with signal line and histogram
- Bollinger Bands (20, 2 std)
- Daily returns, annualized volatility, max drawdown, Sharpe ratio

Data comes from Yahoo Finance via [`yfinance`](https://pypi.org/project/yfinance/); no API key required.
