import yfinance as yf
import pandas as pd
import sqlite3
from config.db_utils import DB_PATH


def last_fetch_time():
    """Returns the last time fundamentals were fetched."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(date) FROM stock_fundamentals")
    last_time = cursor.fetchone()[0]
    conn.close()
    return last_time


def fetch_fundamentals(ticker):
    """Fetches stock fundamentals from Yahoo Finance."""
    stock = yf.Ticker(ticker)
    info = stock.info

    data = {
        "ticker": ticker,
        "date": pd.Timestamp.today().strftime('%Y-%m-%d'),
        "market_cap": info.get("marketCap"),
        "pe_ratio": info.get("trailingPE"),
        "price_to_book": info.get("priceToBook"),
        "beta": info.get("beta"),
        "total_revenue": info.get("totalRevenue"),
        "earnings_growth": info.get("earningsGrowth"),
        "revenue_growth": info.get("revenueGrowth"),
        "debt_to_equity": info.get("debtToEquity"),
        "return_on_assets": info.get("returnOnAssets"),
        "return_on_equity": info.get("returnOnEquity"),
        "short_ratio": info.get("shortRatio"),
        "shares_short": info.get("sharesShort")
    }

    return data


def fetch_and_store_fundamentals(tickers, fetch_interval="daily"):
    """Fetches and stores fundamentals if needed."""
    from store.fundamentals.store_fundamentals import store_fundamentals
    last_time = last_fetch_time()

    # Decide fetch frequency
    today = pd.Timestamp.today().strftime('%Y-%m-%d')
    fetch_needed = False

    if last_time is None:
        fetch_needed = True  # No data exists yet
    else:
        last_time = pd.Timestamp(last_time)
        if fetch_interval == "daily" and (pd.Timestamp.today() - last_time).days >= 1:
            fetch_needed = True
        elif fetch_interval == "weekly" and (pd.Timestamp.today() - last_time).days >= 7:
            fetch_needed = True
        elif fetch_interval == "quarterly" and (pd.Timestamp.today() - last_time).days >= 90:
            fetch_needed = True

    if fetch_needed:
        all_data = []
        for ticker in tickers:
            print(f"📡 Fetching fundamentals for {ticker}...")
            fundamentals = fetch_fundamentals(ticker)
            if fundamentals:
                all_data.append(fundamentals)

        store_fundamentals(all_data)
        print("✅ Fundamentals updated successfully!")
    else:
        print(f"⏳ Fundamentals already updated on {last_time}, skipping fetch.")


if __name__ == "__main__":
    STOCKS = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
    fetch_and_store_fundamentals(STOCKS, fetch_interval="daily")  # Change to "weekly" or "quarterly" as needed
