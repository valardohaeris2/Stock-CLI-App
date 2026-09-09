"""Technical indicators computed on an OHLCV DataFrame."""

import numpy as np
import pandas as pd


def add_moving_averages(df: pd.DataFrame, windows=(20, 50, 200)) -> pd.DataFrame:
    for w in windows:
        df[f"SMA_{w}"] = df["Close"].rolling(window=w).mean()
        df[f"EMA_{w}"] = df["Close"].ewm(span=w, adjust=False).mean()
    return df


def add_rsi(df: pd.DataFrame, window: int = 14) -> pd.DataFrame:
    delta = df["Close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.ewm(alpha=1 / window, min_periods=window, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / window, min_periods=window, adjust=False).mean()

    rs = avg_gain / avg_loss
    df["RSI_14"] = 100 - (100 / (1 + rs))
    return df


def add_macd(df: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.DataFrame:
    ema_fast = df["Close"].ewm(span=fast, adjust=False).mean()
    ema_slow = df["Close"].ewm(span=slow, adjust=False).mean()
    df["MACD"] = ema_fast - ema_slow
    df["MACD_Signal"] = df["MACD"].ewm(span=signal, adjust=False).mean()
    df["MACD_Hist"] = df["MACD"] - df["MACD_Signal"]
    return df


def add_bollinger_bands(df: pd.DataFrame, window: int = 20, num_std: float = 2.0) -> pd.DataFrame:
    mid = df["Close"].rolling(window=window).mean()
    std = df["Close"].rolling(window=window).std()
    df["BB_Mid"] = mid
    df["BB_Upper"] = mid + num_std * std
    df["BB_Lower"] = mid - num_std * std
    return df


def add_daily_returns(df: pd.DataFrame) -> pd.DataFrame:
    df["Daily_Return"] = df["Close"].pct_change()
    return df


def compute_all(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = add_moving_averages(df)
    df = add_rsi(df)
    df = add_macd(df)
    df = add_bollinger_bands(df)
    df = add_daily_returns(df)
    return df


def annualized_volatility(df: pd.DataFrame, trading_days: int = 252) -> float:
    return float(df["Close"].pct_change().std() * np.sqrt(trading_days))


def max_drawdown(df: pd.DataFrame) -> float:
    cumulative = (1 + df["Close"].pct_change().fillna(0)).cumprod()
    running_max = cumulative.cummax()
    drawdown = cumulative / running_max - 1
    return float(drawdown.min())


def sharpe_ratio(df: pd.DataFrame, risk_free_rate: float = 0.0, trading_days: int = 252) -> float:
    daily_returns = df["Close"].pct_change().dropna()
    excess = daily_returns - risk_free_rate / trading_days
    if excess.std() == 0:
        return 0.0
    return float((excess.mean() / excess.std()) * np.sqrt(trading_days))
