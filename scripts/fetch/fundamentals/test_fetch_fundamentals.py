from fetch.fundamentals.fetch_fundamentals import fetch_fundamentals
import pandas as pd


def test_fetch_fundamentals():
    """Tests fetching stock fundamentals for one stock."""
    ticker = "AAPL"
    data = fetch_fundamentals(ticker)

    print(f"\n🔍 {ticker} - Fundamentals Sample:")
    print(pd.DataFrame([data]))


if __name__ == "__main__":
    test_fetch_fundamentals()
