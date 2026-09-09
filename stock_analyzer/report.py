"""Build a human-readable summary report from an analyzed DataFrame."""

import pandas as pd

from . import indicators


def build_report(ticker: str, df: pd.DataFrame) -> str:
    latest = df.iloc[-1]
    first_close = df["Close"].iloc[0]
    last_close = df["Close"].iloc[-1]
    period_return = (last_close / first_close - 1) * 100

    vol = indicators.annualized_volatility(df) * 100
    drawdown = indicators.max_drawdown(df) * 100
    sharpe = indicators.sharpe_ratio(df)

    rsi = latest.get("RSI_14")
    macd = latest.get("MACD")
    macd_signal = latest.get("MACD_Signal")
    sma_50 = latest.get("SMA_50")
    sma_200 = latest.get("SMA_200")

    lines = [
        f"Stock Analysis Report: {ticker.upper()}",
        "=" * (24 + len(ticker)),
        f"Date range:        {df.index[0].date()} to {df.index[-1].date()}",
        f"Latest close:      {last_close:.2f}",
        f"Period return:     {period_return:+.2f}%",
        f"Annualized vol:    {vol:.2f}%",
        f"Max drawdown:      {drawdown:.2f}%",
        f"Sharpe ratio (0% rf): {sharpe:.2f}",
        "",
        "Latest indicators:",
        f"  RSI (14):        {rsi:.2f}" if pd.notna(rsi) else "  RSI (14):        n/a",
        f"  MACD:            {macd:.4f} (signal {macd_signal:.4f})" if pd.notna(macd) else "  MACD:            n/a",
    ]

    if pd.notna(sma_50) and pd.notna(sma_200):
        trend = "bullish (50 SMA > 200 SMA)" if sma_50 > sma_200 else "bearish (50 SMA < 200 SMA)"
        lines.append(f"  Trend:           {trend}")

    if pd.notna(rsi):
        if rsi >= 70:
            lines.append("  RSI signal:      overbought")
        elif rsi <= 30:
            lines.append("  RSI signal:      oversold")
        else:
            lines.append("  RSI signal:      neutral")

    return "\n".join(lines)
