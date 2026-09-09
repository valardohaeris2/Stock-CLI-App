"""Fetch historical price data for a ticker."""

import pandas as pd
import yfinance as yf


def fetch_data(ticker: str, period: str = "1y", interval: str = "1d") -> pd.DataFrame:
    """Download historical OHLCV data for a ticker.

    Raises ValueError if no data is returned (e.g. invalid ticker).
    """
    df = yf.download(ticker, period=period, interval=interval, progress=False, auto_adjust=True)

    if df.empty:
        raise ValueError(f"No data found for ticker '{ticker}' (period={period}, interval={interval})")

    # yfinance returns MultiIndex columns when given a list; flatten just in case.
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df.index.name = "Date"
    return df
