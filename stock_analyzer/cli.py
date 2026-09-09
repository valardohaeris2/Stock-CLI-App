"""Command-line entry point for the stock analyzer."""

import argparse
import sys

from . import indicators, report
from .data import fetch_data


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="stock-analyzer",
        description="Fetch stock data and report technical indicators.",
    )
    parser.add_argument("ticker", help="Ticker symbol, e.g. AAPL")
    parser.add_argument("--period", default="1y", help="History period, e.g. 1mo, 6mo, 1y, 5y, max (default: 1y)")
    parser.add_argument("--interval", default="1d", help="Data interval, e.g. 1d, 1wk, 1mo (default: 1d)")
    parser.add_argument("--plot", action="store_true", help="Show a chart of price and indicators")
    parser.add_argument("--save-chart", metavar="PATH", help="Save chart to PATH instead of displaying it")
    parser.add_argument("--csv", metavar="PATH", help="Save the full indicator table to a CSV file")
    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        raw = fetch_data(args.ticker, period=args.period, interval=args.interval)
    except (ValueError, Exception) as exc:  # yfinance can raise various network errors
        print(f"Error fetching data for '{args.ticker}': {exc}", file=sys.stderr)
        return 1

    df = indicators.compute_all(raw)

    print(report.build_report(args.ticker, df))

    if args.csv:
        df.to_csv(args.csv)
        print(f"\nIndicator table saved to {args.csv}")

    if args.plot or args.save_chart:
        from . import plotting
        plotting.plot_analysis(args.ticker, df, save_path=args.save_chart)

    return 0


if __name__ == "__main__":
    sys.exit(main())
