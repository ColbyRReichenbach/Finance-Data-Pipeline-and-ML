import yfinance as yf
import pandas as pd
from config.constants import SECTOR_ETFS, HISTORICAL_START
from config.db_utils import get_db_connection


def fetch_historical_sector_data(sector_name, etf_symbol, start_date=HISTORICAL_START):
    """Fetch historical sector performance data from Yahoo Finance using ETFs."""
    sector = yf.Ticker(etf_symbol)
    df = sector.history(period="max", start=start_date)

    if df.empty:
        print(f"⚠️ No data found for {sector_name} ({etf_symbol})")
        return None

    df.reset_index(inplace=True)
    df["sector_name"] = sector_name
    df.rename(columns={
        "Date": "date",
        "Open": "open_price",
        "Close": "close_price",
        "High": "high_price",
        "Low": "low_price",
        "Volume": "volume"
    }, inplace=True)

    print(f"🔍 {sector_name} - Historical Sector Data Sample (Cleaned):")
    print(df.head(), "\n")

    return df


def fetch_and_store_historical_sectors():
    """Fetches and stores historical sector data for all sectors."""

    all_data = []

    for sector_name, etf_symbol in SECTOR_ETFS.items():
        try:
            print(f"📡 Fetching live sector data for {sector_name} ({etf_symbol})...")

            df = fetch_historical_sector_data(sector_name, etf_symbol)

            # 🎯 Keep only relevant columns
            df["sector"] = sector_name  # Add symbol for clarity
            required_columns = ["sector", "date", "open_price", "close_price", "high_price", "low_price", "volume"]
            df = df[required_columns]

            all_data.append(df)

        except Exception as e:
            print(f"⚠️ Error fetching data for {sector_name}: {e}")

    if all_data:
        conn = get_db_connection()
        final_df = pd.concat(all_data, ignore_index=True)
        final_df.to_sql("historical_sectors", conn, if_exists="append", index=False)
        conn.close()
        print("✅ Historical sector data stored successfully!")


if __name__ == "__main__":
    fetch_and_store_historical_sectors()
