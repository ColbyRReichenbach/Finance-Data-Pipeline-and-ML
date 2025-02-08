import sqlite3
import pandas as pd
import config

def store_historical_indexes(index_data):
    """
    Insert historical index data into SQLite.
    :param index_data: Dictionary {symbol: DataFrame}
    """
    conn = sqlite3.connect(config.DB_NAME)
    cursor = conn.cursor()

    for symbol, data in index_data.items():
        print(f"🔍 Checking data for {symbol}:")
        print(data.head())  # Debugging: Print first rows

        for _, row in data.iterrows():
            date = str(row["Date"])  # Convert Date to string
            open_price = float(row["Open"]) if not pd.isna(row["Open"]) else None
            high = float(row["High"]) if not pd.isna(row["High"]) else None
            low = float(row["Low"]) if not pd.isna(row["Low"]) else None
            close = float(row["Close"]) if not pd.isna(row["Close"]) else None
            volume = int(row["Volume"]) if not pd.isna(row["Volume"]) else None

            try:
                cursor.execute("""
                INSERT OR IGNORE INTO indexes_historical 
                (index_symbol, date, open, high, low, close, volume)
                VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (symbol, date, open_price, high, low, close, volume))
            except Exception as e:
                print(f"❌ Error inserting row: {e}")
                print(f"Data: {symbol}, {date}, {open_price}, {high}, {low}, {close}, {volume}")

    conn.commit()
    conn.close()
    print("✅ Index historical data stored successfully!")


