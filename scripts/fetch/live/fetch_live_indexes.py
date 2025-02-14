import yfinance as yf
import pandas as pd
from config.constants import INDEX_TICKERS
from config.db_utils import get_db_connection


def fetch_live_index_data(index_symbol):
    """Fetch real-time index data from Yahoo Finance."""
    index = yf.Ticker(index_symbol)
    df = index.history(period="1d", interval="15m")  # 15-min updates

    if df.empty:
        print(f"⚠️ No live data found for {index_symbol}")
        return None

    df.reset_index(inplace=True)
    df["symbol"] = index_symbol
    df.rename(columns={
        "Datetime": "datetime",
        "Open": "open_price",
        "Close": "close_price",
        "High": "high_price",
        "Low": "low_price",
        "Volume": "volume"
    }, inplace=True)

    print(f"🔍 {index_symbol} - Live Index Data Sample (Cleaned):")
    print(df.head(), "\n")

    return df


def fetch_and_store_live_indexes():
    """Fetches and stores live index data for all indexes."""

    all_data = []

    for symbol in INDEX_TICKERS:
        try:
            print(f"📡 Fetching live index data for {symbol}...")

            df = fetch_live_index_data(symbol)

            # 🎯 Keep only relevant columns
            required_columns = ["datetime", "open_price", "close_price", "high_price", "low_price", "volume", "symbol"]
            df = df[required_columns]

            all_data.append(df)

        except Exception as e:
            print(f"⚠️ Error fetching live data for {symbol}: {e}")

    if all_data:
        conn = get_db_connection()
        final_df = pd.concat(all_data, ignore_index=True)
        final_df.to_sql("live_indexes", conn, if_exists="append", index=False)
        conn.close()
        print("✅ Live index data stored successfully!")


if __name__ == "__main__":
    fetch_and_store_live_indexes()
