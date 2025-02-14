import yfinance as yf
import pandas as pd
from config.constants import STOCK_TICKERS, HISTORICAL_START
from config.db_utils import get_db_connection


def fetch_historical_stock_data(ticker, start_date=HISTORICAL_START):
    """Fetch historical stock data from Yahoo Finance."""
    stock = yf.Ticker(ticker)
    df = stock.history(period="max", start=start_date)

    if df.empty:
        print(f"⚠️ No data found for {ticker}")
        return None

    df.reset_index(inplace=True)
    df["ticker"] = ticker
    df.rename(columns={
        "Date": "date",
        "Open": "open_price",
        "Close": "close_price",
        "High": "high_price",
        "Low": "low_price",
        "Volume": "volume"
    }, inplace=True)

    print(f"🔍 {ticker} - Historical Stock Data Sample (Cleaned):")
    print(df.head(), "\n")

    return df


def fetch_and_store_historical_stocks():
    """Fetches and stores historical stock data for all tickers."""

    all_data = []  # Store all fetched data

    for ticker in STOCK_TICKERS:
        try:
            print(f"📡 Fetching historical data for {ticker}...")

            df = fetch_historical_stock_data(ticker)  # Fetch historical data

            # 🎯 Keep only relevant columns
            required_columns = ["date", "open_price", "close_price", "high_price", "low_price", "volume", "ticker"]
            df = df[required_columns]

            all_data.append(df)

        except Exception as e:
            print(f"⚠️ Error fetching data for {ticker}: {e}")

    # 🚀 Store in SQLite
    if all_data:
        conn = get_db_connection()
        final_df = pd.concat(all_data, ignore_index=True)
        final_df.to_sql("historical_stocks", conn, if_exists="append", index=False)
        conn.close()
        print("✅ Historical stock data stored successfully!")


if __name__ == "__main__":
    fetch_and_store_historical_stocks()
