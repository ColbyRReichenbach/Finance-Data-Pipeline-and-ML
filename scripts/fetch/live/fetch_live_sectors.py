import yfinance as yf
import pandas as pd
from config.constants import SECTOR_ETFS
from config.db_utils import get_db_connection


def fetch_live_sector_data(sector_name, etf_symbol):
    """Fetch real-time sector data using sector ETFs."""
    sector = yf.Ticker(etf_symbol)
    df = sector.history(period="1d", interval="15m")  # 15-min updates

    if df.empty:
        print(f"⚠️ No live data found for {sector_name} ({etf_symbol})")
        return None

    df.reset_index(inplace=True)
    df["sector_name"] = sector_name
    df.rename(columns={
        "Datetime": "datetime",
        "Open": "open_price",
        "Close": "close_price",
        "High": "high_price",
        "Low": "low_price",
        "Volume": "volume"
    }, inplace=True)

    print(f"🔍 {sector_name} - Live Sector Data Sample (Cleaned):")
    print(df.head(), "\n")

    return df


def fetch_and_store_live_sectors():
    """Fetches and stores live sector data for all sectors."""

    all_data = []

    for sector_name, etf_symbol in SECTOR_ETFS.items():
        try:
            print(f"📡 Fetching live sector data for {sector_name} ({etf_symbol})...")

            df = fetch_live_sector_data(sector_name, etf_symbol)  # ✅ Pass the correct ETF symbol
            if df is None or df.empty:
                print(f"⚠️ No data available for {sector_name}. Skipping...")
                continue

            # 🎯 Keep only relevant columns
            df["sector"] = sector_name  # Add symbol for clarity
            required_columns = ["sector", "datetime", "open_price", "close_price", "high_price", "low_price", "volume"]
            df = df[required_columns]

            all_data.append(df)

        except Exception as e:
            print(f"⚠️ Error fetching live data for {sector_name}: {e}")

    if all_data:
        conn = get_db_connection()
        final_df = pd.concat(all_data, ignore_index=True)
        final_df.to_sql("live_sectors", conn, if_exists="append", index=False)
        conn.close()
        print("✅ Live sector data stored successfully!")


if __name__ == "__main__":
    fetch_and_store_live_sectors()
