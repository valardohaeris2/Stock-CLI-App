"""Charting for price, moving averages, RSI, and MACD."""

import matplotlib.pyplot as plt
import pandas as pd


def plot_analysis(ticker: str, df: pd.DataFrame, save_path: str | None = None) -> None:
    fig, axes = plt.subplots(
        3, 1, figsize=(12, 10), sharex=True,
        gridspec_kw={"height_ratios": [3, 1, 1]},
    )

    price_ax, rsi_ax, macd_ax = axes

    price_ax.plot(df.index, df["Close"], label="Close", color="black", linewidth=1.2)
    for col, style in (("SMA_50", "--"), ("SMA_200", ":")):
        if col in df:
            price_ax.plot(df.index, df[col], style, label=col, linewidth=1)
    if "BB_Upper" in df and "BB_Lower" in df:
        price_ax.fill_between(df.index, df["BB_Lower"], df["BB_Upper"], color="gray", alpha=0.15, label="Bollinger Bands")
    price_ax.set_title(f"{ticker.upper()} Price & Moving Averages")
    price_ax.legend(loc="upper left")
    price_ax.grid(alpha=0.3)

    if "RSI_14" in df:
        rsi_ax.plot(df.index, df["RSI_14"], color="purple", linewidth=1)
        rsi_ax.axhline(70, color="red", linestyle="--", linewidth=0.8)
        rsi_ax.axhline(30, color="green", linestyle="--", linewidth=0.8)
        rsi_ax.set_ylabel("RSI")
        rsi_ax.grid(alpha=0.3)

    if "MACD" in df:
        macd_ax.plot(df.index, df["MACD"], label="MACD", color="blue", linewidth=1)
        macd_ax.plot(df.index, df["MACD_Signal"], label="Signal", color="orange", linewidth=1)
        macd_ax.bar(df.index, df["MACD_Hist"], color="gray", alpha=0.4, label="Hist")
        macd_ax.set_ylabel("MACD")
        macd_ax.legend(loc="upper left")
        macd_ax.grid(alpha=0.3)

    fig.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=150)
        print(f"Chart saved to {save_path}")
    else:
        plt.show()
