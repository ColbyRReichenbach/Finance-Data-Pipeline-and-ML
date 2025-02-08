import sqlite3
import pandas as pd
import config

def get_sector_id(sector_name, cursor):
    """
    Retrieve or create sector_id from sectors_historical table.
    """
    if not sector_name:
        print("⚠ No sector_name provided.")
        return None

    # Check if the sector exists
    cursor.execute("SELECT sector_id FROM sectors_historical WHERE sector_name = ?", (sector_name,))
    result = cursor.fetchone()

    if result:
        return result[0]
    else:
        # Insert the new sector dynamically with today's date
        cursor.execute("INSERT INTO sectors_historical (sector_name, date) VALUES (?, DATE('now'))", (sector_name,))
        return cursor.lastrowid  # Get the new ID


def get_index_id(index_symbol, cursor):
    """
    Retrieve index_id from indexes_historical table.
    """
    if not index_symbol:
        print("⚠ No index_symbol provided.")
        return None

    cursor.execute("SELECT index_id FROM indexes_historical WHERE index_symbol = ?", (index_symbol,))
    result = cursor.fetchone()

    if result:
        return result[0]
    else:
        print(f"❌ No index_id found for index: {index_symbol}")
        return None

def store_historical_stocks(stock_data):
    """
    Insert historical stock data into SQLite with dynamically retrieved sector_id.
    """
    conn = sqlite3.connect(config.DB_NAME)
    cursor = conn.cursor()

    for symbol, (data, sector_name) in stock_data.items():
        print(f"\n🔍 Processing stock: {symbol}")
        print(f"  ➤ Sector from Yahoo Finance: {sector_name}")

        # Ensure sector exists in the database
        sector_id = get_sector_id(sector_name, cursor)

        # Get index_id from predefined mapping
        index_symbol = config.STOCK_INDEX_MAP.get(symbol, None)
        index_id = get_index_id(index_symbol, cursor)

        for _, row in data.iterrows():
            date = str(row["Date"])
            open_price = float(row["Open"]) if not pd.isna(row["Open"]) else None
            high = float(row["High"]) if not pd.isna(row["High"]) else None
            low = float(row["Low"]) if not pd.isna(row["Low"]) else None
            close = float(row["Close"]) if not pd.isna(row["Close"]) else None
            volume = int(row["Volume"]) if not pd.isna(row["Volume"]) else None

            try:
                cursor.execute("""
                INSERT OR IGNORE INTO stocks_historical 
                (stock_symbol, sector_id, index_id, date, open, high, low, close, volume)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (symbol, sector_id, index_id, date, open_price, high, low, close, volume))
            except Exception as e:
                print(f"❌ Error inserting row: {e}")

    conn.commit()
    conn.close()
    print("✅ Stock historical data stored successfully!")
