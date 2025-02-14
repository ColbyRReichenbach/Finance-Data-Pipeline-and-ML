import yfinance as yf
import pandas as pd
import sqlite3
from config.db_utils import get_db_connection
from config.constants import STOCK_TICKERS  # ✅ Import stock tickers


def fetch_live_stock_data(ticker):
    """Fetch real-time stock price data from Yahoo Finance."""
    stock = yf.Ticker(ticker)
    df = stock.history(period="1d", interval="15m")  # 15-min updates

    if df.empty:
        print(f"⚠️ No live data found for {ticker}")
        return None

    df.reset_index(inplace=True)
    df["ticker"] = ticker
    df.rename(columns={
        "Datetime": "datetime",
        "Open": "open_price",
        "Close": "close_price",
        "High": "high_price",
        "Low": "low_price",
        "Volume": "volume"
    }, inplace=True)

    print(f"🔍 {ticker} - Live Stock Data Sample (Cleaned):")
    print(df.head(), "\n")

    return df


def fetch_and_store_live_stocks():
    """Fetches live stock data for all configured tickers, selects relevant columns, and stores it."""

    all_data = []  # Store all fetched data before storing

    for ticker in STOCK_TICKERS:  # ✅ Loop through stock tickers
        try:
            print(f"📡 Fetching live data for {ticker}...")

            # 🔍 Fetch live stock data (expects a single ticker)
            df = fetch_live_stock_data(ticker)

            # 🎯 Keep only relevant columns
            required_columns = ["datetime", "open_price", "close_price", "high_price", "low_price", "volume", "ticker"]
            df = df[required_columns]

            all_data.append(df)  # ✅ Append cleaned data to list

        except Exception as e:
            print(f"⚠️ Error fetching data for {ticker}: {e}")

    # 🚀 Store the cleaned data in SQLite
    if all_data:
        conn = get_db_connection()
        final_df = pd.concat(all_data, ignore_index=True)
        final_df.to_sql("live_stocks", conn, if_exists="append", index=False)
        conn.close()
        print("✅ Live stock data stored successfully!")


if __name__ == "__main__":
    fetch_and_store_live_stocks()
