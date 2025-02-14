import yfinance as yf
import pandas as pd
from config.constants import INDEX_TICKERS, HISTORICAL_START
from config.db_utils import get_db_connection


def fetch_historical_index_data(index_symbol, start_date=HISTORICAL_START):
    """Fetch historical index data from Yahoo Finance."""
    index = yf.Ticker(index_symbol)
    df = index.history(period="max", start=start_date)

    if df.empty:
        print(f"⚠️ No data found for {index_symbol}")
        return None

    df.reset_index(inplace=True)
    df["symbol"] = index_symbol
    df.rename(columns={
        "Date": "date",
        "Open": "open_price",
        "Close": "close_price",
        "High": "high_price",
        "Low": "low_price",
        "Volume": "volume"
    }, inplace=True)

    print(f"🔍 {index_symbol} - Historical Index Data Sample (Cleaned):")
    print(df.head(), "\n")

    return df


def fetch_and_store_historical_indexes():
    """Fetches and stores historical index data for all indexes."""

    all_data = []

    for symbol in INDEX_TICKERS:
        try:
            print(f"📡 Fetching historical index data for {symbol}...")

            df = fetch_historical_index_data(symbol)

            # 🎯 Keep only relevant columns
            required_columns = ["date", "open_price", "close_price", "high_price", "low_price", "volume", "symbol"]
            df = df[required_columns]

            all_data.append(df)

        except Exception as e:
            print(f"⚠️ Error fetching index data for {symbol}: {e}")

    if all_data:
        conn = get_db_connection()
        final_df = pd.concat(all_data, ignore_index=True)
        final_df.to_sql("historical_indexes", conn, if_exists="append", index=False)
        conn.close()
        print("✅ Historical index data stored successfully!")


if __name__ == "__main__":
    fetch_and_store_historical_indexes()
